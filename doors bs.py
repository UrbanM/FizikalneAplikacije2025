import numpy as np
import random

victories = int(0)


#Create 3 doors that are closed (0), choose one to have a prise (2)
doors=[0,0,0]
doors[np.random.randint(0,3)]=2

#We choose a door
chosen_door=np.random.choice(doors)

#We open a door with a goat
doors[np.random.choice([i for i in range(3) if i!=chosen_door and doors[i]==0])]=1

#Do we change the door? False je ne, True je da
change=False

if change==True:
    chosen_door=[i for i in range(3) if i!=chosen_door and doors[i]!=1][0]

if doors[chosen_door]==2:
    victories += 1
    print("Congratulations, you won the rizzler!")
else:
    print("You got the toilet")



    
    
