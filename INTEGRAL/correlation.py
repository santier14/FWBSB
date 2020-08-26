import numpy as np
from scipy.stats import pearsonr, spearmanr, kendalltau
from matplotlib import pyplot as plt
from random import random
from math import sqrt
from shutil import copyfile

def read_results(data):
    path_store_result="./Catalogue/"
    f=open(path_store_result+data+".txt", "r")
    fr=f.readlines()
    return fr

def read_summary(date):
    path_store_result="./"
    f=open(path_store_result+date+"/ACS/75_2000/Summary"+date+"_ACS_emin75_emax2000_bin0.2-0.txt", "r")
    fr=f.readlines()
    return fr

def read_numpy(date, name):
    filename ="./"+date+"/ACS/75_2000/"+name+".npy"
    data = np.load(filename, allow_pickle=True, encoding='latin1')
    return data

def trans_date(date):
    date = date.replace('20','',1)
    date = date.replace('-','')
    date = date.replace(' ','')
    return str(date)

def trans_name(name):
    name = name.replace(' ','')
    return str(name)

def trans_T0(T0):
    T0 = T0[6:]
    T0 = T0.replace(' ','')
    return str(T0)

def date2sec(time):
    time = time.replace(' ','')
    hours = time[:2]
    minutes = time[3:5]
    seconds = time[6:]
    time = (int(hours)*60+int(minutes))*60+float(seconds)
    return float(time)

def correspond(Param):
    header=["trigger","date","time","GRB_type","snr","peakflux","errpeakflux","fluence","errfluence","T90","errT90","multdur","var","errvar","T0"]
    indice=header.index(Param)
    return indice

def correspond2(Param):
    header=["trigger","date","time","multdur","snr","GRB_type","peakflux","fluence","T90","Tstart","Tend"]
    indice=header.index(Param)
    return indice

def Extract_WBSoneparam(Param, data):
    fr=read_results(data)
    par=[]
    idi=correspond(Param)
    for line in fr:
        if Param in ["trigger","date","time","GRB_type"]:
            par.append(line.split("|")[idi])
        elif Param in ["T0"]:
            par.append(line.split("|")[13])
        else:
            par.append(float(line.split("|")[idi]))
    par=np.array(par)
    if Param=="GRB_type":
        par = np.char.strip(par)
    return par

def Extract_Summaryparam(Param, date):
    fr=read_summary(date)
    par=[]
    idi=correspond2(Param)
    for line in fr:
        if Param in ["trigger","date","time","GRB_type"]:
            par.append(line.split("\t")[idi])
        else:
            par.append(float(line.split("\t")[idi]))
    par=np.array(par)
    if Param=="GRB_type":
        par = np.char.strip(par)
    return par

def Save_Image(p,pic,grbtype,name,T0,T90,err_T90,plot_data,dst,sigma3,sigma5,sigma7):
    plt.figure(p)
    plt.step(plot_data[0,0]-date2sec(trans_T0(T0)), sigma3, linestyle='--', where='post')
    plt.step(plot_data[0,0]-date2sec(trans_T0(T0)), sigma5, linestyle='--', where='post')
    plt.step(plot_data[0,0]-date2sec(trans_T0(T0)), sigma7, linestyle='--', where='post')
    #plt.vlines(0,min(plot_data[0,1])-1000,max(plot_data[0,1])+1000, color='green', label='T0')
    #plt.vlines(Tstart,min(plot_data[0,1])-1000,max(plot_data[0,1])+1000, linestyle='--', color='blue', label='Tstart')
    #plt.vlines(Tend,min(plot_data[0,1])-1000,max(plot_data[0,1])+1000, linestyle='--', color='blue', label='Tend')
    #plt.vlines(T90+err_T90,min(plot_data[0,1])-1000,max(plot_data[0,1])+1000, color='pink', label='T90')
    plt.step(plot_data[0,0]-date2sec(trans_T0(T0)), plot_data[0,1], color='grey', where='post', label='raw data')
    plt.step(plot_data[1,0]-date2sec(trans_T0(T0)), plot_data[1,1], color='blue', where='post', label='')
    plt.step(plot_data[2,0]-date2sec(trans_T0(T0)), plot_data[2,1], linestyle='--', color='purple', where='post', label='SNR')
    plt.ylim(min(plot_data[0,1])-500,max(plot_data[0,1])+500)
    plt.title(name+'\n T90 = '+str(T90)+' ('+grbtype+') pic:'+str(pic))
    plt.xlabel('Time relative to T0 (s)')
    
    plt.savefig(dst+trans_name(name)+".png")
    ok = 'ok'
    return ok

data = "AllFWBSdetectionmodif_2018"

date = Extract_WBSoneparam("date", data)
name = Extract_WBSoneparam("trigger", data)
T90 = Extract_WBSoneparam("T90", data)
err_T90 = Extract_WBSoneparam("errT90", data)
SNR = Extract_WBSoneparam("snr", data)
T0 = Extract_WBSoneparam("T0", data)
grbtype = Extract_WBSoneparam("GRB_type", data)

i=0
pearson = []
ptime = []
namel = []
grbtypel=[]
while i<len(date):
#while i<55:
    try:
        plot_data = read_numpy(trans_date(date[i]), trans_name(name[i]))
    except:
        print()
    finally:
        Tstart = Extract_Summaryparam("Tstart", trans_date(date[i]))
        Tend = Extract_Summaryparam("Tend", trans_date(date[i]))
        j=0
        l=0
        k=0
        t=0
        burst=[]
        burst2=[]
        time=[]
        x = float(date2sec(trans_T0(T0[i])))-2
        if float(T90[i])<2.0:
            y = float(20*(T90[i]+err_T90[i])+date2sec(trans_T0(T0[i])))
        elif float(T90[i])<10.0 and float(T90[i])>2.0:
            y = float(10*(T90[i]+err_T90[i])+date2sec(trans_T0(T0[i])))
        elif float(T90[i])<20.0 and float(T90[i])>10.0:
            y = float(5*(T90[i]+err_T90[i])+date2sec(trans_T0(T0[i])))
        else:
            y = float(5*(T90[i]+err_T90[i])+date2sec(trans_T0(T0[i])))
        if plot_data[1,1][-1]==max(plot_data[1,1]):
            z=1
        else:
            z=0
        while j<len(plot_data[1,0])-z:
            if plot_data[1,0][j]>x and plot_data[1,0][j]<y:
                burst.append(plot_data[1,1][j])
                j=j+1
            else:
                j=j+1
        while k<len(burst):
            if burst[k]<max(burst) and l==0:
                k=k+1
            else:
                l=1
                burst2.append(burst[k])
                time.append(t)
                k=k+1
                t=t+1
        if len(burst2)==len(time) and len(burst2)!=0:
            pearson.append(burst2)
            ptime.append(time)
            namel.append(name[i])
            grbtypel.append(grbtype[i])
    i = i+1
	
i=0
k=0
m=0
short = []
shorttime = []
shortname = []
shorttype = []
long = []
longtime = []
longname = []
longtype = []
other = []
othertime = []
othername = []
othertype = []
pearson_save = pearson
ptime_save = ptime
#while len(pearson)>0:
while i<2:
    j=0
    l=0
    while j<len(pearson):
        if i!=j:
            pearson[i]=pearson_save[i]
            ptime[i]=ptime_save[i]
            pearson[j]=pearson_save[j]
            ptime[j]=ptime_save[j]
            while len(pearson[i])!=len(pearson[j]):
                if len(pearson[i])<len(pearson[j]):
                    pearson[i].append(min(pearson[i])) 
                elif len(pearson[i])>len(pearson[j]):
                    pearson[j].append(min(pearson[j])) 
#                if len(pearson[i])<len(pearson[j]):
#                    pearsonj=pearson[j]
#                    del pearsonj[-1]
#                    pearson[j]=pearsonj
#                    ptimej=ptime[j]
#                    del ptimej[-1]
#                    ptime[j]=ptimej
#                elif len(pearson[i])>len(pearson[j]):
#                    pearsoni=pearson[i]
#                    del pearsoni[-1]
#                    pearson[i]=pearsoni
#                    ptimei=ptime[i]
#                    del ptimei[-1]
#                    ptime[i]=ptimei
            test = pearsonr(pearson[i],pearson[j])
            if test[0]>0.7:
                if l==0:
                    pearson[i]=pearson_save[i]
                    ptime[i]=ptime_save[i]
                    while len(ptime[i])!=len(pearson[i]):
                        if len(ptime[i])<len(pearson[i]):
                            ptime[i].append(max(ptime[i])+1)
                        elif len(ptime[i])>len(pearson[i]):
                            ptimei=ptime[i]
                            del ptimei[-1]
                            ptime[i]=ptimei
                    if m==0:
                        short.append(pearson[i])
                        shorttime.append(ptime[i])
                        shortname.append(namel[i])
                        shorttype.append(grbtypel[i])
                    elif m==1:
                        long.append(pearson[i])
                        longtime.append(ptime[i])
                        longname.append(namel[i])
                        longtype.append(grbtypel[i])
                    #plt.figure(k+1)
                    #plt.step(ptime[i], pearson[i], color='blue', where='post',label=namel[i])
                    l=1
                pearson[i]=pearson_save[i]
                ptime[i]=ptime_save[i]
                pearson[j]=pearson_save[j]
                ptime[j]=ptime_save[j]
                while len(ptime[i])!=len(pearson[j]):
                    if len(ptime[i])<len(pearson[j]):
                        pearsonj=pearson[j]
                        del pearsonj[-1]
                        pearson[j]=pearsonj
                    elif len(ptime[i])>len(pearson[j]):
                        pearson[j].append(min(pearson[j]))
                if m==0:
                    short.append(pearson[j])
                    shorttime.append(ptime[j])
                    shortname.append(namel[j])
                    shorttype.append(grbtypel[j])
                elif m==1:
                    long.append(pearson[j])
                    longtime.append(ptime[j])
                    longname.append(namel[j])
                    longtype.append(grbtypel[j])
                #plt.step(ptime[i], pearson[j], color='grey', where='post', label=namel[j])
                del pearson[j]
                del ptime[j]
                del namel[j]
                del grbtypel[j]
                pearson[i]=pearson_save[i]
                ptime[i]=ptime_save[i]
            else:
                pearson[j]=pearson_save[j]
                ptime[j]=ptime_save[j]
                j = j+1
        else:
            j=j+1
    if l==1:
        del pearson[i]
        del ptime[i]
        del namel[i]
        del grbtypel[i]
    m=m+1
    k=k+1
    i=i+1
    #plt.gca().legend()