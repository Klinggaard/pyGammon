import numpy as np
import random


def moveToken (id1, id2):
    print("id1:", id1)
    print("id2:", id2)
    return id1

#relativeNextStates = np.array([[
#            moveToken(tokenID, ID2) for tokenID in range(5) for ID2 in range(5)]]
#        )

#occupants = relativeNextStates == 1
#occupant_count = np.sum(occupants)

#array = np.asarray([1,2,3,4,5,6,7])

die = np.asarray([0,0,0,0,0,0])

for i in range(10000000):
    die[random.randint(1, 6)-1] += 1

print(die/10000000)