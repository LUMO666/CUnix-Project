import os
import random

if __name__ =='__main__':
    special_num = random.randint(0,11)
    special_weight = 2*random.random()
    ball_list = []
    param_p = open(os.getcwd()+'/param.txt', 'w')
    for i in range(12):
        ball_list.append(str(1))
    ball_list[special_num] = str(special_weight)
    for i in range(12):
        param_p.write(ball_list[i]+'\n')

