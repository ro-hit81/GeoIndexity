"""
This script includes the core GeoIndexity classes and functions.

GeoIndexity classes and functions are based on the Earth Engine API
for Google Earth Engine (GEE). A valid GEE account is therefore
necessary to use GeoIndexity. For more information on setting up your
GEE account and using GeoIndexity, please see https://github.com/ro-hit81/GeoIndexity/blob/main/README.md
"""

import ee
ee.Initialize()

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class Landsat:
    """
    A class to handle Landsat satellite imagery from Google Earth Engine.

    Attributes
    ----------
    roi : list
        The region of interest defined by [xmin, ymin, xmax, ymax].
    start_date : str
        The start date for filtering the image collection (format: 'YYYY-MM-DD').
    end_date : str
        The end date for filtering the image collection (format: 'YYYY-MM-DD').
    collection_id : str
        The ID of the Landsat image collection.
    properties
        Properties for additional filtering, such as CLOUD_COVER.
    """
    def __init__(self, roi, start_date, end_date, collection_id, properties=None):
        """Initializes the Landsat class with region of interest, date range, collection ID, and optional properties.

        Arguments
        ----------
        roi : list
            The region of interest defined by [xmin, ymin, xmax, ymax].
        start_date : str 
            The start date for filtering the image collection (format: 'YYYY-MM-DD').
        end_date : str
            The end date for filtering the image collection (format: 'YYYY-MM-DD').
        collection_id : str
            The ID of the Landsat image collection.
        properties
            Properties for additional filtering, such as CLOUD_COVER.
        """
        
        self.roi = roi
        self.start_date = start_date
        self.end_date = end_date
        self.collection_id= 'LANDSAT/LC08/C02/T1_L2'
        self.properties = properties or {}

    def bound(self):
        """Returns the region of interest as an Earth Engine Geometry Rectangle.

        Returns
        ----------
        ee.Geometry.Rectangle
            The region of interest as a rectangle.
        """
        return ee.Geometry.Rectangle(self.roi) 
    
    def select_product(self):
        """Filters the Landsat image collection based on the date range, region of interest, and optional properties.

        Returns
        ----------
        ee.ImageCollection
            The filtered Landsat image collection.
        
        Raises
        ----------
        KeyError: If an invalid property name is provided.
        """
        image_collection = ee.ImageCollection(self.collection_id)
        image_collection = image_collection.filterDate(self.start_date, self.end_date)
        image_collection = image_collection.filterBounds(self.bound())
        if self.properties:
            valid_properties = {"CLOUD_COVER": int, "CLOUD_LAND_COVER": int}
            for property_name, value in self.properties.items():
                if property_name not in valid_properties:
                    raise KeyError(f"Invalid property name: {property_name}. Supported properties: {', '.join(valid_properties.keys())}.")
                image_collection = image_collection.filter(ee.Filter.lte(property_name, value))
        return image_collection

    def select_mission(self):
        """Provides a dictionary of Landsat missions with their operational date ranges.

        Returns
        ----------
        dict:
            A dictionary where keys are mission names and values are tuples of (start_date, end_date).
        """
        missions = {
            'LANDSAT_1': ('1972-07-23', '1975-01-22'),
            'LANDSAT_2': ('1975-01-22', '1978-03-05'),
            'LANDSAT_3': ('1978-03-05', '1982-07-16'),
            'LANDSAT_4': ('1982-07-16', '1984-03-01'),
            'LANDSAT_5': ('1984-03-01', '2012-05-05'), 
            'LANDSAT_8': ('2013-03-18', '2021-10-30'),
            'LANDSAT_9': ('2021-10-31', 'present')
        }
        return missions

    def number_of_images(self):
        """Prints the total number of images in the filtered Landsat image collection."""
        print(f'Total Landsat images collected: {self.select_product().size().getInfo()}')

class Sentinel:
    """
    A class to handle Sentinel satellite imagery from Google Earth Engine.

    Attributes
    ----------
    roi : list
        The region of interest defined by [xmin, ymin, xmax, ymax].
    start_date : str
        The start date for filtering the image collection (format: 'YYYY-MM-DD').
    end_date : str
        The end date for filtering the image collection (format: 'YYYY-MM-DD').
    collection_id : str
        The ID of the Sentinel image collection.
    properties : dict
        Properties for additional filtering, such as CLOUDY_PIXEL_PERCENTAGE.
    """
    def __init__(self, roi, start_date, end_date, collection_id, properties=None):
        """Initializes the Sentinel class with region of interest, date range, collection ID, and optional properties.

        Arguments
        ----------
        roi : list
            The region of interest defined by [xmin, ymin, xmax, ymax].
        start_date : str
            The start date for filtering the image collection (format: 'YYYY-MM-DD').
        end_date : str
            The end date for filtering the image collection (format: 'YYYY-MM-DD').
        collection_id : str
            The ID of the Sentinel image collection.
        properties : dict, optional
            Properties for additional filtering, such as CLOUDY_PIXEL_PERCENTAGE.
        """
        self.roi = roi
        self.start_date = start_date
        self.end_date = end_date
        self.collection_id= 'COPERNICUS/S2_SR_HARMONIZED'
        self.properties = properties or {}

    def bound(self):
        """Returns the region of interest as an Earth Engine Geometry Rectangle.

        Returns
        ----------
        ee.Geometry.Rectangle
            The region of interest as a rectangle.
        """
        return ee.Geometry.Rectangle(self.roi) 
    
    def select_product(self):
        """Filters the Sentinel image collection based on the date range, region of interest, and optional properties.

        Returns
        ----------
        ee.ImageCollection
            The filtered Sentinel image collection.
        
        Raises
        ----------
        KeyError: If an invalid property name is provided.
        """
        image_collection = ee.ImageCollection(self.collection_id)
        image_collection = image_collection.filterDate(self.start_date, self.end_date)
        image_collection = image_collection.filterBounds(self.bound())
        if self.properties:
            valid_properties = {"CLOUDY_PIXEL_PERCENTAGE": int, "CLOUDY_SHADOW_PERCENTAGE": int, "DARK_FEATURES_PERCENTAGE": int}
            for property_name, value in self.properties.items():
                if property_name not in valid_properties:
                    raise KeyError(f"Invalid property name: {property_name}. Supported properties: {', '.join(valid_properties.keys())}.")
                image_collection = image_collection.filter(ee.Filter.lte(property_name, value))
        return image_collection

    def number_of_images(self):
        """Prints the total number of images in the filtered Sentinel image collection."""
        print(f'Total Sentinel images collected: {self.select_product().size().getInfo()}')

class Geoindexity:
    """
    The core Geoindexity time-series object.
    After initializaton funcionality can be used to calculate indices, plot time-series export
    time-series data.
    ...

    Attributes
    ----------
    roi : list
        The region of interest defined by [xmin, ymin, xmax, ymax].
    start_date : str
        The start date for filtering the image collection (format: 'YYYY-MM-DD').
    end_date : str
        The end date for filtering the image collection (format: 'YYYY-MM-DD').
    collection_id: str
         ID to choose a GEE collection. Default: 'Sentinel', 'Landsat'
    properties: dict
        Properties for additional filtering, such as CLOUDY_PIXEL_PERCENTAGE.
    reducer: str
        Tag indicating the latest used reducer.
    df: DataFrame
        Pandas dataframe that stores information of the latest reduction.

    Methods
    -------
    len():
        Returns the number of images in the time-series.
    bound():
        Returns the AOI as ee.Geometry.Rectanlge
    add_ndvi(image):
        Calculates and adds NDVI band to given image.
        Used inside ndvi_collection function.
    add_evi(image):
        Calculates and adds EVI band to given image.
        Used inside evi_collection function.
    ndvi_collection():
        Maps add_ndvi() to the image collection.
    evi_collection():
        Maps add_evi() to the image collection.
    reduce_ndvi_mean():
        Reduces the time-series collection based on the ROI using NDVI band and mean.
    plot():
       Standard plotting function for the geoindexity time-series object.
    """

    def __init__(self, roi, start_date, end_date, collection_id='Sentinel', properties=None): # collection argument as identifier between Sentinel and Landsat? 
        self.roi = roi
        self.start_date = start_date
        self.end_date = end_date
        self.collection_id = collection_id
        self.properties = properties
        self.reducer = None 
        self.df = None 

        if self.collection_id == 'Sentinel':
            self.collection = Sentinel(roi=self.roi,
                                       start_date=self.start_date,
                                       end_date=self.end_date,
                                       collection_id= 'COPERNICUS/S2_SR_HARMONIZED',
                                       properties=self.properties
                                       ).select_product()

        if self.collection_id == 'Landsat8':
            self.collection = Landsat8(roi=self.roi,
                               start_date=self.start_date,
                               end_date=self.end_date,
                               collection_id= 'LANDSAT/LC08/C02/T1_L2',
                               properties=self.properties
                               ).select_product()

    def __len__(self):
        """Returns the number if images in the time-series."""
        return self.collection.size().getInfo()

    def bound(self):
        """Returns the AOI as ee.Geometry.Rectanlge"""
        return ee.Geometry.Rectangle(self.roi)

    def add_ndvi(self, image):
        """Calculates and adds NDVI band to given image.
        Used inside ndvi_collection function.

            Parameters:
                image (ee.Image): Single image.
            Returns:
                image (ee.Image): Input image with added NDVI band.
        """
        if self.collection_id == 'Sentinel':
            ndvi = image.expression(
                '((nir-red)/(nir+red))',
                {'nir': image.select('B4'),
                 'red': image.select('B8')}
            ).rename('NDVI')
        elif self.collection_id == 'Landsat8':
            ndvi = image.expression(
                '((nir - red)/(nir + red))',
                {'nir': image.select('SR_B5'),
                 'red': image.select('SR_B4')}
            ).rename('NDVI')

        return image.addBands(ndvi)

    def add_evi(self, image):
        """Calculates and adds EVI band to given image.
                Used inside evi_collection function.

                    Parameters:
                        image (ee.Image): Single image.
                    Returns:
                        image (ee.Image): Input image with added EVI band.
                """
        if self.collection_id == 'Sentinel':
            evi = image.expression(
                '2.4*((nir-red)/(nir+ 6*red - 7.5* blue +1))',
                {'nir': image.select('SR_B8'),
                 'red': image.select('SR_B4'),
                 'blue': image.select('SR_B2')}
            ).rename('EVI')


        elif self.collection_id == 'Landsat8':
            evi = image.expression(
                '(2.5 * (nir–red) / (nir + 6 * red – 7.5 * blue + 1)',  # Change to Landsat8 here!
                {'nir': image.select('SR_B5'),
                 'red': image.select('SR_B4'),
                 'blue': image.select('SR_B2')}
            ).rename('EVI')

        return image.addBands(evi)

    def ndvi_collection(self):
        """Maps add_ndvi() to the image collection."""
        self.collection = self.collection.map(self.add_ndvi)

    def evi_collection(self):
        """Maps add_evi() to the image collection."""
        self.collection = self.collection.map(self.add_evi)

    def reduce_ndvi_mean(self):
        """Reduces the time-series collection based on the ROI using NDVI band and mean.

        Attributes reducer and df get assigned.
        """
        # Check if NDVI in collection 
        if not 'NDVI' in x.collection.first().bandNames().getInfo():
            raise ValueError(f"No NDVI band found. Use ndvi_collection method first to calculate NDVI")
            
        aoi = self.bound()

        def aoi_ndvi_mean(image, aoi=aoi):
            """Calculates NDVI mean for a given image based on AOI.
            Inner function of reduce_ndvi_mean().

                Parameters:
                    image (ee.Image): Input image.
                    aoi (ee.Geometry): AOI geometry.
                Returns:
                    feature (ee.Feature): Feature that stores the time-stamp and mean NDVI.
            """
            # Extract the date from the image metadata
            date = ee.Date(image.get('system:time_start')).format("YYYY-MM-dd", 'UTC')

            # Calculate the mean NDVI value within the AOI
            mean = image.select('NDVI').reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=aoi
            ).get('NDVI')

            # Return the date and mean NDVI as a feature
            return ee.Feature(None, {
                'date': date,
                'mean_ndvi': mean
            })

        features = self.collection.map(aoi_ndvi_mean).getInfo()

        # Extract dates and mean NDVI values from the feature collection
        dates = [feature['properties']['date'] for feature in features['features']]
        mean_ndvi = [feature['properties']['mean_ndvi'] for feature in features['features']]

        # Create a DataFrame from the extracted data
        df = pd.DataFrame({
            'Date': dates,
            'Mean_NDVI': mean_ndvi
        })

        # Sort the DataFrame by date
        df_sorted = df.sort_values(by='Date')

        self.df = df_sorted
        self.reducer = 'NDVI_MEAN'

    def plot(self):
        """Standard plotting function for the geoindexity time-series object."""
        if not self.reducer:
            raise ValueError(f"Time-series not reduced yet. Use reducer function based on your selected Index")
        
        if self.reducer == 'NDVI_MEAN':
            plt.figure(figsize=(10, 5))
            plt.plot(self.df['Date'], self.df['Mean_NDVI'], marker='o', linestyle='--')
            plt.title('Mean NDVI Time Series')
            plt.xlabel('Date')
            plt.xticks(rotation=45)
            plt.ylabel('Mean NDVI')
            plt.yticks(np.arange(-1, 1, 0.5))
            plt.grid(True)
            plt.show()
            

    def export_image_to_drive(self, image, description, folder='earth_engine_exports'):
        """Exports a single image to Google Drive.

        Parameters:
            image (ee.Image): Image to export.
            description (str): Description for the exported image.
            folder (str): Folder name in Google Drive where the image will be exported (default: 'earth_engine_exports').
        """
        task = ee.batch.Export.image.toDrive(image=image,
                                             description=description,
                                             folder=folder,
                                             scale=30,  # Adjust scale as needed
                                             region=self.bound())
        task.start()

        print(f'Exporting {description} to Google Drive...')
        print(f'Export task id: {task.id}')
    
    def export_image_collection_to_drive(self, description, folder='earth_engine_exports'):
        """Exports the entire image collection to Google Drive as a single zip file.

        Parameters:
            description (str): Description for the exported image collection.
            folder (str): Folder name in Google Drive where the zip file will be exported (default: 'earth_engine_exports').
        """
        images = self.collection.toList(self.collection.size())
        task = ee.batch.Export.image.toDrive(imageCollection=images,
                                             description=description,
                                             folder=folder,
                                             fileFormat='GeoTIFF',
                                             region=self.bound())
        task.start()

        print(f'Exporting {description} to Google Drive...')
        print(f'Export task id: {task.id}')

    def export_plot_to_drive(self, description, folder='earth_engine_exports'):
        """Exports the current plot to Google Drive as a PNG file.

        Parameters:
            description (str): Description for the exported plot.
            folder (str): Folder name in Google Drive where the plot will be exported (default: 'earth_engine_exports').
        """
        plt.figure(figsize=(10, 5))
        plt.plot(self.df['Date'], self.df['Mean_NDVI'], marker='o', linestyle='--')
        plt.title('Mean NDVI Time Series')
        plt.xlabel('Date')
        plt.xticks(rotation=45)
        plt.ylabel('Mean NDVI')
        plt.yticks(np.arange(-1, 1, 0.5))
        plt.grid(True)

        # Save the plot to a temporary file
        temp_file = 'plot.png'
        plt.savefig(temp_file)
        plt.close()

        # Export the plot file to Google Drive
        task = ee.batch.Export.table.toDrive(collection=ee.FeatureCollection([]),
                                             description=description,
                                             folder=folder,
                                             fileFormat='png',
                                             selectors=['Date', 'Mean_NDVI'])
        task.start()

        print(f'Exporting {description} plot to Google Drive...')
        print(f'Export task id: {task.id}')

def download_plot_local(obj, fig_name='plot.png'):
    """
    Generates and saves a plot locally.

    Parameters:
    - obj: Geoindexity
        The Geoindexity object containing the data to plot.
    - fig_name: str, optional
        The filename to save the plot as (default is 'plot.png').
    """
    plt.figure(figsize=(10, 5))
    plt.plot(obj.df['Date'], obj.df['Mean_NDVI'], marker='o', linestyle='--')
    plt.title('Mean NDVI Time Series')
    plt.xlabel('Date')
    plt.xticks(rotation=45)
    plt.ylabel('Mean NDVI')
    plt.grid(True)
    plt.savefig(fig_name)
    plt.close()

    # Print a message indicating where the file is saved
    print(f'Plot saved as: {fig_name}')
