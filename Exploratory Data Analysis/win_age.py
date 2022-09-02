# Import Libraries
import pandas as pd
from urllib.request import urlopen  
import os.path as osp
import os
import logging
import zipfile
from glob import glob
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
logging.getLogger().setLevel('INFO')

def download_file(url_str, path):
    url = urlopen(url_str)
    output = open(path, 'wb')       
    output.write(url.read())
    output.close()  
    
def extract_file(archive_path, target_dir):
    zip_file = zipfile.ZipFile(archive_path, 'r')
    zip_file.extractall(target_dir)
    zip_file.close()
    
BASE_URL = 'http://tennis-data.co.uk'
DATA_DIR = "tennis_data"
ATP_DIR = './{}/ATP'.format(DATA_DIR)
WTA_DIR = './{}/WTA'.format(DATA_DIR)

ATP_URLS = [BASE_URL + "/%i/%i.zip" % (i,i) for i in range(2000,2019)]
WTA_URLS = [BASE_URL + "/%iw/%i.zip" % (i,i) for i in range(2007,2019)]

os.makedirs(osp.join(ATP_DIR, 'archives'), exist_ok=True)
os.makedirs(osp.join(WTA_DIR, 'archives'), exist_ok=True)

for files, directory in ((ATP_URLS, ATP_DIR), (WTA_URLS, WTA_DIR)):
    for dl_path in files:
        logging.info("downloading & extracting file %s", dl_path)
        archive_path = osp.join(directory, 'archives', osp.basename(dl_path))
        download_file(dl_path, archive_path)
        extract_file(archive_path, directory)
    
ATP_FILES = sorted(glob("%s/*.xls*" % ATP_DIR))
WTA_FILES = sorted(glob("%s/*.xls*" % WTA_DIR))

df_atp = pd.concat([pd.read_excel(f) for f in ATP_FILES], ignore_index=True)
df_wta = pd.concat([pd.read_excel(f) for f in WTA_FILES], ignore_index=True)

logging.info("%i matches ATP in df_atp", df_atp.shape[0])
logging.info("%i matches WTA in df_wta", df_wta.shape[0])

#nomi colonne in lowercase
df_atp.columns = df_atp.columns.str.lower()
#riempio i campi vuoti con 0
df_atp['wsets'].fillna(0, inplace = True)
df_atp['lsets'].fillna(0, inplace = True)

#######################################################################################
'''
#Request 5
names = np.unique((list(df_atp.winner.unique()) + list(df_atp.loser.unique())))
#Trovo la data di esordio di ogni giocatore
start_date = {}
for name in names:
    date = df_atp[(df_atp.winner == name) | (df_atp.loser == name)].date.dt.date.min()
    start_date[name] = date

#Trovo l'età dei giocatori ad oggi 
mean_start_age = 19
df_start = pd.DataFrame({'name':start_date.keys(), 'startdate':start_date.values()})

df_start['startdate'] = pd.to_datetime(df_start['startdate'])
df_atp['date'] = pd.to_datetime(df_atp['date'])
first_date = df_atp.date[0]

win_age_evolution = []

for date in np.unique(df_atp.date.dt.year):
    
    print(date)
    wae = []
    df_start['age'] = mean_start_age + (date - df_start['startdate'].dt.year)
    
    for name in  df_atp[df_atp.date.dt.year == date]['winner']:
        
        idx = df_start['name'] == name
        age = int(df_start[idx]['age'])
        wae.append(age)
        
    win_age_evolution.append(wae)

from matplotlib.animation import FuncAnimation

fig, axes = plt.subplots(figsize=(12,8))
def animate(i):
    axes.clear()
    data = win_age_evolution[i]
    graph = sns.histplot(x = data, discrete = True, ax = axes, color = 'r')
    graph.set(ylim = (0,800), xlim = (18,38), xlabel = 'Age')

ani = FuncAnimation(fig, animate, frames=len(win_age_evolution),interval=400,repeat=True)
plt.show()
ani.save('win_age_evolution1.gif')
'''
#######################################################################################

#Request 6

df_wta.columns = df_wta.columns.str.lower()
idx = df_wta[df_wta.date.isnull() == True]
df_wta.drop(idx.index, axis = 0, inplace = True)

names = np.unique((list(df_wta.winner.unique()) + list(df_wta.loser.unique())))
#Trovo la data di esordio di ogni giocatore
start_date = {}
for name in names:
    date = df_wta[(df_wta.winner == name) | (df_wta.loser == name)].date.dt.date.min()
    start_date[name] = date

mean_start_age = 19
df_start = pd.DataFrame({'name':start_date.keys(), 'startdate':start_date.values()})

df_start['startdate'] = pd.to_datetime(df_start['startdate'])
df_wta['date'] = pd.to_datetime(df_wta['date'])
first_date = df_wta.date[0]

win_age_evolution = []

for date in np.unique(df_wta.date.dt.year):
    
    print(date)
    wae = []
    df_start['age'] = mean_start_age + (date - df_start['startdate'].dt.year)
    for name in  df_wta[df_wta.date.dt.year == date]['winner']:
        
        idx = df_start['name'] == name
        age = int(df_start[idx]['age'])
        wae.append(age)
        
    win_age_evolution.append(wae)

from matplotlib.animation import FuncAnimation

fig, axes = plt.subplots(figsize=(12,8))
def animate(i):
    axes.clear()
    data = win_age_evolution[i]
    graph = sns.histplot(x = data, discrete = True,palette = 'flare', ax = axes, hue = win_age_evolution[i])
    graph.set( xlim = (18,31), xlabel = 'Age')

ani = FuncAnimation(fig, animate, frames=len(win_age_evolution),interval=400,repeat=True)
plt.show()
ani.save('win_age_evolution_wta.gif')