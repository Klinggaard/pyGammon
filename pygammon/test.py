import numpy as np


def moveToken (id1, id2):
    print("id1:", id1)
    print("id2:", id2)
    return id1

relativeNextStates = np.array([[
            moveToken(tokenID, ID2) for tokenID in range(5) for ID2 in range(5)]]
        )

occupants = relativeNextStates == 1
occupant_count = np.sum(occupants)

array = np.asarray([1,2,3,4,5,6,7])

print(array)
print(array.flatten("C"))


print(occupants)
print("oc", occupant_count)
print("count", np.sum(occupants))
print(relativeNextStates)
print("sum", sum(i == 1 for i in relativeNextStates[0]))
relativeNextStates[occupants] = -1
print(relativeNextStates)
print(15*15)

test = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
x = all(item <= 5 for item in test)
test = np.asarray(test)
y = np.all(test == 0)
print(y)
print(all(item == 0 for item in test))
print(test)
print(x)
