import requests, json, time
from datetime import datetime, timedelta

# YOUR NEW PWS DATA
STATION_ID = "KCOARVAD722"
PWS_API_KEY = "b721730c6af0e0c5336b4883f2edf87e" # The key you just found

# Date Range
end_date = datetime.now()
start_date = end_date - timedelta(days=365)
current_date = start_date
all_history = []

print(f"🚀 Starting harvest for {STATION_ID} via PWSweather...")

while current_date <= end_date:
    date_str = current_date.strftime("%Y-%m-%d")
    
    # Direct PWSweather API call
    url = f"https://api.pwsweather.com/v1/stations/{STATION_ID}/history/daily"
    params = {
        "apiKey": PWS_API_KEY,
        "date": date_str
    }
    
    try:
        r = requests.get(url, params=params)
        data = r.json()
        
        # PWSweather structure is slightly different
        if r.status_code == 200 and 'history' in data:
            obs = data['history']
            all_history.extend(obs)
            print(f"✅ {date_str}: Added {len(obs)} records")
        else:
            print(f"⚠️ {date_str}: No records or Error {r.status_code}")
            
    except Exception as e:
        print(f"⚠️ Connection error on {date_str}: {e}")
        
    current_date += timedelta(days=1)
    time.sleep(0.2)

if len(all_history) > 0:
    with open('weather_history.json', 'w') as f:
        json.dump(all_history, f, indent=2)
    print(f"✨ SUCCESS: Saved {len(all_history)} records!")
else:
    print("❌ FATAL: Still no data. Your station might not have history stored on PWSweather yet.")
