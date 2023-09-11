import numpy as np
import pandas as pd
import os

class IMECA_Convertion:
    def __init__ (self, data_path):
        # read data
        self.data_path = data_path
        data = pd.read_csv(self.data_path, header = 10, encoding = 'utf_8')
        # Select only the compunds needed and all NaN values will set to zero
        self.data = data[data['id_parameter'].isin(['O3','NO2','CO','SO2','PM10','PM2.5'])].fillna(0)
        self.n = data.shape[0]       

    def unit_conversion(self):
        print('Unit Conversion Process Started')
        
        def convert_units(row):
            if row['id_parameter'] in ['O3', 'NO2', 'CO', 'SO2'] and row['unit'] != 15:
                row['value'] /= 1000
                row['unit'] = 15
            return row
        
        self.data = self.data.apply(convert_units, axis=1)
    
    print('Unit Conversion Process Completed')

    def IMECA_conversion(self):
        print('IMECA Calculation Process Started')
        
        def generateIMECA(row):
            match row['id_parameter']:
                case 'O3': #Ozono
                    return round(row['value'] * (100/0.11), 2)
                case 'NO2': #Dioxido de nitrogeno
                    return round(row['value'] * (100/0.21), 2)
                case 'CO': #Monoxido de carbono
                    return round(row['value'] * (100/11), 2)
                case 'SO2': #Dioxido de azufre
                    return round(row['value'] * (100/0.13), 2)
                case 'PM10': 
                    if row['value'] >= 0 and row['value'] <= 120:
                        return round(row['value'] * (5/6), 2)
                    elif row['value'] >= 121 and row['value'] <= 320:
                        return round(40 + (row['value'] * 0.5), 2)
                    elif row['value'] > 320:
                        return round(row['value'] * (5/8), 2)
                case 'PM2.5':
                    if row['value'] >= 0 and row['value'] <= 15.4:
                        return round(row['value'] * (50/15.4), 2)
                    elif row['value'] >= 15.5 and row['value'] <= 40.4:
                        return round(20.5 + (row['value'] * (49/24.9)), 2)
                    elif row['value'] >= 40.5 and row['value'] <= 65.4:
                        return round(21.3 + (row['value'] * (49/24.9)), 2)
                    elif row['value'] >= 65.5 and row['value'] <= 150.4:
                        return round(113.2 + (row['value'] * (49/84.9)), 2)
                    elif row['value'] > 150.4:
                        return round(row['value'] * (201/150.5), 2)
        
        self.data['IMECA'] = self.data.apply(generateIMECA, axis = 1)

        print('IMECA Calculation Process Completed')
    
    def saveFile (self):
        name = './../Datos/CalidadAire/ConvertedData/' + self.data_path.split('/')[-1].replace('.CSV', '') + '_IMECA.csv'
        self.data.to_csv(name, index = False, encoding = 'utf-8')
        print(f'File exported at {self.data_path}')
    
# Repeat the process for each document from 2020 to 2023
for year in range(2010, 2023 + 1):
    path = f'./../Datos/CalidadAire/contaminantes_{year}.CSV'
    IMECA = IMECA_Convertion(path)
    IMECA.unit_conversion()
    IMECA.IMECA_conversion()
    IMECA.saveFile()
# import datetime

# # Definir la fecha de inicio y la fecha de fin
# fecha_inicio = datetime.datetime(2010, 1, 1)
# fecha_fin = datetime.datetime(2010, 12, 31)

# # Crear una lista para almacenar las fechas
# fechas_texto = []

# # Iterar a través de las fechas desde la fecha de inicio hasta la fecha de fin
# while fecha_inicio <= fecha_fin:
#     fecha_texto = fecha_inicio.strftime('%d-%m-%Y %H')
#     for _ in range(26):
#         fechas_texto.append(fecha_texto)
    
#     # Agregar una hora a la fecha actual
#     fecha_inicio += datetime.timedelta(hours=1)
# print(fechas_texto)
# print(len(fechas_texto)*5)

