# A tool for fast creation of vegetation index time series in GEE
`geoindexity` provides an accesible fast forward way to create time series of vegetation indices for user defined AOIs and time periods.It is based on Google Earth Engine (GEE). Its main time series class `Geoindexity` is used to filter GEE image collections (Sentinel 2 SRF Harmonized, Landsat), calculating indices,plotting, and exporting data and plots to Google Drive.

**The Landast collection operational**

## About the project
This package was developed by the students Rohit Khati, David Hansen, Gernot Nikolaus and Asad Ullah as part of the Software Development (Python) course at the University of Salzburg in the summer term 2024. 
## Requirements
To use this script, you need:
- Access to Google Earth Engine (GEE) with a valid account and authentication.
- Python libraries: Earth Engine Python API (`ee`), Pandas (`pd`), Matplotlib (`plt`), and NumPy (`np`).
## Installation 
The package is not deployed to PyPI yet. However, you can install the package in your prefered package management system like `conda` that allows for packagae installation using `pip`.  
### pip workflow
Use the following command to install Geoindexity using pip: 
```
pip install git+https://github.com/ro-hit81/GeoIndexity
```
### conda workflow 
Activate your prefered conda environment: 
```
conda activate YOUR_ENVIRONMENT
```

If `pip`is not installed yet use: 
```
conda install pip 
```

After pip is installed, use the command from above: 
```
pip install git+https://github.com/ro-hit81/GeoIndexity

```

### Uninstall package 
To uninstall use the following pip command: 
```
pip uninstall geoindexity 
```

## Working example
Import dependencies:
```python 
import ee 
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 
```
Initialize and authenticate GEE:
```python
ee.Initialize() 
ee.Authenticate() 
```
Import `geoindexity`: 
```python 
import geoindexity.geoindexity as gx
```
```python
roi = [
    12.90,
    47.75,
    13.20,
    47.85,
]
start_date = '2020-01-01'
end_date  = '2020-03-20'
properties = {
    'CLOUDY_PIXEL_PERCENTAGE':10
}

ts = gx.Geoindexity(roi, start_date, end_date, properties=properties, collection_id='Sentinel')

gx.ndvi_collection() 
gx.reduce_ndvi_mean()
gx.plot() 
````
