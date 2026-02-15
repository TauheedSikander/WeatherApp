# 7-Day Weather Forecast Dashboard

An interactive **Weather Forecast Dashboard** built using **Streamlit**, **Open-Meteo API**, and **Matplotlib**.  

Explore a 7-day forecast for any city with clean visuals, detailed analytics, and modern UI design.

## Live Demo

Access the live working app here: [Weather Forecast Dashboard](https://weatherapp-1.streamlit.app/)

## Features

- Search weather by city name  
- Automatic geolocation using Open-Meteo API  
- 7-Day weather forecast  
- Maximum & minimum temperature  
- Daily average humidity  
- Precipitation data  
- Visibility information  
- Interactive temperature and humidity charts  
- Modern dark themed UI with styled weather cards  
- Minimal glowing interactive button  

## Technologies Used

- **Python**  
- **Streamlit** – Web app framework  
- **Open-Meteo API** – Weather and geolocation data  
- **Matplotlib** – Data visualization  
- **NumPy** – Data processing  
- **Requests** – API calls  
- **HTML & CSS** – Custom styling for cards and sections  

## Project Structure
weather-dashboard
│
├── app.py # Main Streamlit app
├── requirements.txt # Dependencies
├── README.md # Project documentation


## How It Works

1. **City Input** – Enter a city name (default: Karachi).  
2. **Geocoding** – Fetches latitude, longitude, and timezone via Open-Meteo API.  
3. **Forecast Retrieval** – Retrieves 7-day data:
   - Max & Min temperature  
   - Precipitation  
   - Humidity  
   - Visibility  
4. **Data Visualization** – Displays:
   - Weekly weather overview cards  
   - Temperature trend bar chart  
   - Humidity trend bar chart  

## Visualizations

- **Temperature Trends:** Side-by-side bar chart for max & min temperatures with data labels  
- **Humidity Analysis:** Bar chart for average daily humidity  

## UI & Design Highlights

- Custom dark radial gradient background  
- Hover animations for weather cards  
- Minimal glowing interactive button  
- Responsive column layout  
- Section dividers and styled headers for clarity  

## Installation & Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/TauheedSikander/weather-dashboard.git
cd weather-dashboard

## Step 2: Install Dependencies

pip install -r requirements.txt

## Step 3: Run the App Locally

streamlit run app.py






