"""
Name:       Your Name
CS230:      Section XXX
Data:       Which data set you used
URL:        Link to your web application online (see extra credit)
Description:    

This program consists of a analytics dashboard implemented with streamlit.
The app loads the Airbnb locations listed on the Boston area.
The user can select which data to query and to display it as a table, or map and boxplot.
"""

import streamlit as st
from streamlit_folium import folium_static

# Streamlit Layout
st.set_page_config(layout="wide")

from map_functions import *
from data_functions import *

# Load Airbnb listing
df, avg_price_neigh = loadBostonData("airbnb.csv")
neighbourhoods = [n for n in df.neighbourhood.unique()]
neighbourhoods.append("All Neighbourhoods")
neighbourhoods.sort()

df, avg_price_neigh = loadBostonData("airbnb.csv")

def showHomepage():
    """
       Function displays the homepage.
    """
    st.markdown("<h1 style='text-align: center; color: black;'>Boston Airbnb Analytics Dashboard</h1>", unsafe_allow_html=True)
    st.text("")
    st.text("")
    st.text("")
    st.text("")
    col1, col2 = st.beta_columns(2)
    col1.text("")
    col1.text("Welcome to the analytics dashboard for Airbnb on the Boston Area.")
    col1.text("On this website you can do the following:")
    col1.text("*  Observe and filter the available Airbnb locations for rent\n on the Boston Area")
    col1.text("*  Filter places within a price range, neighbourhood,\n and availability.")
    col1.text("")
    col1.text("")
    col1.text("To use the app, select the representation and desired filter\n settings, then, click the search button.")
    col2.image("Boston.jpg", width = 450)


def main():
    """
       Function contains the sidebar content and logic of the dashboard app. The contents of the page depend on the features and
       filter settings selected by the user.
    """
    #  SIDEBAR CONTENT 
    with st.sidebar:
        st.sidebar.markdown("<h2 style='text-align: center; color: black;'>Select Neighbourhood(s)</h2>", unsafe_allow_html=True)
        st.sidebar.text("\n\n")

        form = st.form(key='my_form')
        # SELECT DATA VISUALIZATION MODE
        dataDisplay = form.radio("Data display:", ('Boston Map', 'Table'))
    
        # SHOW ALL RESULTS OR FILTER
        Filter = form.radio("Search: ", ('All data', 'Filter'))

        # FILTER SETTINGS
        form.markdown("<h2 style='text-align: center; color: black;'>Filter Results</h2>", unsafe_allow_html=True)
        form.text("")
        form.text("")

        selected_neighbourhoods = form.multiselect("Select Neighbourhood(s)", neighbourhoods)
        minNights = form.number_input("Minimum nights", 1 ,step = 1, format="%d")
        minPrice = form.number_input("Minimum price", 20 ,step = 10, format="%d")
        maxPrice = form.number_input("Maximum price", 100 ,step = 10, format="%d")

        # SUBMIT FORM 
        submit_button = form.form_submit_button(label='Search')

    # HERE LIES ALL THE LOGIC OF THE APP, 
    # THE PROGRAM DECIDES WHICH CONTENT TO SHOW, AND WHICH DATA DEPENDING ON FILTER SETTINGS
    if(submit_button):
        if(Filter == "Filter"):
            # Function call with passed parameters
            filtered_df = filterData(df, selected_neighbourhoods, [minPrice, maxPrice], minNights)
        else:
            # Function call with default parameters
            filtered_df = filterData(df)
        st.markdown("<h1 style='text-align: center; color: black;'>Boston Airbnb Locations</h1>", unsafe_allow_html=True)
        st.text("")
        st.text("")
        if(dataDisplay == "Boston Map"): 
            st.text("The boxplot below depicts the price range of the Airbnb locations per neighbourhood on the Boston area.")
            st.text("Also, the mean price per neighbourhood is shown as a red point over the boxplot. This plot may help you ")
            st.text("as a reference to find the best places (price - location) to stay on Boston.")
            st.text("")
            # CREATE BOXPLOT
            boxplot(df)
            st.text("")
            st.text("")
            st.text("The map highlights Boston's Neighbourhoods. The color depends on the mean price per neighbourhood acoording")
            st.text("to the legend displayed on the figure. Also, the locations that matched your filter settings are placed on the map.")
            st.text("The color of each location depends on the availability, green for available more than 200 days per year, yellow")
            st.text("for locations available between 100 and 200 days per year, and red for locations available less than 100 days per year.")
            st.text("")
            # SHOW MAP
            map = drawMap(avg_price_neigh)
            map = drawLocations(map, filtered_df)
            folium_static(map, width=1000, height=500)
            
        else:
            st.text("The following table shows the Airbnb locations that match the desired filter settings. Also the table is sorted")
            st.text("from least to most expensive location.")
            filtered_df.drop(["latitude", "longitude"], "columns", inplace = True)
            # SORT DATAFRAME BY PRICE AND SHOW IT
            st.write(filtered_df.sort_values("price"))
    else:
       showHomepage()



if __name__ == "__main__":
    main()