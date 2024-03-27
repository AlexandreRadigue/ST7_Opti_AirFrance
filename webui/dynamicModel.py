import json
import ast
import random
import pandas as pd

# from dynamicModel import possible_permutations , scoreAllocation , permutation


pathSeats = "./ST7 -Airfrance - Dynamique/SeatsDict_22Oct.json"
pathPassengers = "./ST7 -Airfrance - Dynamique/PassengersDict_22Oct.json"
pathGroups = "./ST7 -Airfrance - Dynamique/AllGroups_22Oct.json"


with open(pathSeats, "r") as file:
    SeatsAssignOptimDict = json.load(file)

SeatsAssignOptimDict = {
    ast.literal_eval(key): value for key, value in SeatsAssignOptimDict.items()
}

with open(pathPassengers, "r") as file:
    PassengersAssignOptimDict = json.load(file)

PassengersAssignOptimDict = {
    int(key): value for key, value in PassengersAssignOptimDict.items()
}

with open(pathGroups, "r") as file:
    AllGroups = json.load(file)

AllGroups = {int(key): value for key, value in AllGroups.items()}

ChosenSeats = set()
RegisteredGroups = set()
Passengers_Assign_Dict = PassengersAssignOptimDict.copy()
Seats_Assign_Dict = SeatsAssignOptimDict.copy()
max_choices = 5
max_try = 5

# Uploading df

df_21Oct = pd.read_excel(
    "./ST7 -Airfrance - Dynamique/DataSeating 2024.xlsx", sheet_name=0, skipfooter=2
)
df = df_21Oct


def convert_TransitTime(time_val):

    # Convert time to minutes
    total_minutes = time_val.hour * 60 + time_val.minute

    # Check if total minutes is greater than 2 hours or equal to 0
    if total_minutes > 120 or total_minutes == 0:
        return float("inf")  # Return infinity
    else:
        return total_minutes


df["TransitTime"] = df["TransitTime"].apply(convert_TransitTime)

# Create Passengers dictionary
Passengers = dict()
i = 1

number_f = 0
number_m = 0
number_d = 0

transit_times = set()

# Groups : dict[int : List[int]]

Passengers = dict()
i = 1

for group in df.itertuples():
    if not pd.isna(group[2]):
        for k in range(int(group[2])):
            Passengers[i] = {
                "type": 0,
                "group": group[1],
                "transit": group[5],
            }  # 0 <-> female
            number_f += 1
            transit_times.add(group[5])
            i += 1
    if not pd.isna(group[3]):
        for k in range(int(group[3])):
            Passengers[i] = {
                "type": 1,
                "group": group[1],
                "transit": group[5],
            }  # 1 <-> male
            number_m += 1
            transit_times.add(group[5])
            i += 1
    if not pd.isna(group[4]):
        for k in range(int(group[4])):
            Passengers[i] = {
                "type": 2,
                "group": group[1],
                "transit": group[5],
            }  # 2 <-> WCHR
            number_d += 1
            transit_times.add(group[5])
            i += 1

Groups = dict()


for i, passager in Passengers.items():

    if passager["group"] in Groups:
        Groups[passager["group"]].append(i)
    else:
        Groups[passager["group"]] = [i]

Keys = list(Groups.keys()).copy()


for i in Keys:
    if len(Groups[i]) == 1:
        del Groups[i]

# Parameters

weight_f = 70
weight_m = 85
weight_d = 92.5

if sum([4 * number_d, number_f, number_m]) <= 174:
    number_of_rows = 29  # Airbus A320
else:
    number_of_rows = 35  # Airbus A321

number_of_columns = 7  # a(A B C AISLE D E F)

# Z_old transit

z_old = 4.07

# Parameters

WeightsPassengers = {}

for k in range(1, len(Passengers) + 1):
    if Passengers[k]["type"] == 0:
        WeightsPassengers[k] = weight_f
    if Passengers[k]["type"] == 1:
        WeightsPassengers[k] = weight_m
    if Passengers[k]["type"] == 2:
        WeightsPassengers[k] = weight_d


# Def important functions


def ScoreTransit(Passengers_Assign_Dict):

    z_transit = sum(
        [
            Passengers_Assign_Dict[k][0] / Passengers[k]["transit"]
            for k in range(1, len(Passengers) + 1)
        ]
    )

    return (1 - (z_transit - z_old) / z_old) * 100


def ScoreGrouping(Passengers_Assign_Dict, Seats_Assign_Dict):

    satisfaction_scores = []

    for passengers in Groups.values():

        for k in passengers:
            i, j = Passengers_Assign_Dict[k]
            satisfaction_k = 0
            if j not in (3, 5):

                neighbors_k = set(
                    [
                        Seats_Assign_Dict.get((i, j - 1), 0),
                        Seats_Assign_Dict.get((i, j + 1), 0),
                    ]
                )

                if not neighbors_k.intersection(set(passengers)):
                    satisfaction_k = 0
                else:
                    satisfaction_k = 1

            elif j == 3:
                neighbors_k = set(
                    [
                        Seats_Assign_Dict.get((i, j - 1), 0),
                        Seats_Assign_Dict.get((i, j + 2), 0),
                    ]
                )

                if not neighbors_k.intersection(set(passengers)):
                    satisfaction_k = 0
                elif Seats_Assign_Dict.get((i, j - 1), 0) in passengers:
                    satisfaction_k = 1
                else:
                    satisfaction_k = 0.5

            elif j == 5:
                neighbors_k = set(
                    [
                        Seats_Assign_Dict.get((i, j + 1), 0),
                        Seats_Assign_Dict.get((i, j - 2), 0),
                    ]
                )

                if not neighbors_k.intersection(set(passengers)):
                    satisfaction_k = 0
                elif Seats_Assign_Dict.get((i, j + 1), 0) in passengers:
                    satisfaction_k = 1
                else:
                    satisfaction_k = 0.5

            satisfaction_scores.append(satisfaction_k)

    # Calcul du score de groupement moyen (pourcentage de satisfaction)
    grouping_score = (sum(satisfaction_scores) / len(satisfaction_scores)) * 100

    return grouping_score


from itertools import combinations


def subgroups(grp_size, valid_seats):
    """
    This function returns all the sublists of n=grp_size elements from a list valid_seats.
    """

    if grp_size > len(valid_seats):
        return []
    elif grp_size < 1:
        return "La taille du groupe doit être d'au moins 1."
    else:
        return [
            valid_seats[i : i + grp_size]
            for i in range(len(valid_seats) - grp_size + 1)
        ]


def potential_permutations(grp_size, chosen_seats):
    """
    This function returns all the potentiel permuations of a group of size n=grp_size
    """

    valid_seats = [
        (i, j)
        for i in range(1, number_of_rows + 1)
        for j in range(1, number_of_columns + 1)
        if (j != 4 and (i, j) not in chosen_seats)
    ]

    choices = subgroups(grp_size, valid_seats)

    return choices


def permutation(
    Old_allocation, New_allocation, Passengers_Assign_old_Dict, Seats_Assign_old_Dict
):
    """
    This function returns the new configuration of the plane after doing the permutation between two groups of passengers
    """

    Passengers_Assign_New_Dict, Seats_Assign_New_Dict = (
        Passengers_Assign_old_Dict.copy(),
        Seats_Assign_old_Dict.copy(),
    )

    for l in range(len(Old_allocation)):

        Passenger_Assign_Old = Old_allocation[l][2]
        Passenger_Assign_New = New_allocation[l][2]

        Seat_Assign_Old = (Old_allocation[l][0], Old_allocation[l][1])
        Seat_Assign_New = (New_allocation[l][0], New_allocation[l][1])

        # Swap passenger-seat assignments in the dictionaries
        Seats_Assign_New_Dict[Seat_Assign_New] = Passenger_Assign_Old
        Seats_Assign_New_Dict[Seat_Assign_Old] = Passenger_Assign_New

        Passengers_Assign_New_Dict[Passenger_Assign_Old] = Seat_Assign_New
        if Passenger_Assign_New != None:
            Seats_Assign_New_Dict[Passenger_Assign_New] = Seat_Assign_Old

    return Passengers_Assign_New_Dict, Seats_Assign_New_Dict


def CheckBaryConst(Passengers_Assign_Dict):
    """
    This function checks if the barycentre constraints are verified
    """

    res = True

    i_bary = sum(
        [
            WeightsPassengers[k] * Passengers_Assign_Dict[k][0]
            for k in range(1, len(Passengers) + 1)
        ]
    ) / sum(WeightsPassengers.values())
    j_bary = sum(
        [
            WeightsPassengers[k] * Passengers_Assign_Dict[k][1]
            for k in range(1, len(Passengers) + 1)
        ]
    ) / sum(WeightsPassengers.values())

    if i_bary > 16.5 or i_bary < 13.5 or j_bary > 4.5 or 3.5 > j_bary:
        res = False

    return res


def CheckWCHConst(Passengers_Assign_Dict, Seats_Assign_Dict):
    """
    This function checks if the WCHR constraints are verified
    """

    res = True
    for k in range(1, len(Passengers) + 1):
        if Passengers[k]["type"] == 2:
            i, j = Passengers_Assign_Dict[k]
            if (
                j not in [3, 6]
                or Seats_Assign_Dict.get((i, j - 1), 0) != None
                or Seats_Assign_Dict.get((i + 1, j - 1), 0) != None
                or Seats_Assign_Dict.get((i + 1, j), 0) != None
            ):
                res = False
                break

    return res


def CheckNewAllocation(Passengers_Assign_Dict, Seats_Assign_Dict):
    """
    This function checks if the new configuration is valid or not
    """

    res = True

    if not CheckBaryConst(Passengers_Assign_Dict):
        res = False
        return res

    if not CheckWCHConst(Passengers_Assign_Dict, Seats_Assign_Dict):
        res = False
        return res

    if (
        ScoreTransit(Passengers_Assign_Dict) / ScoreTransit(PassengersAssignOptimDict)
        < 0.75
        or ScoreTransit(Passengers_Assign_Dict)
        / ScoreTransit(PassengersAssignOptimDict)
        > 1.5
    ):
        res = False
        return res

    if (
        ScoreGrouping(Passengers_Assign_Dict, Seats_Assign_Dict)
        / ScoreGrouping(PassengersAssignOptimDict, SeatsAssignOptimDict)
        < 0.95
        or ScoreGrouping(Passengers_Assign_Dict, Seats_Assign_Dict)
        / ScoreGrouping(PassengersAssignOptimDict, SeatsAssignOptimDict)
        > 1.5
    ):
        res = False

    return res


def possible_permutations(
    group_number, chosen_seats, Passengers_Assign_old_Dict, Seats_Assign_old_Dict
):
    """
    This function returns all the valid permutations among all the possible ones
    """

    grp_size = len(AllGroups[group_number]["passengers"])
    optimal_allocation_group = [
        (PassengersAssignOptimDict[k][0], PassengersAssignOptimDict[k][1], k)
        for k in AllGroups[group_number]["passengers"]
    ]
    res = [
        [
            (PassengersAssignOptimDict[k][0], PassengersAssignOptimDict[k][1])
            for k in AllGroups[group_number]["passengers"]
        ]
    ]

    for allocation in potential_permutations(grp_size, chosen_seats):
        allocation_group = [
            (seat[0], seat[1], SeatsAssignOptimDict[(seat[0], seat[1])])
            for seat in allocation
        ]
        PassengersAssignNewDict, SeatsAssignNewDict = permutation(
            optimal_allocation_group,
            allocation_group,
            Passengers_Assign_old_Dict,
            Seats_Assign_old_Dict,
        )
        if CheckNewAllocation(PassengersAssignNewDict, SeatsAssignNewDict):
            res.append(allocation)

    return res


def scoreAllocation(allocations_list):
    max_row_total = 0
    max_column_total = 0

    for allocation in allocations_list:
        max_row_allocation = sum(
            1 for seat in allocation if seat[0] <= number_of_rows / 3
        ) / len(allocation)

        y = sum(1 for seat in allocation if seat[1] in [2, 6])
        max_column_allocation = (len(allocation) - y) / len(allocation)

        max_row_total = max(max_row_total, max_row_allocation)
        max_column_total = max(max_column_total, max_column_allocation)

    return 100 * (max_column_total + max_row_total) / 2


# Functions to call


def Options(group_nbr):
    """
    This function registers a given group
    """

    if group_nbr in RegisteredGroups:
        print("Your group already registred ")

    elif group_nbr == 0 or type(group_nbr) != int:
        print("Group number must be a positive integer")
    else:

        choices = possible_permutations(
            group_nbr, ChosenSeats, Passengers_Assign_Dict, Seats_Assign_Dict
        )

        RandomNumbers = {}
        All_possible_allocations = {}
        Scores = {}
        for i in range(max_try):
            random.seed(i)
            RandomNumbers[i] = sorted(
                [0]
                + random.sample(
                    range(1, len(choices)), min(len(choices), max_choices) - 1
                )
            )
            All_possible_allocations[i] = [choices[n] for n in RandomNumbers[i]]
            Scores[i] = scoreAllocation(All_possible_allocations[i])

        random_numbers = RandomNumbers[max(Scores, key=Scores.get)]

        score_register = min(len(choices), max_choices) / max_choices
        score_choice = max(Scores.values())

        All_options = [choices[n] for n in random_numbers]

        return All_options, score_choice, score_register


def updating(group_nbr, chosenAllocation_nbr):

    choices, _, _ = Options(group_nbr)

    global RegisteredGroups
    RegisteredGroups.add(group_nbr)

    chosenAllocation = choices[chosenAllocation_nbr - 1]
    global ChosenSeats
    ChosenSeats.update(seat for seat in chosenAllocation)

    optimal_allocation_group = [
        (seat[0], seat[1], Seats_Assign_Dict[seat]) for seat in choices[0]
    ]
    chosen_allocation_group = [
        (seat[0], seat[1], Seats_Assign_Dict[seat])
        for seat in choices[chosenAllocation_nbr - 1]
    ]
    global Passengers_Assign_Dict, Seats_Assign_Dict
    Passengers_Assign_Dict, Seats_Assign_Dict = permutation(
        optimal_allocation_group,
        chosen_allocation_group,
        Passengers_Assign_Dict,
        Seats_Assign_Dict,
    )


print(Options(65))
