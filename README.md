# RotiNat is to calculate ROTI

RotiNat version 0.0.3 was a Python package for calculating the Rate of Total Electron Content Index (ROTI) from GPS TEC data. It is designed to aid ionospheric studies and space weather analysis. This package is developed by Tesfay-Tesfu (PhD student), under the supervision of Dr. Nat Gopalswamy (NASA Goddard Space Flight Center, Heliophysics Division) and Dr. Virginia Klausner (UNIVAP, Brazil). Their guidance and incredible support have been instrumental in this effort.

---

## Mathematical Expressions:

### Rate of TEC (ROT)
The Rate of Total Electron Content (ROT) is calculated as the difference in TEC values between two consecutive time points divided by the time interval:

![Rate of TEC Index (ROTI)](https://raw.githubusercontent.com/Tesfay-Tesfu/Ionospheric-TEC-ROTI-Interactives/main/ROT.png)


---

### Rate of TEC Index (ROTI)

The Rate of TEC Index (ROTI) is calculated as the standard deviation of ROT over a given time window:

![Rate of TEC Index (ROTI)](https://raw.githubusercontent.com/Tesfay-Tesfu/Ionospheric-TEC-ROTI-Interactives/main/ROTI.png)


---

# Why RotiNat ?

- The name RotiNat combines "ROTI" and "Nat," honoring Dr. Nat Gopalswamy for his encouragement and support during challenging years.

---

# Features

- Computes ROT (Rate of TEC) and ROTI (Rate of TEC Index) from TEC data.
- Supports input from Cmn and other common data formats.
- Provides easy-to-use functions for preprocessing and analysis.

---

# Installation

## Prerequisite Libraries

Make sure you have the following libraries installed:

```bash
-pip install numpy
-pip install pandas
-pip install os
```

---

# Install the package directly from PyPI:

```bash
pip install RotiNat
```

---

# Alternatively

```bash
pip3 install RotiNat
```

---

# Importing Required Libraries

The following libraries are required for using RotiNat:

```bash
import os
import glob
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
import ipywidgets as widgets
from IPython.display import display
```

---

# Example Usage

## Below is an example of how to use the RotiNat package using a single file:

```python
import pandas as pd
import numpy as np
import os
from RotiNat import ROT30s, ROTI5m, ROTI_CAPES
import warnings
# Suppress runtime warnings from numpy
warnings.filterwarnings("ignore", category=RuntimeWarning, module="numpy")
###############################################################################################
# Define file path and parameters
file_path = "/YOURPATH/file_name.Cmn"
Ele_mask = 30  # You can change the Elevation mask based on your interest
skiprows = 5  # Number of lines to skip (This lines to skip after TEC Rinex processes using Gopi)

###############################################################################################
# Read the TEC data file
data = pd.read_csv(
    file_path,
    delim_whitespace=True,
    skiprows=skiprows,
    header=None,
    names=['MJdatet', 'Time', 'PRN', 'Az', 'Ele', 'Lat', 'Lon', 'Stec', 'Vtec', 'S4']
)
# Extract relevant columns
Time_sec = np.round(data['Time'].values * 3600).astype(int)  # Convert time from hours to seconds
tec = data['Vtec'].values  # Vertical TEC values
PRN = data['PRN'].values  # Satellite PRN
Ele = data['Ele'].values  # Elevation angles
Lon = data['Lon'].values  # Longitude values
Lat = data['Lat'].values  # Latitude values
###############################################################################################
# Calculate ROT30s (Rate of TEC at 30s intervals)
Time_sec_out, PRN_out, Ele_out, Lon_out, Lat_out, rot30s = ROT30s(
    Time_sec, PRN, Ele, Lon, Lat, Ele_mask, tec
)
# Calculate ROTI5m (Rate of TEC Index over 5 minutes)
Time_sec_out2, PRN_out2, Ele_out2, Lon_out2, Lat_out2, roti_5m = ROTI5m(
    Time_sec_out, PRN_out, Ele_out, Lon_out, Lat_out, Ele_mask, rot30s
)
###############################################################################################
if len(Time_sec_out2) > 0:
    # Create DataFrames for ROT30s and ROTI5m results
    ROT30s_data = pd.DataFrame({
        'Hour_UT': Time_sec_out / 3600,  # Convert seconds to hours
        'PRN': PRN_out,
        'Elev_deg': Ele_out,
        'Lon_deg': Lon_out,
        'Lat_deg': Lat_out,
        'ROT30s_TECU/min': rot30s
    })

    ROTI5m_data = pd.DataFrame({
        'Hour_UT': Time_sec_out2 / 3600,  # Convert seconds to hours
        'PRN': PRN_out2,
        'Elev_deg': Ele_out2,
        'Lon_deg': Lon_out2,
        'Lat_deg': Lat_out2,
        'ROTI5m_TECU/min': roti_5m
    })

    # Get the directory of the input file path
    directory = os.path.dirname(file_path)
    # Save the outputs
    ROT30s_data.to_csv(os.path.join(directory, 'ROT30s_data.Cmn'), sep='\t', index=False, float_format='%.4f')
    ROTI5m_data.to_csv(os.path.join(directory, 'ROTI5m_data.Cmn'), sep='\t', index=False, float_format='%.4f')
###############################################################################################
```

---

## Applying RotiNat to Multiple Files in Two Folders (Disturbance and Quiet)

If you need to apply RotiNat for multiple files located in two different folders (e.g., Disturbance and Quiet), use the following:

```python
# Just copy only this two lines and run it. Follow the pop-out interactive instructions
from RotiNat import ROTI_CAPES
ROTI_CAPES()
```

---

# Contacts: 
* Email: tesfayphysics@gmail.com
* GitHub: https://github.com/Tesfay-Tesfu

---

## Badges

The following badges highlight the licenses associated with this project:

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
[![AGPL License](https://img.shields.io/badge/license-AGPL-blue.svg)](http://www.gnu.org/licenses/agpl-3.0)

---

## Acknowledgements

 - [CAPES, UNIVAP](https://github.com/Tesfay-Tesfu)
 - [GSFC, NASA Heliophysics Division](https://github.com/Tesfay-Tesfu)
 - [COSPAR](https://github.com/Tesfay-Tesfu)
 - [Institute for Space Astrophysics and Planetology (INAF), Italy](https://github.com/Tesfay-Tesfu)
 - [Dr. Arian Ojeda Gonzalez](https://github.com/Tesfay-Tesfu)
 - [Dr. Gebregiorgis Abrha, Dr. Yikdem Mengesha](https://github.com/Tesfay-Tesfu)
 
---
 
## References:

- [Daniel Okoh (2025). Programs to Compute ROT and ROTI (https://www.mathworks.com/matlabcentral/fileexchange/129239-programs-to-compute-rot-and-roti), MATLAB Central File Exchange. Retrieved January 18, 2025.](https://www.mathworks.com/matlabcentral/fileexchange/129239-programs-to-compute-rot-and-roti)

