# -*- coding: utf-8 -*-
# @Time    : 2020-04-06 16:35
# @Author  : zxl
# @FileName: UserCF.py


import numpy as np

class UserCF():

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

    def cal_sim(self,user_item_dic):
        """
        计算用户之间相似度
        :param user_item_dic:
        :return:sim_dic, avg_rating_dic
        """
        sim_dic={}
        avg_rating_dic={}
        for u in user_item_dic.keys():
            rating=0
            for i in user_item_dic[u].keys():
                rating+=user_item_dic[u][i]
            avg_rating_dic[u]=rating/len(user_item_dic[u])

        k=0
        total=len(user_item_dic)
        user_item_dic2={}
        user_item_dic3={}
        for u in user_item_dic:
            user_item_dic2[u]={}
            user_item_dic3[u]={}
            for i in user_item_dic[u]:
                user_item_dic2[u][i]=user_item_dic[u][i]-avg_rating_dic[u]
                user_item_dic3[u][i] = (user_item_dic[u][i] - avg_rating_dic[u])**2
        self.user_item_dic2=user_item_dic2

        for u in user_item_dic.keys():
            print("cal sim:"+str(k)+"/"+str(total))
            k+=1
            sim_dic[u]={}
            for v in user_item_dic.keys():
                if v==u :
                    continue
                if v in sim_dic.keys() and u in sim_dic[v].keys():#已经计算过
                    sim_dic[u][v]=sim_dic[v][u]
                    continue
                if len(set(user_item_dic[u]).intersection(set(user_item_dic[v]))) == 0:
                    continue

                P=list(set(user_item_dic[u]).intersection(set(user_item_dic[v])))
                nume=0
                demo1=0
                demo2=0
                for p in P:
                    nume+=user_item_dic2[u][p]*user_item_dic2[v][p]
                    demo1+=user_item_dic3[u][p]
                    demo2+=user_item_dic3[v][p]
                if demo1!=0 and demo2!=0:
                    sim_dic[u][v]=nume/(np.sqrt(demo1)*np.sqrt(demo2))
        return sim_dic,avg_rating_dic


    def train(self,X,Y):
        """
        :param X: (n,2),[（user,item）,...]元组
        :param Y: (n,),(rating,...)
        :return: None
        """
        self.user_item_dic,self.item_user_dic=self.form_dic(X,Y)
        print('dic load finished!')
        self.sim_dic,self.avg_rating_dic=self.cal_sim(self.user_item_dic)
        print('sim_dic calculation finished!')



    def predict(self,X):
        """
        :param X: (n,2),[(user,iterm),...]
        :return: Y,(n,),(rating,...)
        """
        res=[]
        k=0
        total=len(X)
        for u,i in X:
            print('predict:'+str(k)+'/'+str(total))
            k+=1
            r_avg=self.avg_rating_dic[u]
            r2=0
            nume = 0
            demo = 0
            #v是与u相似并且对i评分过的用户
            for v in list(set(self.sim_dic[u].keys()).intersection(set(self.item_user_dic[i].keys()))):
                if self.sim_dic[u][v]<0.5:#TODO，可以将相似度大于某个阈值的用户给筛选出来
                    continue
                nume+=self.sim_dic[u][v]*self.user_item_dic2[v][i]
                demo+=self.sim_dic[u][v]
            if demo!=0:
                r2=nume/demo
            res.append(r_avg+r2)
        return np.array(res)