# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 23:54:58 2019

@author: Caro
"""
## Codigo para practica de ferromagnetismo

import nidaqmx
import matplotlib.pyplot as plt
import numpy as np
import os
import time
#%%
#ai0 campo H
#ai1 campo B
#ai2 termocupla
#%%
DIFFERENTIAL = 10106 #Diferencial
RSE = 10083   #Referenciado
NRSE = 10078 #No referenciado


#Levanto voltaje 
with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev15/ai6",terminal_config = nidaqmx.constants.TerminalConfiguration.RSE)  #Termocupla
    #task.ai_channels.add_ai_voltage_chan("Dev15/ai1",terminal_config = nidaqmx.constants.TerminalConfiguration.DIFFERENTIAL)  # fuente sinusoidal
    #task.ai_channels.add_ai_voltage_chan("Dev15/ai2",terminal_config = nidaqmx.constants.TerminalConfiguration.RSE)     #Integrador 
    task.timing.cfg_samp_clk_timing(2000, samps_per_chan=40000)
    data = task.read(number_of_samples_per_channel=40000,timeout=20.0)
      
    task.wait_until_done()     

    
#%%
time1 = 40000/2000 
tiempo1 = np.linspace(0,time1,len(data))
plt.plot(tiempo1,data)
plt.xlabel('Tiempo [s]')
plt.ylabel('Voltaje [V]')
plt.legend(loc='best')
plt.grid()

np.mean(data)
np.std(data)


#%%

dataH = data[1]
dataB = data[2]
dataT = data[0]
#dataB1 = dataB[0:150000]
#dataH1 = dataH[0:150000]
#dataB2 = dataB[150000:300000]
#dataH2 = dataH[150000:300000]
#dataB3 = dataB[300000:450000]
#dataH3 = dataH[300000:450000]
#dataB4 = dataB[450000:600000]
#dataH4 = dataH[450000:600000]
#dataB5 = dataB[600000:750000]
#dataH5 = dataH[600000:750000]

time = 600000/2000 
tiempo = np.linspace(0,time,len(dataB))   
plt.figure(1)
plt.plot(tiempo,dataH,'o-',label='H')
plt.xlabel('Tiempo [s]')
plt.ylabel('Voltaje [V]')
plt.legend(loc='best')
plt.grid()
#a = np.arange(len(dataB))
plt.figure(2)
plt.plot(tiempo,dataB,label='B')
plt.xlabel('Tiempo [s]')
plt.ylabel('Voltaje [V]')
plt.legend(loc='best')
plt.grid()
plt.figure(3)
plt.plot(tiempo[0:-1:5],dataT[0:-1:5],label='T')
plt.xlabel('Tiempo [s]')
plt.ylabel('Voltaje [V]')
plt.legend(loc='best')
plt.grid()
plt.figure(8)
plt.plot(dataH[70000:70040],dataB[70000:70040],label='Histeresis')
plt.xlabel('Tiempo [s]')
plt.ylabel('Voltaje [V]')
plt.legend(loc='best')
plt.grid()
plt.figure(4)
plt.plot(dataH[0:-1:5],dataB[0:-1:5],label='T')
plt.figure(5)
plt.plot(dataH2,dataB2,label='T')
plt.figure(6)
plt.plot(dataH3,dataB3,label='T')
plt.figure(7)
plt.plot(dataH4,dataB4,label='T')
plt.figure(8)
plt.plot(dataH5,dataB5,label='T')





#%%
np.savetxt('4.txt',np.transpose([dataT,dataB,dataH]),delimiter='\t')
    #%%
    
        
#Levanto voltaje de la temperatura
#with nidaqmx.Task() as task:
 #   task.ai_channels.add_ai_thrmcpl_chan("Dev15/ai2")   #del mismo canal que antes
  #  task.timing.cfg_samp_clk_timing(1000, samps_per_chan=60000)
    #dataTV = task.read(number_of_samples_per_channel=60000,timeout=60.0)
   #datosT.append(dataTV)
   #task.wait_until_done()
    
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_thrmcpl_chan("Dev15/ai2",name_to_assign_to_channel="", min_val=0.0, max_val=100.0, units=nidaqmx.constants.TemperatureUnits.DEG_C, thermocouple_type=nidaqmx.constants.ThermocoupleType.K)
        task.timing.cfg_samp_clk_timing(10000, samps_per_chan=60000)
        dataTV = task.read(number_of_samples_per_channel=60000,timeout=60.0)
        task.wait_until_done()

#%%
#Grafico datos

time = 60000/10000     

tiempo = np.linspace(0,time,len(dataTV))       #No se si esto es necesario


plt.plot(tiempo,dataTV)
plt.xlabel('Tiempo [s]')
plt.ylabel('Voltaje [V]')
plt.grid()

#%%
plt.plot(tiempo,data2)   
figure(3)
plt.plot(tiempo,dataTV)
#%%
#Ahora veo otra forma, a ver si podemos graficar en tiempo real (no se si saldrá o servirá de algo)
#Pruebo solo con un canal

plt.ion()   #Hace que no se cierren los graficos

i = 0 #Contador

with nidaqmx.Task() as task:
    task.ai_channels.add_ai_thrmcpl_chan("Dev6/ai2")     #así indico que levante temperatura la termocupla
                          
    while i<180
    dataT = task.read(number_of_samples_per_channel=samples_per_channel)
    plt.scatter(i,data[0],c='r')
    plt.pause(0.05)
    datosT.append(dataT)
    i = i+1
    





