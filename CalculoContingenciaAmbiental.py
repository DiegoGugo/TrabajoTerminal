import pandas as pd
import numpy as np

#create class
class ContingenciaAmbiental:
    def __init__(self, data):
        self.data = data
        self.max_values = []
        self.O3 = []
        self.PM10 = []
        self.PM2_5 = []
        self.FaseI = []
        self.FaseII = []
        self.FaseCombinada = []
    
    def split_24hours (self):
        #Separar los datos en 24 elementos y almacenarlos en listas independientes
        for i in range(0, len(self.data), 24):
            self.max_values.append(self.data['Max_Value'].iloc[i:i+24].tolist())
            self.O3.append(self.data['O3_IMECA'].iloc[i:i+24].tolist())
            self.PM10.append(self.data['PM10_IMECA'].iloc[i:i+24].tolist())
            self.PM2_5.append(self.data['PM2.5_IMECA'].iloc[i:i+24].tolist())
        #print(self.max_values)

    def CalcularFaseContingencia(self):
        n = len(self.O3)
        self.FaseI = np.zeros(n)
        self.FaseII = np.zeros(n)
        self.FaseCombinada = np.zeros(n)

        for i, (O3_day, PM10_day, PM25_day) in enumerate(zip(self.O3, self.PM10, self.PM2_5)):
            
            O3_max = max(O3_day)
            PM10_max = max(PM10_day)
            PM10_max = max(PM25_day)

            #Fase Combinada (FC)
            if (O3_max > 150 and (PM10_max > 140 or PM10_max > 140)) or (O3_max > 140 and (PM10_max > 150 or PM10_max > 150)):
                self.FaseCombinada[i] = 1
            #Fase I (FI)
            elif (O3_max > 150) or (PM10_max > 150 or PM10_max > 150):
                self.FaseI[i] = 1
            #Fase II (FII)
            elif (O3_max > 200) or (PM10_max > 200 or PM10_max > 200):                
                self.FaseII[i] = 1 
    
    def CrearEstructura(self):

        date = pd.date_range(start='2010-01-01', end='2023-12-31', freq='D')

        fases_data = pd.DataFrame({'Fecha':date,
                                   'Fase I':self.FaseI,
                                   'Fase II':self.FaseII,
                                   'Fase Combinada':self.FaseCombinada
                                   })

        hour_name = []
        for hour in range(1, 25):
            hour_name.append(f'Hora {hour}')
        hours_data = pd.DataFrame(data = self.max_values, columns = hour_name)

        # unificar datasets
        new_data = pd.concat([fases_data, hours_data], axis = 1)

        return new_data

data = pd.read_csv('Contaminantes_2010_2023_prep.csv') 
CA = ContingenciaAmbiental(data)
CA.split_24hours()
CA.CalcularFaseContingencia()
new_data = CA.CrearEstructura()

new_data.to_csv('ContingenciasAmbientales_2010_2023.csv', index = False, encoding = 'utf-8')

print(new_data['Fase I'].sum())
print(new_data['Fase II'].sum())
print(new_data['Fase Combinada'].sum())



