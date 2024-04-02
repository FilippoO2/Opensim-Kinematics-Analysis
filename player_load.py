import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from full_body_kinematics import create_kinematics_dataframe
from config import kinematics_folder, keypoint, rows_to_skip, participant_mass, csv_file, sheet_name


def calculate_player_load_vectorized(x_acc, y_acc, z_acc, start, end, slice_start=None, slice_end=None):
    """ Calculates the player load across the duration of a trial or point.
    ----------
    Parameters
    x_acc: pandas series of the x acceleration
    y_acc: pandas series of the y acceleration
    z_acc: pandas series of the z acceleration
    start: int of the start frame for the calculation
    end: int of the end frame for the calculation
    slice_start: int of the frame to begin a slice of data (default is None)
    slice_end: int of the frame to end a slice of data (default is None)
    ----------
    Returns
    A player load value of the player load across that point
    """
    if slice_start is None:
        x_diff = x_acc[start:end-1].values - x_acc[start+1:end].values
        y_diff = y_acc[start:end-1].values - y_acc[start+1:end].values
        z_diff = z_acc[start:end-1].values - z_acc[start+1:end].values
        player_load = np.sqrt((x_diff**2 + y_diff**2 + z_diff**2)/100).sum()
    
    elif slice_start is not None and slice_end is not None:
        x_diff = x_acc[start:slice_start-1].values - x_acc[start+1:slice_start].values
        y_diff = y_acc[start:slice_start-1].values - y_acc[start+1:slice_start].values
        z_diff = z_acc[start:slice_start-1].values - z_acc[start+1:slice_start].values
        player_load = np.sqrt((x_diff**2 + y_diff**2 + z_diff**2)/100).sum()

        x_diff2 = x_acc[slice_end:end-2].values - x_acc[slice_end+1:end-1].values
        y_diff2 = y_acc[slice_end:end-2].values - y_acc[slice_end+1:end-1].values
        z_diff2 = z_acc[slice_end:end-2].values - z_acc[slice_end+1:end-1].values
        player_load += np.sqrt((x_diff2**2 + y_diff2**2 + z_diff2**2)/100).sum()
    
    return player_load

def calculate_player_load(kinematics_folder, trial_number, start, end=None, slice_start=None, slice_end=None):
    """ Calculates the player load across the duration of a trial or point.
    ----------
    Parameters
    trial_number: string of the trial number to extract
    start: int of the start frame for the calculation (default is None)
    end: int of the end frame for the calculation (default is None)
    first_end: int of the frame to begin a slice of data (default is None)
    first_start: int of the frame to end a slice of data (default is None)
    ----------
    Returns
    A player load value of the player load across that point
    """
    rows_of_data_to_skip = rows_to_skip
    kinematics_df = create_kinematics_dataframe(kinematics_folder, trial_number, keypoint, rows_of_data_to_skip)
    if kinematics_df is None:
        return 0
    else:
        x_acc = kinematics_df[f"{keypoint}_X (m/s^2)"]
        y_acc = kinematics_df[f"{keypoint}_Y (m/s^2)"]
        z_acc = kinematics_df[f"{keypoint}_Z (m/s^2)"]
        if end is None:
            player_load = calculate_player_load_vectorized(x_acc, y_acc, z_acc, 0, len(kinematics_df))
            print(f"Processing data for trial number {trial_number}.")
            return player_load
        elif end and not slice_start:
            if start - rows_of_data_to_skip <= 0:
                start = 1
            else:
                start -= rows_of_data_to_skip
                end -= rows_of_data_to_skip
            if end > len(kinematics_df):
                end = len(kinematics_df)
            player_load = calculate_player_load_vectorized(x_acc, y_acc, z_acc, start, end)
            print(f"Processing data for trial number {trial_number}.")
            return player_load
        elif slice_start:
            #we cannot start from a negative number so must begin start at 0 
            if start - rows_of_data_to_skip <= 0:
                start = 1
            else:
                start -= rows_of_data_to_skip
                end -= rows_of_data_to_skip
                slice_start -= rows_of_data_to_skip
                slice_end -= rows_of_data_to_skip
            if end > len(kinematics_df):
                end = len(kinematics_df)
            player_load = calculate_player_load_vectorized(x_acc, y_acc, z_acc, start, end, slice_start, slice_end)
            print(f"Processing data for trial number {trial_number}.")
            return player_load

#if you want to calculate an individual trial, because you are slicing it up, you can use the following code
trial_number = "02"
start = 0
end = 500
slice_start = 1
slice_end = 60

player_load = calculate_player_load(kinematics_folder, trial_number, start, end, slice_start, slice_end)
print(player_load)