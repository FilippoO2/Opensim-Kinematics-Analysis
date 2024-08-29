import os
import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import csv
from config import csv_file, sheet_name


def create_point_dict(csv_file, sheet_name=None):
    """ Creates a dictionary that contains the frame numbers for the points in each trial.
    The dictionary will be used to crop the data just to the points.
    -------
    Parameters:
    Path to the CSV file containing the points of interest
    Name of sheet if in an Excel Workbook
    -------
    Required CSV file headers and format example:
    Trial, Point, Point Start Frame, Point End Frame
    01, 1, 0, 2952
    01, 2, 4000, 5603
    -------
    Output:
    Dictionary with the following format used to crop data to the points of interest:
    {
        "trial_01": {
            "point1": [0, 2952],
            "point2": [4000, 5603]}, 
        "trial_02": {
            "point1": [0, 2100],
            "point2": [3715, 4737]},
        ...
    }
    """ 
    # Read csv file  
    if sheet_name:
        df = pd.read_excel(csv_file, sheet_name=sheet_name)
    else:
        df = pd.read_csv(csv_file)
    # Create empty dictionary to store trials and points
    trial_dict = {}

    #if a value is null, it will be filled in with the value from the previous row (suitable only for filling in trial numbers!)
    df.ffill(inplace=True)

    # Iterate over the rows of the DataFrame
    for _, row in df.iterrows():
        if pd.isnull(row["Trial"]) or row["Trial"] == "Trial":
            continue
        trial_num = int(row["Trial"])
        # the trial number needs to be in the format 01, 02, 03, etc.
        if trial_num < 10:
            trial_num = f"0{trial_num}"

        # Extract trial number, point number, start frame, and end frame from each row
        trial_num = f"trial_{trial_num}"
        point_num = f"point{row['Point']}"
        start_frame = row['Point Start Frame']
        end_frame = row['Point End Frame']

        # Create a list with start and end frames
        frame_pair = [start_frame, end_frame]

        # Stop the loop if the trial number is not a number (i.e. you have reached the end of the trials)
        if not str(row['Trial']).isdigit():
            break        
        # Check if the trial number is already in the result dictionary
        if trial_num not in trial_dict:
            # If not, add the trial number as a key with an empty dictionary as its value
            trial_dict[trial_num] = {}

        # Add the point number and its corresponding frame pair to the trial
        trial_dict[trial_num][point_num] = frame_pair
        
        # Update last_trial_num and last_end_frame for the next iteration
        last_trial_num = trial_num
        last_end_frame = end_frame
    return trial_dict

# to check a dictionary is correct you can use:
#print(create_point_dict(csv_file, sheet_name))
