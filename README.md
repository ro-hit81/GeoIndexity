# GeoIndexity Script Documentation
Here, a package will be created which will use the power of Google Earth Engine in the Backend, and provide the tools to calculate the indices along with the time series for user specified date and area.

## About
This package was developed by the students Rohit Khati, David Hansen, Gernot Nikolaus and Asad Ullah as part of the Software Development (Python) course at the University of Salzburg. The goal of the project was to create a GitHub repository to manage all requests, issues and collaboration within the team.

## Overview
This script provides classes and functions to interact with satellite imagery from Google Earth Engine (GEE). It focuses on handling Landsat and Sentinel satellite data, calculating vegetation indices (NDVI and EVI), reducing time-series data, plotting time-series, and exporting data and plots to Google Drive.

### About the package
The Python Package gives useres the opportunity to access remote sensing indices from Sentinel-2 as well as Landsat, and calculate their repective times series charts for their study area. In this process, Google Earth Engine is used.

### Requirements

To use this script, you need:
- Access to Google Earth Engine (GEE) with a valid account and authentication.
- Python libraries: Earth Engine Python API (`ee`), Pandas (`pd`), Matplotlib (`plt`), and NumPy (`np`).

### Classes and Functions

#### Landsat Class

The `Landsat` class provides methods to handle Landsat satellite imagery from Google Earth Engine.

##### Attributes

- `roi`: Region of interest defined by [xmin, ymin, xmax, ymax].
- `start_date`: Start date for filtering the image collection ('YYYY-MM-DD').
- `end_date`: End date for filtering the image collection ('YYYY-MM-DD').
- `collection_id`: ID of the Landsat image collection ('LANDSAT/LC08/C02/T1_L2' by default).
- `properties`: Optional properties for additional filtering (e.g., CLOUD_COVER).

##### Methods

- `bound()`: Returns the region of interest as an Earth Engine Geometry Rectangle.
- `select_product()`: Filters the Landsat image collection based on the date range, region of interest, and optional properties.
- `select_mission()`: Provides a dictionary of Landsat missions with their operational date ranges.
- `number_of_images()`: Prints the total number of images in the filtered Landsat image collection.

#### Sentinel Class

The `Sentinel` class handles Sentinel satellite imagery from Google Earth Engine.

##### Attributes

- `roi`: Region of interest defined by [xmin, ymin, xmax, ymax].
- `start_date`: Start date for filtering the image collection ('YYYY-MM-DD').
- `end_date`: End date for filtering the image collection ('YYYY-MM-DD').
- `collection_id`: ID of the Sentinel image collection ('COPERNICUS/S2_SR_HARMONIZED' by default).
- `properties`: Optional properties for additional filtering (e.g., CLOUDY_PIXEL_PERCENTAGE).

##### Methods

- `bound()`: Returns the region of interest as an Earth Engine Geometry Rectangle.
- `select_product()`: Filters the Sentinel image collection based on the date range, region of interest, and optional properties.
- `number_of_images()`: Prints the total number of images in the filtered Sentinel image collection.

#### Geoindexity Class

The `Geoindexity` class serves as the core time-series object for handling satellite imagery data, calculating indices, reducing time-series data, plotting, and exporting.

##### Attributes

- `roi`: Region of interest defined by [xmin, ymin, xmax, ymax].
- `start_date`: Start date for filtering the image collection ('YYYY-MM-DD').
- `end_date`: End date for filtering the image collection ('YYYY-MM-DD').
- `collection_id`: Identifier for choosing a GEE collection ('Sentinel' or 'Landsat' by default).
- `properties`: Optional properties for additional filtering (e.g., CLOUDY_PIXEL_PERCENTAGE).
- `reducer`: Indicates the latest used reducer (e.g., 'NDVI_MEAN').
- `df`: Pandas DataFrame storing information of the latest reduction.

##### Methods

- `bound()`: Returns the region of interest as an Earth Engine Geometry Rectangle.
- `add_ndvi(image)`: Calculates and adds NDVI band to the given image.
- `add_evi(image)`: Calculates and adds EVI band to the given image.
- `ndvi_collection()`: Maps `add_ndvi()` to the image collection.
- `evi_collection()`: Maps `add_evi()` to the image collection.
- `reduce_ndvi_mean()`: Reduces the time-series collection based on the ROI using NDVI band and mean.
- `plot()`: Standard plotting function for the `Geoindexity` time-series object.
- `export_image_to_drive(image, description, folder='earth_engine_exports')`: Exports a single image to Google Drive.
- `export_image_collection_to_drive(description, folder='earth_engine_exports')`: Exports the entire image collection to Google Drive as a single zip file.
- `export_plot_to_drive(description, folder='earth_engine_exports')`: Exports the current plot to Google Drive as a PNG file.

#### Additional Functions

- `download_plot_local(obj, fig_name='plot.png')`: Generates and saves a plot locally.
