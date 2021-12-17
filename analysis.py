# Steffi Hung
# Mountain Biogeography
# Fall 2021
# Final Project
# Method combines lake and river data before combining with basin data

print("Starting analysis.")

# Importing
import pandas as pd
import contextily as cx
import geopandas as gpd

# Opening dataset
usbas = gpd.read_file(
    './Input/Basins/US Basins/Sedimentary Basins/SedimentaryBasins_US_May2011_v2.shp'
).drop(
    [
        'Area_sq_km', 
        'Area_sq_mi', 
    ], 
    axis = 1
).rename(
    columns={
        "NAME": "BASIN"
    }
)
# Dropping a bunch 'o basins
usbas = usbas.drop([4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 23, 25, 26, 27, 28, 29, 30, 31])

#

# EDITING DELAWARE SUBBASIN TO FIT INTO INTEREST LIST
# Delaware basin (which is subbasin of the permian and thus kind of included in above)
dela = gpd.read_file(
    './Input/Basins/US Basins/Sedimentary Basins/Delaware/ShalePlay_Delaware_Boundary_EIA_201909.shp'
).drop(
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
).rename(
    columns={
        "Shale_play": "BASIN"
    }
)
# Changes 'NAME' of Delaware to DELAWARE
dela.at[0, "BASIN"] = "DELAWARE"

#

#Western Canada Sedimentary Basin
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

wcsb = wcsb.to_crs(4326)
# creates separate data frame to preserve component pieces
w_sub = wcsb[['BASIN', 'geometry']]

# Changes name of subcomponents of basin so they can be dissolved
wcsb.at[0, "BASIN"] = "WESTERN CANADA SEDIMENTARY BASIN"
wcsb.at[1, "BASIN"] = "WESTERN CANADA SEDIMENTARY BASIN"
wcsb.at[2, "BASIN"] = "WESTERN CANADA SEDIMENTARY BASIN"
wcsb.at[3, "BASIN"] = "WESTERN CANADA SEDIMENTARY BASIN"
wcsb.at[4, "BASIN"] = "WESTERN CANADA SEDIMENTARY BASIN"
wcsb.at[5, "BASIN"] = "WESTERN CANADA SEDIMENTARY BASIN"

wcsb = wcsb.dissolve(by='BASIN').reset_index()

#####

# NEW DATAFRAME COMBINING DELAWARE AND INTEREST
bas = usbas.append(dela)
bas = bas.append(wcsb).reset_index()
bas = bas.drop(
    columns={
        'index'
    }, axis = 1
)

# EDITING HYDRO DATA
# North American lake data
lac = gpd.read_file(
    './Input/Hydro/North American Lakes/hydrography_p_lakes_v2.shp'
).drop(
    ['OBJECTID', 
    'UIDENT',
    'TYPE',
    'COUNTRY',
    'NAMEFR', 
    'NAMESP', 
    'EDIT_DATE', 
    'EDIT',
    'Shape_Leng',
    'Shape_Area' 
    ], 
    axis = 1
).dropna().reset_index() 
lac = lac.drop(
    columns={
        'index'
    }, axis = 1
)
# Setting category to lake
lac['TYPE'] = 'LAKE' 

# EDITING RIVERS
riv = gpd.read_file(
    './Input/Hydro/North American Rivers/hydrography_l_rivers_v2.shp').drop(
    [
        'NAMEFR',
        'UIDENT',
        'TYPE',
        'COUNTRY',
        'NAMEFR', 
        'NAMESP', 
        'EDIT_DATE', 
        'EDIT',
        'Shape_Leng' 
    ], 
    axis = 1
).dropna().reset_index()
riv = riv.drop(
    columns={
        'index'
    }, axis = 1
)
# Setting category to river
riv['TYPE'] = 'RIVER'

#####

# NEW DATA FRAME combining rivers and lakes
# list of gdfs to concat
hyd_ls = [riv, lac]
# concat the gdfs
hydro = gpd.GeoDataFrame(
    pd.concat(
        hyd_ls, 
        ignore_index=True
    ), 
    crs=hyd_ls[0].crs
)
# sorting gdf by name in english
hydro = hydro.sort_values(
    by='NAMEEN'
).reset_index() # and resetting index
# renaming name in english column to name
hydro = hydro.rename(
    columns={
        "NAMEEN": "NAME"
    }
)
# Deleting old index column
hydro = hydro.drop(
    [
        'index'
    ], 
    axis = 1
)

# Changing column order
hydro = hydro[
    [
        'NAME', 
        'TYPE',
        'geometry',  
    ]
]
# Dropping duplicates
hydro = hydro.drop_duplicates(
    subset=[
        'NAME'
    ]
)
hydro = hydro.reset_index().drop(
    [
        'index'
    ], 
    axis = 1
)

hydro = hydro.to_crs(4326)

#####################

# Faults 
fault_q = gpd.read_file(
    "./Input/Faults/SHP/Qfaults_US_Database.shp").drop(
    columns={
        'section_na',
        'fault_id',
        'section_id',
        'dip_direct',
        'slip_sense',
        'strike',
        'fault_leng',
        'review_dat',
        'fault_url',
        'ref_id',
        'Shape_Leng',
        'Location',
        'linetype',
        'age',
        'slip_rate',
        'scale',
        'cooperator',
        'earthquake',
        'symbology',
        'class',
        'certainty'
    }
).rename(
    columns={
        'fault_name': 'FAULT'
    }
)

fault_area = gpd.read_file(
    "./Input/Faults/SHP/fault_areas.shp"
    ).drop(
    columns={
        'fault_id',
        'age',
        'section_id',
        'slipsense',
        'cooperator',
        'url',
        'ref_id',
        'Shape_Leng',
        'Shape_Area'
    }
).rename(
    columns={
        'name': 'FAULT'
    }
)

fault_ca = gpd.read_file(
    "./Input/Faults/SHP/ca_offshore.shp"
    ).drop(
    columns={
        'FAULT_ZONE',
        'SECTION_NA',
        'OTHER_NAME',
        'FAULT_ID',
        'SLIP_RATE',
        'SLIP_SENSE',
        'SHAPE_LENG',
        'MAPPED_SCA',
        'LINE_TYPE',
        'EXPRESSION',
        'FLT_SOURCE',
        'Location',
        'Section_ID',
        'FLT_AGE'
    }
).rename(
    columns={
        'FAULT_NAME': 'FAULT',
    }
)

faults = fault_area
faults = faults.append(fault_ca)
faults = faults.append(fault_q)

# Isolating lakes and rivers in basins
basin_hydro = hydro.sjoin(bas).drop(
    [
        'index_right',
    ], 
    axis = 1
)
# Changing column order
basin_hydro = basin_hydro[
    [
        'NAME', 
        'TYPE',
        'BASIN',
        'geometry',  
    ]
]

basin_hydro_gpd = gpd.GeoDataFrame(basin_hydro)

basin_hydro = basin_hydro.sort_values(
    by='BASIN'
).reset_index()

basin_hydro = basin_hydro.drop(
    [
        'index'
    ], 
    axis=1
)

# Fault basin join
flt_bas = faults.sjoin(bas)
flt_bas = flt_bas.drop(
    columns={
        'index_right'
    }
)
flt_bas = flt_bas[
    [
        'FAULT',
        'BASIN',
        'geometry'
    ]
]

fault_agg = flt_bas.dissolve(by="BASIN").reset_index()
fault_agg = fault_agg[
    [
        'BASIN',
        'FAULT',
        'geometry'
    ]
]

#

# Analyzing data
print("Calculating number of unique lakes and rivers that would work for data collection.")
uniq_hydro = pd.unique(
    basin_hydro[
        'NAME'
    ]
)
uniq_hydro = pd.DataFrame(uniq_hydro)
num = uniq_hydro.count()
num = int(num)
print()
print(f"There are {num} rivers and lakes in the basins of interest.")

#

#Maps
print("Printing map of rivers by basin of interest.")
ax = basin_hydro.plot(
    column = 'BASIN', 
    figsize = (10,10), 
    alpha = 0.5,  
)
gdf2 = basin_hydro.to_crs(3857)
ax1 = gdf2.plot(
    column = 'BASIN', 
    figsize = (10,10), 
    alpha = 0.5, 
    legend = True, 
    legend_kwds={
        'bbox_to_anchor': (1, 1)
        } 
)
back_hydro = cx.add_basemap(
    ax1, 
    source=cx.providers.Stamen.TonerLite
)
ax.set_axis_off()

#

print("Analysis complete.")
