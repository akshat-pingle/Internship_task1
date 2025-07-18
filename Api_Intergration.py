import requests
import json
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# --- Step 1: Configuration ---
API_KEY = "3cf9ef9ce344e517b82b172feeba599b"  
CITY = "Tokyo"
URL = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric"

# --- Step 2: Fetch Data from API ---
response = requests.get(URL)
data = response.json()

# --- Step 3: Error Handling ---
if response.status_code != 200:
    print("❌ API Request Failed")
    print("Status Code:", response.status_code)
    print("Response:", json.dumps(data, indent=2))
    exit()

# --- Step 4: Extract Relevant Data ---
dates = []
temperatures = []

try:
    for forecast in data["list"]:
        dt_txt = forecast["dt_txt"]  # Date and time
        temp = forecast["main"]["temp"]  # Temperature

        # Convert date string to datetime object
        date = datetime.strptime(dt_txt, "%Y-%m-%d %H:%M:%S")

        # Collect data (e.g., every 6 hours)
        if date.hour in [6, 12, 18]:  # Optional: fewer points
            dates.append(dt_txt)
            temperatures.append(temp)
except KeyError:
    print("❌ 'list' key not found in response. Here's the full response:")
    print(json.dumps(data, indent=2))
    exit()

# --- Step 5: Data Visualization ---
plt.figure(figsize=(12, 6))
sns.lineplot(x=dates, y=temperatures, marker="o", color="blue")
plt.xticks(rotation=45)
plt.title(f"Forecasted Temperatures for {CITY}")
plt.xlabel("Date & Time")
plt.ylabel("Temperature (°C)")
plt.tight_layout()
plt.grid(True)
plt.show()
