import os
import struct
import numpy as np
import matplotlib.pyplot as plt
import layer
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
        out = F.relu(out) 
        out = F.max_pool2d(out, 2, 2) 
        out = self.conv2(out) 
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
    fig, ax = plt.subplots( nrows=1,
                            ncols=len(idx),
                            sharex=True,
                            sharey=True, )
    ax = ax.flatten()
    axidx = 0
    for i in idx:
        img = images[i]
        ax[axidx].imshow(img, cmap='Greys', interpolation='nearest')
        axidx += 1        
    ax[0].set_xticks([])
    ax[0].set_yticks([])
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    labels,images = load_pic()
    model = load_model()
    idx = np.random.randint(0, high=9999, size=5)
    show_pic(images,idx)
