引用库
os
math
copy

环境设置
四个信号塔位置分别为[5,5][15,5][5,15][15,15]
设备第一次连接节点，系统会记录下设备号并将其信息录入系统中
当设备直接或间接连接至节点时，当前时间单位上的坐标会上传到云端，如未连接则在轨迹记录中记录[999,999]
当两个设备同一时间位于同一坐标时认为可传播病毒

param.txt为配置文件
第一行为仿真设备数，第二行是仿真时间单位数

data.txt为数据文件
行代表仿真日期数，列代表不同的设备号，列数的值与设备号相同

generate_data.py为数据生成文件
第一轮数据随机生成在地图中，生成范围为长宽[-5,25]的区间内，假设每单位时间设备的轴上位移为[-4,4]

Manager.py为主文件
功能部分
Covid_core.track_device(dev_num) 指定设备号为dev_num并查询其轨迹
Covid_core.Covid_check([x,y]) 指定坐标[x,y]查看历史上该坐标出现的感染者数
Covid_core.Covid_check1([x,y]) 指定坐标[x,y]查看最后一个时间单位该坐标出现的感染者数
Covid_core.check_device() 查看当前已录入的设备号

代码注释
class Coordinate为坐标类
class Device为系统记录设备类，坐标为整数以模拟系统最小分辨单元，num为设备号
class Real_Device为真实设备类，坐标为浮点数

Device_dis(dev_a,dev_b)计算两个设备间距离
Device_exist(dev, dev_num_list)查看设备是否在设备号列表里
Device_exist_list(dev, dev_list)查看设备是否在设备号列表里

Build_net(talk_dis, date) talk_dis为通信距离，date为当前时间单位各设备列表，将各个设备间按照通信距离限制形成的子网络计算出来
Direct_link(node_list, date, talk_dis) node_list为节点列表，date为当前时间单位各设备列表，talk_dis为通信距离，输出当前时间单位直接与节点连接的设备列表

load_param()载入参数
load_data(Scale, Period)根据参数载入数据

Monitor类为仿真及监控系统类
成员
Device_signup_list 设备登记列表
Device_track_dict 设备轨迹表
linknode_list 预置的节点表
covid_list 感染的设备表
talk_dis 通信距离
spread_dis 病毒传播距离 0指同一个位置会感染

update(self,date) 根据date数据，更新设备坐标表
Covid_set(self, inc_num_list) 对inc_num_list中的设备投放病毒
Covid_spread(self, date) 根据date数据，预测病毒传播

运行步骤
python generate_data.py
python Manager.py
当前主函数中的数据为挑选仿真的一组数据，能够比较好的展示效果，重新generate过后可以先查看print出来的Covid_core.covid_list里的感染设备号，然后Covid_core.track_device查看感染设备号的轨迹，对比输出找一个同时出现的坐标点测试两个check函数