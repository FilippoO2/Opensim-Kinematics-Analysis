import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from config import heart_rate_folder, participant_age

hr_max = 220 - participant_age

zones_coefficients = [
    (0.5*hr_max,0.6*hr_max,1),
    (0.6*hr_max,0.7*hr_max,2),
    (0.7*hr_max,0.8*hr_max,3),
    (0.8*hr_max,0.9*hr_max,4),
    (0.9*hr_max,1*hr_max,5),
]


def convert_hours_to_seconds(time):
    time = time.split(":")
    hours = int(time[0])
    minutes = int(time[1])
    seconds = int(time[2])
    return hours*3600 + minutes*60 + seconds


def calculate_trimp_score(heart_rates):
    """ Calculate the TRIMP score for a given list of heart rates
    --------
    Parameters
    heart_rates: list of heart rates
    --------
    Returns
    float of the TRIMP score
    """
    time_spent_in_zone = {1:0,2:0,3:0,4:0,5:0}

    for hr in heart_rates:
        for lower, upper, coefficient in zones_coefficients:
            if lower<= hr <= upper:
                time_spent_in_zone[coefficient] += 1

    trimp_total = sum(key*val for key, val in time_spent_in_zone.items()) / 60
    return trimp_total


def process_files(heart_rate_folder, discipline, start, end):
    """ Process the heart rate files for a given discipline
    --------
    Parameters
    heart_rate_folder: string of the folder containing the heart rate data
    discipline: string of the discipline to process
    start: int of the start frame for the calculation
    end: int of the end frame for the calculation
    --------
    Returns
    A data frame of the results
    """
    file_list = os.listdir(os.path.join(heart_rate_folder, discipline))
    results = pd.DataFrame(columns=["File", "Average", "Max", "TRIMP"])

    for file in file_list:
        file_path = os.path.join(heart_rate_folder, discipline, file)
        data = pd.read_csv(file_path, header=2).iloc[start:end]
        heart_rate_values = data['HR (bpm)']
        time = data['Time']

        average_hr = np.mean(heart_rate_values)
        max_hr = np.max(heart_rate_values)
        trimp = calculate_trimp_score(heart_rate_values)

        results = results._append({"Discipline": discipline, "Average": average_hr, "Max": max_hr, "TRIMP": trimp}, ignore_index=True)

        plt.title(file)
        time_seconds = [convert_hours_to_seconds(t) for t in time]
        plt.plot(time_seconds, heart_rate_values)
        #plt.show()

    return results


def write_results(results, filename):
    results.to_csv(filename, mode='a', index=False)



results_folder = ""
discipline = "Men's Singles"
start = 60
end = 2800

results = process_files(heart_rate_folder, discipline, start, end)
write_results(results, results_folder)
