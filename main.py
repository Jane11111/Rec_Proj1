# -*- coding: utf-8 -*-
# @Time    : 2020-04-06 17:18
# @Author  : zxl
# @FileName: main.py

import random
import numpy as np
from CF.UserCF import UserCF
from CF.ItermCF import ItemCF
from sklearn.metrics import mean_squared_error
from matplotlib import pyplot as plt

def load(path):
    data=[]
    with open(path,'r') as f:
        for l in f.readlines():
            l=l.replace('\n','')
            arr=l.split('::')
            data.append([int(arr[0]),int(arr[1]),int(arr[2])])
    return np.array(data)

def split(data):
    """
    按照8：2划分训练集和测试集
    需要保证训练集与测试集合包含user与item集合相等
    :param data: (user_id,item_id,rating)
    :return: train_x,train_y,test_x,test_y,x:(user_id,item_id),y:(rating,)
    """
    user_item_dic={}
    item_user_dic={}
    for u,i,r in data:
        if u not in user_item_dic.keys():
            user_item_dic[u]={}
        if i not in item_user_dic.keys():
            item_user_dic[i]={}
        user_item_dic[u][i]=r
        item_user_dic[i][u]=r
    stop=False
    remove_user_set=set()
    remove_item_set=set()
    while not stop:#删除只有一条记录的user和item
        print('hereXXxxxxxxxxxxxxxxxxxx')
        stop=True
        for u in user_item_dic.keys():
            if u in remove_user_set:
                continue#已经移除，不再考虑
            count=0
            for i in user_item_dic[u].keys():
                if i not in remove_item_set:
                    count+=1

            if count<2:
                stop=False
                remove_user_set.add(u)
        for i in item_user_dic.keys():
            if i in remove_item_set:
                continue#已经移除，不再考虑
            count=0
            for u in item_user_dic[i].keys():
                if u not in remove_user_set:
                    count+=1

            if count<2:
                stop=False
                remove_item_set.add(i)


    for u in remove_user_set:
        user_item_dic.pop(u)
    for u in user_item_dic.keys():
        i_lst=list(user_item_dic[u].keys())
        for i in i_lst:
            if i in remove_item_set:
                user_item_dic[u].pop(i)

    for i in remove_item_set:
        item_user_dic.pop(i)
    for i in item_user_dic.keys():
        u_lst=list(item_user_dic[i].keys())
        for u in u_lst:
            if u in remove_user_set:
                item_user_dic[i].pop(u)

    record_num=0
    for u in user_item_dic.keys():
        for i in user_item_dic[u].keys():
            record_num+=1

    test_user_item_dic={}
    test_item_user_dic={}
    test_num=0
    #保证test中含有全部user与item
    for u in user_item_dic.keys():
        test_num2=np.ceil(len(user_item_dic.keys())*0.2)
        i_lst=list(user_item_dic[u].keys())
        random.shuffle(i_lst)
        for i in i_lst:
            if test_num2<=0:
                break
            test_num2-=1
            r=user_item_dic[u][i]
            if u not in test_user_item_dic.keys():
                test_user_item_dic[u]={}
            if i not in test_item_user_dic.keys():
                test_item_user_dic[i]={}
            test_user_item_dic[u][i]=r
            test_item_user_dic[i][u]=r
            test_num+=1
    if len(test_item_user_dic.keys())<len(item_user_dic.keys()):#需要所有item包含到test里面
        for i in set(item_user_dic.keys()).difference(set(test_item_user_dic.keys())):
            u_lst=list(item_user_dic[i].keys())
            random.shuffle(u_lst)
            for u in u_lst:
                test_user_item_dic[u][i]=user_item_dic[u][i]
                test_item_user_dic[i]={}
                test_item_user_dic[i][u]=user_item_dic[u][i]
                break

    #保证train中包含全部user与item
    u_lst=list(test_user_item_dic.keys())
    for u in u_lst:
        i_lst=list(test_user_item_dic[u].keys())
        random.shuffle(i_lst)
        while len(test_user_item_dic[u].keys()) ==len(user_item_dic[u].keys()):#防止train中无这个user
            print('here.........')
            for i in i_lst:
                if len(test_item_user_dic[i] )>1 and len(test_user_item_dic[u])>1:
                    test_user_item_dic[u].pop(i)
                    test_item_user_dic[i].pop(u)
                    test_num-=1
                    break#跳出这个for循环
    i_lst=list(test_item_user_dic.keys())
    for i in i_lst:
        u_lst=list(test_item_user_dic[i].keys())
        while len(test_item_user_dic[i].keys()) == len(item_user_dic[i].keys()):#防止train中无这个item
            print('here------------')
            for u in u_lst:
                if len(test_user_item_dic[u])>1 and len(test_item_user_dic[i])>1:
                    test_item_user_dic[i].pop(u)
                    test_user_item_dic[u].pop(i)
                    test_num-=1
                    break#跳出这个for循环

    #保证test中数据数目占0.2
    while  test_num < np.ceil(record_num*0.2):
        print('here3*************')
        u_lst=list(user_item_dic.keys())
        # random.shuffle(u_lst)
        for u in u_lst:
            i_lst=list(user_item_dic[u].keys())
            # random.shuffle(i_lst)
            for i in i_lst:
                if i not in test_user_item_dic[u].keys() and len(item_user_dic[i])-len(test_item_user_dic[i])>=2:
                    test_user_item_dic[u][i]=user_item_dic[u][i]
                    test_item_user_dic[i][u]=item_user_dic[i][u]
                    test_num+=1
                    break#跳出for 循环
            if test_num>=np.ceil(record_num*0.2):
                break

    while test_num > np.ceil(record_num*0.2):
        print('here4&&&&&&&&&&&&&&')
        u_lst=list(test_user_item_dic.keys())
        # random.shuffle(u_lst)
        for u in u_lst:
            i_lst=list(test_user_item_dic[u].keys())
            # random.shuffle(i_lst)
            for i in i_lst:
                if len(test_user_item_dic[u])>1 and len(test_item_user_dic[i])>1:
                    test_user_item_dic[u].pop(i)
                    test_item_user_dic[i].pop(u)
                    test_num-=1
                    break
            if test_num <=np.ceil(record_num*0.2):
                break
    train_data=[]
    test_data=[]

    with open('tmp.txt','w') as w:
        w.write('user\n')
        w.write(str(len(test_user_item_dic))+'\n')
        w.write(str(len(user_item_dic))+'\n')
        w.write('item\n')
        w.write(str(len(test_item_user_dic))+'\n')
        w.write(str(len(item_user_dic))+'\n')
        for u in user_item_dic:
            w.write(str(len(user_item_dic[u]))+"   "+str(len(test_user_item_dic[u]))+'\n')
        w.write('...................\n')
        for i in item_user_dic:
            w.write(str(len(item_user_dic[i]))+"   "+str(len(test_item_user_dic[i]))+"\n")


    for u in user_item_dic.keys():

        for i in user_item_dic[u].keys():
            if i in test_user_item_dic[u].keys():
                test_data.append([u,i,user_item_dic[u][i]])
            else:
                train_data.append([u,i,user_item_dic[u][i]])
    return train_data,test_data


def load2(path):
    data = []
    with open(path, 'r') as f:
        for l in f.readlines():
            l = l.replace('\n', '')
            arr = l.split(',')
            data.append([int(arr[0]), int(arr[1]), int(arr[2])])
    return np.array(data)

if __name__ == "__main__":
    root="/Users/jane/Documents/ECNU/研一下/推荐系统/作业/作业1/ml-1m/ml-1m/"
    rating_file=root+"ratings.txt"
    train_file=root+"train.txt"
    test_file=root+"test.txt"

    train_data=load2(train_file)
    test_data=load2(test_file)

    # cf=UserCF()
    cf=ItemCF()
    cf.train(train_data[:,:-1],train_data[:,-1])
    predict_y=cf.predict(test_data[:,:-1])

    plt.scatter(test_data[:,-1],predict_y)
    plt.xlabel('true rating')
    plt.ylabel('prediction rating')
    plt.title('User CF')
    plt.show()
    mse=mean_squared_error(test_data[:,-1],predict_y)
    print(mse)








    # data=load(rating_file)
    # train_data,test_data=split(data)
    #
    # with open(train_file,'w') as w:
    #     for arr in train_data:
    #         w.write(str(arr[0])+','+str(arr[1])+','+str(arr[2])+'\n')
    # with open(test_file, 'w') as w:
    #     for arr in test_data:
    #         w.write(str(arr[0]) + ',' + str(arr[1]) + ',' + str(arr[2]) + '\n')


