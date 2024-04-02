import os
import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import csv
import numpy as np
from full_body_kinematics import calculate_mech_energies
from config import kinematics_folder, keypoint, rows_to_skip, participant_mass, csv_file, sheet_name




def calculate_external_mechanical_work(kinematics_folder, trial_number, start, end=None, slice_start=None, slice_end=None):
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
    kinematics_df = calculate_mech_energies(kinematics_folder, trial_number)
    if kinematics_df is None:
        print(f"No data for Trial Number {trial_number}. Skipping...")
        return 0,0
    else:
        delta_te = kinematics_df["Change in Total Energy (J)"]
        rows_of_data_to_skip = rows_to_skip
        delta_te_negative = delta_te < 0
        delta_te_positive = delta_te > 0
        # if end is None, we have not been given a point and calculate the work for the entire trial
        if end is None:
            #negative work is the sum of all the negative changes in energy
            negative_work = delta_te[delta_te_negative].sum()
            #positive work is the sum of all the positive changes in energy
            positive_work = delta_te[delta_te_positive].sum()
            print(f"Processing data for trial number {trial_number}.")
            return negative_work, positive_work
        #if we have been given an end frame but no slice, we calculate the work for that time (usually a point within a trial)
        elif end and not slice_start:
            #because we have skipped rows, we need to adjust the start and end frames
            #we cannot start from a negative number so must begin start at 0 
            if start - rows_of_data_to_skip <= 0:
                start = 1
            else:
                start -= rows_of_data_to_skip
                end -= rows_of_data_to_skip
            #negative work is the sum of all the negative changes in energy
            negative_work = delta_te[start:end][delta_te_negative].sum()
            #positive work is the sum of all the positive changes in energy
            positive_work = delta_te[start:end][delta_te_positive].sum()
            print(f"Processing data for trial number {trial_number}.")
            return negative_work, positive_work
        #if we have a slice point, we use first_end and first_start to slice points within start and end
        elif slice_start:
            #we cannot start from a negative number so must begin start at 0 
            if start - rows_of_data_to_skip <= 0:
                start = 1
            else:
                start -= rows_of_data_to_skip
                end -= rows_of_data_to_skip
                slice_start -= rows_of_data_to_skip
                slice_end -= rows_of_data_to_skip
            #negative work is the sum of all the negative changes in energy
            negative_work = delta_te[start:slice_start][delta_te_negative].sum() + delta_te[slice_end:end][delta_te < 0].sum()
            #positive work is the sum of all the positive changes in energy
            positive_work = delta_te[start:slice_start][delta_te_positive].sum() + delta_te[slice_end:end][delta_te > 0].sum()
            print(f"Processing data for trial number {trial_number}.")
            return negative_work, positive_work
        else:
            print(f"Error calculating work for trial {trial_number}")
            return 0,0

# If you want to calculate an individual trial, because you are slicing it up, you can use the following code
trial_number = "02"
start = 0
end = 500
slice_start = 1
slice_end = 60


negative_work, positive_work = calculate_external_mechanical_work(kinematics_folder, trial_number, start, end, slice_start, slice_end)
print(negative_work, positive_work)

