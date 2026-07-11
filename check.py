import json
import urllib.request
import urllib.error

print("Starting Webcam Health Check...\n")

# 1. Open and read your database
with open('webcams.json', 'r') as file:
    webcams = json.load(file)

broken_cams = 0

# 2. Loop through every camera
for cam in webcams:
    title = cam.get('title', 'Unknown Camera')
    
    # Check if it has a channelId
    if 'channelId' in cam:
        url = f"https://www.youtube.com/channel/{cam['channelId']}/live"
        
        try:
            # Pretend to be a normal web browser knocking on the door
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req)
            print(f"✅ [ONLINE] {title}")
            
        except urllib.error.URLError as e:
            print(f"❌ [OFFLINE] {title} - {e.reason}")
            broken_cams += 1
    else:
        print(f"⚠️ [SKIPPED] {title} (No Channel ID provided)")

print("\n--- Health Check Complete ---")
if broken_cams > 0:
    print(f"Warning: {broken_cams} camera(s) appear to be offline.")
else:
    print("All cameras are online and healthy!")
