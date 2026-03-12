import requests, json, time
from datetime import datetime, timedelta

# YOUR WORKING WU DETAILS
STATION_ID = "KCOARVAD722"
API_KEY = "0b649979d0b348b1a49979d0b318b138"

# Date Range: 365 days
end_date = datetime.now()
start_date = end_date - timedelta(days=365)
current_date = start_date
all_history = []

print(f"🚀 Starting Weather Underground harvest for {STATION_ID}...")

while current_date <= end_date:
    date_str = current_date.strftime("%Y%m%d")
    
    # Weather Underground Daily History Endpoint
    url = f"https://api.weather.com/v2/pws/history/all?stationId={STATION_ID}&format=json&units=e&date={date_str}&apiKey={API_KEY}"
    
    try:
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            if 'observations' in data:
                obs = data['observations']
                all_history.extend(obs)
                print(f"✅ {date_str}: Added {len(obs)} records")
        elif r.status_code == 204:
            print(f"⚪ {date_str}: No data for this date.")
        else:
            print(f"❌ {date_str}: Error {r.status_code}")
            
    except Exception as e:
        print(f"⚠️ Connection error on {date_str}: {e}")
        
    current_date += timedelta(days=1)
    # WU limit is 30/min, so 2 seconds is perfect
    time.sleep(2.0)

if len(all_history) > 0:
    with open('weather_history.json', 'w') as f:
        json.dump(all_history, f, indent=2)
    print(f"✨ SUCCESS: Saved {len(all_history)} records to weather_history.json")
else:
    print("❌ FATAL: Weather Underground returned no data. Check if the API Key is active.")
