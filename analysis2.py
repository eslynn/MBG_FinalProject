# Steffi Hung
# Mountain Biogeography
# Fall 2021
# Final Project
# Method keeps lake and river data separate

import geopandas as gpd

# USBASINS
usbas = gpd.read_file(
    './Input/Basins/US Basins/Sedimentary Basins/SedimentaryBasins_US_May2011_v2.shp'
)
# Dropping a bunch 'o basins
usbas = usbas.drop([4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 23, 25, 26, 27, 28, 29, 30, 31])
usbas = usbas.drop(
    [
        'Area_sq_km', 
        'Area_sq_mi', 
    ], 
    axis = 1
)
usbas = usbas.rename(
    columns={
        "NAME": "BASIN"
    }
)

#DELAWARE SUBBASIN
# Delaware basin (which is subbasin of the permian and thus kind of included in above)
dela = gpd.read_file(
    './Input/Basins/US Basins/Sedimentary Basins/Delaware/ShalePlay_Delaware_Boundary_EIA_201909.shp'
)
dela = dela.drop(
    [
        'Basin', 
        'Lithology', 
        'Age_shale', 
        'Area_sq_mi', 
        'Area_sq_km',
        'Shape_Leng',
        'Shape_Area'
    ], 
    axis = 1
)
dela = dela.rename(
    columns={
        "Shale_play": "BASIN"
    }
)
dela.at[0, "BASIN"] = "DELAWARE"

#WESTERN CANADA SEDIMENTARY BASIN
wcsb = gpd.read_file(
    './Input/Basins/CA Basins/WCSB/fg0301_py_ll.shp'
).drop(
    columns={
        'MAP_NAME',
        'ID'
    }
).rename(
    columns={
        'DESCR1': 'BASIN'
    }
)

wcsb.at[0, "BASIN"] = "WESTERN CANADA SEDIMENTARY BASIN"
wcsb.at[1, "BASIN"] = "WESTERN CANADA SEDIMENTARY BASIN"
wcsb.at[2, "BASIN"] = "WESTERN CANADA SEDIMENTARY BASIN"
wcsb.at[3, "BASIN"] = "WESTERN CANADA SEDIMENTARY BASIN"
wcsb.at[4, "BASIN"] = "WESTERN CANADA SEDIMENTARY BASIN"
wcsb.at[5, "BASIN"] = "WESTERN CANADA SEDIMENTARY BASIN"

wcsb = wcsb.dissolve(by='BASIN').reset_index()
wcsb = wcsb.to_crs(4326)

# BAS APPEND
bas = usbas.append(dela)
bas = bas.append(wcsb)

# EDITING LAKES
lac = gpd.read_file(
    './Input/Hydro/North American Lakes/hydrography_p_lakes_v2.shp'
)
# Dropping uneccary columns
lac = lac.drop(
    [
        'UIDENT',
        'OBJECTID',
        'TYPE',
        'COUNTRY',
        'NAMEFR',
        'NAMESP',
        'EDIT_DATE', 
        'EDIT',
    ], 
    axis = 1
)
# lac = lac.dropna()
# lac = lac.replace([None], 'Unnamed lake') 
lac = lac.to_crs(4326)

#####

# EDITING RIVERS
riv = gpd.read_file(
    './Input/Hydro/North American Rivers/hydrography_l_rivers_v2.shp')
riv = riv.drop(
    [
        'UIDENT',
        'TYPE',
        'COUNTRY',
        'NAMEFR',
        'NAMESP',
        'EDIT_DATE', 
        'EDIT',
    ], 
    axis = 1
)
# riv = riv.dropna()
# riv = riv.replace([None], 'Unnamed river')
riv = riv.to_crs(4326)

###

hydro = lac
hydro = hydro.append(riv)

#######

bas_lac = bas.overlay(lac, how='union')
bas_lac = bas_lac.sort_values(by='NAMEEN')
bl_size = bas_lac.sort_values(by='Shape_Area', ascending=False)
bl_size = bl_size.dropna().reset_index()
bl_size = bl_size.drop(
    columns={
        'index'
    }, axis = 1
)
bl_size = bl_size.drop(
    columns={
        'geometry',
        'Shape_Leng'
    }, axis = 1
)

bas_riv = bas.overlay(riv, how='union', keep_geom_type=False)
bas_riv = bas_riv.sort_values(by='NAMEEN')

ca_lac = wcsb.overlay(lac, how="union")
ca_lac = ca_lac.sort_values(by='Shape_Area', ascending=False)
ca_lac = ca_lac.dropna()

#

import project_functions as pf
pf.cx_plot(bas_riv, 'BASIN', 15, 0.2, 'k')
pf.cx_plot(ca_lac, 'BASIN', 15, 0.2, 'k')
pf.cx_plot(bas_lac, 'BASIN', 15, 0.2, 'k')
