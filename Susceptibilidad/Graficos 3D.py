# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 20:01:04 2019

@author: Wallace
"""

from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

fig=plt.figure()
ax=  plt.axes(projection='3d')

FASEALU5RAD= (np.squeeze(np.asarray(FASEALU5))*(np.pi))/180
FASEALU4RAD= (np.squeeze(np.asarray(FASEALU4))*(np.pi))/180
FASEALU3RAD= (np.squeeze(np.asarray(FASEALU3))*(np.pi))/180
FASEALU2RAD= (np.squeeze(np.asarray(FASEALU2))*(np.pi))/180
FASEALU1RAD= (np.squeeze(np.asarray(FASEALU1))*(np.pi))/180
#armo la funcion 
def Conductividad(x, y,D,d):
    return ((16*np.tan(y))/(x*4*(np.pi)*(D**2-d**2)))*10**7

#%%
#grafico de la manera 1 usando una superficie y grids de los datos.
#elijo las variables y las escribo como matrices para  poder graficarlas
x = FREQSALU1
y = FASEALU1RAD
z= Conductividad (x,y,0.019,0.008)
X, Y = np.meshgrid(x, y)
Z = Conductividad(X, Y,0.019,0.008)

#%%
fig=plt.figure()
ax=  plt.axes(projection='3d')
ax.plot_surface(X, Y, Z, rstride=1, cstride=1,cmap='viridis', edgecolor='none')
ax.set_title('Susceptibilidad');

#%%
#grafico de la manera 2 usando triangulacion
fig
ax = plt.axes(projection='3d')
ax.scatter(x, y, z, c=z, cmap='viridis', linewidth=0.5);
ax.plot_trisurf(x, y, z,cmap='viridis', edgecolor='none');

#%%
#graficos 2d de fase vs suceptibiidad
plt.figure()
plt.plot(FREQSALU5,Conductividad(FREQSALU5,FASEALU5RAD,0.019,0.018),"-o",color="blue")
plt.plot(FREQSALU4,Conductividad(FREQSALU4,FASEALU4RAD,0.019,0.015),"-o",color="orange")
plt.plot(FREQSALU3,Conductividad(FREQSALU3,FASEALU3RAD,0.019,0.013),"-o",color="red")
plt.plot(FREQSALU2,Conductividad(FREQSALU2,FASEALU2RAD,0.019,0.010),"-o",color="black")
plt.plot(FREQSALU1,Conductividad(FREQSALU1,FASEALU1RAD,0.019,0.008),"-o",color="purple")


FASEALU5RAD2 = np.unwrap(FASEALU5RAD) 

plt.figure()
plt.plot(FREQSALU5,np.tan(FASEALU5RAD2))

plt.figure()
plt.plot(FREQS,FaseRad)