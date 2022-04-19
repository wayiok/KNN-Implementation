import pandas as pd
import numpy as np


from sklearn.preprocessing import MinMaxScaler

# Importamos los modelos
from pyod.models.abod import ABOD
from pyod.models.cblof import CBLOF
from pyod.models.feature_bagging import FeatureBagging
from pyod.models.hbos import HBOS
from pyod.models.iforest import IForest
from pyod.models.knn import KNN
from pyod.models.lof import LOF
from scipy import stats

import matplotlib.pyplot as plt
import matplotlib
import scipy.stats as stats
import os

Valor1 = 'VALOR_HORA'
Valor2 = 'VALOR_DURACION'

files = len(os.listdir('Ataques/temp/logs')) 

for f in os.listdir('Ataques/temp/first_outliers/'):
    os.remove(os.path.join('Ataques/temp/first_outliers/', f))

#Por cada archivo csv de 5000 logs

for number in range(files) :
    
    df = pd.read_csv("Ataques/temp/logs/logs_" + str(number) + ".csv")
    
    print(df[['FECHA_Y_HORA','DURACION']])

    df['VALOR_HORA'] = pd.to_timedelta(df.HORA_1).dt.total_seconds()
    df['VALOR_DURACION'] = df['DURACION']

    df.plot.scatter(Valor1,Valor2)
    scaler = MinMaxScaler(feature_range=(0, 1))
    df[[Valor1,Valor2]] = scaler.fit_transform(df[[Valor1,Valor2]])

    X1 = df[Valor1].values.reshape(-1,1)
    X2 = df[Valor2].values.reshape(-1,1)

    X = np.concatenate((X1,X2),axis=1)
    random_state = np.random.RandomState(42)
    outliers_fraction = 0.05
    # Definimos los calificadores a utilizar
    classifiers = {
            'K Nearest Neighbors (KNN)': KNN(contamination=outliers_fraction)
    }

    xx , yy = np.meshgrid(np.linspace(0,1 , 200), np.linspace(0, 1, 200))

    for i, (clf_name, clf) in enumerate(classifiers.items()):
        clf.fit(X)
        # predecir la puntuacion de anomalia sin procesar
        scores_pred = clf.decision_function(X) * -1
            
        # prediccion de un valor atipico o inlier de una categoria de puntos de datos
        y_pred = clf.predict(X)
        n_inliers = len(y_pred) - np.count_nonzero(y_pred)
        n_outliers = np.count_nonzero(y_pred == 1)
        plt.figure(figsize=(10, 10))
        #print(y_pred)

        # copia del dataframe
        dfx = df
        dfx['outlier'] = y_pred.tolist()
        
        # Inlier
        IX1 =  np.array(dfx[Valor1][dfx['outlier'] == 0]).reshape(-1,1)
        IX2 =  np.array(dfx[Valor2][dfx['outlier'] == 0]).reshape(-1,1)
        
        # Outlier
        OX1 =  dfx[Valor1][dfx['outlier'] == 1].values.reshape(-1,1)
        OX2 =  dfx[Valor2][dfx['outlier'] == 1].values.reshape(-1,1)
             
        print('OUTLIERS : ',n_outliers,'INLIERS : ',n_inliers, clf_name)
            
        # valor del umbral para considerar un punto de datos inlier o outlier
        threshold = stats.scoreatpercentile(scores_pred,100 * outliers_fraction)
            
        # La funcion de decision calcula la puntuac1ion bruta de anomalia para cada punto.
        Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()]) * -1
        Z = Z.reshape(xx.shape)
        
        # Grafico
        plt.contourf(xx, yy, Z, levels=np.linspace(Z.min(), threshold, 7),cmap=plt.cm.Blues_r)
        a = plt.contour(xx, yy, Z, levels=[threshold],linewidths=2, colors='red')
        plt.contourf(xx, yy, Z, levels=[threshold, Z.max()],colors='orange')
        b = plt.scatter(IX1,IX2, c='white',s=20, edgecolor='k')
        c = plt.scatter(OX1,OX2, c='black',s=20, edgecolor='k')
        plt.axis('tight')  
        
        plt.legend(
            [a.collections[0], b,c],
            ['Funcion de Decision Aprendida', 'Logs Normales','Logs con Anomalias'],
            prop=matplotlib.font_manager.FontProperties(size=10),
            loc=2)
          
        plt.xlim((0, 1))
        plt.ylim((0, 1))
        plt.title(clf_name)
        
    #plt.show()    

    print(df)  
    print(df[[Valor1,Valor2]])

    # Sobreescribimos los archivos analizadas y generamos nuevos con las anomalia


    df.to_csv("Ataques/temp/logs/logs_"+ str(number) + ".csv",index=False)  
    dfo = df[df['outlier'] == 1]
    dfo.to_csv("Ataques/temp/first_outliers/fout_" + str(number) +".csv",index=False)
    print('ARCHIVO CREADO   ---> ' +'Ataques/temp/first_outliers/fout_' + str(number) + '.csv' )
