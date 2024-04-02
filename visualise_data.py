import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from full_body_kinematics import create_kinematics_dataframe, calculate_mech_energies
from config import kinematics_folder, keypoint, csv_file, sheet_name, plot_path, plot_data, rows_to_skip
from point_dict_creator import create_point_dict

def generate_plots_in_loop(kinematics_folder, trial_dict, data_type, file_path):
    """
    Generate plots for each trial number and store them in a list.
    
    Parameters:
        kinematics_folder (str): Folder containing kinematics files.
        trial_numbers (list of str): List of trial numbers.
    
    Returns:
        list of matplotlib.pyplot.Figure: List of plots generated for each trial.
    """
    plots = []  # List to store the plots
    rows_of_data_to_skip = rows_to_skip

    for trial_number in trial_dict:
        trial_num = trial_number[-2:]
        df = calculate_mech_energies(kinematics_folder, trial_num)
        if df is None:
            print(f"No data for Trial Number {trial_number}. Skipping...")
            continue        
        trial_points = trial_dict[trial_number]
        for point_num in trial_points:
            point_start = trial_points[point_num][0]
            point_end = trial_points[point_num][1]
            if data_type == "Position":
                time = df['time'].iloc[point_start:point_end]
                # Calculate the offset to adjust the time values
                time_offset = time.iloc[0]
                # Subtract the offset from all the time values
                time -= time_offset
                x_position = df[f'{keypoint}_X (m)'].iloc[point_start:point_end]
                y_position = df[f'{keypoint}_Y (m)'].iloc[point_start:point_end]
                z_position = df[f'{keypoint}_Z (m)'].iloc[point_start:point_end]
                plt.figure()
                plt.plot(time, x_position, label='X Position', color='black', linestyle='dashed')
                plt.plot(time, y_position, label='Y Position', color='black', linestyle='dotted')
                plt.plot(time, z_position, label='Z Position', color='black', linestyle='solid')
                plt.title(f'{trial_number} {point_num} - Position vs Time', fontsize=12, font = 'Times New Roman')
                plt.xlabel('Time (s)', fontsize=12, font = 'Times New Roman')
                plt.ylabel("Position (m)", fontsize=12, font = 'Times New Roman')
                plt.legend()
            elif data_type == "Velocity":
                time = df['time'].iloc[point_start:point_end]
                # Calculate the offset to adjust the time values
                time_offset = time.iloc[0]
                # Subtract the offset from all the time values
                time -= time_offset
                x_velocity = df[f'{keypoint}_X (m/s)'].iloc[point_start:point_end]
                y_velocity = df[f'{keypoint}_Y (m/s)'].iloc[point_start:point_end]
                z_velocity = df[f'{keypoint}_Z (m/s)'].iloc[point_start:point_end]
                plt.figure()
                plt.plot(time, x_velocity, label='X Velocity', color='black', linestyle='dashed')
                plt.plot(time, y_velocity, label='Y Velocity', color='black', linestyle='dotted')
                plt.plot(time, z_velocity, label='Z Velocity', color='black', linestyle='solid')
                plt.title(f'{trial_number} {point_num} - Velocity vs Time', fontsize=12, font = 'Times New Roman')
                plt.xlabel('Time (s)', fontsize=12, font = 'Times New Roman')
                plt.ylabel("Velocity (m/s)", fontsize=12, font = 'Times New Roman')
                plt.legend(prop={'family' : 'Times New Roman', 'size'   : 12})
            elif data_type == "Acceleration":
                time = df['time'].iloc[point_start:point_end-1]
                # Calculate the offset to adjust the time values
                time_offset = time.iloc[0]
                # Subtract the offset from all the time values
                time -= time_offset
                x_acceleration = df[f'{keypoint}_X (m/s^2)'].iloc[point_start:point_end-1]
                y_acceleration = df[f'{keypoint}_Y (m/s^2)'].iloc[point_start:point_end-1]
                z_acceleration = df[f'{keypoint}_Z (m/s^2)'].iloc[point_start:point_end-1]
                plt.figure()
                plt.plot(time, x_acceleration, label='X Acceleration', color='black', linestyle='dashed')
                plt.plot(time, y_acceleration, label='Y Acceleration', color='black', linestyle='dotted')
                plt.plot(time, z_acceleration, label='Z Acceleration', color='black', linestyle='solid')
                plt.title(f'{trial_number} {point_num} - Acceleration vs Time', fontsize=12, font = 'Times New Roman')
                plt.xlabel('Time (s)', fontsize=12, font = 'Times New Roman')
                plt.ylabel("Acceleration (m/s^2)", fontsize=12, font = 'Times New Roman')
                plt.legend(prop={'family' : 'Times New Roman', 'size'   : 12})
            elif data_type == "Energy":
                time = df['time'].iloc[point_start:point_end]
                # Calculate the offset to adjust the time values
                time_offset = time.iloc[0]
                # Subtract the offset from all the time values
                time -= time_offset
                pe = df['Potential Energy (J)'].iloc[point_start:point_end]
                ke = df['Kinetic Energy (J)'].iloc[point_start:point_end]
                te = df['Total Energy (J)'].iloc[point_start:point_end]
                plt.figure()
                plt.plot(time, pe, label='Potential Energy',color='black', linestyle='dashed')
                plt.plot(time, ke, label='Kinetic Energy', color='black', linestyle='dotted')
                plt.plot(time, te, label='Total Energy', color='black', linestyle='solid')
                plt.title(f'{trial_number} {point_num} - Energy vs Time', fontsize=12, font = 'Times New Roman')
                plt.xlabel('Time (s)', fontsize=12, font = 'Times New Roman')
                plt.ylabel('Energy (J)', fontsize=12, font = 'Times New Roman')
                plt.legend(prop={'family' : 'Times New Roman', 'size' : 12})
                ax = plt.gca()
                    # Setting font properties for the tick labels
                ax.tick_params(axis='both', which='major', labelsize=12, labelcolor='black', labelfontfamily='Times New Roman')
    
            else:
                print("Make sure you have entered a suitable data type into the config file. Options are: 'Position', 'Velocity', 'Acceleration' or 'Energy'")

            #save fig to file path location
            file_name = f"{trial_number}_{point_num}_{data_type}.png"
            plt.savefig(os.path.join(file_path, file_name), dpi = 1200)
            print("Plot saved as: ", file_name)
            plt.close()
            
    
    print(f"All plots of {data_type} saved in {file_path}.")

# Get the point directory using the csv file and sheetname from the directory
trial_dict = create_point_dict(csv_file, sheet_name)

# Create a folder to store the plots - plot_path and plot_data are accessed in config file
plot_data_path = os.path.join(plot_path, plot_data)
os.makedirs(plot_data_path, exist_ok=True)

all_plots = generate_plots_in_loop(kinematics_folder, trial_dict, plot_data, plot_data_path)
