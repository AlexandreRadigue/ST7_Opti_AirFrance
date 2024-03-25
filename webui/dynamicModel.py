import json
import ast
import random
from dynamicModel import possible_permutations , scoreAllocation , permutation


pathSeats = "./ST7 -Airfrance - Dynamique/SeatsDict_22Oct.json"
pathPassengers = "./ST7 -Airfrance - Dynamique/PassengersDict_22Oct.json"
pathGroups = "./ST7 -Airfrance - Dynamique/AllGroups_22Oct.json"


with open(pathSeats, 'r') as file:
    SeatsAssignOptimDict = json.load(file)

SeatsAssignOptimDict = {ast.literal_eval(key): value for key, value in SeatsAssignOptimDict.items()}

with open(pathPassengers, 'r') as file:
    PassengersAssignOptimDict = json.load(file)

PassengersAssignOptimDict = {int(key): value for key, value in PassengersAssignOptimDict.items()}

with open(pathGroups, 'r') as file:
    AllGroups = json.load(file)

AllGroups = {int(key): value for key, value in AllGroups.items()}

ChosenSeats = set()
RegisteredGroups =set()
Passengers_Assign_Dict = PassengersAssignOptimDict.copy()
Seats_Assign_Dict = SeatsAssignOptimDict.copy() 
max_choices = 5
max_try=5


def Options(group_nbr, ChosenSeats = set(), RegisteredGroups =set(),Passengers_Assign_Dict = PassengersAssignOptimDict.copy() , Seats_Assign_Dict = SeatsAssignOptimDict.copy() ,max_choices = 5, max_try=5):

    '''
    This function registers a given group
    '''

    if group_nbr in RegisteredGroups :
        print('Your group already registred ')
        
    elif group_nbr == 0 or type(group_nbr) != int:
        print('Group number must be a positive integer')
    else :

        choices = possible_permutations(group_nbr, ChosenSeats,Passengers_Assign_Dict, Seats_Assign_Dict)

        RandomNumbers ={}
        All_possible_allocations = {}
        Scores ={}
        for i in range(max_try) :
            random.seed(i)
            RandomNumbers[i] = sorted([0]+ random.sample(range(1, len(choices)), min(len(choices),max_choices)-1))
            All_possible_allocations[i] = [choices[n] for n in RandomNumbers[i]]
            Scores[i] = scoreAllocation(All_possible_allocations[i])

        random_numbers = RandomNumbers[max(Scores, key=Scores.get)]

        score_register = min(len(choices),max_choices)/max_choices
        score_choice = max(Scores.values())

        All_options= [choices[n] for n in random_numbers]

    
        return All_options , score_choice, score_register
    
def updating(group_nbr, chosenAllocation_nbr, ChosenSeats = set(), RegisteredGroups =set(),Passengers_Assign_Dict = PassengersAssignOptimDict.copy() , Seats_Assign_Dict = SeatsAssignOptimDict.copy() ,max_choices = 5, max_try=5):

    choices , _ , _ = Options(group_nbr, ChosenSeats , RegisteredGroups ,Passengers_Assign_Dict, Seats_Assign_Dict,max_choices, max_try)

    RegisteredGroups.add(group_nbr)


    chosenAllocation = choices[chosenAllocation_nbr -1]
    ChosenSeats.update(seat for seat in chosenAllocation)

    optimal_allocation_group = [(seat[0], seat[1],Seats_Assign_Dict[seat]) for seat in choices[0] ]
    chosen_allocation_group = [(seat[0], seat[1],Seats_Assign_Dict[seat]) for seat in choices[chosenAllocation_nbr -1] ]
    PassengersAssignDict , SeatsAssignDict = permutation(optimal_allocation_group,chosen_allocation_group,Passengers_Assign_Dict,Seats_Assign_Dict)



    return ChosenSeats , RegisteredGroups ,  PassengersAssignDict , SeatsAssignDict
    


