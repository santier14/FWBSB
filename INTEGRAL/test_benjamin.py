import numpy as np
from matplotlib import pyplot as plt

def read_results(data):
    path_store_result="./Catalogue/"
    f=open(path_store_result+data+".txt", "r")
    fr=f.readlines()
    return fr

def read_detections(date):
    path_store_result="./"
    f=open(path_store_result+date+"/ACS/75_2000/"+date+"_ACS_emin75_emax2000_bin0.2-0.txt", "r")
    fr=f.readlines()
    return fr

def read_numpy(date, name):
    file_name ="./"+date+"/ACS/75_2000/"+name+".npy"
    #file_name="180101_ACS-1.0.npy"
    #print(file_name)
    data = np.load(file_name,allow_pickle=True,encoding='latin1')
    return data

def trans_date(date):
    date = date.replace('20','',1)
    date = date.replace('-','')
    date = date.replace(' ','')
    return str(date)

def correspond(Param):
    header=["trigger","date","time","GRB_type","snr","peakflux","errpeakflux","fluence","errfluence","T90","errT90","multdur","var","errvar","T0"]
    indice=header.index(Param)
    return indice

def Extract_WBSoneparam(Param, data):
    fr=read_results(data)
    par=[]
    idi=correspond(Param)
    for line in fr:
        if Param in ["trigger","date","time","GRB_type"]:
            par.append(line.split("|")[idi])
        else:
            par.append(float(line.split("|")[idi]))
    par=np.array(par)
    if Param=="GRB_type":
        par = np.char.strip(par)
    return par

def Extract_alertname(date):
    fr=read_detections(date)
    par=[]
    idi=0
    for line in fr:
        par.append(line.split(" \t")[idi])
    par=np.array(par)
    return par


data = "AllFWBSdetection_2018"
param = "date"  
date = Extract_WBSoneparam(param, data)
name = Extract_alertname(trans_date(date[0]))

print(trans_date(date[0]))
print(name[0])

test = read_numpy(trans_date(date[0]), name[0])
print(test[1])

#all_detection = open("./Catalogue/AllFWBSdetection_2018.txt", "r")
#
#line = all_detection.readline()
#
#while line:
#    print(line)
#    line = all_detection.readline()
#
#print(line)

#all_detection.close()    
#modiftest
