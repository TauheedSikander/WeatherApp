import streamlit as st
import requests
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

# Page setup
st.set_page_config(page_title="Weather Forecast Dashboard", layout="wide")

# Custom dark styling (minor section header improvements + minimal glowing button)
st.markdown("""
    <style>
    .main {
        background: radial-gradient(circle at top left, #0f2027, #203a43, #2c5364);
        color: white;
        font-family: 'Poppins', sans-serif;
    }
    h1, h2, h3 {
        color: #f1f1f1;
        text-align: center;
        font-weight: 600;
    }
    .section {
        margin-top: 40px;
        margin-bottom: 20px;
        padding-bottom: 8px;
        border-bottom: 2px solid rgba(255,255,255,0.2);
    }
    .city-info {
        background: linear-gradient(135deg, rgba(255,215,0,0.06), rgba(255,215,0,0.03));
        border: 1px solid rgba(255, 215, 0, 0.12);
        border-radius: 12px;
        padding: 12px 18px;
        text-align: center;
        margin: 18px auto;
        width: 72%;
        color: #ffe082;
        font-weight: 500;
        box-shadow: 0 0 12px rgba(255, 215, 0, 0.06);
    }

    .weather-card {
        background: rgba(255, 255, 255, 0.04);
        border-radius: 14px;
        padding: 18px;
        margin: 10px;
        transition: 0.18s;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        box-shadow: 0 3px 12px rgba(255, 215, 0, 0.06);
    }
    .weather-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 6px 20px rgba(255, 215, 0, 0.10);
    }
    .temp {
        font-size: 22px;
        font-weight: 700;
        color: #FFD700;
        margin: 6px 0;
    }
    .label {
        font-weight: 500;
        color: #a8dadc;
        margin-bottom: 6px;
    }

    /* Minimal glowing button */
    div[data-testid="stButton"] > button {
        background: linear-gradient(90deg, #FFD700, #ffb703);
        color: #000;
        font-weight: 600;
        border: none;
        border-radius: 10px;
        padding: 0.5em 1.1em;
        transition: all 0.22s ease;
        box-shadow: 0 0 4px #FFD700;
    }
    div[data-testid="stButton"] > button:hover {
        transform: scale(1.03);
        box-shadow: 0 0 6px #FFD700;
    }

    /* --- Improved Section Titles --- */
    .section-title {
        font-size: 22px;
        font-weight: 600;
        text-align: center;
        color: #ffffff;
        margin-top: 45px;
        margin-bottom: 15px;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    .divider-line {
        width: 120px;
        height: 3px;
        background: rgba(255, 215, 0, 0.6);
        margin: 0 auto 25px auto;
        border-radius: 2px;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("7-Day Weather Forecast Dashboard")
st.write("Enter a city name to explore its 7-day weather forecast with clean visuals and analytical insights.")

# Input
city_name = st.text_input("Enter City Name:", "Karachi")

if st.button("Get Weather"):
    try:
        # Geocoding
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}"
        geo_data = requests.get(geo_url).json()
        info = geo_data["results"][0]
        lat, lon, timezone = info["latitude"], info["longitude"], info["timezone"]

        # City info card
        st.markdown(f"""
            <div class="city-info">
                <strong>{city_name.title()}</strong> &nbsp; | &nbsp; Lat: {lat:.4f}, Lon: {lon:.4f} &nbsp; | &nbsp; Timezone: {timezone}
            </div>
        """, unsafe_allow_html=True)

        # Forecast data
        forecast_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
            f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,"
            f"relative_humidity_2m_mean,visibility_mean&timezone=auto"
        )
        data = requests.get(forecast_url).json()

        days = data["daily"]["time"]
        max_temps = data["daily"]["temperature_2m_max"]
        min_temps = data["daily"]["temperature_2m_min"]
        precips = data["daily"]["precipitation_sum"]
        humidities = data["daily"]["relative_humidity_2m_mean"]
        visibilities = data["daily"]["visibility_mean"]

        # --- Weekly Forecast Overview Section ---
        st.markdown("<div class='section-title'>Weekly Forecast Overview</div>", unsafe_allow_html=True)
        st.markdown("<div class='divider-line'></div>", unsafe_allow_html=True)

        cards = []
        for i in range(len(days)):
            date_obj = datetime.strptime(days[i], "%Y-%m-%d")
            day_name = date_obj.strftime("%A")
            card_html = f"""
                <div class="weather-card">
                    <h3 style="margin:0;">{day_name}</h3>
                    <div class="label">{days[i]}</div>
                    <div class="temp">{max_temps[i]}°C / {min_temps[i]}°C</div>
                    <div style="color:#d1e7e7; font-size:14px; margin-top:6px;">
                        Humidity: {humidities[i]}% &nbsp; | &nbsp; Rain: {precips[i]} mm &nbsp; | &nbsp; Vis: {int(visibilities[i])} m
                    </div>
                </div>
            """
            cards.append(card_html)

        # Render cards in rows of 3; center last card if single
        i = 0
        while i < len(cards):
            chunk = cards[i:i+3]
            if len(chunk) == 3:
                c1, c2, c3 = st.columns(3)
                with c1: st.markdown(chunk[0], unsafe_allow_html=True)
                with c2: st.markdown(chunk[1], unsafe_allow_html=True)
                with c3: st.markdown(chunk[2], unsafe_allow_html=True)
            elif len(chunk) == 2:
                c1, c2 = st.columns(2)
                with c1: st.markdown(chunk[0], unsafe_allow_html=True)
                with c2: st.markdown(chunk[1], unsafe_allow_html=True)
            else:
                c_left, c_center, c_right = st.columns([1, 1.2, 1])
                with c_center: st.markdown(chunk[0], unsafe_allow_html=True)
            i += 3

        # --- Charts Section ---
        st.markdown("<div class='section-title'>Temperature & Humidity Trends</div>", unsafe_allow_html=True)
        st.markdown("<div class='divider-line'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        # Temperature Chart
        with col1:
            fig1, ax1 = plt.subplots(figsize=(7, 4))
            x = np.arange(len(days))
            width = 0.35
            bars_max = ax1.bar(x - width/2, max_temps, width, label="Max Temp (°C)", color="#FFD700", alpha=0.85)
            bars_min = ax1.bar(x + width/2, min_temps, width, label="Min Temp (°C)", color="#00b4d8", alpha=0.85)

            # Labels on bars
            for rect in bars_max:
                height = rect.get_height()
                ax1.text(rect.get_x() + rect.get_width()/2, height + 0.5, f'{int(height)}°C',
                         ha='center', va='bottom', color='black', fontsize=9,
                         bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=1))
            for rect in bars_min:
                height = rect.get_height()
                ax1.text(rect.get_x() + rect.get_width()/2, height + 0.5, f'{int(height)}°C',
                         ha='center', va='bottom', color='black', fontsize=9,
                         bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=1))

            # Axis labels and titles
            ax1.set_xticks(x)
            ax1.set_xticklabels([datetime.strptime(d, "%Y-%m-%d").strftime("%d %b") for d in days],
                                rotation=25, ha='right', color="black")
            ax1.set_facecolor("#1a1a1a")
            ax1.tick_params(colors='black')
            ax1.set_ylabel("Temperature (°C)", color="black", fontsize=10)
            ax1.set_xlabel("Date", color="black", fontsize=10)
            ax1.set_title("Daily Temperature Trends", color="black", fontsize=12, fontweight="bold")
            ax1.legend()
            ax1.grid(True, linestyle='--', alpha=0.35)
            st.pyplot(fig1)

        # Humidity Chart
        with col2:
            fig2, ax2 = plt.subplots(figsize=(7, 4))
            bars_hum = ax2.bar(np.arange(len(days)), humidities, color="#ffb703", alpha=0.9)

            # Labels on bars
            for rect in bars_hum:
                height = rect.get_height()
                ax2.text(rect.get_x() + rect.get_width()/2, height + 0.5, f'{int(height)}%',
                         ha='center', va='bottom', color='black', fontsize=9,
                         bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=1))

            # Axis labels and titles
            ax2.set_xticks(np.arange(len(days)))
            ax2.set_xticklabels([datetime.strptime(d, "%Y-%m-%d").strftime("%d %b") for d in days],
                                rotation=25, ha='right', color="black")
            ax2.set_facecolor("#1a1a1a")
            ax2.tick_params(colors='black')
            ax2.set_ylabel("Humidity (%)", color="black", fontsize=10)
            ax2.set_xlabel("Date", color="black", fontsize=10)
            ax2.set_title("Average Daily Humidity", color="black", fontsize=12, fontweight="bold")
            ax2.grid(True, linestyle='--', alpha=0.35)
            st.pyplot(fig2)

    except Exception as e:
        st.error("City not found or data unavailable. Please try again.")
        st.write(e)
