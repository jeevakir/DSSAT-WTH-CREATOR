import pandas as pd
from utils import utils
from libs import wth_handler

default_headers = ["DATE", "SRAD", "TMAX", "TMIN", "RAIN", "DEWP", "WIND", "PAR", "EVAP", "RHUM"]
input_headers=["DATE", "TMAX", "TMIN", "RAIN", "RHUM", "SRAD","WIND", "EVAP", "PAR", "DEWP"]
directory=r'/run/media/jeeva/DATA/code-fun/python/DSSAT-convertor-CLI/Renamed/ssp126/mid'
#directory=r'/run/media/jeeva/DATA/code-fun/python/DSSAT-convertor-CLI/Renamed/Historical_IMD'

def main():

    csvs=utils.get_csv_files(directory)
    for csv_file in csvs:
        wth_handler.format_wth(directory,csv_file,default_headers,input_headers)
        print(csv_file)

if __name__ == "__main__":
    main()