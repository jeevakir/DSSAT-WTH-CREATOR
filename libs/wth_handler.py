import pandas as pd
import numpy as np
import pyhigh
from os import path
import requests
import urllib

file_header = """$WEATHER DATA : TNAU

@  INSI      LAT     LONG    ELEV     TAV     AMP   REFHT   WNDHT
   TNAU   11.000   77.000   xx427   -99.0   -99.0   -99.0   -99.0
@  DATE    SRAD    TMAX    TMIN    RAIN    DEWP    WIND     PAR    EVAP    RHUM"""

coordi_csv='TN-Dist-wth-name.csv'
column_widths=[7, 8, 8, 8, 8, 8, 8, 8, 8, 8]
input_date_format='%Y-%m-%d' #'%d/%m/%Y'


def format_wth(directory,csv_file,out_headers,in_headers):
    data=pd.read_csv(path.join(directory,csv_file))
    data=data.rename(columns=dict(zip(data.columns,in_headers)))
    data=data.reindex(columns=in_headers, fill_value=-99.0)
    tav,tamp=calculate_tav(data)
    lat,lon,elev=get_coord(coordi_csv,csv_file.rsplit('.',1)[0]) 
    wth_header=create_header(tav,tamp,lat,lon,elev,file_header,csv_file)
    date_format(data)
    data=data[out_headers]
    data.loc[:,data.columns[0]]=data[data.columns[0]].astype(int)
    data.loc[:,data.columns[1:]]=data[data.columns[1:]].astype(float)
    out_file=gen_outfile_name(data,csv_file)
    wth_write_out(data,wth_header,path.join(directory,out_file))

def calculate_tav(data_in):
    data_in['DATE']=pd.to_datetime(data_in['DATE'],format=input_date_format)
    data_in['YEAR']=data_in['DATE'].dt.year
    data_in['MONTH']=data_in['DATE'].dt.month
    tav=(data_in['TMAX'].mean()+data_in['TMIN'].mean())/2
    monthly_avg=data_in.groupby('MONTH')[['TMAX','TMIN']].mean()
    monthly_avg=(monthly_avg['TMAX']+monthly_avg['TMIN'])/2
    tamp=monthly_avg.max()-monthly_avg.min()
    return tav,tamp

def gen_outfile_name(data_in,in_filename):
    years=pd.to_datetime(data_in['DATE'],format='%Y%j').dt.year
    syear=years.min()
    nyears=years.max() - years.min()
    prefix=path.basename(in_filename)[:4]
    out_name=prefix.upper()+str(syear)[2:]+str(nyears)+".WTH"
    return out_name
    
def get_coord(coord_csv,in_csv):
    details=pd.read_csv(coord_csv)
    details=details.set_index(['Name'])
    coords=details.loc[in_csv]
    lat=f"{coords.lat:6.3f}"
    long=f"{coords.lon:6.3f}"
    elev=get_elev(lat,long)
    return lat,long,elev   

def create_header(tav,tamp,lat,lon,elev,file_header,csv_file):
    out_header=file_header.replace("-99.0", f"{tav:5.1f}",1) #tav
    out_header=out_header.replace("-99.0",f"{tamp:5.1f}",1) #amp
    out_header=out_header.replace("11.000",lat,1) #lat
    out_header=out_header.replace("77.000",lon,1) #lon
    out_header=out_header.replace("xx427",f"{elev:5d}",1) #elev
    out_header=out_header.replace("TNAU",path.basename(csv_file)[:4].upper())
    return out_header

def date_format(data_in):
    data_in['DATE']=data_in['DATE'].dt.strftime("%Y%j")

def wth_write_out(data,out_header,out_file):
    fmt=''
    for i in range(0,len(column_widths)):
        if i == 0:
            fmt=f"%{column_widths[i]}d"
        else:
            fmt+=f"%{column_widths[i]}.1f"
    with open(out_file, "w") as file:
        file.write(out_header+'\n')
        for index,row in data.iterrows():
            file.write((fmt) % tuple(row.values))
            file.write('\n')
        file.close()

def get_elev(lat,lon):
    elev_url=r'https://epqs.nationalmap.gov/v1/json?'
    elev_url=r'https://api.opentopodata.org/v1/etopo1?locations='
    result = requests.get((elev_url + lat+","+lon))
    elevation=result.json()['results'][0]['elevation']
    elevation=int(elevation)
    return elevation