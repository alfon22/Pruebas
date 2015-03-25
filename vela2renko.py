# -*- coding: utf-8 -*-
"""
Created on Sun Feb  1 19:26:00 2015

@author: alf
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick_ohlc
import datetime



ladrillo = 2        # tamaño del ladrillo renko, sera un parametro o fijado en codigo
cierre_ladrillo = 0     #valor de cierre del último ladrillo colocado
                        # o el valor de apertura del primero
sentido = 0         # sentido del último ladrillo 0 baja 1 sube
tamaño_giro = ladrillo * 1  #valor necesario para que cambie de sentido
acumulado_mecha = 0     #arrastra el tamaño de la vela en sentido contrario



def calculaLadrillo(x):
#funcion para calcular si es necesario añadir ladrillos renco por cada
#vela, y en caso afirmativos, cuantos?, en que sentido?
    global cierre_ladrillo
    global ladrillo
    dif = x.iloc[0] - cierre_ladrillo
    if np.abs(dif) > ladrillo:
        num_lad = dif//ladrillo
        poneLadrillo(num_lad)
            
    
def poneLadrillo(n):
    global cierre_ladrillo
    global df_v
    while np.abs(n) > 0:
        if n > 0:
            apertura = cierre_ladrillo
            cierre = cierre_ladrillo + ladrillo            
            alto = cierre
            bajo = cierre_ladrillo
            cierre_ladrillo = cierre
            n = n - 1
        else:
            apertura = cierre_ladrillo
            cierre = cierre_ladrillo - ladrillo
            alto = cierre_ladrillo
            bajo = cierre
            cierre_ladrillo = cierre
            n = n + 1
        dia = 700000 + len(df_v)+1        
        df_v.loc[len(df_v)+1] = [dia ,apertura,alto,bajo,cierre]
        
    
#carga el fichero con los datos de velas de un indicador
#inicializa un dataframe en blanco para poder agregar ladrillos renko
df_o = pd.read_csv('/home/alf/Pruebas/GOOG-TLV_INDX_S19.csv',parse_dates='Date',index_col='Date')
df_v = pd.DataFrame(columns=['Date','Open','High','Low','Close'])


#Establezco el ladrillo al 5% de la diferencia máx de los cierres
ladrillo = np.round((df_o['Close'].max()-df_o['Close'].min())/100*5)

#invierte el dataframe para poder calcular los ladrillos por el principio
df_o.sort_index(axis=0,ascending=True,inplace = True)

cierre_ladrillo = df_o['Open'][0] #Inicializa la variable

# Recorro el dataFream origen y cargo los datos en el dataFrame vela
df_o.apply(calculaLadrillo ,axis=1)

# Formatea el data frame de entrada para poder representarlo
df_o.drop('Volume',inplace=True,axis=1)
df_o.reset_index(inplace=True,drop=True)
df_o['Date'] = df_o.index + 700000
columnas = ['Date','Open', 'High', 'Low', 'Close']
df_o = df_o[columnas]

# Invierto el data frame para empezar por las fechas más antiguas
df_o.sort_index(axis=0,ascending=True,inplace = True)

# convierte de dataframe a tuplas
tuples = [tuple(x) for x in df_v.values]
tuplesB = [tuple(x) for x in df_o.values]

fig = plt.figure(figsize=[12,10],facecolor='#07000d',edgecolor='g')

ax = plt.subplot2grid((4,4),(0,0), rowspan=2, colspan=4,axisbg='#07000d')
candlestick_ohlc(ax, tuples, width=0.5,colorup='#9eff15', colordown='#ff1717')
# Hace visible las regillas en ambos graficos
ax.grid(True,color='w')
ax.axes.yaxis.set_ticklabels([])
# Cambia el color del marco del grafico
ax.spines['bottom'].set_color('#5998ff')
ax.spines['top'].set_color('#5998ff')
ax.spines['left'].set_color('#5998ff')
ax.spines['right'].set_color('#5998ff')
ax.tick_params(axis='x',color='w')
# Pone etiquetas blancas en el eje y de color blanco
ax.yaxis.label.set_color='w'
ax.autoscale_view()


ax1 = plt.subplot2grid((4,4),(2,0), rowspan=2, colspan=4,axisbg='#07000d')
candlestick_ohlc(ax1, tuplesB, width=0.6,colorup='#9eff15', colordown='#ff1717')
# Hace visible las regillas en ambos graficos
ax1.grid(True,color='w')
ax1.axes.yaxis.set_ticklabels([])
# Cambia el color del marco del grafico
ax1.spines['bottom'].set_color('#5998ff')
ax1.spines['top'].set_color('#5998ff')
ax1.spines['left'].set_color('#5998ff')
ax1.spines['right'].set_color('#5998ff')
ax1.tick_params(axis='x',color='w')
# Pone etiquetas blancas en el eje y de color blanco
ax1.yaxis.label.set_color='w'
ax1.autoscale_view()



plt.ylabel('Velas')
plt.xlabel('Tiempo')
plt.suptitle('Valores de Google')
plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
#plt.setp(plt.gca().get_yticklabels())
plt.savefig('/home/alf/Pruebas/velas.png',dpi=450,papertype='a0')
plt.show()
