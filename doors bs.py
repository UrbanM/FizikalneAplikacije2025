import numpy as np
import random

victories_c = int(0)
victories_s = int(0)

for _ in range(10000):

    #Create 3 doors that are closed (0), choose one to have a prise (2)
    doors=[0,0,0]
    doors[np.random.randint(0,3)]=2

    #We choose a door
    chosen_door=np.random.choice(doors)

    #We open a door with a goat
    doors[np.random.choice([i for i in range(3) if i!=chosen_door and doors[i]==0])]=1

    #We change the door
    chosen_door=[i for i in range(3) if i!=chosen_door and doors[i]!=1][0]

    if doors[chosen_door]==2:
        victories_c += 1

    #Ponovno izračunamo za primer če ne odpremo vrat

    #Create 3 doors that are closed (0), choose one to have a prise (2)
    doors=[0,0,0]
    doors[np.random.randint(0,3)]=2

    #We choose a door
    chosen_door=np.random.choice(doors)

    #We open a door with a goat
    doors[np.random.choice([i for i in range(3) if i!=chosen_door and doors[i]==0])]=1

    #We don't change the door

    if doors[chosen_door]==2:
        victories_s += 1

print("Winning percentage when switching doors: ", victories_c/10000*100, "%")
print("Winning percentage when not switching doors: ", victories_s/10000*100, "%")

    




    
    
