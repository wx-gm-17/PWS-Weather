import requests, json, time, os
from datetime import datetime, timedelta

# Your Xweather Developer Credentials
CLIENT_ID = "uE7sqhcGr6Y3pXoM2o62g"
CLIENT_SECRET = "xrOsFGHT9pNkCLCg6Cies6TXdvCIUMLy27dEJJO4"
STATION_ID = "pws:KCOARVAD722" # Note the 'pws:' prefix

# Let's start with 30 days to guarantee a fast, successful save
end_date = datetime.now()
start_date = end_date - timedelta(days=30)
current_date = start_date
all_history = []

print(f"🚀 Starting Xweather harvest for {STATION_ID}...")

while current_date <= end_date:
    date_str = current_date.strftime("%Y-%m-%d")
    url = f"https://data.api.xweather.com/observations/archive/{STATION_ID}"
    
    params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "from": date_str,
        "to": date_str,
        "limit": 1000
    }
    
    try:
        r = requests.get(url, params=params)
        data = r.json()
        
        if data.get('success') and data.get('response'):
            # Xweather nested structure: response[0]['periods']
            obs = data['response'][0].get('periods', [])
            if obs:
                all_history.extend(obs)
                print(f"✅ {date_str}: Added {len(obs)} records")
            else:
                print(f"⚪ {date_str}: No data found for this day.")
        else:
            print(f"❌ {date_str}: API Error - {data.get('error', {}).get('description', 'Unknown')}")
            
    except Exception as e:
        print(f"⚠️ Connection error on {date_str}: {e}")
        
    current_date += timedelta(days=1)
    time.sleep(0.1) # Xweather is fast!

# The "Safety Net" Save
if len(all_history) > 0:
    with open('weather_history.json', 'w') as f:
        json.dump(all_history, f, indent=2)
    print(f"✨ SUCCESS: {len(all_history)} Xweather records saved!")
else:
    print("❌ FATAL: No data found. Try removing 'pws:' from the ID if this continues.")
