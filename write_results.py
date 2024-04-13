import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
import point_dict_creator
from external_mechanical_work import calculate_external_mechanical_work
from distance_covered import calculate_distance_covered
from player_load import calculate_player_load
from config import kinematics_folder, keypoint, rows_to_skip, participant_mass, csv_file, sheet_name, data_path


def extract_metric_for_each_point(kinematics_folder, trial_dict, metric = "Work Done"):
    """ Extracts the negative and positive work for each point in a dictionary.
    ----------
    Parameters
    kinematics_folder: string of the folder containing the kinematics files
    point_dict: dictionary of the points to extract the work from
    metric: string of the metric to extract - Work Done, Distance Covered or Player Load (Boyd et al., 2011)
    ----------
    Returns
    A dictionary of the desired metric for each point
    """
    metric_dict = {}
    #iterate through the trial dictionary and assign the trials and points to the work dictionary 
    for trial, point_dict in trial_dict.items():
        metric_dict[trial] = {}
        for point, frames in point_dict.items():
            #calculate the work for each point and add it to the value of that trial key
            if metric == "Work Done":
                neg_work, pos_work = calculate_external_mechanical_work(kinematics_folder, trial[-2:], start=frames[0], end=frames[1])
                if neg_work is not None and pos_work is not None:
                    metric_dict[trial][point] = {"Negative Work": neg_work, "Positive Work": pos_work}
            elif metric == "Distance Covered":
                distance =  calculate_distance_covered(kinematics_folder, trial[-2:], start=frames[0], end=frames[1])
                if distance is not None:
                    metric_dict[trial][point] = distance
            elif metric == "Player Load":
                player_load = calculate_player_load(kinematics_folder, trial[-2:], start=frames[0], end=frames[1])
                if player_load is not None:
                    metric_dict[trial][point] = player_load
            else:
                print("Error: Maybe you didn't type the metric correctly. Options are: 'Work Done', 'Distance Covered' or 'Player Load'.")
    return metric_dict


def write_metric_to_csv(kinematics_folder, trial_dict, metric, rows_to_skip = 50):
    """ Writes the metric of choice for each point to a CSV file.
    ----------
    Parameters
    kinematics_folder: string of the folder containing the kinematics files
    Dictionary of the points to extract the metric from
    Metric of choice - Work Done, Distance Covered or Player Load (Boyd et al., 2011)
    ----------
    Returns
    A CSV file of the desired metric for each point
    """
    if not os.path.exists(data_path):
        # If not, create it
        os.makedirs(data_path)
    if metric == "Work Done":
        work_dict = extract_metric_for_each_point(kinematics_folder, trial_dict, "Work Done")
        filename = os.path.join(data_path + "/point_works.csv")
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Trial", "Point", "Negative Work (J)", "Positive Work (J)"])
            for trial, point_dict in work_dict.items():
                for point, works in point_dict.items():
                    writer.writerow([trial[-2:], point[-1], works["Negative Work"], works["Positive Work"]])

    elif metric == "Distance Covered":
        distance_dict = extract_metric_for_each_point(kinematics_folder, trial_dict, "Distance Covered")
        filename = os.path.join(data_path + "/distance_covered.csv")
        with open(filename, "w", newline = '') as file:
            writer = csv.writer(file)
            writer.writerow(["Trial", "Point", "Distance Covered (m)"])
            for trial, point_dict in distance_dict.items():
                for point, distance in point_dict.items():
                    writer.writerow([trial[-2:], point[-1], distance])
    
    elif metric == "Player Load":
        player_load_dict = extract_metric_for_each_point(kinematics_folder, trial_dict, "Player Load")
        filename = os.path.join(data_path + "/player_load.csv")
        with open(filename, "w", newline = '') as file:
            writer = csv.writer(file)
            writer.writerow(["Trial", "Point", "Player Load (AU)"])
            for trial, point_dict in player_load_dict.items():
                for point, player_load in point_dict.items():
                    writer.writerow([trial[-2:], point[-1], player_load])



#create dict of points for each trial - needed to crop data to points
trial_dict = point_dict_creator.create_point_dict(csv_file, sheet_name) 

#Example use of extracting EMW, Distance Covered and Player Load from all points from one participant 
for metric in ["Distance Covered", "Player Load", "Work Done"]:
    write_metric_to_csv(kinematics_folder, trial_dict, metric)

