# -*- coding: utf-8 -*-
# @Time    : 2020-04-06 16:36
# @Author  : zxl
# @FileName: MF.py

import numpy as np
from sklearn.metrics import mean_squared_error

class MF:
    def __init__(self):
        pass
    def form_dic(self,X,Y):
        """
        将X，Y存储为user_item字典与item_user字典
        :param X:
        :param Y:
        :return:
        """
        user_item_dic={}
        item_user_dic={}
        for k in range(len(X)):
            u,i=X[k]
            r=Y[k]
            if u not in user_item_dic.keys():
                user_item_dic[u]={}
            user_item_dic[u][i]=r
            if i not in item_user_dic.keys():
                item_user_dic[i]={}
            item_user_dic[i][u]=r
        return user_item_dic,item_user_dic

    def opt(self,user_item_dic,item_user_dic,K,learning_rate):
        """
        梯度下降方法寻找最小
        :param user_item_dic:
        :return:
        """

        user_vector_dic = {}
        item_vector_dic = {}
        for u in user_item_dic:
            user_vector_dic[u] = np.random.rand(K, )
        for i in item_user_dic:
            item_vector_dic[i] = np.random.rand(K, )

        thres=0.5
        error=1
        count=0
        for u in user_item_dic:
            for i in user_item_dic[u]:
                count+=1

        while error>thres:#需要mse小于某一个阈值，迭代才会停止

            user_deri_dic = {}
            item_deri_dic = {}

            for i in user_item_dic:
                pi=user_vector_dic[i]
                if i not in user_deri_dic:
                    user_deri_dic[i]=0*pi
                for j in user_item_dic[i]:
                    qj=user_vector_dic[j]
                    if j not in item_deri_dic:
                        item_deri_dic[j]=0*qj
                    user_deri_dic[i]+=2*(np.dot(pi,qj)-user_item_dic[i][j])*qj
                    item_deri_dic[j]+=2*(np.dot(pi,qj)-item_user_dic[j][i])*pi
            for i in user_vector_dic:
                user_deri_dic[i]=user_deri_dic[i]/count+2*user_vector_dic[i]
            for j in item_vector_dic:
                item_deri_dic[j]=item_deri_dic[j]/count+2*item_vector_dic[j]

            # for i in user_vector_dic:
            #     pi=user_vector_dic[i]
            #     deri=2*pi
            #     for j in user_item_dic[i]:
            #         qj=item_vector_dic[j]
            #         deri+=(2*(np.dot(pi,qj)-user_item_dic[i][j])*qj)/count
            #     user_deri_dic[i]=deri
            # for j in item_user_dic:
            #     qj=item_vector_dic[j]
            #     deri=2*qj
            #     for i in item_user_dic[j]:
            #         pi=user_vector_dic[i]
            #         deri+=(2*(np.dot(pi,qj)-item_user_dic[j][i])*pi)/count
            #     item_deri_dic[j]=deri

            #更新
            for i in user_vector_dic:
                user_vector_dic[i]-=learning_rate*user_deri_dic[i]
            for j in item_vector_dic:
                item_vector_dic[j]-=learning_rate*item_deri_dic[j]
            error=0
            for u in user_item_dic:
                for i in user_item_dic[u]:
                    count+=1
                    error+=(np.dot(user_deri_dic[u],item_deri_dic[i])-user_item_dic[u][i])**2
            print(error/count)
        return user_vector_dic,item_vector_dic


    def train(self,X,Y,K=5,learning_rate=0.001):
        user_item_dic, item_user_dic =self.form_dic(X,Y)
        self.user_vector_dic,self.item_vector_dic=self.opt(user_item_dic,item_user_dic,K,learning_rate)


    def predict(self,X):
        res=[]
        for u,i in X:
            res.append(np.dot(self.user_vector_dic[u],self.item_vector_dic[i]))
        return np.array(res)
