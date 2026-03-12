import requests

CLIENT_ID = "uE7sqhcGr6Y3pXoM2o62g"
CLIENT_SECRET = "xrOsFGHT9pNkCLCg6Cies6TXdvCIUMLy27dEJJO4"

# We will test three common ways Xweather identifies your station
ids_to_test = ["KCOARVAD722", "pws:KCOARVAD722", "4C:EB:D6:1E:22:57"]

for s_id in ids_to_test:
    print(f"🔍 Testing Station ID: {s_id}...")
    url = f"https://data.api.xweather.com/observations/{s_id}"
    params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    
    try:
        r = requests.get(url, params=params)
        data = r.json()
        if data.get('success'):
            print(f"✅ SUCCESS! Found data for {s_id}")
            print(f"🌡️ Current Temp: {data['response']['ob']['tempF']}°F")
            break # Stop once we find the right one
        else:
            error_msg = data.get('error', {}).get('description', 'Unknown Error')
            print(f"❌ Failed for {s_id}: {error_msg}")
    except Exception as e:
        print(f"⚠️ Connection error: {e}")
