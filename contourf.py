#!/usr/bin/python
import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

def contourf(filename, skip, label):
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
    zonename=["0.000000E+00 yr"]
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
            zonename.append(tmpline[2])
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

    #ask user to choose zone
    while 1:
        print('Please choose the number of zone from following list:')
        for i in range(len(zonename)):
            print('# %s %s'% (i+1, zonename[i]))
        chosezone=int(input('Enter your choice:'))
        if chosezone>=1 and chosezone<=len(zonename):
            break
    
    #ask user to choose label
    while 1:
        print('Please choose the number of label from following list:')
        for i in range(3, len(label)):
            print('# %s %s'% (i, label[i]))
        choselabel=int(input('Enter your choice:'))
        if choselabel>=3 and choselabel<len(label):
            break

    #set x,y and z
    x=zone2[chosezone]['X']
    y=zone2[chosezone]['Z']
    z=zone2[chosezone][label[choselabel]]
    realplot(x,y,z,chosezone,label[choselabel])

#real plot function
def realplot(X,Y,Z,i,label):               
    #plot contour. level=8: number of contour; cmap: color of line
    plt.tricontourf(X,Y,Z,10,alpha=0.5,cmap='jet')
            
    #add digit label in line, black, with 0.XX
    #C=plt.tricontour(X0,Y0,Z0,10,alpha=0.5,cmap='jet')
    #plt.clabel(C,inline=True,colors='k',fmt='%1.2f')
    #show color bar
    plt.colorbar()
    #show title
    plt.title('zone'+str(i)+' '+label)
    plt.xlabel('Distance')
    plt.ylabel('Depth')

    #show final plot
    plt.show()  

#highlight output
def esc(code):
    return f'\033[{code}m'

#build path, return path 
def setpath():
    #define default path
    path='/Users/leixu/Documents/Ting/program/contourf/'
    #highlight path
    printpath=esc('31;1;4') + path + esc(0)

    #loop to change path, break only with pathinput==y or n
    while 1:
        pathinput=input('Current path is %s, do you wang to change it? (y/n)'%(printpath))

        #get new path
        if pathinput== 'y' or pathinput=='Y':
            #get new path until confirm
            while 1:
                newpath=input("Please input new path: ")
                newprintpath=esc('31;1;4') + newpath + esc(0)
                pathconfirm=input('New path is %s, confirm with this? (y/n)'%newprintpath)
                if pathconfirm=='y':
                    break
            path=newpath
            break
        #keep original path
        if pathinput== 'n' or pathinput=='N':
            break
    return path

#build filename
def setfile(printpath):
     #ask user to choose file type
        filename=['co2d_conc.dat','co2d_min.dat','co2d_tim.dat']
        printfilename=[]
        for name in filename:
            tmp=esc('31;1;4') + name + esc(0)
            printfilename.append(tmp)
        print('Current path is %s, please choose the file you want to load:'% printpath)
        for i in range(len(filename)):
            print('# %s %s'%(i,printfilename[i]))
        #loop to get fileinput
        while 1:
            fileinput=input('Please enter the number:')
            fileinput=int(fileinput)
            if fileinput>=0 and fileinput<=2:
                break
        return filename[fileinput]

#main function, with simple console UI
def main():
    #infinit loop to exe, until exit is enter in the end
    #contourf()
    time=1
    #dictionary to store file type, with skip lines and label name
    file={'co2d_conc.dat':[10,('X,Y,Z,Sg,Sl,T,pH,Density_L,t_ca+2,t_mg+2,t_na+,t_k+,t_fe+2,t_alo2-,t_sio2(aq),t_cl-,t_hco3-,t_so4-2').split(',')],
    'co2d_min.dat':[11,('X,Y,Z,T,SMco2,Porosity,Permeabi.,halite,illite,quartz,albite,kaolinite,calcite,dolomite,ankerite-2 ,chlorite   ,magnesite  ,k-feldspar ,muscovite  ,siderite-2 ,pyrite,anhydrite  ,anorthite  ,smectite-na,smectite-ca,gypsum').split(',')]}
   
    while (time):
        #define path
        path=setpath()
        printpath=esc('31;1;4') + path + esc(0)

        #ask user to choose file type
        filename=setfile(printpath)

        #call contourf to plot contourf
        contourf(path+filename,file[filename][0],file[filename][1])

        time-=1


if __name__ == '__main__':
    main()
