import os
import copy

class Ball(object):
    def __init__(self, num, weight):
        self.num = num
        self.weight = weight

def Balance(left, right):
    sum_left = 0
    sum_right = 0
    for Ball in left:
        sum_left = sum_left + Ball.weight
    for Ball in right:
        sum_right = sum_right + Ball.weight
    if sum_left > sum_right:
        return ("L")
    elif sum_left < sum_right:
        return("R")
    else:
        return("B")

def Load_param():
    param_p = open(os.getcwd()+'/param.txt', 'r')
    ball_list = []
    line = param_p.readline()
    while line:
        ball_list.append(float(line))
        line = param_p.readline()
    Ball_list = []
    for i in range(len(ball_list)):
        Ball_list.append(Ball(i,ball_list[i]))
    param_p.close()
    return Ball_list

def Heavy_Balance(Heavy_list, Light_list, Standard_list):
    if Balance([Heavy_list[0],Light_list[1],Light_list[2],Light_list[3]], [Light_list[0],Standard_list[0],Standard_list[1],Standard_list[2]]) == 'L':
        if Balance([Heavy_list[0]], [Standard_list[0]]) == 'L':
            print('Ball ', Heavy_list[0].num , ' is special, weigh ' , Heavy_list[0].weight)
            print('Ball ', Heavy_list[0].num , ' is heavier')
        elif Balance([Heavy_list[0]], [Standard_list[0]]) == 'B':
            print('Ball ', Light_list[0].num , ' is special, weigh ' , Light_list[0].weight)
            print('Ball ', Light_list[0].num , ' is lighter')
        else:
            print("Algo Error!")
    elif Balance([Heavy_list[0],Light_list[1],Light_list[2],Light_list[3]], [Light_list[0],Standard_list[0],Standard_list[1],Standard_list[2]]) == 'R':
        if Balance([Light_list[1]], [Light_list[2]]) == 'R':
            print('Ball ', Light_list[1].num , ' is special, weigh ' , Light_list[1].weight)
            print('Ball ', Light_list[1].num , ' is lighter')
        elif Balance([Light_list[1]], [Light_list[2]]) == 'L':
            print('Ball ', Light_list[2].num , ' is special, weigh ' , Light_list[2].weight)
            print('Ball ', Light_list[2].num , ' is lighter')
        elif Balance([Light_list[1]], [Light_list[2]]) == 'B':
            print('Ball ', Light_list[3].num , ' is special, weigh ' ,Light_list[3].weight)
            print('Ball ', Light_list[3].num , ' is lighter')
        else:
            print("Algo Error!")
    elif Balance([Heavy_list[0],Light_list[1],Light_list[2],Light_list[3]], [Light_list[0],Standard_list[0],Standard_list[1],Standard_list[2]]) == 'B':
        if Balance([Heavy_list[1]], [Heavy_list[2]]) == 'R':
            print('Ball ', Heavy_list[2].num , ' is special, weigh ' , Heavy_list[2].weight)
            print('Ball ', Heavy_list[2].num , ' is heavier')
        elif Balance([Heavy_list[1]], [Heavy_list[2]]) == 'L':
            print('Ball ', Heavy_list[1].num , ' is special, weigh ' , Heavy_list[1].weight)
            print('Ball ', Heavy_list[1].num , ' is heavier')
        elif Balance([Heavy_list[1]], [Heavy_list[2]]) == 'B':
            print('Ball ', Heavy_list[3].num , ' is special, weigh ' , Heavy_list[3].weight)
            print('Ball ', Heavy_list[3].num , ' is heavier')
        else:
            print("Algo Error!")
    else:
        print("Algo Error!")

if __name__ == '__main__':
    Ball_list = Load_param()
    #Locked_list = copy.deepcopy(Ball_list)
    Ball_list_A = Ball_list[0:4]
    Ball_list_B = Ball_list[4:8]
    Ball_list_C = Ball_list[8:12]

    if Balance(Ball_list_A, Ball_list_B) == 'B':
        #Locked_list = copy.deepcopy(Ball_list_C)
        if Balance([Ball_list_C[0], Ball_list_C[1]], [Ball_list_C[2], Ball_list_B[0]]) == 'B':
            print('Ball ', Ball_list_C[3].num , ' is special, weigh ' , Ball_list_C[3].weight)
            if Balance([Ball_list_C[3]], [Ball_list_B[0]]) == 'R':
                print('Ball ', Ball_list_C[3].num , ' is lighter')
            elif Balance([Ball_list_C[3]], [Ball_list_B[0]]) == 'L':
                print('Ball ', Ball_list_C[3].num , ' is heavier')
            else:
                print("Algo Error!")

        elif Balance([Ball_list_C[0], Ball_list_C[1]], [Ball_list_C[2], Ball_list_B[0]]) == 'L':
            if Balance([Ball_list_C[0]], [Ball_list_C[1]]) == 'L':
                print('Ball ', Ball_list_C[0].num , ' is special, weigh ' , Ball_list_C[0].weight)
                print('Ball ', Ball_list_C[0].num , ' is heavier')
            elif Balance([Ball_list_C[0]], [Ball_list_C[1]]) == 'R':
                print('Ball ', Ball_list_C[1].num , ' is special, weigh ' , Ball_list_C[1].weight)
                print('Ball ', Ball_list_C[1].num , ' is heavier')
            elif Balance([Ball_list_C[0]], [Ball_list_C[1]]) == 'B':
                print('Ball ', Ball_list_C[2].num , ' is special, weigh ' , Ball_list_C[2].weight)
                print('Ball ', Ball_list_C[2].num , ' is lighter')
            else:
                print("Algo Error!")
        elif Balance([Ball_list_C[0], Ball_list_C[1]], [Ball_list_C[2], Ball_list_B[0]]) == 'R':
            if Balance([Ball_list_C[0]], [Ball_list_C[1]]) == 'R':
                print('Ball ', Ball_list_C[0].num , ' is special, weigh ' , Ball_list_C[0].weight)
                print('Ball ', Ball_list_C[0].num , ' is lighter')
            elif Balance([Ball_list_C[0]], [Ball_list_C[1]]) == 'L':
                print('Ball ', Ball_list_C[1].num , ' is special, weigh ' , Ball_list_C[1].weight)
                print('Ball ', Ball_list_C[1].num , ' is lighter')
            elif Balance([Ball_list_C[0]], [Ball_list_C[1]]) == 'B':
                print('Ball ', Ball_list_C[2].num , ' is special, weigh ' , Ball_list_C[2].weight)
                print('Ball ', Ball_list_C[2].num , ' is heavier')
            else:
                print("Algo Error!")
        else:
            print("Algo Error!")

    elif Balance(Ball_list_A, Ball_list_B) == 'L':
        Heavy_Balance(Ball_list_A, Ball_list_B, Ball_list_C)
    elif Balance(Ball_list_A, Ball_list_B) == 'R':
        Heavy_Balance(Ball_list_B, Ball_list_A, Ball_list_C)
    else:
        print("Algo Error!")    
