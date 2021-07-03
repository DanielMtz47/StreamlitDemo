import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random

def loadBostonData(filename):
    """Loads csv data, removes irrelevant columns and returns dataFrame.

    Args:
        filename ([string]): Name of the csv file to load.

    Returns:
        [pandas dataFrame]: Dataframe that contains the loaded dataset.
        [dictionary]: Dictionary containing the mean price per neighbourhood.
    """
    # Airbnb listings from Bostom
    df = pd.read_csv(filename, index_col= "id")
    neighbourhoods = df.neighbourhood.unique()

    # Dictionary: Neighbourhood (key) : mean_price (value)
    avg_price_perNeighborhood = {}

    df = cleanData(df)
    for neigh in neighbourhoods:
        df_neigh = df.loc[df.neighbourhood == neigh]
        # calculate average price per neighbourhood.
        avg_price_perNeighborhood[neigh] = df_neigh.price.mean()
        
    return df, avg_price_perNeighborhood


def cleanData(df):
    """Removes irrelevant columns for this analysis from the loaded dataset.

    Args:
        df ([pandas dataFrame]): dataFrame containing the loaded dataset

    Returns:
        [pandas dataFrame]: dataFrame only with essential columns.
    """
    # Drop column (Irrelevant)
    df.drop(["host_id", "host_name","neighbourhood_group", "number_of_reviews",
     "last_review", "reviews_per_month", "calculated_host_listings_count"], "columns", inplace = True)

    # Filter dataFrame 
    df = df.loc[df.price > 0]

    return df


def filterData(df, neighbourhoods = ["All Neighbourhoods"], price_range = None, minimum_nights = None):
    """Filters dataframe according to user's filters. Function returns the desired locations filtering
        neighbhourhood, price range, and minimum_nights data.

    Args:
        df ([pandas dataFrame]): Loaded dataset
        neighbourhoods (List, optional): List of neighbourhoods to filter. Defaults to "All Neighbourhoods".
        price_range ([List], optional): List containing min and max price. Defaults to None.
        minimum_nights ([List], optional): Minimum nights to stay. Defaults to None.

    Returns:
        [pandas dataFrame]: Filtered dataFrame.
    """
    
    filtered_df = pd.DataFrame([], columns= df.columns)
    if("All Neighbourhoods" not in neighbourhoods):
        for n in neighbourhoods:
            filtered_df = filtered_df.append(df.loc[df.neighbourhood == n])
    else:
        filtered_df = df

    if(price_range != None):
        filtered_df = filtered_df.loc[(filtered_df.price >= price_range[0]) & (filtered_df.price <= price_range[1])]

    if(minimum_nights != None):
        filtered_df = filtered_df.loc[filtered_df.minimum_nights <= minimum_nights]

    return filtered_df


def boxplot(df):
    """Creates a boxplot containing the prices ranges per neighbourhood.

    Args:
        df ([pandas dataFrame]): Dataframe containing all neighbourhood info.
    """
    neighbourhoods = df.neighbourhood.unique()
    neighData = []
    
    for n in neighbourhoods:
        neighData.append(df.price.loc[df.neighbourhood == n])
    
    colors = [f"#{random.randrange(0x1000000):06x}" for i in range(len(neighData))]
    fig, ax = plt.subplots(figsize=(15,5))

    # rectangular box plot
    bplot1 = ax.boxplot(neighData,
                        positions=np.array(range(len(neighData)))*2.0-0.4,
                        sym = '',
                        widths = 0.6,
                        vert=True, 
                        patch_artist=True)

    ax.set_title('Mean price per Neighbourhood',fontsize = 24)

    xa = -0.4
    for a in neighData:
        ax.scatter(xa, a.mean(), c='r')
        xa +=2

    for patch, color in zip(bplot1['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.5)

    ax.set_xlabel("Neighbourhood",fontsize = 18)
    ax.set_ylabel("Price",fontsize = 18)
    plt.xticks(range(0, len(neighbourhoods) * 2, 2), neighbourhoods, rotation='vertical')
    plt.xlim(-3, 51)

    st.pyplot(fig)



