import os

# The variables you need to change:

# The keypoint of interest
keypoint = "center_of_mass"

participant = "Doubles-1/P05"
participant_mass = 82.2
participant_age = 20

# The number of rows to skip in the kinematic data -  Needed if model does not start in correct position
rows_to_skip = 35
# The path to the csv file containing the trial and point start and end frames
# See point_dict_creator.py for more information on csv_file setup
csv_file = "D:/filip/Notational anaylsis updated.xlsx" 
sheet_name = "Doubles 1" # Needed if trials are on a specific sheet

# The path to the folder containing the .sto files of kinematic data
kinematics_folder = f"D:/filip/Python/Badminton Data/{participant}/trc_hrnet/kinematics" # path to directory with kinematic data
#Where you want to write the extracted metrics to
data_path = f"D:/filip/Python/Badminton Data/{participant}"

# Path where you want to save plots (inside P01 directory)
plot_path = f"D:/filip/Python/Badminton Data/{participant}/plots"

#Type of data to plot - Can be ["Position", "Velocity", "Acceleration" or "Energy"]
plot_data = "Energy"

heart_rate_folder = "D:/filip/Python/Badminton Data/Heart Rate Data" # path to directory with heart rate data