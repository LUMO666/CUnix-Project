import numpy as np

class my_softmax(object):
    def __init__(self):
        pass
    def forward(self,input):
        output = np.zeros(input.shape)
        idb = 0
        for batch in input:
            bot = sum(np.exp(batch))
            ide = 0
            for elem in batch:
                output[idb,ide] = np.exp(elem)/bot
                ide += 1
            idb += 1
        return np.log(output)


class my_relu(object):
    def __init__(self):
        pass
    def forward(self,input):
        output = (input>0)*input
        return output

class my_linear(object):
    def __init__(self,parameters):
        self.w = parameters[0]
        self.b = parameters[1]

    def forward(self,input):
        output = np.matmul(input,self.w.T)
        output = output + self.b
        return output

class my_conv(object):
    def __init__(self,parameters):
        self.core = parameters[0]
        #print(self.core)
        self.bias = parameters[1]
        self.core_size = self.core.shape[2]
        self.input_channel = self.core.shape[1]
        self.output_channel = self.bias.shape[0]
        self.stride = 1
        self.padding = 0

    def forward(self,input):
        #print(self.core_size)
        #print(self.input_channel)
        #print(self.output_channel)
        #print(self.stride)
        batch_size = input.shape[0]
        output = np.zeros((batch_size,self.output_channel,np.floor(((input.shape[2]-self.core_size+2*self.padding)/self.stride)+1).astype(np.int),np.floor(((input.shape[3]-self.core_size+2*self.padding)/self.stride)+1).astype(np.int)))
        if self.padding != 0:
            for batch in input:
                for graph in batch:
                    ori_shape = graph.shape
                    graph = np.concatenate((graph,np.zeros((self.padding,ori_shape[1]))),axis=0)
                    graph = np.concatenate((np.zeros((self.padding,ori_shape[1])),graph),axis=0)
                    graph = np.concatenate((graph,np.zeros((ori_shape[0]+2*self.padding,self.padding))),axis=1)
                    graph = np.concatenate((np.zeros((ori_shape[0]+2*self.padding,self.padding)),graph),axis=1)
        idb = 0
        for graph in input:
            for idoc in range(self.output_channel):  
                idic = 0              
                for in_chan in graph:
                    idx = 0
                    while idx*self.stride <= in_chan.shape[0]-self.core_size:
                        idy = 0
                        while idy*self.stride <= in_chan.shape[1]-self.core_size:
                            output[idb,idoc,idx,idy] += np.sum(self.core[idoc,idic]*in_chan[idx*self.stride:idx*self.stride+self.core_size,idy*self.stride:idy*self.stride+self.core_size])
                            idy += 1
                        idx += 1
                    idic += 1
                output[idb,idoc] += self.bias[idoc]
            idb += 1

        return output

class my_pooling(object):
    def __init__(self):
        self.padding = 0
        self.mod = 'max'
        pass

    def forward(self,input,f,s):
        batch_size = input.shape[0]
        input_channel = input.shape[1]
        output = np.zeros((batch_size,input_channel,np.floor(((input.shape[2]-f+2*self.padding)/s)+1).astype(np.int),np.floor(((input.shape[3]-f+2*self.padding)/s)+1).astype(np.int)))
        if self.padding != 0:
            for batch in input:
                for graph in batch:
                    ori_shape = graph.shape
                    graph = np.concatenate((graph,np.zeros((self.padding,ori_shape[1]))),axis=0)
                    graph = np.concatenate((np.zeros((self.padding,ori_shape[1])),graph),axis=0)
                    graph = np.concatenate((graph,np.zeros((ori_shape[0]+2*self.padding,self.padding))),axis=1)
                    graph = np.concatenate((np.zeros((ori_shape[0]+2*self.padding,self.padding)),graph),axis=1)
        idb = 0
        for batch in input:
            idic = 0
            for graph in batch:
                idx = 0
                while idx*s <= graph.shape[0]-f:
                    idy = 0
                    while idy*s <= graph.shape[1]-f:
                        output[idb,idic,idx,idy] = np.max(graph[idx*s:idx*s+f,idy*s:idy*s+f])
                        idy += 1
                    idx += 1
                idic += 1
            idb += 1

        return output

