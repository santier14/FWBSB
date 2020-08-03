import numpy
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
    filename ="./"+date+"/ACS/75_2000/"+name+".npy"
    data = numpy.load(filename, allow_pickle=True, encoding='latin1')
    return data

def trans_date(date):
    date = date.replace('20','',1)
    date = date.replace('-','')
    date = date.replace(' ','')
    return str(date)

def trans_name(name):
    name = name.replace(' ','')
    return str(name)

def trans_time(time):
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


data = "AllFWBSdetection_2018"
date = Extract_WBSoneparam("date", data)
name = Extract_WBSoneparam("trigger", data)
start = Extract_WBSoneparam("time", data)
T90 = Extract_WBSoneparam("T90", data)
err_T90 = Extract_WBSoneparam("errT90", data)
plot_data = read_numpy(trans_date(date[0]), trans_name(name[0]))

plt.vlines(0,min(plot_data[0,1])-1000,max(plot_data[0,1])+1000, color='green')
plt.vlines(T90[0]+err_T90[0],min(plot_data[0,1])-1000,max(plot_data[0,1])+1000, color='pink')
plt.step(plot_data[0,0]-trans_time(start[0]), plot_data[0,1], color='grey')
plt.step(plot_data[1,0]-trans_time(start[0]), plot_data[1,1], color='blue')
plt.step(plot_data[2,0]-trans_time(start[0]), plot_data[2,1], linestyle='--', color='purple',)
plt.ylim(min(plot_data[0,1])-500,max(plot_data[0,1])+500)
plt.show

