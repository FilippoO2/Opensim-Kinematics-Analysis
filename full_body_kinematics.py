import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
from config import kinematics_folder, keypoint, rows_to_skip, participant_mass, csv_file, sheet_name


def extract_labels(filename):
    """ Read the .sto file and return the labels (column names). """
    with open(filename, 'r') as file:
        # Skip initial lines until the line starting with 'time' is found
        for line in file:
            if line.startswith('time'):
                # Extract labels from the line starting with 'time'
                labels = line.strip().split('\t')
                return labels
    # If 'time' is not found, raise an error
    raise ValueError("Labels starting with 'time' not found in the file.")


def create_kinematics_dataframe(kinematics_folder, trial_number, keypoint, rows_of_data_to_skip, planes = ["X", "Y", "Z"]): 
    """ Extracts kinematic data of a keypoint from an OpenSim .sto file.
    ----------
    Parameters
    kinematics_folder: name of the folder containing the kinematics files
    trial_number: string of the trial number to extract
    keypoint: string of the keypoint to extract
    planes: list of strings of the planes to extract (default is ["X", "Y", "Z"] - other choices are ["Ox", "Oy", "Oz"])
    ----------
    Returns
    A dataframe for that trial with position, velocity and acceleration data for the keypoint in the specified planes
    """
    rows_of_data_to_skip = rows_to_skip

    #create filelise of relevant files for that trial
    filelist = [os.path.join(kinematics_folder,f) for f in os.listdir(kinematics_folder) if trial_number in f and "global" in f]

    if not filelist:  # If file list is empty
        print(f"No files found for trial number {trial_number}. Skipping...")
        pass
    else:
        keypoint_data = pd.DataFrame()  # Initialize an empty DataFrame to store the keypoint data

        #loop through the .sto files for that trial
        for filename in filelist:
            if "BodyKinematics_pos_global" in filename:
                labels = extract_labels(filename)
                # Extract the keypoint data
                pos_data_frame = pd.read_csv(filename, sep="\t", skiprows=rows_to_skip, names=labels)  
                keypoint_data["time"] = pos_data_frame["time"].iloc[rows_of_data_to_skip:]
                for plane in planes:
                    # add the values to our dataframe
                    keypoint_data[f"{keypoint}_{plane} (m)"] = pos_data_frame[f"{keypoint}_{plane}"].iloc[rows_of_data_to_skip:]
            #if file contains velocity data
            elif "BodyKinematics_vel_global" in filename: 
                labels = extract_labels(filename)
                # Extract the keypoint data
                vel_data_frame = pd.read_csv(filename, sep="\t", skiprows=rows_to_skip, names=labels)
                for plane in planes:
                    # add the values to our dataframe
                    keypoint_data[f"{keypoint}_{plane} (m/s)"] = vel_data_frame[f"{keypoint}_{plane}"].iloc[rows_of_data_to_skip:]
                    time_diff = keypoint_data["time"].diff()
                    keypoint_data[f"{keypoint}_{plane} (m/s^2)"] = keypoint_data[f"{keypoint}_{plane} (m/s)"].diff()/ time_diff            
            else:
                pass       
        return keypoint_data
   


#calculate potential and kinetic energy of the keypoint
def calculate_mech_energies(kinematics_folder, trial_number):
    """ Calculates the potential, kinetic and total energy of the keypoint.
    ----------
    Parameters
    kinematics_folder: string of the folder containing the kinematics files
    trial_number: string of the trial number to extract
    ----------
    Returns
    An updated data frame for that trial with the potential, kinetic and total energy of the keypoint
    """
    rows_of_data_to_skip = rows_to_skip
    # Create the kinematic dataframe using the function from above 
    kinematics_df = create_kinematics_dataframe(kinematics_folder, trial_number, keypoint, rows_of_data_to_skip)
    # make sure the dataframe exists
    if kinematics_df is not None:
        #potential_energy = mass * g * height (Y-axis)
        if f"{keypoint}_Y (m)" in kinematics_df.columns:
            pe = participant_mass * 9.81 * kinematics_df[f"{keypoint}_Y (m)"]
        else:
            print(f"Column {keypoint}_Y (m) not found in DataFrame")
        #kinetic_energy = 0.5 * mass * velocity^2
        kinematics_df["Resultant Velocity (m/s)"] = np.sqrt(kinematics_df[f"{keypoint}_X (m/s)"]**2 + kinematics_df[f"{keypoint}_Y (m/s)"]**2 + kinematics_df[f"{keypoint}_Z (m/s)"]**2)
        ke = 0.5 * participant_mass * kinematics_df["Resultant Velocity (m/s)"]**2
        #print(ke)
        #total energy = pe + ke
        te = pe + ke
        # change in total energy
        delta_te = te.diff()

        #add these energies to our dataframe
        kinematics_df["Potential Energy (J)"] = pe
        kinematics_df["Kinetic Energy (J)"] = ke
        kinematics_df["Total Energy (J)"] = te
        kinematics_df["Change in Total Energy (J)"] = delta_te
        
        #Check your dataframe using 
        #print(kinematics_df)

        return kinematics_df
    else:
        pass


