# Steffi Hung
# Mountain Biogeography
# Fall 2021
# Final project
# function(s) for use in basin analysis

def cx_plot(gdf, column, figsize, alpha, ec):
    """Creates real perty graph, make sure column name is in quotes, figsize is an integer, and alpha is a decimal under 1, k thx bye
    
    eg. cx_plot(mygdf, "column", 10, 0.5, 'k')
    """
    import contextily as cx

    ax = gdf.plot(
        column = column, 
        figsize = (figsize,figsize), 
        alpha = alpha, 
        edgecolor=ec, 
        legend=True
        )
    gdf2 = gdf.to_crs(3857)
    ax1 = gdf2.plot(
        column = column, 
        figsize = (figsize,figsize), 
        alpha = alpha, 
        edgecolor=ec, 
        legend = True, 
        legend_kwds={
            'bbox_to_anchor': (1, 1)
            }
        )
    cx.add_basemap(
        ax1, 
        source=cx.providers.Stamen.TonerLite
        )
    ax.set_axis_off()
