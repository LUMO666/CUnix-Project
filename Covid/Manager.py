import os
import math
import copy


class Coordinate(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Device(object):
    def __init__(self, cord, num):
        self.x = round(cord.x)
        self.y = round(cord.y)
        self.num = num

class Real_Device(object):
    def __init__(self, cord, num):
        self.x = cord.x
        self.y = cord.y
        self.num = num

def Device_dis(dev_a, dev_b):
    if dev_a.x == 999 or dev_a.y ==999 or dev_b.x == 999 or dev_b.y == 999:
        return 999
    else:
        return(math.sqrt((dev_a.x-dev_b.x)*(dev_a.x-dev_b.x)+(dev_a.y-dev_b.y)*(dev_a.y-dev_b.y)))

def Device_exist(dev, dev_num_list):
    return(dev.num in dev_num_list)

def Device_exist_list(dev, dev_list):
    exist = False
    for exist_dev in dev_list:
        if dev.num == exist_dev.num:
            exist = True
    return exist

def Print_dev_list(dev_list):
    for dev in dev_list:
        print(dev.num, ' ')

def Build_net(talk_dis, date):
    Net_list = []
    Net_dev_list = []
    listener_list = copy.deepcopy(date)
    for dev in date:
        listener_list.pop(0)
        for listener in listener_list:
            if Device_dis(dev, listener) <= talk_dis:
                if Device_exist(dev, Net_dev_list):
                    if Device_exist(listener, Net_dev_list):
                        for net in Net_list:
                            if Device_exist(dev, net):
                                dev_net = net
                            if Device_exist(listener, net):
                                listener_net = net
                        if dev_net != listener_net:
                            merge_net = list(set(dev_net + listener_net))
                            Net_list.remove(dev_net)
                            Net_list.remove(listener_net)
                            Net_list.append(merge_net)
                    else:
                        Net_dev_list.append(listener.num)
                        for net in Net_list:
                            if Device_exist(dev, net):
                                net.append(listener.num)
                else:
                    Net_dev_list.append(dev.num)
                    if Device_exist(listener, Net_dev_list):
                        for net in Net_list:
                            if Device_exist(listener, net):
                                net.append(dev.num)
                    else:
                        Net_dev_list.append(listener.num)
                        Net_list.append([dev.num, listener.num])
    '''
    x_list = []
    y_list = []
    for dev in date:
        print(dev.num,'(',dev.x,',',dev.y,')')
        x_list.append(dev.x)
        y_list.append(dev.y)
    print(Net_list)
    print(Net_dev_list)

    fig = plt.figure()
    plt.scatter(x_list,y_list)
    plt.show()
    '''
    return Net_list, Net_dev_list

def Direct_link(node_list, date, talk_dis):
    Dl_list = []
    for node in node_list:
        for dev in date:
            if Device_dis(node, dev) <= talk_dis:
                if not(dev.num in Dl_list):
                    Dl_list.append(dev.num)
    return Dl_list

def load_param():
    param_p = open(os.getcwd()+'/param.txt', 'r')
    Scale = int(param_p.readline())
    Period = int(param_p.readline())
    param_p.close()
    return Scale, Period

def load_data(Scale, Period):
    Cord_list = []
    Device_list = []
    Real_dev_list = []
    data_p = open(os.getcwd()+'/data.txt', 'r')
    for date in range(Period):
        date_list = []
        data_str = [i for i in data_p.readline().split()]
        for device in data_str:
            device_cord = device.split(',')
            date_list.append(Coordinate(float(device_cord[0]),float(device_cord[1])))
        Cord_list.append(date_list)
    for date in Cord_list:
        d_list = []
        rd_list = []
        for i in range(len(date)):
            d_list.append(Device(date[i], i))
            rd_list.append(Real_Device(date[i],i))
        Device_list.append(d_list)
        Real_dev_list.append(rd_list)
    return Device_list, Real_dev_list

class Monitor(object):
    def __init__(self):
        self.Device_signup_list = []
        self.Device_track_dict = {}
        self.linknode_list = [Device(Coordinate(5,5),-1), Device(Coordinate(5,15),-2),Device(Coordinate(15,5),-3),Device(Coordinate(15,15),-4)]
        self.covid_list = []
        self.talk_dis = 2
        self.spread_dis = 0

    def update(self, date):
        Net_list, Net_dev_list = Build_net(self.talk_dis, date)
        Dl_list = Direct_link(self.linknode_list, date, self.talk_dis)
        available_list = copy.deepcopy(Dl_list)
        for dev_num in self.Device_track_dict.keys():
            self.Device_track_dict[dev_num].append([999,999])
        for dev_num in Dl_list:
            if dev_num in Net_dev_list:
                for net in Net_list:
                    if dev_num in net:
                        available_list = list(set(available_list+net))
        for dev_num in available_list:
            if dev_num in self.Device_signup_list:
                self.Device_track_dict[dev_num][-1] = [round(date[dev_num].x),round(date[dev_num].y)]
            else:
                self.Device_signup_list.append(dev_num)
                if len(self.Device_track_dict) != 0:
                    key = list(self.Device_track_dict.keys())[0]
                    self.Device_track_dict[dev_num] = [[999,999] for i in range(len(self.Device_track_dict[key]))]
                    self.Device_track_dict[dev_num][-1] = [round(date[dev_num].x),round(date[dev_num].y)]
                else:
                    self.Device_track_dict[dev_num] = [[round(date[dev_num].x),round(date[dev_num].y)]]
    def Covid_set(self, inc_num_list):
        self.covid_list = list(set(self.covid_list + inc_num_list))

    def Covid_spread(self, date):
        Net_list, Net_dev_list = Build_net(self.spread_dis, date)
        for infected in self.covid_list:
            if infected in Net_dev_list:
                for net in Net_list:
                    if infected in net:
                        print(infected)
                        print(net)
                        print(date[infected].x,',',date[infected].y)
                        self.covid_list = list(set(self.covid_list + net))

    def Covid_check(self,cord):
        count = 0
        check_list = []
        for infected in self.covid_list:
            for i_cord in self.Device_track_dict[infected]:
                if cord == i_cord:
                    count = count + 1
                    check_list.append(infected)
                    break
        print('Sum of Infected in Position',cord,'is',count,':')
        print(check_list)

    def Covid_check1(self,cord):
        count = 0
        check_list = []
        for infected in self.covid_list:
            if cord == self.Device_track_dict[infected][-1]:
                count = count + 1
                check_list.append(infected)
        print('Sum of Infected in Position',cord,'is',count,':')
        print(check_list)

    def track_device(self, device_num):
        if self.Device_track_dict. __contains__(device_num):
            print('Succesfully Track Device',device_num)
            print(self.Device_track_dict[device_num])
        else:
            print('No Device ',device_num, 'in Monitor System')

    def check_device(self):
        print('List Device Already Log in:')
        print(self.Device_signup_list)

    
if __name__ == '__main__':
    Scale, Period = load_param()
    Device_list, Real_dev_list = load_data(Scale, Period)
    
    Covid_core = Monitor()
    Covid_core.Covid_set([0])
    
    for i in range(Period):
        Covid_core.update(Real_dev_list[i])
        Covid_core.Covid_spread(Device_list[i])
        
    #Covid_core.check_device()
    print(Covid_core.covid_list)
    Covid_core.track_device(336)
    Covid_core.track_device(121)
    Covid_core.track_device(353)
    Covid_core.track_device(206)
    Covid_core.track_device(80)
    Covid_core.track_device(213)
    Covid_core.track_device(93)
    Covid_core.track_device(113)

    Covid_core.Covid_check([18,5])
    Covid_core.Covid_check1([18,5])
    
