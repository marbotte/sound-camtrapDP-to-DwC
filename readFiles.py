import os
import pandas as pd

dir = "../data_transformacion/"

dircontent = os.listdir(dir)

observations = pd.read_csv(dir + 'observations.csv')
deployments = pd.read_csv(dir + 'deployments.csv')
media = pd.read_csv(dir + 'media.csv')

mapping = pd.ExcelFile(dir + 'Sistematización de datos - pamDP.xlsx')
mapping.sheet_names
allSheets = pd.read_excel(dir + 'Sistematización de datos - pamDP.xlsx',sheet_name=None)
allSheets.__class__.__name__
colMedia = allSheets['media.csv']['pamDP Field Name'].to_list()
[media.columns.index(x) if x in media.columns else None for x in colMedia]
