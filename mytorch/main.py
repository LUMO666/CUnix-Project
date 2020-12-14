import os
import struct
import numpy as np
import matplotlib.pyplot as plt
from layer import my_conv, my_linear, my_pooling, my_relu, my_softmax
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


class ConvNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 10, 5) 
        self.conv2 = nn.Conv2d(10, 20, 3)
        self.fc1 = nn.Linear(20*10*10, 500) 
        self.fc2 = nn.Linear(500, 10) 
    def forward(self,x):
        in_size = x.size(0) 
        out = self.conv1(x) 
        #print('conv1:',out)
        out = F.relu(out)
        #print('relu1:',out) 
        out = F.max_pool2d(out, 2, 2)
        #print('pool1:',out) 
        #test = torch.ones(1,10,12,12)
        out = self.conv2(out)
        #print('conv2:',out) 
        out = F.relu(out) 
        out = out.view(in_size, -1) 
        out = self.fc1(out) 
        out = F.relu(out) 
        out = self.fc2(out) 
        out = F.log_softmax(out, dim=1) 
        return out

def load_model():
    model = ConvNet()
    state_dict = torch.load('./model')
    model.load_state_dict(state_dict)
    return model
def load_pic():
    images_path = './t10k-images-idx3-ubyte'
    labels_path = './t10k-labels-idx1-ubyte'

    with open(labels_path, 'rb') as lbpath:
        magic, n = struct.unpack('>II',
                                 lbpath.read(8))
        labels = np.fromfile(lbpath,
                             dtype=np.uint8)

    with open(images_path, 'rb') as imgpath:
        magic, num, rows, cols = struct.unpack('>IIII',
                                               imgpath.read(16))
        images = np.fromfile(imgpath,
                             dtype=np.uint8).reshape(len(labels),28,28)
    return labels,images
def show_pic(images,idx):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    axidx = 0
    
    img = images[idx[0]]
    ax.imshow(img, cmap='Greys', interpolation='nearest')
            
    plt.show()

def show_conv(parameters):
    fig, ax = plt.subplots( nrows=1,
                            ncols=10,
                            sharex=True,
                            sharey=True, )
    ax = ax.flatten()
    axidx = 0
    for i in range(10):
        img = np.squeeze(parameters[i],axis=0)
        print(img)
        ax[axidx].imshow(img, cmap='Greys', interpolation='nearest')
        axidx += 1        
    ax[0].set_xticks([])
    ax[0].set_yticks([])
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    labels,images = load_pic()
    model = load_model()
    my_model = []
    for i in model.parameters():
        #print(i)
        my_model.append(i.detach().numpy())
        #print(i.detach().numpy())
    #print(model.parameters())
    #print('m2:',my_model[2])
    #print('m3:',my_model[3])
    myconv1 = my_conv([my_model[0],my_model[1]])
    myconv2 = my_conv([my_model[2],my_model[3]])
    mylin1 = my_linear([my_model[4],my_model[5]])
    mylin2 = my_linear([my_model[6],my_model[7]])
    mypool = my_pooling()
    myrelu = my_relu()
    mysoftmax = my_softmax()

    idx = np.random.randint(0, high=9999, size=2)
    img = images[idx[0]]
    #img = images[2]
    img = np.expand_dims(img,0)
    img = np.expand_dims(img,0)

    output = myconv1.forward(img/255)
    #print('myconv1:',output)
    output = myrelu.forward(output)
    #print('myrelu1:',output)
    output = mypool.forward(output,2,2)
    #print('mypool1:',output)
    test = np.ones((1,10,12,12))
    output = myconv2.forward(output)
    #output = myconv1.forward(test)
    #print('myconv2:',output)
    output = myrelu.forward(output)
    output = output.reshape((1,-1))
    output = mylin1.forward(output)
    output = myrelu.forward(output)
    output = mylin2.forward(output)
    output = mysoftmax.forward(output)
    print('my_torch_output:',output)
    print('my_torch_result:',np.argmax(output))

    out = model(torch.from_numpy(img/255).float())
    print('pytorch_output:',out)
    print('pytorch_result:',np.argmax(out.detach().numpy()))
    #np.set_printoptions(precision=4)
    error = output - out.detach().numpy()
    #print('m2:',my_model[2])
    #print('m3:',my_model[3])
    #print('m2_s:',my_model[2].shape)
    print('error:',error)
    #show_conv(my_model[0])
    #print(sum(sum(error)))
    #print(np.sum(error))
    #print(output)
    #print(model(torch.from_numpy(img/255).float()))

    show_pic(images,idx)

