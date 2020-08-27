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


# Même programme que correlation jusqu'a la ligne 136 #
data = "AllFWBSdetectionmodif_2018"

date = Extract_WBSoneparam("date", data)
name = Extract_WBSoneparam("trigger", data)
T90 = Extract_WBSoneparam("T90", data)
err_T90 = Extract_WBSoneparam("errT90", data)
SNR = Extract_WBSoneparam("snr", data)
T0 = Extract_WBSoneparam("T0", data)
grbtype = Extract_WBSoneparam("GRB_type", data)

i=0
p=1
snr = []
ptime = []
namel = []
grbtypel=[]
pics = []
raw = []
sigma3 = []
sigma5 = []
sigma7 = []
while i<len(date):
    try:
        plot_data = read_numpy(trans_date(date[i]), trans_name(name[i]))
    except:
        print()
    finally:
        j=0
        t=0
        pic=0
        burst = []
        time = []
        brut =[]
        # On définit les limites à 3, 5 et 7 sigmas (qui seront afficher sur les graphes pour nous aider à chosir notre limite visuellement #
        s3 =[]
        s5 = []
        s7 = []
        while j<len(plot_data[0,1]):
            # value = le sigma pour chaque point de notre courbe (200ms) #
            value = (plot_data[0,1][j]-plot_data[2,1][j])/sqrt(plot_data[2,1][j])
            s3.append((3*sqrt(plot_data[2,1][j])) + plot_data[2,1][j])
            s5.append((5*sqrt(plot_data[2,1][j])) + plot_data[2,1][j])
            s7.append((7*sqrt(plot_data[2,1][j])) + plot_data[2,1][j])
            # On fait un test sur les valeurs précédants la valeur calculé pour savoir si c'est un pic ou juste la continuité d'un pic déja mesurée #
            if j<2:
                valuem1=0
                valuem2=0
            else:
                valuem1=(plot_data[0,1][j-1]-plot_data[2,1][j-1])/sqrt(plot_data[2,1][j-1])
                valuem2=(plot_data[0,1][j-2]-plot_data[2,1][j-2])/sqrt(plot_data[2,1][j-2])
            if value>=5 and valuem1<5 and valuem2<5:
                pic=pic+1
            value2 = plot_data[0,0][j]-date2sec(trans_T0(T0[i]))
            burst.append(value)
            time.append(value2)
            j=j+1
        snr.append(burst)
        ptime.append(time)
        namel.append(name[i])
        pics.append(pic)
        sigma3.append(s3)
        sigma5.append(s5)
        sigma7.append(s7)
        # Ici on tri nos sursaut en fonction de leur nombre de pics (Si moins de 5 => courts sinon long) et ensuite on rassemble les sursauts avec le même nombre de pics #
        if pics[p-1]<5:
            if pics[p-1]==1:
                dst="./Catalogue/CHABERT_short/1pic/"
            elif pics[p-1]==2:
                dst="./Catalogue/CHABERT_short/2pics/"
            else:
                dst="./Catalogue/CHABERT_short/other/"
        else:
            if pics[p-1]<10:
                dst="./Catalogue/CHABERT_long/nottoolong/"
            else:
                dst="./Catalogue/CHABERT_long/verylong/"
        # On enregistre le graphe dans le bon répertoire à l'aide du tri précédent #
        image = Save_Image(p,pics[i],grbtype[i],name[i],T0[i],T90[i],err_T90[i],plot_data,dst,sigma3[i],sigma5[i],sigma7[i])
        p=p+1
    i=i+1
