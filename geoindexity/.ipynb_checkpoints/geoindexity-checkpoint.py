"""
This script includes the core GeoIndexity classes and functions.

GeoIndexity classes and functions are based on the Earth Engine API
for Google Earth Engine (GEE). A valid GEE account is therefore
necessary to use GeoIndexity. For more information on setting up your
GEE account and using GeoIndexity, please see https://github.com/ro-hit81/GeoIndexity/blob/main/README.md
"""

import ee
ee.Initialize()

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
        self.collection_id= collection_id
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
                image_collection=image_collection.filter(ee.Filter.lte(property_name, value))
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
    properties
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
        properties
            Properties for additional filtering, such as CLOUDY_PIXEL_PERCENTAGE.
        """
        self.roi = roi
        self.start_date = start_date
        self.end_date = end_date
        self.collection_id= collection_id
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
            valid_properties = {"CLOUDY_PIXEL_PERCENTAGE": int, "CLOUDY_SHADOW_PERCENTAGE": int, "DARK_FEATURES_PERCENTAGE": int}
            for property_name, value in self.properties.items():
                if property_name not in valid_properties:
                    raise KeyError(f"Invalid property name: {property_name}. Supported properties: {', '.join(valid_properties.keys())}.")
                image_collection=image_collection.filter(ee.Filter.lte(property_name, value))
        return image_collection

    def number_of_images(self):
        """Prints the total number of images in the filtered Landsat image collection."""
        print(f'Total Sentinel images collected: {self.select_product().size().getInfo()}')




        