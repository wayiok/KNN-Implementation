import pandas as pd
from io import StringIO 
import csv 

f = open('LogsPostgresql/LOGS_EJEMPLO.log')

userAtribute = 'Tstamp:'
id = 0
logsOriginales = []
logsLimpios = ['LOG_ID,BDD,USUARIO,IP,PID,FECHA_1,HORA_1,FECHA_Y_HORA,COMANDO,DURACION,RESULTADO']
logsQuery = []
totalLineasBorradas = 0;
numeroLogsOriginales = 0;
numeroLogsLimpios = 0;
queryLog= ''
duracionSelect = "0.0";
resultadoConsulta = "OK";
sentencia= '';
log=''
query = ''

#Recoleccion de Datos
lineas = f.readlines()

for linea in lineas:
	logsOriginales.append(linea)
	if userAtribute in linea:
		queryLog = ''
		#id asignado
		id = id +1
		#Atributos sacados del log
		temp = linea.split('\t')
		databaseName = linea.split(' ')[1]
		userName = linea.split(' ')[2]
		ip = linea.split(' ')[3]
		pid = linea.split(' ')[4]
		date = linea.split(' ')[5]
		hour = linea.split(' ')[6]
		date2 = linea.split(' ')[8]
		hour2 =  linea.split(' ')[9]
		cmdType = linea.split(' ')[11]

		#Atributos extras por tipo de log 

		if cmdType[8:] == "SELECT" or cmdType[8:] == "INSERT" or cmdType[8:] == "SET":
			if 'ERROR' in linea:
				resultadoConsulta = "ERROR"
			else:	
				if 'SENTENCIA' in linea:
					duracionSelect = "0.0"
				else:
					duracionSelect = linea.split(' ')[15]

		if cmdType[8:] == "idle":
			if 'ERROR' in linea:
					resultadoConsulta = "ERROR"
	
		if 'sentencia' in linea:
			query = linea.split('sentencia:')[1]
			#print(query)	
			sentencia = query	
        

        #Estructura del nuevo log
		log = str(id) + ',' + databaseName[4:] + ',' + userName[5:] + ',' + ip[7:] + ',' + pid[4:] + ',' + date[7:] + ',' + hour + ',' + date2[13:] + ' ' + hour2 + ',' + cmdType[8:] + ',' + duracionSelect + ',' + resultadoConsulta 
		query = str(id) + ' -> ' + sentencia
		duracionSelect = "0.0"
		resultadoConsulta = "OK"
		sentencia = ''
		print(log)
		logsLimpios.append(log)
	else:

		#Extraccion de la cadena de texto del query
		query = linea

	logsQuery.append(query)
	

numeroLogsOriginales = len(logsOriginales)
numeroLogsLimpios = len(logsLimpios)
totalLineasBorradas = numeroLogsOriginales - numeroLogsLimpios

print("LINEAS ARCHIVO ORIGINAL: " , numeroLogsOriginales,"LOGS OBTENIDOS:", numeroLogsLimpios, "LINEAS DESECHADAS:", totalLineasBorradas)

#Genereamos un archivo CSV con los logs limpios y el query en un archivo de texto 

with open('Ataques/temp/logsAtaque.csv', 'w') as csvfile:
    		filewriter = csv.writer(csvfile, delimiter=',',
                            		quotechar='|', quoting=csv.QUOTE_MINIMAL)
    		for log in logsLimpios:
    			filewriter.writerow(log.split(','))

with open('Ataques/temp/querys/querys.txt', 'w') as filehandle:
    filehandle.writelines("%s\n" % place for place in logsQuery)

print('-------------------------------------------------------------------------')
