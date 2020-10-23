import os
import random
import copy
from Manager import Coordinate

if __name__ == '__main__':
    param_p = open(os.getcwd()+'/param.txt', 'r')
    Scale = int(param_p.readline())
    Period = int(param_p.readline())
    param_p.close()

    data_p = open(os.getcwd()+'/data.txt', 'w')

    Cord_origin = [Coordinate(30*random.random()-5,30*random.random()-5) for i in range(Scale)]
    Cord_iter = copy.deepcopy(Cord_origin)
    Cord_list = []
    for i in range(Period):
        for cord in Cord_iter:
            cord.x = cord.x + (8*random.random()-4)
            cord.y = cord.y + (8*random.random()-4)
        Cord_list.append(copy.deepcopy(Cord_iter))

    for date in Cord_list:
        for cord in date:
            data_p.write(str(cord.x)+','+str(cord.y)+' ')
        data_p.write('\n')
    data_p.close()


    
    