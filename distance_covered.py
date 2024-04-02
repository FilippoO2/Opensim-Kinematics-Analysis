import pandas as pd
import numpy as np
from full_body_kinematics import create_kinematics_dataframe
from config import kinematics_folder, keypoint, rows_to_skip, participant_mass, csv_file, sheet_name

def adjust_frame_numbers(rows_of_data_to_skip, start, end, slice_start=None, slice_end=None):
    if start - rows_of_data_to_skip <= 0:
        start = 1
    else:
        start -= rows_of_data_to_skip
    end -= rows_of_data_to_skip
    if slice_start is not None and slice_end is not None:
        slice_start -= rows_of_data_to_skip
        slice_end -= rows_of_data_to_skip
        return start, end, slice_start, slice_end
    return start, end

def calculate_distance_covered(kinematics_folder, trial_number, start, end=None, slice_start=None, slice_end=None):
    """ Calculates the negative and positive external mechanical works.
    ----------
    Parameters
    trial_number: string of the trial number to extract
    start: int of the start frame for the calculation (default is None)
    end: int of the end frame for the calculation (default is None)
    first_end: int of the frame to begin a slice of data (default is None)
    first_start: int of the frame to end a slice of data (default is None)
    ----------
    Returns
    An updated data frame for that trial with the negative and positive external mechanical works
    """
    rows_of_data_to_skip = rows_to_skip
    kinematics_df = create_kinematics_dataframe(kinematics_folder, trial_number, keypoint, rows_of_data_to_skip)
    if kinematics_df is None:
        print(f"No data for Trial Number {trial_number}. Skipping...")
        return 0
    else:
        x_position = kinematics_df[f"{keypoint}_X (m)"]
        y_position = kinematics_df[f"{keypoint}_Y (m)"]
        z_position = kinematics_df[f"{keypoint}_Z (m)"]
        # if end is None, we have not been given a point and calculate the work for the entire trial
        if end is None:
            #calculate the distance covered by the keypoint
            x_diff = x_position.diff()
            y_diff = y_position.diff()
            z_diff = z_position.diff()
            # Calculate Euclidean distance
            distance = np.sqrt(x_diff**2 + y_diff**2 + z_diff**2).sum()
            print(f"Processing data for trial number {trial_number}.")# Calculate differences between consecutive points
            return distance
        #if we have been given an end frame but no slice, we calculate the work for that time (usually a point within a trial)
        elif end and not slice_start:
            start, end = adjust_frame_numbers(rows_of_data_to_skip, start, end)
            # Slice the dataframes to the desired range
            x_position_range = x_position.iloc[start:end]
            y_position_range = y_position.iloc[start:end]
            z_position_range = z_position.iloc[start:end]
            #calculate differences between consecutive points
            x_diff = x_position_range.diff()
            y_diff = y_position_range.diff()
            z_diff = z_position_range.diff()
            # Calculate Euclidean distance
            distance = np.sqrt(x_diff**2 + y_diff**2 + z_diff**2).sum()
            print(f"Processing data for trial number {trial_number}.")# Calculate differences between consecutive points
            return distance
        #if we have a slice point, we use first_end and first_start to slice points within start and end
        elif slice_start:
            distance = 0
            start, end, slice_start, slice_end = adjust_frame_numbers(rows_of_data_to_skip, start, end, slice_start, slice_end)
            #calculate the distance covered by the keypoint
            # Slice the dataframes to the desired range
            x_position_range = x_position.iloc[start:slice_start]
            y_position_range = y_position.iloc[start:slice_start]
            z_position_range = z_position.iloc[start:slice_start]
            #calculate differences between consecutive points
            x_diff = x_position_range.diff()
            y_diff = y_position_range.diff()
            z_diff = z_position_range.diff()
            # Calculate Euclidean distance
            d1 = np.sqrt(x_diff**2 + y_diff**2 + z_diff**2).sum()
            distance += d1
            # Slice the dataframes to the desired range
            x_position_range2 = x_position.iloc[slice_end:end]
            y_position_range2 = y_position.iloc[slice_end:end]
            z_position_range2 = z_position.iloc[slice_end:end]
            #calculate differences between consecutive points
            x_diff2 = x_position_range2.diff()
            y_diff2 = y_position_range2.diff()
            z_diff2 = z_position_range2.diff()
            # Calculate Euclidean distance
            d2 = np.sqrt(x_diff2**2 + y_diff2**2 + z_diff2**2).sum()
            distance += d2
            print(f"Processing data for trial number {trial_number}.")
            return distance

# If you want to calculate an individual trial, because you are slicing it, you can use the following code
trial_number = "02"
start = 0
end = 500
slice_start = 0
slice_end = 60

distance = calculate_distance_covered(kinematics_folder, trial_number, start, end, slice_start, slice_end)
print(distance)
