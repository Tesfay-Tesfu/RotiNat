import os
import glob
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
import ipywidgets as widgets
from IPython.display import display
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning, module="numpy")

def display_title_and_subtitle():
    print("=" * 80)
    print("\n This TEC-ROTI Processing developed by Tesfu Tesfay (TT) - Gopalswamy's Scholar\n")
    print("=" * 80)
    print("\n I would like to thankful to CAPES, IPD, UNIVAP, Brazil and Virginia \n")
    print("=" * 80)
    print("\n It is a great pleasure working at NASA-GSFC - 671 under Gopalswamy\n")
    print("=" * 80)
    print("\n If you may have challenges please contact me via tesfayphysics@gmail.com\n")
    print("=" * 80)
    print("\nInstructions:")
    print("Select Disturbed & Quiet folders.")
    print("=" * 80)
    print("Please make sure that you are using the ionospheric GPS-TEC data with .Cmn extension file name.")
    print("Select Disturbed & Quiet folders.")
###################################################################################    
root = tk.Tk()
root.withdraw()
skiprows = simpledialog.askinteger("Input", "Enter number of skip lines:", minvalue=0, maxvalue=20)
###################################################################################
def ROT30s(Time_sec, PRN, Ele, Lon, Lat, Ele_mask, tec):
    if len(Time_sec) <= 1:
        print('Error: length of input vectors must be at least 2')
        return [], [], [], [], [], []
    
    PRN = pd.Series(PRN).astype(str)
    PRN_uni = PRN.unique()
    
    Time_sec_out = []
    PRN_out = []
    Ele_out = []
    Lon_out = []
    Lat_out = []
    rot30s = []

    for PRN_values in PRN_uni:
        rng = len(tec)
        PRN_uni_data = np.where((PRN[:rng] == PRN_values) & (Ele[:rng] > Ele_mask))[0]
        if len(PRN_uni_data) > 0:
            Time_seci = Time_sec[PRN_uni_data]
            Elei = Ele[PRN_uni_data]
            Loni = Lon[PRN_uni_data]
            Lati = Lat[PRN_uni_data]
            teci = tec[PRN_uni_data]
            for tsec in range(min(Time_seci), max(Time_seci) + 1, 30):
                PRN_uni_datas1 = np.where(np.abs(Time_seci - tsec) <= 15)[0]
                PRN_uni_datas2 = np.where(np.abs(Time_seci - tsec + 30) <= 15)[0]
                if len(PRN_uni_datas1) > 0 and len(PRN_uni_datas2) > 0:

                    rot30s.append((np.mean(teci[PRN_uni_datas2]) - np.mean(teci[PRN_uni_datas1])) / 0.5)
                    Time_sec_out.append(tsec + 30)
                    PRN_out.append(PRN_values)
                    Ele_out.append(np.mean(Elei[PRN_uni_datas2]))
                    Lon_out.append(np.mean(Loni[PRN_uni_datas2]))
                    Lat_out.append(np.mean(Lati[PRN_uni_datas2]))
    
    return (np.array(Time_sec_out), np.array(PRN_out), np.array(Ele_out), 
            np.array(Lon_out), np.array(Lat_out), np.array(rot30s))

def ROTI5m(Time_sec, PRN, Ele, Lon, Lat, Ele_mask, rot30s):
    if len(Time_sec) <= 1:
        print('Error: length of input vectors must be at least 2')
        return [], [], [], [], [], []
    
    PRN = pd.Series(PRN).astype(str)
    PRN_uni = PRN.unique()
    
    Time_sec_out = []
    PRN_out = []
    Ele_out = []
    Lon_out = []
    Lat_out = []
    roti_5m = []

    for PRN_values in PRN_uni:
        rng = len(rot30s)
        PRN_uni_data = np.where((PRN[:rng] == PRN_values) & (Ele[:rng] > Ele_mask))[0]
        if len(PRN_uni_data) > 0:
            Time_seci = Time_sec[PRN_uni_data]
            Elei = Ele[PRN_uni_data]
            Loni = Lon[PRN_uni_data]
            Lati = Lat[PRN_uni_data]
            rot30si = rot30s[PRN_uni_data]
            for tsec in range(min(Time_seci), max(Time_seci) + 1, 300):
                PRN_uni_datas = np.where(np.abs(Time_seci - tsec) <= 150)[0]
                if len(PRN_uni_datas) > 0:

                    Time_sec_out.append(tsec)
                    roti_5m.append(np.std(rot30si[PRN_uni_datas], ddof=1))
                    PRN_out.append(PRN_values)
                    Ele_out.append(np.mean(Elei[PRN_uni_datas]))
                    Lon_out.append(np.mean(Loni[PRN_uni_datas]))
                    Lat_out.append(np.mean(Lati[PRN_uni_datas]))
    
    return (np.array(Time_sec_out), np.array(PRN_out), np.array(Ele_out), 
            np.array(Lon_out), np.array(Lat_out), np.array(roti_5m))

def select_folders():
    root = tk.Tk()
    root.withdraw()
    disturb_folder = filedialog.askdirectory(mustexist=True, title='Select the Disturb Folder')
    quiet_folder = filedialog.askdirectory(mustexist=True, title='Select the Quiet Folder')
    return [disturb_folder, quiet_folder]

def process_roti_data(folders, Ele_mask=30):
    for folder in folders:
        listA = glob.glob(f'{folder}/*.cmn')
        output_rot30s_folder = os.path.join(folder, 'ROT30s_Processed')
        output_roti5m_folder = os.path.join(folder, 'ROTI5m_Processed')

        os.makedirs(output_rot30s_folder, exist_ok=True)
        os.makedirs(output_roti5m_folder, exist_ok=True)
        
        for file_path in listA:
            ###############################################################################################
            data = pd.read_csv(
                file_path, delim_whitespace=True, skiprows=skiprows, header=None,
                names=['MJdatet', 'Time', 'PRN', 'Az', 'Ele', 'Lat', 'Lon', 'Stec', 'Vtec', 'S4']
            )
            #
            Time_sec = np.round(data['Time'].values * 3600).astype(int)
            tec = data['Vtec'].values
            PRN = data['PRN'].values
            Ele = data['Ele'].values
            Lon = data['Lon'].values
            Lat = data['Lat'].values
###############################################################################################
            
            Time_sec_out, PRN_out, Ele_out, Lon_out, Lat_out, rot30s = ROT30s(Time_sec, PRN, Ele, Lon, Lat, Ele_mask, tec)
            Time_sec_out2, PRN_out2, Ele_out2, Lon_out2, Lat_out2, roti_5m = ROTI5m(Time_sec_out, PRN_out, Ele_out, Lon_out, Lat_out, Ele_mask, rot30s)
            
            if len(Time_sec_out2) > 0:
                rot30s_data = pd.DataFrame({
                    'Hour_UT': Time_sec_out / 3600,
                    'PRN': PRN_out,
                    'Elv_deg': Ele_out,
                    'Lon_deg': Lon_out,
                    'Lat_deg': Lat_out,
                    'ROT30s_TECU/min': rot30s
                })
                
                roti5m_data = pd.DataFrame({
                    'Hour_UT': Time_sec_out2 / 3600,
                    'PRN': PRN_out2,
                    'Elv_deg': Ele_out2,
                    'Lon_deg': Lon_out2,
                    'Lat_deg': Lat_out2,
                    'ROTI5m_TECU/min': roti_5m
                })
                
                output_rot30s_path = os.path.join(output_rot30s_folder, os.path.basename(file_path))
                output_roti5m_path = os.path.join(output_roti5m_folder, os.path.basename(file_path))
                
                rot30s_data.to_csv(output_rot30s_path, sep='\t', index=False, float_format='%.4f')
                roti5m_data.to_csv(output_roti5m_path, sep='\t', index=False, float_format='%.4f')

    print("CongratuLations! Your Processing completed [Thanks to NASA GSFC & UNIVAP, CAPES].")

def ROTI_CAPES():
    display_title_and_subtitle()
    folders = select_folders()
    Ele_mask = simpledialog.askinteger("Input", "Enter El Mask (degrees):", minvalue=0, maxvalue=90)    
    process_roti_data(folders, Ele_mask)

########################
if __name__ == "__main__":
    ROTI_CAPES()
# The End !!!