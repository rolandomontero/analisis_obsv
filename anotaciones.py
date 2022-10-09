#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        anotaciones
# Purpose:     Analisa las observaciones de alumnos y clasifica como:
#
#
# Author:      Rolando Montero
#
# Created:     07-10-2022
# Copyright:   (c) Rolando Montero 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import argparse
from progress.bar import Bar
import os, time, random
from pysentimiento import create_analyzer
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="Mostrar información de depuración", action="store_true")
parser.add_argument("-f", "--file", help="Nombre de archivo a procesar")


args = parser.parse_args()

# Aquí procesamos lo que se tiene que hacer con cada argumento
if args.verbose:
    print ("depuración activada!!!")

if args.file:
    print("El nombre de archivo a procesar es: ", args.file)


    frases = pd.read_excel(io=args.file, usecols="B,E,G", sheet_name="Hoja1")
    frases.insert(2, 'NEG', '0', allow_duplicates=False)
    frases.insert(3, 'NEU', '0', allow_duplicates=False)
    frases.insert(4, 'POS', '0', allow_duplicates=False)
    analyzer = create_analyzer(task="sentiment", lang="es")
    bar1 = Bar('Analizando:', max=len(frases.index))
    os.system("cls")
    for i in frases.index:
        a=analyzer.predict(frases["Anotación"][i])
        frases["POS"][i]=(a.probas['POS']>0.80)*1
        frases["NEU"][i]=(a.probas['NEU']>0.80)*1
        frases["NEG"][i]=(a.probas['NEG']>0.80)*1
        if(i==1):
            print("El nombre de archivo a procesar es: ", args.file)
            os.system("cls")

        bar1.next()

    bar1.finish()
    print(frases)
    print('Se guarda el análisis como  analisis_'+ args.file)
    frases.to_excel('analisis_'+ args.file)


