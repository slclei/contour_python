#!/usr/bin/python
import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

def contourf():
    #step 1 open file
    #build file name
    #yr='200yr'
    #element='XCO2a'
    path='/Users/leixu/Documents/Ting/program/contourf/'
    #filename, choose 1 from 3 cases:
    # co2d_conc.dat, data start at line 11. 
    # col name: VARIABLES =X,Y,Z,Sg,Sl,T,pH,Density_L,t_ca+2,t_mg+2,t_na+,t_k+,t_fe+2,t_alo2-,t_sio2(aq),t_cl-,t_hco3-,t_so4-2
    filename=path+'co2d_conc.dat'
    skip=10
    label=('X,Y,Z,Sg,Sl,T,pH,Density_L,t_ca+2,t_mg+2,t_na+,t_k+,t_fe+2,t_alo2-,t_sio2(aq),t_cl-,t_hco3-,t_so4-2').split(',')

    # co2d_min.dat, data start at line 12.
    # col name: VARIABLES =X,Y, Z,T,SMco2,Porosity,Permeabi.,halite,illite,quartz,albite,kaolinite,calcite,dolomite,ankerite-2 ,chlorite   ,magnesite  ,k-feldspar ,muscovite  ,siderite-2 ,pyrite,anhydrite  ,anorthite  ,smectite-na,smectite-ca,gypsum
    #filename=path+'co2d_conc.dat'
    #skip=11

    # co2d_tim.dat, data start at line 14
    # col name: ELEM    Time(yr)        Sg         Sl      T(C)     pH       SMco2     Porosity    Perm(m^2)  t_ca+2      t_mg+2      t_na+       t_k+        t_fe+2      t_alo2-     t_sio2(aq)  t_cl-       t_hco3-     t_so4-2     halite      illite      quartz      albite      kaolinite   calcite     dolomite    ankerite-2  chlorite    magnesite   k-feldspar  muscovite   siderite-2  pyrite      anhydrite   anorthite   smectite-na smectite-ca gypsum      co2(g)      chg.bal.(eq
    #filename=path+'co2d_conc.dat'
    #skip=13

    #load sample into lines
    fp=open(filename,'r')
    lines=fp.readlines()
    fp.close()

    #save data into matrix. Note: several matrixes are used for several zones
    #number of zones, defalut is 1
    n_zone=1
    #dictionary to record data in each zone
    zone={1:[]}
    #save data to zones
    for line in lines:
        #skip rows with text
        if skip>0:
            skip-=1
            continue
        #split the line with space
        tmpline=line.split()
        #print(len(tmpline))
        #add a zone if this line start with ZONE, and skip this line
        if tmpline[0]=='ZONE':
            n_zone+=1
            zone[n_zone]=[]
            continue

        #add data of this line to zone[n_zone]
        #travse string to float
        tmpfloat=[]
        for item in tmpline:
            tmpfloat.append(float(item))
        zone[n_zone].append(tmpfloat)

    #build second dictionary, to store each col in each zone
    #i.e.zone2[1]={'X':[],'Y':[]...}
    zone2={}
    #loop for each zone
    for i in range(n_zone):
        #get data from each zone
        tmplist=zone[i+1]
        zone2[i+1]={}
        #store each col in zone2[i]
        for line in tmplist:
            for j in range(len(label)):
                #initialize zone2[i+1] in the first time
                if label[j] not in zone2[i+1]:
                    zone2[i+1][label[j]]=[]
                #append element in each col to each label in zone2[i+1]
                zone2[i+1][label[j]].append(line[j])
        #del col 'Y'
        del zone[i+1][:][1]

    #loop for each zone
    #TODO test 1 1st
    for i in range(1,10):
        #buid data for mesh (X and Y) and height (Z) 
        #X and Y are mesh, in col 'X' and 'Z'
        #Z is in other cols
        X0=zone2[i+1]['X']
        Y0=zone2[i+1]['Z']
        #grid for X and Y
        X,Y=np.mgrid[np.min(X0):np.max(X0):5,np.min(Y0):np.max(Y0):5]
        points=[]
        for j in range(len(X0)):
            tmppoint=[X0[j],Y0[j]]
            points.append(tmppoint)

        #plot for each label
        for j in range(10,11):
            #change col in label to be 2D array
            Z0=zone2[i+1][label[j]]
            Z=griddata(points,Z0,(X,Y),method='linear')                       

            #plot contour. level=8: number of contour; cmap: color of line
            plt.contourf(X,Y,Z,4,alpha=0.5,cmap='jet',extend='both')
            C=plt.contour(X,Y,Z,4,alpha=0.5,cmap='jet')
            #add digit label in line, black, with 0.XX
            plt.clabel(C,inline=True,colors='k',fmt='%1.2f')
            #show color bar
            plt.colorbar()
            #show title
            plt.title('zone'+str(i)+' '+label[j])
            plt.xlabel('Distance')
            plt.ylabel('Depth')

            #show final plot
            plt.show()
   

if __name__ == '__main__':
    contourf()
