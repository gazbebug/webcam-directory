import json
import urllib.request
import re

print("Starting Self-Healing & Hunter Script...\n")

with open('webcams.json', 'r+') as file:
    webcams = json.load(file)
    
    for cam in webcams:
        # 1. THE HUNTER: If there is a channel ID, hunt for the newest video ID
        if cam.get('channelId'):
            url = f"https://www.youtube.com/channel/{cam['channelId']}/live"
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                response = urllib.request.urlopen(req, timeout=10)
                html = response.read().decode('utf-8')
                
                # Dig through the page code to find the new 11-letter ID
                match = re.search(r'rel="canonical" href="https://www.youtube.com/watch\?v=(.{11})"', html)
                if match:
                    new_id = match.group(1)
                    cam['youtubeId'] = new_id  # Automatically updates the ID!
                    cam['status'] = 'online'
                    print(f"✅ [HUNTED] {cam['title']} -> Found new ID: {new_id}")
                else:
                    cam['status'] = 'offline'
                    print(f"⚠️ [OFFLINE] {cam['title']} -> Channel is not currently live")
            except:
                cam['status'] = 'offline'
                print(f"❌ [ERROR] {cam['title']} -> Could not reach channel")
                
        # 2. MEGA-NETWORKS: If there is no channelId, just test the existing video ID
        elif cam.get('youtubeId'):
            url = f"https://www.youtube.com/watch?v={cam['youtubeId']}"
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                response = urllib.request.urlopen(req, timeout=10)
                html = response.read().decode('utf-8')
                
                # YouTube returns a page even if the video is dead, so we check for error text
                if 'Video unavailable' in html or 'This live event has ended' in html:
                     cam['status'] = 'offline'
                     print(f"⚠️ [OFFLINE] {cam['title']} -> Video stream ended")
                else:
                     cam['status'] = 'online'
                     print(f"✅ [CHECKED] {cam['title']} -> Stream is still active")
            except:
                cam['status'] = 'offline'

    # Save all the new IDs back to the database
    file.seek(0)
    json.dump(webcams, file, indent=2)
    file.truncate()
