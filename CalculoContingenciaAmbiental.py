import pandas as pd
import numpy as np

#create class
class ContingenciaAmbiental:
    def __init__(self, data):
        self.data = data
        self.MaxCompound = data['MAX_Compound'].values
        self.MaxValue = data['Max_Value'].values
        self.FaseI = []
        self.FaseII = []
        self.FaseCombinada = []
    
    def CalcularFaseContingencia(self):
        if self.MaxCompound == ''
