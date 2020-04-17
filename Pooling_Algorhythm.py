# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 10:10:27 2020

Plots out how simulations go

@author: kaica
"""

import numpy as np
import random


Testing_Pool = np.zeros(shape = (10000))

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
        
        
def positive_person_adding(numb_positive,Testing_Pool):
    """Adds given number of positive tested people into function"""
    Testing_Pool = list(Testing_Pool)
    for Pos_add in range(numb_positive):
        Testing_Pool[Pos_add] = 1
        
    """Then shuffles array"""
    Testing_Pool = random.sample(Testing_Pool, len(Testing_Pool))
    
    return Testing_Pool
  
  

def extractDigits(lst): 
    res = [] 
    #print(lst)
    for el in lst: 
        sub = el
        res.append([sub]) 
      
    return(res) 

def find_indiv_positives(Group_Lists,test_counter):
    """Finds the lists that only contain 1s"""
    indiv_return_list=[]
    #print(len(Group_Lists))
    for indiv_group in Group_Lists:
        test_counter +=1
        if max(indiv_group) == 1:
            for indiv_Val in indiv_group:
                indiv_return_list.append(indiv_Val)
    return indiv_return_list, test_counter     
        
def n_groups_calc_halfing(Full_Testing_Pool,initial_groupsize,round_num):
       """How the n_groups_updates"""
       desired_size_of_each_group= int(initial_groupsize/(2**round_num))
       #print(desired_size_of_each_group)
       if desired_size_of_each_group == 0:
           n_groups = len(Full_Testing_Pool)
           return n_groups, desired_size_of_each_group
       else:
           n_groups = int(len(Full_Testing_Pool)/desired_size_of_each_group)
       if len(Full_Testing_Pool) % desired_size_of_each_group > 0:
           n_groups +=1
       return n_groups, desired_size_of_each_group
       #n_groups = int((initial_n_groups)*doubler*len(Full_Testing_Pool)) +1#makes it so the groups are around half as big
       #len(Full_Testing_Pool)*(1/10)*initial_n_groups*2

def Full_Sim_of_Testing(Full_Testing_Pool,n_groups):
    """The sorting algorhythm that finds the positives in as few tests as possible"""
    n_groups_list= []
    size_of_each_group = []
    test_counter = 0
    initial_n_groups = n_groups
    initial_group_size= n_groups
    
    doubler = 0
    while min(Full_Testing_Pool) == 0: #Until it gets down to smallest chunk
        n_groups,desired_size_of_each_group = n_groups_calc_halfing(Full_Testing_Pool,initial_group_size,doubler)#makes it so the groups are around half as big

        doubler +=1
        if n_groups == len(Full_Testing_Pool):
            Chunked_tests = extractDigits(Full_Testing_Pool)
        else:
            #print(Full_Testing_Pool,n_groups)
            Chunked_tests = list(chunks(Full_Testing_Pool,n_groups))
        if n_groups > len(Full_Testing_Pool): #If the group size is too large
            n_groups= len(Full_Testing_Pool)          
        Full_Testing_Pool,test_counter = find_indiv_positives(Chunked_tests,test_counter)
        
        
        
        #print(len(Full_Testing_Pool))

        n_groups_list.append(n_groups)
        size_of_each_group.append(desired_size_of_each_group)
            

    
    return Full_Testing_Pool,test_counter,n_groups_list,size_of_each_group

#SImulates a certain amount of times how long it takes to find 7 people

import pandas as pd
import tqdm
from tqdm import tqdm
Simul_dataframe = {"Size of People in Initial Group":[],
                   "number of tests_required":[],
                   "True_Positive_Cases":[]
                   ,"True_Positive_Cases_String":[]
                   ,"Group_Progression":[]
                   ,"Size_of_Group_Progression":[]}

Simul_dataframe_rounds = {"Size of People in Initial Group":[],
                   "number of tests_required":[],
                   "True_Positive_Cases":[]
                   ,"True_Positive_Cases_String":[]
                   ,"Group_Progression":[]
                   ,"Size_of_Group_Progression":[]
                   ,"Round_Num":[]}


for Group_prog in range(12):
        key = "Group Num in Round " + str(Group_prog + 1) 
        if key not in Simul_dataframe:
            Simul_dataframe[key] = []
        key = "Size of Group Num in Round " + str(Group_prog + 1)
        if key not in Simul_dataframe:
            Simul_dataframe[key] = []


for True_Positive_Cases in tqdm(range(1,101,10)):
   #Full_Testing_Pool = positive_person_adding(True_Positive_Cases,Testing_Pool)
   for random_izer in range(20): #How many times the program is rerun
      Full_Testing_Pool = positive_person_adding(True_Positive_Cases,Testing_Pool)
      for num_of_initial_groups in range(1,1001):    
    
            Final_results, final_test_num, How_Many_Groups,size_of_each_group = Full_Sim_of_Testing(Full_Testing_Pool,num_of_initial_groups)
            Simul_dataframe["Size of People in Initial Group"].append(num_of_initial_groups)
            Simul_dataframe["number of tests_required"].append(final_test_num)
            Simul_dataframe["True_Positive_Cases"].append(True_Positive_Cases)
            Simul_dataframe["True_Positive_Cases_String"].append(str(True_Positive_Cases) + " Cases")
            Simul_dataframe["Group_Progression"].append(How_Many_Groups)
            Simul_dataframe["Size_of_Group_Progression"].append(size_of_each_group)
            for Group_prog in range(12):
                key = "Group Num in Round " + str(Group_prog)
                if key not in Simul_dataframe:
                    Simul_dataframe[key] = [How_Many_Groups[Group_prog]]
                else:
                    try:
                        Simul_dataframe[key].append(How_Many_Groups[Group_prog])
                    except:
                        Simul_dataframe[key].append(0)
            for Group_prog in range(12):
                key = "Size of Group Num in Round " + str(Group_prog)
                if key not in Simul_dataframe:
                    Simul_dataframe[key] = [size_of_each_group[Group_prog]]
                else:
                    try:
                        Simul_dataframe[key].append(size_of_each_group[Group_prog])   #Adds Zero Value otherwise 
                    except:
                        Simul_dataframe[key].append(0)
                     
                        
            """Transformed Round-based Dataset"""
            for indiv_round in  size_of_each_group:      
                Simul_dataframe_rounds["Size of People in Initial Group"].append(num_of_initial_groups)
                Simul_dataframe_rounds["number of tests_required"].append(final_test_num)
                Simul_dataframe_rounds["True_Positive_Cases"].append(True_Positive_Cases)
                Simul_dataframe_rounds["True_Positive_Cases_String"].append(str(True_Positive_Cases) + " Cases")
                Simul_dataframe_rounds["Group_Progression"].append(How_Many_Groups)
                Simul_dataframe_rounds["Size_of_Group_Progression"].append(size_of_each_group)
                Simul_dataframe_rounds["Round_Num"].append(indiv_round+1)





del Simul_dataframe["Group Num in Round 12"]
del Simul_dataframe["Size of Group Num in Round 12"]

for rower in Simul_dataframe:
    print(rower)
    print(len(Simul_dataframe[rower]))

Simul_dataframe = pd.DataFrame(Simul_dataframe)
import os
os.chdir('C:/Users/kaica/Documents/Pooling_Algorithin_COVID')
"""
lines = Simul_dataframe.plot.line(x='num_of_initial_groups'
                                  , y='number of tests_required'
                                  ,legend ='True_Positive_Cases')
"""
import seaborn as sns
from matplotlib.pyplot import figure
#figure(num=None, figsize=(50, 60), dpi=80, facecolor='w', edgecolor='k')

sns.set(rc={'figure.figsize':(11.7,8.27)}) 

ax = sns.lineplot(x="Size of People in Initial Group"
                  , y="number of tests_required"
                  , hue="True_Positive_Cases_String",
                  
                  data=Simul_dataframe)
ax.set_title("Number of Tests Required Before The Final True Ones Are Selected")
ax_save= ax.get_figure()
ax_save.savefig('True_Positives_Adjusted_Full_Plot.png', dpi=100)

Simul_dataframe.to_csv("COVID_POOLED_TEST.CSV")
Simul_dataframe_rounds.to_csv("COVID_POOLED_TEST_TRANSFORMED.CSV")

#def group_splitting_algo():


#Add False Positive and True Negative