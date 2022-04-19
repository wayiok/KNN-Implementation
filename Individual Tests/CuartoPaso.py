import pandas as pd 
import os
import requests

files = len(os.listdir('Ataques/temp/first_outliers'))
querys = []
counter = 0

 # Abrimos el archivo de texto de querys y los cargamos a la lista
with open('Ataques/temp/querys/querys.txt', 'r') as filehandle:
    filecontents = filehandle.readlines()
    for line in filecontents:
        current_place = line[:-1]
        querys.append(current_place)
    

files = len(os.listdir('Ataques/temp/first_outliers')) -1


def obtenerQuery(idQuery):
        sqlStatement = ''
        query = ''
        for line in querys:
            if ' -> ' in line:
                id = line.split(' -> ')[0]
                if id == idQuery:
                    sqlStatement = line.split(' -> ')[1]             
                            
        return(sqlStatement)


def analizarInjection(logId):
    global counter
    query = obtenerQuery(logId)
    if '1=1' and 'union' in query:
        print('-----ALERTA-----')
        print('LOG-ID = ' + logId)
        print('INYECCIÓN TIPO 1 DETECTADA: Operador Union')
        print(query)
        counter += 1
    else:   
        if '1=1' in query:
            print('-----ALERTA-----')
            print('LOG-ID = ' + logId)
            print('INYECCIÓN TIPO 2 DETECTADA: Tautologia')
            print(query)
            counter += 1
        else:
                if ';' in query:
                    if 'exec(' in query:
                        print('-----ALERTA-----')
                        print('LOG_ID = ' + logId)
                        print('INYECCIÓN TIPO 6 DETECTADA: Codificacion Alternativa')
                        print(query)
                        counter += 1
                    elif 'waitfor delay' in query:
                        print('-----ALERTA-----')
                        print('LOG_ID = ' + logId)
                        print('INYECCIÓN TIPO 5 DETECTADA: Inferencia Booleaano')
                        print(query)
                        counter += 1  
                    elif 'CREATE' and ';drop table' in query:
                        print('-----ALERTA-----')
                        print('LOG_ID = ' + logId)
                        print('INYECCIÓN TIPO 7 DETECTADA: Procedimiento Almacenado')
                        print(query)
                        counter += 1   
                    elif 'SLEEP' in query:
                        print('-----ALERTA-----')
                        print('LOG_ID = ' + logId)
                        print('INYECCIÓN TIPO 3 DETECTADA: Inferencia - Basado en el Tiempo')
                        print(query)    
                        counter += 1
                    else:   
                        print('-----ALERTA-----')
                        print('LOG_ID = ' + logId)
                        print('INYECCIÓN TIPO 4 DETECTADA: Piggy Backed')
                        print(query)
                        counter += 1
           

# def postearAnomalia(base,usuario,ip,pid,fecha2,ataque,tipo):
#     r = requests.post('http://localhost:3000/api/logs', data ={'nombre_base': base,
#                                                                 'nombre_usuario': usuario,
#                                                                 'ip_log': ip,
#                                                                 'pid': pid,
#                                                                  'time_stamp_log': fecha2,
#                                                                 'ataque': ataque,
#                                                                 'tipo_ataque': tipo}) 
  

for number in range(files+1):

    firstOutliers =  pd.read_csv('Ataques/temp/first_outliers/fout_' + str(number) + '.csv')
    outliersLogs = firstOutliers['LOG_ID']

    for i in outliersLogs:
         analizarInjection(str(i))
    #     postearAnomalia('pruebaf','washios','127.0.0.3','12121','Thu, 18 Jun 2021 14:07:38 UTC +00:00',False,'')

print('------------------------------------------')
print('NUMERO DE INYECCIONES DETECTADAS:   ' + str(counter))
print('------------------------------------------')
