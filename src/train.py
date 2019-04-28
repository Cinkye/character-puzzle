import time

import data as Data
import matplotlib.pyplot as plt
import model as Model
import numpy as np
import torch
import torch.nn as nn
from sklearn.metrics import f1_score, precision_score, recall_score

device = 'cuda'

def train_iter(data,model,criterion,optimizer,batch_size,voc_size):
    [dataset_X,dataset_opt,dataset_gd],datset_size = data.get_train_data()
    loss = 0
    losses = list()
    for i in range(0,datset_size - batch_size,batch_size):
        #time
        begin_time = time.time()

        # padding X with `voc_size`
        X = dataset_X[i : i + batch_size]
        lens = torch.tensor([len(X[i]) for i in range(len(X))]).to(device)
        max_len = max([len(X[i]) for i in range(len(X))])
        X = [xiter + [voc_size for _ in range(max_len - len(xiter))] for xiter in X]
        X = torch.tensor(X).to(device)

        gd = dataset_gd[i : i + batch_size]
        gd = torch.LongTensor(gd).to(device)
        opt = dataset_opt[i : i + batch_size]
        opt = torch.tensor(opt).to(device)

        output = model(X,opt,lens)
        
        #optim
        optimizer.zero_grad()
        loss = criterion(output,gd)
        loss.backward()
        optimizer.step()
        
        losses.append(loss.item())
        
        if i % 500 == 0:
            print(i,"/",datset_size," with time: ",time.time()-begin_time,end = "\r")
    return np.average(losses)

def train(max_epoch,batch_size = 5):
    loss = list()
    f1 = list()
    data = Data.Data(n_for_1 = 2)
    voc_size = data.get_voc_size()
    model = Model.Encoder(batch_size = batch_size,voc_size = voc_size, hidden_size = 100, device = device ,n_layers = 1,dropout = 0).to(device)
    for _ in range(max_epoch):
        print('epoch :',_)
        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.SGD(model.parameters(),lr = 0.001)

        loss.append(train_iter(data,model,criterion,optimizer,batch_size,voc_size))
        print(_,loss[-1])

        if _ % 100 == 0:
            f1.append(sample(dataset = data, model = model,batch_size = batch_size))
        if _ % 1000 == 0:
            torch.save(model.state_dict(),"./model" + str(_))
    torch.save(model.state_dict(),"./model" + str(time.time))
    plt.plot(loss)
    plt.show()

def sample(dataset,model,batch_size):
    voc_size = dataset.get_voc_size()
    [dataset_X,dataset_opt,dataset_gt],datset_size = dataset.get_test_data()
    y_gt = [] #ground truth
    y_pd = [] #prediction
    softmax = torch.nn.Softmax(dim = 1).cuda()
    for i in range(0,datset_size - batch_size,batch_size):
        # padding X with `voc_size`
        X = dataset_X[i : i + batch_size]
        lens = torch.tensor([len(X[i]) for i in range(len(X))]).to(device)
        max_len = max([len(X[i]) for i in range(len(X))])
        X = [xiter + [voc_size for _ in range(max_len - len(xiter))] for xiter in X]
        X = torch.tensor(X).to(device)

        gt = dataset_gt[i : i + batch_size]
        gt = torch.LongTensor(gt).to(device)
        opt = dataset_opt[i : i + batch_size]
        opt = torch.LongTensor(opt).to(device)

        output = model(X,opt,lens)

        y_gt += gt.tolist()
        y_pd += [pd[1] > 0.5 for pd in softmax(output).tolist()]

    f1 = f1_score(y_gt, y_pd)
    print('\r\t\t\t\t\t\t\t\tF1: {}'.format(f1))
    #print('Precision: {}'.format(precision_score(y_gt, y_pd)))
    #print('Recall: {}'.format(recall_score(y_gt, y_pd)))
    return f1


if __name__ == "__main__":
    train(max_epoch=10000,batch_size=50)
