# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 10:45:15 2023

@author: eric_
"""

import geocoder
import glob
from datetime import datetime
import matplotlib.pyplot as plt
from PIL import Image, ExifTags
import random

raw_pic_loc = r'C:\Users\eric_\Desktop\python_projects\photos\raw\*.jpg' #r reverses the backslashes
output_pic_loc = r'C:\Users\eric_\Desktop\python_projects\photos\final\\' #\\ needed as single \ escapes the string

def exif_tags(pic):
    #https://exiv2.org/tags.html
    for key, val in pic._getexif().items():
        if key in ExifTags.TAGS:
            print(f'{ExifTags.TAGS[key]}({key}):{val}')
    return

def degrees_to_decimal_pil(geo_dict,geo_loc=2):
    decimal = ((geo_dict[34853][geo_loc][0])
               +(geo_dict[34853][geo_loc][1]/60)
               +(geo_dict[34853][geo_loc][2]/3600))
    if ((geo_dict[34853][geo_loc-1] == 'S') or (geo_dict[34853][geo_loc-1] == 'W')):
        decimal = -decimal
    return decimal

def find_exif_geo_data(pic):
    lat = degrees_to_decimal_pil(pic._getexif(),2)
    long = degrees_to_decimal_pil(pic._getexif(),4)
    geo_pos = geocoder.osm([lat, long], method='reverse')
    return geo_pos

def import_pictures(raw_pic_loc):
    files = glob.glob(raw_pic_loc, recursive=True)
    return files

def rename_pictures(output_pic_loc,files,save=True):
    dates = []
    locations = None
    for f in files:
        pic = Image.open(f)
        auto = 'A'
        try:
            geo_pos = find_exif_geo_data(pic)
            country_code = geo_pos.json["country_code"].upper()
            try:
                city = geo_pos.json['town']
            except: city = geo_pos.json['city']
        except:
            city, country_code, locations = manual_location_input(pic,locations)
            auto = 'M'
        date = datetime.strptime(pic._getexif()[36867],'%Y:%m:%d %H:%M:%S').strftime('%Y-%m-%d')
        dates.append(datetime.strptime(pic._getexif()[36867],'%Y:%m:%d %H:%M:%S'))
        exif = pic.info['exif']

        rand_bit = '%06x' % random.randrange(16**6)
        if save==True:
            pic.save(f'{output_pic_loc}{date}_{city},{country_code}_{auto}_{rand_bit}.jpg', exif=exif)
    return dates, locations

def manual_location_input(pic,locations=None):
    if locations == None:
        locations = sorted(['Washington DC,US','Nagoya,JP','Estepona,ES','London,GB',
                     'Paris,FR','Amsterdam,NL','Copenhagen,DK','Stockholm,SE',
                     'Kalmar,SE','Tokyo,JP'],key=lambda s: s[0:])+['Other']
    plt.imshow(pic)
    plt.show()
    for count, value in enumerate(locations,start=1):
        print(f'{count}) {value}')
    select = input('Select Location: ')
    if int(select) == len(locations):
        new_loc = input('Write locations: ')
        locations = [new_loc] + locations
        new_city = new_loc.split(',')[0]
        new_country = new_loc.split(',')[1]
        return new_city,new_country,locations
    city = locations[int(select)-1].split(',')[0]
    country = locations[int(select)-1].split(',')[1]
    return city,country,locations

files = import_pictures(raw_pic_loc)
dates,locations = rename_pictures(output_pic_loc,files,save=True)