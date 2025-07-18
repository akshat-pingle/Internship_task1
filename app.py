import requests
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime


st.title("🌤 Weather Forecast Dashboard")
st.subheader("Live 5-Day Forecast Data using OpenWeatherMap API")


city = st.text_input("Enter City Name", "Tokyo")


API_KEY = "3cf9ef9ce344e517b82b172feeba599b"  
url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"


response = requests.get(url)
data = response.json()

if response.status_code != 200 or "list" not in data:
    st.error("Failed to fetch data. Please check city name or API key.")
    st.json(data)
else:
    forecast_list = data["list"]
    dates = []
    temps = []

    for forecast in forecast_list:
        dt_txt = forecast["dt_txt"]
        temp = forecast["main"]["temp"]
        date = datetime.strptime(dt_txt, "%Y-%m-%d %H:%M:%S")
        if date.hour in [6, 12, 18]:
            dates.append(dt_txt)
            temps.append(temp)

   
    df = pd.DataFrame({"DateTime": dates, "Temperature (°C)": temps})
    st.write(df)

    
    st.subheader(f"Temperature Trend for {city}")
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=df, x="DateTime", y="Temperature (°C)", marker="o")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)
