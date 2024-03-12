import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Prepare DataFrame for season and weather
def create_season_df(df):
    season_df = all_df.groupby(by="season").instant.nunique().reset_index()
    season_df.rename(columns={
        "instant": "cnt"
    }, inplace=True)
    
    return season_df

def create_weather_df(df):
    weather_df = all_df.groupby(by="weathersit").instant.nunique().reset_index()
    weather_df.rename(columns={
        "instant": "cnt"
    }, inplace=True)
    
    return weather_df

# Load cleaned data
all_df = pd.read_csv("day.csv")

# Generate season_df
season_df = create_season_df(all_df)
weather_df = create_weather_df(all_df)

# Mapping Season Labels
season_mapping = {1: 'Springer', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
weather_mapping = {1: 'Clear',2: 'Mist',3: 'Light Snow',4: 'Heavy Rain'}

# Replace numeric labels with season names
season_df['season'] = season_df['season'].replace(season_mapping)

# Handling missing label for 'Heavy Rain'
weather_df['weather_label'] = weather_df['weathersit'].map(weather_mapping)

extra_row = pd.DataFrame({'weathersit': [4], 'cnt': [0], 'weather_label': ['Heavy Rain']})
weather_df = pd.concat([weather_df, extra_row], ignore_index=True)

# Preperae colors Bar Plot
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

# customer demographic
st.subheader("Rental Demographics")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(100,50))

    sns.barplot(
        y="cnt", 
        x="season",
        data=season_df.sort_values(by="cnt", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Number of Rental by Season", loc="center", fontsize=100)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=80)
    ax.tick_params(axis='y', labelsize=80)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(100,50))

    sns.barplot(
    y="cnt",
    x="weather_label",
    hue="weathersit",
    data=weather_df.sort_values(by="cnt", ascending=False),
    palette=colors,
    order=['Clear', 'Mist', 'Light Snow', 'Heavy Rain'],
    ax=ax
    )
    ax.set_title("Number of Rental by Weather", loc="center", fontsize=100)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=80)
    ax.tick_params(axis='y', labelsize=80)
    st.pyplot(fig)