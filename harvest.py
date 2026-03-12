import requests, json, time, os
from datetime import datetime, timedelta

# Your Credentials
CLIENT_ID = "uE7sqhcGr6Y3pXoM2o62g"
CLIENT_SECRET = "xrOsFGHT9pNkCLCg6Cies6TXdvCIUMLy27dEJJO4"
STATION_ID = "KCOARVAD722"

end_date = datetime.now()
start_date = end_date - timedelta(days=365)
current_date = start_date
all_history = []

print(f"🚀 Starting harvest for {STATION_ID}...")

while current_date <= end_date:
    date_str = current_date.strftime("%Y-%m-%d")
    url = f"https://data.api.xweather.com/observations/archive/{STATION_ID}"
    params = {"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET, "from": date_str, "limit": 1000}
    
    try:
        r = requests.get(url, params=params)
        if r.status_code == 200:
            data = r.json()
            if data.get('success'):
                obs = data['response'][0].get('periods', [])
                all_history.extend(obs)
                print(f"✅ {date_str}: Added {len(obs)} records")
        time.sleep(0.5) 
    except Exception as e:
        print(f"⚠️ Error on {date_str}: {e}")
    current_date += timedelta(days=1)

with open('weather_history.json', 'w') as f:
    json.dump(all_history, f, indent=2)

print("✨ Done! History saved to weather_history.json")