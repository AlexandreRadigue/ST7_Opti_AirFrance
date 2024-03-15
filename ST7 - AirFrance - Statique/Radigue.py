# Modules de base
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Module relatif à Gurobi
from gurobipy import *

# Module csv
import csv
import matplotlib.pyplot as plt

# Module Time
import threading
import time


number_of_seats = 174

# Load the Excel file into a pandas DataFrame

df_21Oct = pd.read_excel('ST7 - AirFrance/DataSeating 2024.xlsx', sheet_name=0 , skipfooter=2)
df_22Oct = pd.read_excel('ST7 - AirFrance/DataSeating 2024.xlsx', sheet_name=1 , skipfooter=2)
df_23Oct = pd.read_excel('ST7 - AirFrance/DataSeating 2024.xlsx', sheet_name=2 , skipfooter=2)
df_24Oct = pd.read_excel('ST7 - AirFrance/DataSeating 2024.xlsx', sheet_name=3 , skipfooter=2)
df_30Oct = pd.read_excel('ST7 - AirFrance/DataSeating 2024.xlsx', sheet_name=4 , skipfooter=2)
df_05Nov = pd.read_excel('ST7 - AirFrance/DataSeating 2024.xlsx', sheet_name=5 , skipfooter=2)
df_07Nov = pd.read_excel('ST7 - AirFrance/DataSeating 2024.xlsx', sheet_name=6 , skipfooter=2)

# On créer la liste de dataframes

df = [df_21Oct, df_22Oct, df_23Oct, df_24Oct, df_30Oct, df_05Nov, df_07Nov]

# Number of rows and columns per row based on the airplane configuration
number_of_rows = 29  # Rows are 1-indexed from 1 to 29
seats_per_row = 6    # 6 seats per row (0,1,2,3,4,5)
number_of_seats = 174
weight_f = 70 # weight female
weight_m = 85 # weight male
weight_d = 92.5 # weight disabled

# Fonction Passagers


def optimisation(i):

    Passagers = dict()
    number_f = 0
    number_m = 0
    number_d = 0

    for group in df[i].itertuples():
        for j in range(2,5):
            if not pd.isna(group[j]):
                for k in range(int(group[j])):
                    Passagers[i] = {'gender': j-2, 'group':group[1], 'transit': float('inf') }
                    if group[5].hour*60 + group[5].minute != 0:
                        Passagers[i]['transit'] = group[5].hour*60 + group[5].minute
                    if j == 2: number_f+=1
                    elif j==3: number_m+=1
                    else: number_d+=1
                    i+=1

    m = Model("airplane_seating")

    # Weights is a dictionary mapping (i, j, k) to a weight, as discussed earlier

    # Create decision variables for each seat and passenger
    # The decision variable x will be a 3D dictionary with the keys being the row number,
    # the seat within the row, and the unique identifier for each passenger.

    AssignmenVarDict = {(i, j, k) : m.addVar(vtype = GRB.BINARY, name=f'passager_{i}_{j}_{k}')
                        for i in range(1, number_of_rows + 1)
                        for j in range(1, seats_per_row + 1)
                        for k in range(1, len(Passagers)+1)}
    # Each passenger has a seat
    SEATSASSIGNMENTCONST = m.addConstr(quicksum([AssignmenVarDict[(i, j, k)]
                                                for i in range(1, number_of_rows + 1)
                                                for j in range(1, seats_per_row + 1)
                                                for k in range(1,len(Passagers)+1)]) == len(Passagers))
    # Each passenger must have one seat
    PERSONSEATCONSTDIC = { k: m.addConstr(quicksum([AssignmenVarDict[(i, j, k)]
                                                    for i in range(1, number_of_rows + 1)
                                                    for j in range(1, seats_per_row + 1) ]) == 1)
                                                    for k in range(1,len(Passagers)+1) }
    # Constraint Airplane Centrage
    i_m = quicksum([weight_m * i* AssignmenVarDict[(i, j, k)]
                    for i in range(1, number_of_rows+1)
                    for j in range(1, seats_per_row+1 )
                    for k in range(1, len(Passagers)+1)
                    if Passagers[k]['gender']==1])
    i_f = quicksum([weight_m * i* AssignmenVarDict[(i, j, k)]
                    for i in range(1, number_of_rows+1)
                    for j in range(1, seats_per_row+1 )
                    for k in range(1, len(Passagers)+1)
                    if Passagers[k]['gender']==0])
    i_h = quicksum([weight_m * i* AssignmenVarDict[(i, j, k)]
                    for i in range(1, number_of_rows+1)
                    for j in range(1, seats_per_row+1 )
                    for k in range(1, len(Passagers)+1)
                    if Passagers[k]['gender']==2])

    i_bary = (i_m + i_f +i_h)/( weight_m * number_m + weight_f * number_f + weight_d * number_d)

    j_m = quicksum([weight_m * j* AssignmenVarDict[(i, j, k)]
                    for i in range(1, number_of_rows+1)
                    for j in range(1, seats_per_row+1 )
                    for k in range(1, len(Passagers)+1)
                    if Passagers[k]['gender']==1])
    j_f = quicksum([weight_m * j* AssignmenVarDict[(i, j, k)]
                    for i in range(1, number_of_rows+1)
                    for j in range(1, seats_per_row+1 )
                    for k in range(1, len(Passagers)+1)
                    if Passagers[k]['gender']==0])
    j_h = quicksum([weight_m * j* AssignmenVarDict[(i, j, k)]
                    for i in range(1, number_of_rows+1)
                    for j in range(1, seats_per_row+1 )
                    for k in range(1, len(Passagers)+1)
                    if Passagers[k]['gender']==2])

    j_bary = (j_m + j_f + j_h)/( weight_m * number_m + weight_f * number_f + weight_d * number_d)

    IMAXBARYCONST = m.addConstr(i_bary <= 17)
    IMINBARYCONST = m.addConstr(13 <= i_bary)
    JMAXBARYCONST = m.addConstr(j_bary <= 4)
    JMINBARYCONST = m.addConstr(3 <= j_bary)

    # Define the weights for the Manhattan distance
    a = 0.9  # Weight for the row distance
    b = 0.1  # Weight for the column distance

    # Objective function to minimize the weighted sum of distances between all passengers in the same group
    objective_groups = quicksum(
        a * abs(i1 - i2) + b * abs(j1 - j2) * AssignmenVarDict[(i1, j1, k1)] * AssignmenVarDict[(i2, j2, k2)]
        for i1 in range(1, number_of_rows + 1)
        for j1 in range(1, seats_per_row + 1)
        for i2 in range(1, number_of_rows + 1)
        for j2 in range(1, seats_per_row + 1)
        for k1 in Passagers.keys()
        for k2 in Passagers.keys()
        if Passagers[k1]['group'] == Passagers[k2]['group'] and k1 != k2
    )

    # Front rows (lower i) should have lower weight
    objective_transit = quicksum( [AssignmenVarDict[(i, j, k)]* i*(1/Passagers[k]['transit'])
                        for i in range(1, number_of_rows+1)
                        for j in range(1, seats_per_row+1 )
                        for k in range(1, len(Passagers)+1)
                        if Passagers[k]['transit'] != float('inf') ])

    m.setObjective(objective_groups + objective_transit, GRB.MINIMIZE)

    # Run optimization and suppress output
    m.params.outputflag = 0 
    m.optimize()

    # If the model is infeasible or unbounded, turn off presolve and optimize again
    if m.status in [GRB.INF_OR_UNBD, GRB.INFEASIBLE, GRB.UNBOUNDED]:
        m.setParam(GRB.Param.Presolve, 0)
        m.optimize()

    # Post-processing of results
    if m.status == GRB.OPTIMAL:
        # Post-processing of results
        # Extract the seating arrangement from the model
        seating_arrangement = {}
        for i in range(1, number_of_rows + 1):
            for j in range(1, seats_per_row + 1):
                for k in Passagers.keys():
                    if AssignmenVarDict[(i, j, k)].X > 0.5:  # Ensure the variable is part of the solution
                        seating_arrangement[(i, j)] = k
        print(f"Seating arrangement: {seating_arrangement}")
        print(f'Optimal objective value (z*): {round(m.objVal, 2)}')
    else:
        print("Optimization was unsuccessful. Status code:", m.status)
        m.computeIIS()
        m.write("model.ilp")
        print("The infeasibility file has been written to 'model.ilp'")

    # Define the seating arrangement
    seating_arrangement = seating_arrangement

    # Create a plot
    fig, ax = plt.subplots()

    # Plot the seating arrangement
    for seat, Passagers in seating_arrangement.items():
        ax.text(seat[1], seat[0], Passagers, ha='center', va='center')

    # Mark positions without passengers
    for i in range(1, number_of_rows + 1):
        for j in range(1, seats_per_row + 1):
            if (i, j) not in seating_arrangement:
                ax.scatter(j, i, color='red')

    # Set the limits and labels of the plot
    ax.set_xlim(0.5, seats_per_row + 0.5)
    ax.set_ylim(0.5, number_of_rows + 0.5)
    ax.set_xticks(range(1, seats_per_row + 1))
    ax.set_yticks(range(1, number_of_rows + 1))
    ax.set_xticklabels([chr(65 + i) for i in range(seats_per_row)]) # permet de générer les lettres A,B,C,D,E,F grâce à chr()
    ax.set_yticklabels(range(1, number_of_rows + 1))
    ax.grid(True)

    # Add labels and title
    plt.xlabel('Seats')
    plt.ylabel('Rows')
    plt.title('Seating Arrangement')

    # Display the plot
    plt.gca().invert_yaxis()  # Invert y-axis to match the plane layout
    plt.show()


# optimisation(1)


# Fonction pour afficher le temps qui défile
def display_timer():
    start_time = time.time()
    while True:
        elapsed_time = time.time() - start_time
        print(f"\rTemps écoulé : {elapsed_time:.2f} secondes", end="", flush=True)
        time.sleep(0.1)

# Lancer le thread pour afficher le temps
timer_thread = threading.Thread(target=display_timer)
timer_thread.start()

# Boucle principale
for i in range(1,len(df)):
    start_time_iteration = time.time()
    optimisation(i)
    end_time_iteration = time.time()
    duration_iteration = end_time_iteration - start_time_iteration
    print(f"\nDurée de l'itération {i+1}: {duration_iteration:.2f} secondes")
