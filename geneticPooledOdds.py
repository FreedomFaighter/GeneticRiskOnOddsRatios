#!/usr/bin/python
#python geneticPooledOdds.py {ID} {File Name} {Age} {Gender} {Excel spreadsheet}
import ensemblRESTApi
import pandas as pd
import numpy as np
#import random
from datetime import datetime
import sys
import csv
#excel sheet with info on first tab/sheet
excelSheetName = str(sys.argv[5])
fileName = str(sys.argv[2])
age = int(sys.argv[3])
gender = str(sys.argv[4])
idAtInvoke=sys.argv[1]
SNPdf = pd.read_excel(excelSheetName, sheetname = 'Master_SNP_List', parse_cols = 'A,C,E,M,N')
SNPdf['DBName'] = SNPdf['DBName'].astype(str)
SNPdf['DBName'] = SNPdf.DBName.str.strip(' ')
d = SNPdf.columns
d = ['rsid', 'Genotype', 'Disease', 'Reference', 'OR']
SNPdf.columns = d
SNPdf['rsid'] = SNPdf['rsid'].astype(str)
SNPdf.rsid = SNPdf.rsid.str.strip(' ').str.strip('\n')
SNPdf.Genotype = SNPdf.Genotype.astype(str)
SNPdf.Genotype = SNPdf.Genotype.str.strip(' ')
SNPdf['OR'] = SNPdf['OR'].astype(float)
series1 = pd.Series([0 for _ in range(len(SNPdf['Reference']))], index = SNPdf.index)
for i in range(len(series1)):
    if SNPdf['Reference'].iloc[i] == "Yes":
        series1.iloc[i] = 1
    else:
        series1.iloc[i] = 0
SNPdf.Reference = series1.astype(int)

prevalence = pd.read_excel(excelSheetName, sheetname = 'Sheet1', parse_cols = 'A,C,D,E,G')
prevalence.head()
prevalence
d = prevalence.columns
d = d.str.strip(' ')
prevalence.columns = d
prevalence.Disease = prevalence.Disease.astype(str)
prevalence.Disease = prevalence.Disease.str.strip(' ')
prevalence.Gender = prevalence.Gender.str.strip(' ')
prevalence.Prevalence = prevalence.Prevalence.astype(float)
prevalence.Age = prevalence.Age.astype(str)
prevalence = prevalence[prevalence['SampleSize'] != 'NaN']
series1 = pd.Series([0 for _ in range(len(prevalence['Gender']))], index = prevalence.index)
series2 = pd.Series([0 for _ in range(len(prevalence['Gender']))], index = prevalence.index)
for i in range(len(prevalence['Gender'])):
    if prevalence['Gender'].iloc[i] == "Both":
        series1.iloc[i] = 1
        series2.iloc[i] = 1
    if prevalence['Gender'].iloc[i] == "Male":
        series1.iloc[i] = 1
        series2.iloc[i] = 0
    if prevalence['Gender'].iloc[i] == "Female":
        series1.iloc[i] = 0
        series2.iloc[i] = 1
prevalence["Male"] = series1.astype(int)
prevalence["Female"] = series2.astype(int)
series1 = pd.Series([0 for _ in range(len(prevalence['Gender']))], index = prevalence.index)
series2 = pd.Series([0 for _ in range(len(prevalence['Gender']))], index = prevalence.index)
for i in range(len(prevalence['Age'])):
    def parseAge(a):
        b = a
        if '-' in a:
            b = a.split('-')
            if len(b) == 2:
                series1.iloc[i] = b[0]
                series2.iloc[i] = b[1]
        else:    
            b = b.replace('+', '')
            if b == 'nan':
                series1.iloc[i] = 0
            else:
                series1.iloc[i] = int(b)
            series2.iloc[i] = 200
                
    parseAge(prevalence['Age'].iloc[i])
prevalence['MinAge'] = series1.astype(int)
prevalence['MaxAge'] = series2.astype(int)

# Reading source file
data = {}
with open(fileName) as file:
    for line in file:
        (key, val) = line.split(":")
        key = key.replace('"', '')
        key = key.replace(' ', '')
        val = val.replace('"', '')
        val = val.replace(' ', '')
        val = val.replace('\n', '')
        val = val.replace('\r', '')
        # Getting rid of empty reads
        if val != '__' and val != '--' and key != 'id':
            data[key] = val

def PooledOddsForDisease(disease, PopulationProbability):
#    print(disease)
    subSNPdf = SNPdf[SNPdf['Disease'] == disease]
    uniq = subSNPdf['rsid'].unique()
    results = ensemblRESTApi.getGenotypeProbabilities(uniq)
    SNPsPersonHas = list(set(data.keys()) & set(uniq))
    DictionaryOfSNPAndGenotype = {}
    for i in SNPsPersonHas:
        DictionaryOfSNPAndGenotype[i] = data[i]
    k = pd.DataFrame(list(data.items()), index = data.keys())
    del k[0]
    k.columns = [fileName]
    def findConditionalProbabilities(popProb, OddsAndPGn):
        if disease == "Cognitive_Function":
            print(OddsAndPGn)
        def secant(f, p0, p1, TOL = 0.001, N = 2000):
            i = 2
            q0 = f(p0)
            q1 = f(p1)
            while i <= N:
                p = p1 - q1 * (p1 - p0) / (q1 - q0)
                if abs(p - p1) < TOL:
                    return p
                i += 1
                p0 = p1
                q0 = q1
                p1 = p
                q1 = f(p)
        def findp0p1(d):
            IsNegative = None
            WasNegative = None
            p0 = 0.0 #None
            p1 = 0.0 #None
            for i in range(len(d['Initial Candidates'])):
                if d['Initial Candidates'].iloc[i] < 0:
                    IsNegative = True
                    if WasNegative == False:
                        p1 = d['Initial Candidates'].index[i]
                        return p0, p1
                    if p0 is None:
                        p0 = d['Initial Candidates'].index[i]
                    if d['Initial Candidates'].iloc[i] > p0:
                        p0 = d['Initial Candidates'].index[i]
                elif d['Initial Candidates'].iloc[i] > 0:
                    IsNegative = False
                    if WasNegative == True:
                        p1 = d['Initial Candidates'].index[i]
                        return p0, p1
                    if p0 is None:
                        p0 = d['Initial Candidates'].index[i]
                    if d['Initial Candidates'].iloc[i] < p0:
                        p0 = d['Initial Candidates'].index[i]
                if IsNegative == True:
                    WasNegative = True
                else:
                    WasNegative = False
            return p0, p1
        def computePDG_1(x):
            result = -popProb
            result += x * OddsAndPGn['PGn'].iloc[0]
            for i in range(1,len(OddsAndPGn)):
                result += OddsAndPGn['OR'].iloc[i] * x / (OddsAndPGn['OR'].iloc[i] * x - x + 1) * OddsAndPGn['PGn'].iloc[i]
            return result
        df = pd.DataFrame([], index = np.linspace(0.0001, 1, 100), columns = ["Initial Candidates"])
        for i in range(len(df)):
            p_0 = df.index[i]
            df["Initial Candidates"].iloc[i] = computePDG_1(p_0)
        p0, p1 = findp0p1(df)
        conditionalPDG_1 = secant(computePDG_1, p0, p1)
        if conditionalPDG_1 > 0:
            conditionalPDG_2 = OddsAndPGn['OR'].iloc[1] * conditionalPDG_1 / (OddsAndPGn['OR'].iloc[1] * conditionalPDG_1 - conditionalPDG_1 + 1)
            conditionalPDG_3 = OddsAndPGn['OR'].iloc[2] * conditionalPDG_1 / (OddsAndPGn['OR'].iloc[2] * conditionalPDG_1 - conditionalPDG_1 + 1)
        else:
            conditionalPDG_1 = 0
            conditionalPDG_2 = 0
            conditionalPDG_3 = 0
        return [conditionalPDG_1, conditionalPDG_2, conditionalPDG_3]
    SNPDictionary = {}
    #startTime = datetime.now()
    for i in SNPsPersonHas:
        def matchString(index, ts):
            return (index == ts) | (index == ts[1] + ts[0])
        def stripPipe(t):
            temp = t.split('|')
            return temp[0] + temp[1]
        tempDF = subSNPdf[subSNPdf['rsid'] == i]
        OddsAndPDns = pd.DataFrame(list(tempDF['OR']), index = tempDF['Genotype'], columns = ['OR'])
        series = pd.Series([0 for _ in range(len(OddsAndPDns.index))], index = tempDF['Genotype'])
        for k, j in enumerate(results[i]['population_genotypes']):
            if 'ALL' in j['population']:
                tempString = stripPipe(j['genotype'])
                tempDF = SNPdf[(SNPdf['rsid'] == i) & (SNPdf['Genotype'] == tempString)]
                if len(tempDF) == 0:
                    tempDF = SNPdf[SNPdf['rsid'] == i]
                    tempDF = tempDF[tempDF['Genotype'] == tempString[1] + tempString[0]]
                if len(tempDF) == 1:
                    for o in range(len(OddsAndPDns)):
                        if matchString(OddsAndPDns.index[o], tempString):
                            series.iloc[o] = float(j['frequency'])

        if disease == "Stroke_All":
            print(series)
        OddsAndPDns['OR'] = OddsAndPDns['OR'].astype(float)
        OddsAndPDns['PGn'] = series.astype(float)
        OddsAndPDns = OddsAndPDns.sort_values(['OR'], ascending = [True])
        OddsAndPDns['OR'] = OddsAndPDns['OR'] / OddsAndPDns['OR'].iloc[0]
        OddsAndPDns['Conditional'] = pd.Series(findConditionalProbabilities(PopulationProbability, OddsAndPDns), index = OddsAndPDns.index)

        SNPDictionary[i] = OddsAndPDns
    #print(datetime.now() - startTime)
    denom = PopulationProbability / (1-PopulationProbability)
    for i in SNPDictionary.keys():
        product = 1
        adjustedOR = []
        for j in range(len(SNPDictionary[i]['Conditional'])):
            tmp = SNPDictionary[i]['Conditional'].iloc[j]
        #print(tmp / (1-tmp))
            adjustedOR.append((tmp / (1-tmp)) / denom)
            product *= ((tmp / (1-tmp)) / denom)
        SNPDictionary[i]['AdjustedOR'] = pd.Series(adjustedOR, index = SNPDictionary[i].index)
    pooledOdds = 1
    for i in DictionaryOfSNPAndGenotype.keys():
        if(len(SNPDictionary[i][SNPDictionary[i].index == DictionaryOfSNPAndGenotype[i]]['AdjustedOR']) == 1):
            pooledOdds *= SNPDictionary[i][SNPDictionary[i].index == DictionaryOfSNPAndGenotype[i]]['AdjustedOR'].iloc[0]
    return pooledOdds

diseasesList = prevalence['Disease'].unique()
outputDF = {}
for i, j in enumerate(diseasesList):
    if j == "Allergic_Rhinitis":
        outputDF[j] = PooledOddsForDisease(j, prevalence[prevalence['Disease'] == j]['Prevalence'].iloc[0])
    elif j == "Alzheimer_Disease":
        if age < 65:
            outputDF[j] = PooledOddsForDisease(j, prevalence[(prevalence['Disease'] == j) & (prevalence['Age'] == "65-69") & (prevalence['Gender'] == "Both")]['Prevalence'].iloc[0])
        elif age > 65 & age < 90:
            outputDF[j] = PooledOddsForDisease(j, prevalence[(prevalence['Disease'] == j) & (prevalence['MinAge'] <= age) & (prevalence['MaxAge'] >= age) & (prevalence['Gender'] == 'Both')]['Prevalence'].iloc[0])
        else:
            outputDF[j] = PooledOddsForDisease(j, prevalence[(prevalence['Disease'] == j) & (90 <= age) & (prevalence['Gender'] == 'Both')]['Prevalence'].iloc[0])
    elif j == "Celiac_disease":
        outputDF[j] = PooledOddsForDisease(j, prevalence[prevalence['Disease'] == j]['Prevalence'].iloc[0])
    # Cognitive_Function is in Disease_Genetics.xlsx but contains no OR to use for calculation
    #elif j == "Cognitive_Function":
    #    if age < 60:
    #        outputDF[j] = PooledOddsForDisease(j, prevalence[(prevalence['Disease'] == j) & (prevalence['MinAge'] == 60)]['Prevalence'].iloc[0])
    #    else:
    #        k = prevalence[(prevalence['Disease'] == j) & (prevalence['MinAge'] <= age) & (prevalence['MaxAge'] >= age)]['Prevalence'].iloc[0]
    #        print(j, k)
    #        outputDF[j] = PooledOddsForDisease(j, k)
    elif j == "Coronary_Artery_Disease":
        if age < 18:
            outputDF[j] = PooledOddsForDisease(j, prevalence[(prevalence['Disease'] == j) & (prevalence['Age'] == '18-44')]['Prevalence'].iloc[0])
        else:
            outputDF[j] = PooledOddsForDisease(j, prevalence[(prevalence['Disease'] == j) & (prevalence['MinAge'] <= age) & (prevalence['MaxAge'] >= age)]['Prevalence'].iloc[0])
    elif j == "Type_2_Diabetes_Mellitus":
        if age < 18:
            outputDF[j] = PooledOddsForDisease(j, prevalence[(prevalence['Disease'] == j) & (prevalence['Age'] == '18-44')]['Prevalence'].iloc[0])
        else:
            outputDF[j] = PooledOddsForDisease(j, prevalence[(prevalence['Disease'] == j) & (prevalence['MinAge'] <= age) & (prevalence['MaxAge'] >= age)]['Prevalence'].iloc[0])
    elif j == "Gout":
        outputDF[j] = PooledOddsForDisease(j, prevalence[(prevalence['Disease'] == j)]['Prevalence'].iloc[0])
    elif j == "Heart_Failure":
        if age < 18:
            outputDF[j] = PooledOddsForDisease(j, prevalence[(prevalence['Disease'] == j) & (prevalence['Age'] == '18-44')]['Prevalence'].iloc[0])
        else:
            outputDF[j] = PooledOddsForDisease(j, prevalence[(prevalence['Disease'] == j) & (prevalence['MinAge'] <= age) & (prevalence['MaxAge'] >= age)]['Prevalence'].iloc[0])
    # no odds ratios for the snps associated with Hyperhomocysteinemia
    #elif j == "Hyperhomocysteinemia":
    #    if age < 67:
    #        outputDF[j] = PooledOddsForDisease(j, prevalence[(prevalence['Disease'] == j) & (prevalence['Age'] == '67-74') & (prevalence['Gender'] == gender)]['Prevalence'].iloc[0])
    #    else:
    #       outputDF[j] = PooledOddsForDisease(j, prevalence[(prevalence['Disease'] == j) & (prevalence['MinAge'] <= age) & (prevalence['MaxAge'] >= age) & (prevalence['Gender'] == gender)]['Prevalence'].iloc[0])
    # no odds ratios associated with Hyperlipidemia
    #elif j == "Hyperlipidemia":
    #    outputDF[j] = PooledOddsForDisease(j, prevalence[(prevalence['Disease'] == j)]['Prevalence'].iloc[0])
    #elif j == "Low_HDL":
    #    if age < 20:
    #        outputDF[j] = PooledOddsForDisease(j, prevalence[(prevalence['Disease'] == j) & (prevalence['Age'] == '20-39') & (prevalence['Gender'] == gender)]['Prevalence'].iloc[0])
    #    else:
    #       outputDF[j] = outputDF[j] = PooledOddsForDisease(j, prevalence[(prevalence['Disease'] == j) & (prevalence['MinAge'] <= age) & (prevalence['MaxAge'] >= age) & (prevalence['Gender'] == gender)]['Prevalence'].iloc[0])
    #elif j == "Insomnia":
    #    outputDF[j] = PooledOddsForDisease(j, 0.299)
    elif j == "Major_Depressive_Disorder":
        if age < 18:
            outputDF[j] = PooledOddsForDisease(j, prevalence[(prevalence['Disease'] == j) & (prevalence['Age'] == '18-29')]['Prevalence'].iloc[0])
        else:
            outputDF[j] = PooledOddsForDisease(j, prevalence[(prevalence['Disease'] == j) & (prevalence['MinAge'] <= age) & (prevalence['MaxAge'] >= age)]['Prevalence'].iloc[0])
    elif j == "Osteoarthritis":
        outputDF[j] = PooledOddsForDisease(j, prevalence[(prevalence['Disease'] == j) & (prevalence['Gender'] == gender)]['Prevalence'].iloc[0])
    elif j == "OsteoarthritisHip":
        outputDF[j] = PooledOddsForDisease(j, prevalence[(prevalence['Disease'] == j) & (prevalence['Gender'] == gender)]['Prevalence'].iloc[0])
    elif j == "Osteoporosis":
        if age < 50:
            outputDF[j] = PooledOddsForDisease(j, prevalence[(prevalence['Disease'] == j) & (prevalence['Gender'] == gender) & (prevalence['Age'] == '50-59')]['Prevalence'].iloc[0])
        else:
            outputDF[j] = PooledOddsForDisease(j, prevalence[(prevalence['Disease'] == j) & (prevalence['Gender'] == gender) & (prevalence['MinAge'] <= age) & ( prevalence['MaxAge'] >= age)]['Prevalence'].iloc[0])
    #elif j == "Rheumatoid_arthritis":
    #    outputDF[j] = PooledOddsForDisease(j, prevalence[(prevalence['Disease'] == j)]['Prevalence'].iloc[0])
    #Need to figure out what's going on with Stroke_All
    #elif j == "Stroke_All":
    #    if age < 18:
    #        outputDF[j] = PooledOddsForDisease(j, prevalence[(prevalence['Disease'] == j) & (prevalence['Age'] == '18-44')]['Prevalence'].iloc[0])
    #    else:
    #        outputDF[j] = PooledOddsForDisease(j, prevalence[(prevalence['Disease'] == j) & (prevalence['MinAge'] <= age) & (prevalence['MaxAge'] >= age)]['Prevalence'].iloc[0])
    elif j == "StrokeLarge_Vessel":
        if age < 18:
            outputDF[j] = PooledOddsForDisease(j, prevalence[(prevalence['Disease'] == j) & (prevalence['Age'] == '18-44')]['Prevalence'].iloc[0])
        else:
            outputDF[j] = PooledOddsForDisease(j, prevalence[(prevalence['Disease'] == j) & (prevalence['MinAge'] <= age) & (prevalence['MaxAge'] >= age)]['Prevalence'].iloc[0])
    #elif j == "Ischemic_Stroke":
    #    if age < 18:
    #        outputDF[j] = PooledOddsForDisease(j, prevalence[(prevalence['Disease'] == j) & (prevalence['Age'] == '18-44')]['Prevalence'].iloc[0])
    #    else:
    #        outputDF[j] = PooledOddsForDisease(j, prevalence[(prevalence['Disease'] == j) & (prevalence['MinAge'] <= age) & (prevalence['MaxAge'] >= age)]['Prevalence'].iloc[0])
    elif j == "Venous_thromboembolism":
        outputDF[j] = PooledOddsForDisease(j, prevalence[(prevalence['Disease'] == j)]['Prevalence'].iloc[0])
    elif (j == "Polycystic_Ovary_Syndrome") & (gender == 'Female'):
        outputDF[j] = PooledOddsForDisease(j, prevalence[(prevalence['Disease'] == j)]['Prevalence'].iloc[0])
    #elif j == "Hypertension":
    #    if age < 18:
    #        outputDF[j] = PooledOddsForDisease(j, prevalence[(prevalence['Disease'] == j) & (prevalence['Age'] == '18-44')]['Prevalence'].iloc[0])
    #    else:
    #        outputDF[j] = PooledOddsForDisease(j, prevalence[(prevalence['Disease'] == j) & (prevalence['MinAge'] <= age) & (prevalence['MaxAge'] >= age)]['Prevalence'].iloc[0])
    elif j == "Iron_Deficiency":
        if gender == "Male":
            if age < 12:
                outputDF[j] = PooledOddsForDisease(j, prevalence[(prevalence['Disease'] == j) & (prevalence['Gender'] == gender) & (prevalence['Age'] == '12-15')]['Prevalence'].iloc[0])
            else:
                outputDF[j] = PooledOddsForDisease(j, prevalence[(prevalence['Disease'] == j) & (prevalence['Gender'] == gender) & (prevalence['MinAge'] <= age) & (prevalence['MaxAge'] >= age)]['Prevalence'].iloc[0])
        elif gender == "Female":
            if age < 12:
                outputDF[j] = PooledOddsForDisease(j, prevalence[(prevalence['Disease'] == j) & (prevalence['Gender'] == gender) & (prevalence['Age'] == '12-15')]['Prevalence'].iloc[0])
            else:
                outputDF[j] = PooledOddsForDisease(j, prevalence[(prevalence['Disease'] == j) & (prevalence['Gender'] == gender) & (prevalence['MinAge'] <= age) & (prevalence['MaxAge'] >= age)]['Prevalence'].iloc[0])
    elif j == "Migrane_Headache":
        if age < 18:
            outputDF[j] = PooledOddsForDisease(j, prevalence[(prevalence['Disease'] == j) & (prevalence['Age'] == '18-44')]['Prevalence'].iloc[0])
        else:
            outputDF[j] = PooledOddsForDisease(j, prevalence[(prevalence['Disease'] == j) & (prevalence['MinAge'] <= age) & (prevalence['MaxAge'] >= age)]['Prevalence'].iloc[0])
    elif j == "Obesity":
        if age < 18:
            outputDF[j] = PooledOddsForDisease(j, prevalence[(prevalence['Disease'] == j) & (prevalence['Age'] == '18-44')]['Prevalence'].iloc[0])
        else:
            outputDF[j] = PooledOddsForDisease(j, prevalence[(prevalence['Disease'] == j) & (prevalence['MinAge'] <= age) & (prevalence['MaxAge'] >= age)]['Prevalence'].iloc[0])

writer = csv.writer(open('{0}.csv'.format(str(idAtInvoke)), 'wb'))
for key, value in outputDF.items():
   writer.writerow([key, value])
