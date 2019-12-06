#!/usr/bin/env python
# coding: utf-8

# In[5]:

import numpy as np
import visa
import matplotlib.pyplot as plt
import time as time
rm = visa.ResourceManager()

# Inicializo el lock-in
resource_name = 'GPIB0::11::INSTR' # ID en INTERFASE -> set up
resource_name2 = 'USB0::0x0699::0x0363::C065089::INSTR'
rm = visa.ResourceManager()
lockin = rm.open_resource(resource_name)
osci=rm.open_resource(resource_name2)
print(lockin.query('*IDN?'))
print(osci.query('*IDN?'))


# In[83]:


def med_barrido_en_freq(FREQ_I, FREQ_F, DELTA_FREQ, SLEEP_TIME):
    """ Recibe los parámetros constantes y retorna
    X_array, Y_array, R_array, THETA_array.

    Requiere que el lock-in está inicializado
    """

    # Inicialización de variables
    FREQ_array = np.arange(FREQ_I, FREQ_F, DELTA_FREQ)

    X_array = np.zeros_like(FREQ_array, dtype=float)
    Y_array = np.zeros_like(FREQ_array, dtype=float)



AMPLITUDSINALU3v2=[]
FASESINALU3v2=[]
VOLTOSCISINALU3v2=[]
FREQSSINALU3v2=np.linspace(10,1100,218)


AMPLITUDALU4v3=[]
FASEALU4v3=[]
VOLTOsciALU4v3=[]
FREQALU4v3=np.linspace(10,3000,299)


    # Rutina
for i in range (len(FREQALU4v3)):
    if lockin.query_ascii_values('OUTP ? 3')[0]>0.1:
        lockin.write(f'SENS {24:f}')   
    elif 0.1>lockin.query_ascii_values('OUTP ? 3')[0]>0.05:
        lockin.write(f'SENS {23:f}') 
    elif 0.05>lockin.query_ascii_values('OUTP ? 3')[0]>0.02:
        lockin.write(f'SENS {22:f}')
    elif 0.02>lockin.query_ascii_values('OUTP ? 3')[0]>0.01:
        lockin.write(f'SENS {21:f}')
    elif 0.01>lockin.query_ascii_values('OUTP ? 3')[0]>0.005:
        lockin.write(f'SENS {20:f}')
    elif 0.005>lockin.query_ascii_values('OUTP ? 3')[0]>0.002:
        lockin.write(f'SENS {19:f}')
    elif 0.002>lockin.query_ascii_values('OUTP ? 3')[0]>0.001:
        lockin.write(f'SENS {18:f}')
    freq = FREQALU4v3[i]           # Actiualizo la frecuencia
    lockin.write(f'FREQ {freq:f}')
    VOLTOsciALU4v3.append(osci.query_ascii_values("MEASU:MEAS1:VAL?")[0])
    time.sleep(2)              # Espero al estacionario        
    AMPLITUDALU4v3.append(lockin.query_ascii_values('OUTP ? 3'))
    FASEALU4v3.append(lockin.query_ascii_values("OUTP ? 4"))
    
CorrientePrinALU4v3 = np.asarray(VOLTOsciALU4v3)/100
CorrientePrinNOppALU4v3 = np.asarray(VOLTOsciALU4v3)/200
        

plt.figure()
#Mesa 25cm
plt.plot(FREQALU4v1,np.tan((-1)*DifFaseALU4v1Rad),"-o")
plt.plot(FREQALU4v2,np.tan((-1)*DifFaseALU4v2Rad),"-o")
plt.plot(FREQALU4v3,np.tan((-1)*DifFaseALU4v3Rad),"-o")


DifFaseALU4v1 = np.squeeze(np.asarray(FASEALU4v1))-np.squeeze(np.asarray(FASESINALU4v1))
DifFaseALU4v1Rad=DifFaseALU4v1*(np.pi)/180


DifFaseALU4v2 = np.squeeze(np.asarray(FASEALU4v2))-np.squeeze(np.asarray(FASESINALU4v1))
DifFaseALU4v2Rad=DifFaseALU4v2*(np.pi)/180


DifFaseALU4v3 = np.squeeze(np.asarray(FASEALU4v3))-np.squeeze(np.asarray(FASESINALU4v1))
DifFaseALU4v3Rad=DifFaseALU4v3*(np.pi)/180



plt.figure()
plt.plot(FREQS,FaseRad,"o")
plt.figure()
plt.plot(FREQS,AMPLITUD,"o")
plt.figure()
plt.plot(FREQS,CorrientePrin,"o")
plt.figure()
plt.plot(FREQS,CorrientePrinNOpp,"o")

Relacionlinear= np.squeeze(np.asarray(AMPLITUD))/CorrientePrinNOpp
plt.figure()
plt.plot(FREQS,Relacionlinear,"o")



