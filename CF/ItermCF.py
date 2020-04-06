# -*- coding: utf-8 -*-
# @Time    : 2020-04-06 16:36
# @Author  : zxl
# @FileName: ItermCF.py

import numpy as np

class ItemCF:
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

    def cal_sim(self,item_user_dic):
        sim_dic={}
        item_like_dic={}#每个item评分高于2的用户dic
        for i in item_user_dic:
            for u in item_user_dic[i]:
                if item_user_dic[i][u]<2:
                    continue
                if i not in item_like_dic:
                    item_like_dic[i]={}
                item_like_dic[i][u]=item_user_dic[i][u]
        k=0
        total=len(item_like_dic)
        for i in item_like_dic.keys():
            sim_dic[i]={}
            print('cal: '+str(k)+'/'+str(total))
            k+=1
            N_i=len(item_like_dic[i])
            for j in item_like_dic.keys():
                if i==j:
                    continue
                if j in sim_dic and i in sim_dic[j]:
                    sim_dic[i][j]=sim_dic[j][i]
                    continue
                nume=len(set(item_like_dic[i]).intersection(set(item_user_dic[j])))
                N_j=len(item_user_dic[j])
                if nume!=0:
                    sim_dic[i][j]=nume/np.sqrt(N_i*N_j)
        return sim_dic

    def cal_avg(self,user_item_dic):
        avg_dic={}
        for u in user_item_dic:
            if u not in avg_dic:
                avg_dic[u]=0
            for i in user_item_dic[u]:
                avg_dic[u]+=user_item_dic[u][i]
            avg_dic[u]/=len(user_item_dic[u])
        return avg_dic


    def train(self,X,Y):
        self.user_item_dic, self.item_user_dic=self.form_dic(X,Y)
        self.sim_dic=self.cal_sim(self.item_user_dic)
        self.avg_dic=self.cal_avg(self.user_item_dic)







    def predict(self,X):
        res=[]
        k=0
        total=len(X)
        for u,i in X:
            print('predict: '+str(k)+'/'+str(total))
            k+=1
            #没有与i相似的物品，或者与i相似的物品与u评价过的商品无交集
            if i not in self.sim_dic or len(set(self.user_item_dic[u]).intersection(self.sim_dic[i])) ==0:
                res.append(self.avg_dic[u])
                continue
            lst=list(set(self.user_item_dic[u]).intersection(self.sim_dic[i]))
            r1=0
            r2=0
            for j in lst:
                r1+=self.sim_dic[i][j]*self.user_item_dic[u][j]
                r2+=self.sim_dic[i][j]
            if r2==0:
                res.append(self.avg_dic[u])
            else:
                res.append(r1/r2)
        return res
