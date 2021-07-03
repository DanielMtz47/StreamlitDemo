import folium

# FOLIUM MAPS IMPLEMENTATION BASED ON:
# https://github.com/priyaavec/streamlit-demo-deploy/blob/master/streamlit_example4.py

def drawMap(avg_price_neigh):
    """Creates folium map using the geojson of  Boston. Also, the map is colored according to
        mean price.

    Args:
        avg_price_neigh ([dict]): Dictionary containing the mean prices per neighbourhood.

    Returns:
        [folium map instance]: Map instance to be drawn on streamlit.
    """
    # Locate Boston Area map
    map = folium.Map(location=[42.311145, -71.057083], tiles='CartoDB positron', name="Light Map",
                zoom_start=11, attr="My Data attribution")
    
    # Draw color map depending on average airbnb cost
    folium.Choropleth(
    # Neighbourhoods from Boston
    geo_data = f"boston.geojson",   
    name = "Boston Airbnb",
    data = avg_price_neigh,
    columns = ["neighbourhood"],
    key_on = "feature.properties.name",
    fill_color = "YlOrRd",
    fill_opacity = 0.85,
    line_opacity = .01,
    ).add_to(map)

    folium.features.GeoJson('boston.geojson',
                        name="name", popup = folium.features.GeoJsonPopup(fields=["name"])).add_to(map)
    return map

def drawLocations(map, df_filtered):
    """Plots the filtered locations into the map, the color of each location depends on its availability.

    Args:
        map ([folium map instance]): Map instance to be drawn on streamlit.
        df_filtered ([pandas dataFrame]): DataFrame containing the filtered locations.

    Returns:
        [type]: [description]
    """
    for i in df_filtered.index.values:
        # LOCATION COLOR DEPENDS ON AVAILABILITY
        if(df_filtered.availability_365[i] > 200):
            c = "#008000"
        if(df_filtered.availability_365[i] > 100 and df_filtered.availability_365[i] < 200):
            c = "#ffff00"
        if(df_filtered.availability_365[i] < 100):
            c = "#ff0000"
            
        folium.Circle( location=[ df_filtered.latitude[i], df_filtered.longitude[i] ], color = c, fill_color= c , radius = 1 ).add_to(map)
    return map