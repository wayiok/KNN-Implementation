import pandas as pd
from io import StringIO 
import csv 
import matplotlib
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn import preprocessing
import numpy as np
import os

#Leemos elarchivo CSV y lo usamos como objeto

logs = pd.read_csv('Ataques/temp/logsAtaque.csv')
del logs['BDD']
del logs['IP']
del logs['FECHA_1']
del logs['PID']
print(logs.head())
logs['FECHA_Y_HORA'] = pd.to_datetime(logs.FECHA_Y_HORA)


##Dividir el archivo de logs en set mas pequenios

with open('Ataques/temp/logsAtaque.csv', 'r') as f:
    csvfile = f.readlines()

linesPerFile = 100
filename = 0

## Eliminar y crear archivos

for f in os.listdir('Ataques/temp/logs/'):
    os.remove(os.path.join('Ataques/temp/logs/', f))


for i in range(0,len(csvfile),linesPerFile):
    with open('Ataques/temp/logs/logs_' + str(filename) + '.csv', 'w+') as f:
        if filename >= 1: 
            f.write(csvfile[0]) 
        f.writelines(csvfile[i:i+linesPerFile])
    filename += 1

print('ARCHIVO CREADO ---> ' +'Ataques/temp/logs/logs_' + str(filename-1) + '.csv' )
print('-------------------------------------------------------------------------')

