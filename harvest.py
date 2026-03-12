import requests, json, time
from datetime import datetime, timedelta

# Xweather Credentials
CLIENT_ID = "uE7sqhcGr6Y3pXoM2o62g"
CLIENT_SECRET = "xrOsFGHT9pNkCLCg6Cies6TXdvCIUMLy27dEJJO4"
# Using your Arvada coordinates as the primary lookup
LOC = "39.80,-105.09"

# Calculate dates
end_date = datetime.now()
start_date = end_date - timedelta(days=30)
current_date = start_date
all_history = []

print(f"🚀 Starting Xweather harvest for {LOC}...")

while current_date <= end_date:
    date_str = current_date.strftime("%Y-%m-%d")
    url = f"https://data.api.xweather.com/observations/archive/{LOC}"
    
    params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "from": date_str,
        "to": date_str,
        "filter": "pws",
        "limit": 1000
    }

    # This 'Header' tells Xweather we are calling from your authorized domain
    headers = {
        "Referer": "https://zackhine.github.io" 
    }
    
    try:
        r = requests.get(url, params=params, headers=headers)
        data = r.json()
        
        if data.get('success') and data.get('response'):
            obs = data['response'][0].get('periods', [])
            if obs:
                all_history.extend(obs)
                print(f"✅ {date_str}: Added {len(obs)} records")
            else:
                print(f"⚪ {date_str}: No records found.")
        else:
            error_desc = data.get('error', {}).get('description', 'Unknown Error')
            print(f"❌ {date_str}: API Error - {error_desc}")
            
    except Exception as e:
        print(f"⚠️ Connection error: {e}")
        
    current_date += timedelta(days=1)
    time.sleep(0.2)

if len(all_history) > 0:
    with open('weather_history.json', 'w') as f:
        json.dump(all_history, f, indent=2)
    print(f"✨ SUCCESS: {len(all_history)} records saved to weather_history.json")
else:
    print("❌ FATAL: No data found. Xweather may not have your PWS in the archive yet.")
