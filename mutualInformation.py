#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import csv
import os
import time
import re
import sys
import math
import shutil

def filefromCorpus(corpusOriginal, tipo = ['txt']):
    
    salida = list();
    ruta = corpusOriginal;
    for root,dirs,files in os.walk(ruta):
    
        for file in [f for f in files]:
            #print(os.path.join(root, file))

            ruta = str(os.path.join(root, file));
            if ruta.split(".")[-1] in tipo:
                salida.append(os.path.join(root, file));
    return salida;

def classesFromCorpus(archivos):
    
    users = list()
    path = archivos;
    for base, dirs, files in os.walk(path):

        users = dirs;
        break;    
    return users;

def convert2Dict(a):
    
    res = dict();
    for element in a:
        res[element] = dict();
    return res;    

def main(argv):
    
    
    corpus = argv[1];
    
    
    
    archivoSalidaRasgo = "mutualInformation";
    if len(argv) > 2:
        archivoSalidaRasgo = argv[2].split(".")[0];
        
        
    rasgos = classesFromCorpus(corpus);    
    regexp = "\\#+[\\w_]+[\\w\\'_\\-]*[\\w_]+|@[\\w_]+|[a-zA-Z'ÁÉÍÓÚáéíóúñÑüÜ]+-*[a-zA-Z'ÁÉÍÓÚáéíóúñÑüÜ]+|[a-zA-Z'ÁÉÍÓÚáéíóúñÑüÜ]+|[<>]?[:;=8][\\-o\\*\\']?[\\)\\]\\(\\[oOdDpP/\\:\\}\\{@\\|\\\\3\\*]|[\\)\\]\\(\\[oOdDpP/\\:\\}\\{@\\|\\\\3\\*][\\-o\\*\\']?[:;=8][<>]?|[.]+|[/,$?:;!()&%#=+{}*~.]+"
    patter = re.compile(regexp);    
    
    for rasgo in rasgos:
        corpusImagenes = corpus + "/" + rasgo;
        archivoSalida = archivoSalidaRasgo + "_" + rasgo + ".csv";
        clases = convert2Dict(classesFromCorpus(corpusImagenes));
        
        print(str(rasgo));
        
            
        archivos = filefromCorpus(corpusImagenes);
        
        probabilidad_Clase = dict();
        for archivo in archivos:
            if not probabilidad_Clase.has_key(archivo.split("/")[-2]):
                probabilidad_Clase[archivo.split("/")[-2]] = 0;
            probabilidad_Clase[archivo.split("/")[-2]] += 1;
            
        for archivo in archivos:
            leer = open(archivo, "r");
            clase = archivo.split("/")[-2]; 
            conjunto = set();
            for line in leer:
                palabras = patter.findall(line);
                palabrasMinusculas = list();
                for palabra in palabras:
                    palabrasMinusculas.append(palabra.lower());
                palabras = palabrasMinusculas;    
                conjunto |= set(palabras);
            leer.close();    
            
            for palabra in conjunto:
                if not clases[clase].has_key(palabra):
                    clases[clase][palabra] = 0;
                clases[clase][palabra] += 1;
                
            
        
        
        writer = csv.writer(open(archivoSalida, "w"), delimiter=',');
        for clase in clases.keys():
            writer.writerow(["Class", clase]);
            writer.writerow(["Palabra", "Mutual information"]);
            for palabra in clases[clase].keys():
                total_palabra = 0;
                for claseCount in clases.keys():
                    if clases[claseCount].has_key(palabra):
                        total_palabra += clases[claseCount][palabra];
                    
                p_conjunta = clases[clase][palabra] / float(len(archivos));
                p_palabra = total_palabra / float(len(archivos));
                p_clase = probabilidad_Clase[clase] / float(len(archivos));
                
                #mutual_information = p_conjunta * math.log( p_conjunta / (p_palabra*p_clase), 2);
                mutual_information =  math.log( p_conjunta / (p_palabra*p_clase), 2);
                writer.writerow([palabra, mutual_information]);
                
                
if __name__ == "__main__":
    main(sys.argv);
