import ee
ee.Initialize()

class Landsat:
    def __init__(self, roi, start_date, end_date, collection_id, properties=None):
        self.roi = roi
        self.start_date = start_date
        self.end_date = end_date
        self.collection_id= collection_id
        self.properties = properties or {}

    def bound(self):
        return ee.Geometry.Rectangle(self.roi) 
    
    def select_product(self):
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
        missions = {
            'LANDSAT_1': ('1972-07-23', '1975-01-22'),
            'LANDSAT_2': ('1975-01-22', '1978-03-05'),
            'LANDSAT_3': ('1978-03-05', '1982-07-16'),
            'LANDSAT_4': ('1982-07-16', '1984-03-01'),
            'LANDSAT_5': ('1984-03-01', '2012-05-05'), 
            'LANDSAT_8': ('2013-03-18', '2021-10-30'),
            'LANDSAT_9': ('2021-10-31', 'present')
        }


    

    def number_of_images(self):
        print(f'Total Landsat images collected: {self.select_product().size().getInfo()}')
    
class Sentinel:
    def __init__(self, roi, start_date, end_date, collection_id, properties=None):
        self.roi = roi
        self.start_date = start_date
        self.end_date = end_date
        self.collection_id= collection_id
        self.properties = properties or {}

    def bound(self):
        return ee.Geometry.Rectangle(self.roi) 
    
    def select_product(self):
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
        print(f'Total Sentinel images collected: {self.select_product().size().getInfo()}')




        