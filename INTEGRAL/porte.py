import numpy as np
from scipy.stats import pearsonr, spearmanr, kendalltau
from matplotlib import pyplot as plt
from random import random

def porte(hauteur,largeur,centre,X):
    porte = []
    for x in X:
        if x>=(centre-largeur/2) and x<=(centre+largeur/2):
            porte.append(hauteur)
        else:
            y=0
            porte.append(y)
    return porte



def dbporte(hauteur,largeur,centre,hauteur2,largeur2,centre2,X):
    porte = []
    for x in X:
        if x>=(centre-largeur/2) and x<=(centre+largeur/2):
            porte.append(hauteur)
        elif x>=(centre2-largeur2/2) and x<=(centre2+largeur2/2):
            porte.append(hauteur2)
        else:
            y=0
            porte.append(y)
    return porte

def tpporte(hauteur,largeur,centre,hauteur2,largeur2,centre2,hauteur3,largeur3,centre3,X):
    porte = []
    for x in X:
        if x>=(centre-largeur/2) and x<=(centre+largeur/2):
            porte.append(hauteur)
        elif x>=(centre2-largeur2/2) and x<=(centre2+largeur2/2):
            porte.append(hauteur2)
        elif x>=(centre3-largeur3/2) and x<=(centre3+largeur3/2):
            porte.append(hauteur3)
        else:
            y=0
            porte.append(y)
    return porte
	
def porte_rd(hauteur,largeur,centre,X):
    porte = []
    for x in X:
        if x>=(centre-largeur/2) and x<=(centre+largeur/2):
            porte.append(hauteur)
        else:
            y=random()
            porte.append(y)
    return porte

x = np.linspace(-5, 5, num=100)
Y = np.linspace(-5, 5, num=11)
Z = np.linspace(-5, 5, num=11)

portes=tpporte(2,1,0,2,1,2,2,1,4,x)
k=1
for z in Z:
    for y in Y:
        portes2=tpporte(4,1,0,2,1,y,2,1,z,x)
        test=pearsonr(portes,portes2)[0]
        plt.figure(k)
        plt.step(x,portes,x,portes2)
        plt.title(test)
        k=k+1


# ############ Shift ############

# Y = np.linspace(1, 4, num=4)
# portes=porte(2,2,0,x)
# for y in Y:
    # portes2=porte(2,2,y,x)
    
    # plt.figure(y)
    # plt.step(x,portes,x,portes2)
    # plt.axis([-5, 5,-0.5, 5])
    # test_corr = np.corrcoef(portes,portes2)[0,1]
    # test_pear = pearsonr(portes,portes2)[0]
    # test_spear = spearmanr(portes,portes2)[0]
    # test_kenda = kendalltau(portes,portes2)[0]
    
    # print(" corr=",test_corr,"\n pearson=",test_pear,"\n spearman=",test_spear,"\n kendall=",test_kenda,"\n")
	

# ############ Different width ############

# Y = np.linspace(1, 4, num=4)
# portes=porte(2,2,0,x)
# for y in Y:
    # portes2=porte(2,y,0,x)
    
    # plt.figure(y)
    # plt.step(x,portes,x,portes2)
    # plt.axis([-5, 5,-0.5, 5])
    # test_corr = np.corrcoef(portes,portes2)[0,1]
    # test_pear = pearsonr(portes,portes2)[0]
    # test_spear = spearmanr(portes,portes2)[0]
    # test_kenda = kendalltau(portes,portes2)[0]
    
    # print(" corr=",test_corr,"\n pearson=",test_pear,"\n spearman=",test_spear,"\n kendall=",test_kenda,"\n")


# ############ Different height ############

# Y = np.linspace(1, 4, num=4)
# portes=porte(2,2,0,x)
# for y in Y:
    # portes2=porte(y,2,0,x)
    
    # plt.figure(y)
    # plt.step(x,portes,x,portes2)
    # plt.axis([-5, 5,-0.5, 5])
    # test_corr = np.corrcoef(portes,portes2)[0,1]
    # test_pear = pearsonr(portes,portes2)[0]
    # test_spear = spearmanr(portes,portes2)[0]
    # test_kenda = kendalltau(portes,portes2)[0]
    
    # print(" corr=",test_corr,"\n pearson=",test_pear,"\n spearman=",test_spear,"\n kendall=",test_kenda,"\n")


# ############ Shift with a different parameter ############

# height = 3
# width = 1
# Y = np.linspace(1, 4, num=4)
# portes=porte(2,2,0,x)
# for y in Y:
    # portes2=porte(height,width,y,x)
    
    # plt.figure(y)
    # plt.step(x,portes,x,portes2)
    # plt.axis([-5, 5,-0.5, 5])
    # test_corr = np.corrcoef(portes,portes2)[0,1]
    # test_pear = pearsonr(portes,portes2)[0]
    # test_spear = spearmanr(portes,portes2)[0]
    # test_kenda = kendalltau(portes,portes2)[0]
    
    # print(" corr=",test_corr,"\n pearson=",test_pear,"\n spearman=",test_spear,"\n kendall=",test_kenda,"\n")


# ############ Shift with a random function ############

# portes=porte_rd(3,2,0,x)
# portes2=porte_rd(3,2,0,x)

# plt.step(x,portes,x,portes2)
# plt.axis([-5, 5,-0.5, 5])

# test_corr = np.corrcoef(portes,portes2)[0,1]
# test_pear = pearsonr(portes,portes2)[0]
# test_spear = spearmanr(portes,portes2)[0]
# test_kenda = kendalltau(portes,portes2)[0]

# print(" corr=",test_corr,"\n pearson=",test_pear,"\n spearman=",test_spear,"\n kendall=",test_kenda)