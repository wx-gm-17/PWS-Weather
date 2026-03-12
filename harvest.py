import requests, json, time
from datetime import datetime, timedelta

# Your Credentials
CLIENT_ID = "uE7sqhcGr6Y3pXoM2o62g"
CLIENT_SECRET = "xrOsFGHT9pNkCLCg6Cies6TXdvCIUMLy27dEJJO4"
# Xweather usually requires 'pws:' before the ID
STATION_ID = "pws:KCOARVAD722" 

end_date = datetime.now()
start_date = end_date - timedelta(days=365)
current_date = start_date
all_history = []

print(f"🚀 Starting harvest for {STATION_ID}...")

while current_date <= end_date:
    date_str = current_date.strftime("%Y-%m-%d")
    # Archive endpoint
    url = f"https://data.api.xweather.com/observations/archive/{STATION_ID}"
    params = {
        "client_id": CLIENT_ID, 
        "client_secret": CLIENT_SECRET, 
        "from": date_str, 
        "limit": 1000
    }
    
    try:
        r = requests.get(url, params=params)
        data = r.json()
        
        if data.get('success') and data.get('response'):
            obs = data['response'][0].get('periods', [])
            if obs:
                all_history.extend(obs)
                print(f"✅ {date_str}: Added {len(obs)} records")
            else:
                # If no records, let's try WITHOUT the 'pws:' prefix just for this day
                print(f"⚠️ {date_str}: No records with pws: prefix, trying fallback...")
                params_fallback = params.copy()
                r_fb = requests.get(f"https://data.api.xweather.com/observations/archive/KCOARVAD722", params=params_fallback)
                fb_data = r_fb.json()
                if fb_data.get('success') and fb_data['response'][0].get('periods'):
                    all_history.extend(fb_data['response'][0]['periods'])
                    print(f"✅ {date_str}: Fallback worked!")

        time.sleep(0.3)
    except Exception as e:
        print(f"⚠️ Error on {date_str}: {e}")
        
    current_date += timedelta(days=1)

# Save only if we actually found something
if len(all_history) > 0:
    with open('weather_history.json', 'w') as f:
        json.dump(all_history, f, indent=2)
    print(f"✨ SUCCESS: Saved {len(all_history)} records to weather_history.json")
else:
    print("❌ FATAL: No data found for any variations of the ID.")
