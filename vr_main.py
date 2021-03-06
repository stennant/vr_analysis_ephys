import glob
import os
import vr_parameters
import vr_process_movement
import vr_plot_stops
import vr_plot_spikes
import vr_stops
import vr_sorted_firing_times
import vr_trial_types
import vr_plot_continuous_data
import vr_fft
import vr_filter
import vr_oscillations
import vr_rewrite_continuous_data
import vr_optogenetics
import vr_optogenetics_behaviour
#import vr_theta_gamma_correlation
import vr_referencing
import numpy as np
import vr_split_data
import vr_spectrogram
import vr_track_location_analysis

prm = vr_parameters.Parameters()


def init_vr_params():
    # - 30 cm black box;60 cm outbound journey;20 cm reward zone;60 cm outbound journey;30 cm black box
    prm.set_stop_threshold(0.7)  # speed is given in cm/200ms 0.7*1/2000
    prm.set_num_channels(16)
    prm.set_movement_ch('100_ADC2.continuous')
    prm.set_opto_ch('100_ADC3.continuous')
    prm.set_waveform_size(40)  # number of sampling points to take when taking waveform for spikes (1ms)

    prm.set_track_length(200)
    prm.set_beginning_of_outbound(30)
    prm.set_reward_zone(90)


def init_open_field_params():
    pass

'''
Initializes parameters
    filepath : string, location of raw data file
    filename : string, name of raw data file (without raw.kwd extension)
    good_channels : int, list, channels that are not dead
    stop_threshold : float, given in cm/200ms.
        example:
        0.7cm/200ms = 0.7(1/200cm)/ms = 0.7(1000/200cm/s) = 0.7(5cm/s) = 0.7/5 cm/s
    num_channels : int, number of recording channels
    movement_ch : channel number for movement information
'''


def init_params():

    filename = 'mcos_M2_D1_2018-06-04_14-32-13'
    prm.set_filepath('/Users/sarahtennant/Work/Analysis/Opto_data/mcos/' + str(filename))
    prm.set_behaviour_data_path('/Users/sarahtennant/Work/Analysis/Opto_data/mcos/' + str(filename) + '/Behaviour/Data/')
    prm.set_behaviour_analysis_path('/Users/sarahtennant/Work/Analysis/Opto_data/mcos/' + str(filename) + '/Behaviour/Analysis/')
    prm.set_firings_path('//Users/sarahtennant/Work/Analysis/Opto_data/mcos/' + str(filename) + '/T4_firings.mda')

    prm.set_sampling_rate(30000)
    prm.set_file(prm.get_filepath(), prm.get_filename())
    prm.set_num_tetrodes(4)
    prm.set_current_tetrode(2)
    prm.set_current_continuous(13)

    prm.set_is_open_field(False)
    prm.set_is_vr(True)
    prm.set_is_opto(False)

    if prm.is_vr is True:
        init_vr_params()

    if prm.is_open_field is True:
        init_open_field_params()


def process_a_dir(dir_name):
    print('All folders in {} will be processed.'.format(dir_name))
    prm.set_date(dir_name.rsplit('/', 2)[-2])
    prm.set_filepath(dir_name)

    #process movement information and plot stops per trial
    #vr_process_movement.save_or_open_movement_arrays(prm)
    #vr_trial_types.save_or_open_trial_arrays(prm)
    #vr_plot_stops.plot_stops(prm)
    print('Stops have been plotted')


    # plot firing times of clusters against location
    #vr_sorted_firing_times.process_firing_times(prm)
    print('Firing locations of clusters have been plotted')

    #vr_fft.test_fft(prm)

    # Split the data according to movement and stationary
    #vr_split_data.save_indicies_for_movement_and_stationary(prm)
    # Split the data according to light and no light
    #vr_split_data.save_indicies_for_light_and_no_light(prm)

    #light, no_light = vr_optogenetics.split_light_and_no_light_trials(prm) # need for plot stops and plotting continuous

    for c, channel in enumerate(np.arange(1,16,1)): # loop through channels
        if channel ==0 or channel == 1 or channel ==2 or channel ==3 or channel ==4 or channel ==5 or channel ==6 or channel ==7 or channel ==8 or channel ==9 or channel ==10 : # pick which channels to analyse and plot

            #load continuous data
            channel_data = vr_plot_continuous_data.load_continuous_data(prm, channel)

            #reference channel # warning: referencing may interfere with theta and gamma data
            #referenced_data_all = vr_referencing.load_reference_channel(prm, channel)
            #referenced_data_all = vr_referencing.reference_channel(channel_data, referenced_data_all)

            #filter data
            channel_data_all = vr_filter.custom_filter(channel_data, 0.5, 300, 30000, color='k')
            channel_data_all_spikes = vr_filter.custom_filter(channel_data, 600, 6000, 30000, color='k')
            theta = vr_filter.theta_filter(channel_data, 30000)
            gamma = vr_filter.gamma_filter(channel_data, 30000)

            if prm.is_opto is True:
                # Plot some example stuff for optogenetics
                #vr_plot_continuous_data.plot_continuous_opto(prm, channel_data_all,channel,light,no_light, theta, gamma,channel_data_all_spikes)
                print('continuous has been loaded and plotted')
                # split channel data by light/no light and movement / stationary
                #light_movement, nolight_movement, light_stationary, nolight_stationary = vr_split_data.split_light_nolight_movement_stationary(prm, channel_data_all)
                #print('channel data split')
                #plot power spectrums for light and no light, movement and stationary
                #vr_fft.calculate_and_plot_power_spectrum_split(prm, light_movement, nolight_movement, light_stationary, nolight_stationary, channel)
                #print('power spectrum has been loaded and plotted')

            if prm.is_opto is False:
                data = vr_track_location_analysis.stack_datasets(prm,channel_data_all,channel_data_all_spikes,theta,gamma)#stack all datasets
                #plot continuous data per trial
                #vr_track_location_analysis.plot_continuous_trials(prm, data, channel) # plot example trials
                #split based on movement and stationary
                before_stop, after_stop = vr_track_location_analysis.find_before_and_after_stops(prm,data[1000000:35000000,:])
                vr_track_location_analysis.stop_start_power_spectra(prm, before_stop, after_stop, channel)
                #look at theta and gamma at diff track locations
                #outbound,rewardzone,homebound= vr_track_location_analysis.split_locations(prm,data)
                #movement/stationary power spectra
                vr_track_location_analysis.stop_start_power_spectra_locations(prm,before_stop, after_stop, channel)
                #plot continuous
                vr_track_location_analysis.make_stop_start_continuous_plot(prm, channel, before_stop, after_stop)

                #plot power spectra for different speeds
                middle_upper,upper, middle_lower, lower = vr_track_location_analysis.power_spectra_speed(prm,data[1000000:35000000,:], channel)
                vr_track_location_analysis.power_spectra_speed_locations(prm,middle_upper,upper, middle_lower, lower, channel)
                #plot example data at diff track locations
                #vr_track_location_analysis.plot_track_locations_examples(prm,0, channel,data=outbound[:,2])
                #vr_track_location_analysis.plot_track_locations_examples(prm,1, channel,data=rewardzone[:,2])
                #vr_track_location_analysis.plot_track_locations_examples(prm,2, channel,data=homebound[:,2])

                #plot power spectra of track locations
                #vr_track_location_analysis.calculate_and_plot_power_spectrum_track_locations(prm, outbound, rewardzone, homebound, channel)

    # load and plot stops with opto highlighted - have to do this after main opto loop
    #vr_plot_stops.plot_opto_stops(prm)




def process_files():
    prm.get_filepath()
    for name in glob.glob(prm.get_filepath()+'*'):
        print(name)
        os.path.isdir(name)
        print("Files processed")

        process_a_dir(name + '/')
        print("Files processed")


def main():
    print('-------------------------------------------------------------')
    print('Check whether the arrays have the correct size in the folder. '
          'An incorrect array only gets deleted automatically if its size is 0. Otherwise, '
          'it needs to be deleted manually in order for it to be generated again.')
    print('-------------------------------------------------------------')

    init_params()
    print('params processed')
    process_files()


if __name__ == '__main__':
    main()
