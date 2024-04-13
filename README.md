# OpenSim Kinematics Analysis

Kinematic analysis of data from OpenSim .sto files
- Extracts distance covered, 'player load' and external mechanical work of a keypoint (e.g. centre of mass) for a specified time frame within a trial (e.g. a rally within a match).
- Analyses heart rate data. 
- Provides visualisations of key point kinematics.

How the package works:

config.py - where you set the variables needed to run the package.

point_dict_creator.py - Reads an Excel file containing the point start and end frames within a trial. This is used to crop data so that measurements are made for movement during points only.

full_body_kinematics.py - creates a pandas dataframe for the trial of interest using the associated position and velocity .sto files. Resultant velocity, accelerations and energies are calculated and added to the dataframe.

player_load.py - Using the accelerations from the dataframe, a player load value is calculated for the specified time. The equation used for this can be found from Boyd et al.(2011):  [https://journals.humankinetics.com/view/journals/ijspp/6/3/article-p311.xml](https://doi.org/10.1123/ijspp.6.3.311) 

distance_covered.py - Calculates the total distance covered by summing the incremental distances along each axis of movement.

external_mechanical_work.py - Computes the changes in total energy across the point. Increments are summed to return a positive external work value. Decrements are summed to return a negative work external work value. 

heart_rate.py - Reads a csv containing heart rate data, calculates the average, max and Edward's TRIMP score (From the heart rate monitor book by Sally Edwards). 

write_results.py - Writes the results to csv files that are stored in a specified folder.

visualise_data.py - Can be used to visualise a plot for each point. Is able to plot position, velocity, acceleration or mechanical energy.
