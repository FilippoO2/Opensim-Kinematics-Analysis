import os

# The variables you need to change:

# The keypoint of interest e.g. ("center_of_mass")
keypoint = 

#Name of participants folder e.g. ("P01")
participant = 
participant_mass =    # kg
participant_age =     # years

# The number of rows to skip in the kinematic data - Needed if model does not start in correct position 
rows_to_skip = 35
# csv file path containing the trial point start and end frames for the participant - see point_dict_creator.py for more information on csv_file setup
csv_file =  
sheet_name = None # Needed if trials are on a specific sheet

# The path to the folder containing the .sto files of kinematic data
kinematics_folder = f"......{participant}/trc_hrnet/kinematics"
#Where you want to write the extracted metrics to
data_path = f"......{participant}"

# Path where you want to save plots (inside P01 directory)
plot_path = f"......{participant}/plots"

#Type of data to plot - Can be ["Position", "Velocity", "Acceleration" or "Energy"]
plot_data = "Energy"

heart_rate_folder =  # path to directory with heart rate data
