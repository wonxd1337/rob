import requests
import time
import re

API = "https://discord.com/api/v9"

def get_key(token, channel_id, shortlink, timeout=60):
    url = f"{API}/channels/{channel_id}/messages"
    h = {"Authorization": token, "Content-Type": "application/json"}
    try:
        r = requests.post(url, headers=h, json={"content": f"/bypass url: {shortlink}"})
        if r.status_code != 200:
            return None
    except:
        return None
    start = time.time()
    while time.time() - start < timeout:
        try:
            resp = requests.get(f"{url}?limit=10", headers=h, timeout=5)
            if resp.status_code != 200:
                time.sleep(2)
                continue
            for m in resp.json():
                match = re.search(r'(FREE_[a-fA-F0-9]{32,})', m.get('content', ''))
                if match:
                    return match.group(1)
                if "error" in m.get('content', '').lower():
                    return None
        except:
            pass
        time.sleep(2)
    return None