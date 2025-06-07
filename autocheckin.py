import os
import requests
import json
import logging
from urllib.parse import urlparse, parse_qs

logging.basicConfig(
    level=logging.INFO,  
    format='%(asctime)s - %(levelname)s - %(message)s'
)

API_ENDPOINTS = {
    "Honkai: Star Rail": "https://sg-public-api.hoyolab.com/event/luna/os/sign?act_id=e202303301540311"
    # "Zenless Zone Zero": "https://sg-public-api.hoyolab.com/event/luna/zzz/os/sign?act_id=e202406031448091"
}

HTTP_GAME_HEADER = {
    "Honkai: Star Rail": "hsr",
    "Zenless Zone Zero": "zzz"
}

class DiscordWebhook:
    def __init__(self):
        self.webhookURL = os.getenv("WEBHOOK_URL")
        self.iconURL = {
            "Honkai: Star Rail":"https://i.imgur.com/o0hyhmw.png",
            "Zenless Zone Zero":"https://preview.redd.it/zenless-zone-zero-icon-v0-9ss6qz6tuwx81.png?width=1080&crop=smart&auto=webp&s=3818f47bf93f33a46ec714258e552ac0363873c6"
        }

        if not self.webhookURL:
            logging.error("WEBHOOK_URL not provided in environment variables")
            raise ValueError("Missing required environment variable: WEBHOOK_URL")
    
    def _generateEmbed(self, game):
        return {
            "title": game + " Auto Check-in",
            "author": {
                "name": game,
                "icon_url": self.iconURL[game]
            },
            "description": f"Check-in completed for {game}",
            "color": 0xBB0BB5,
            "footer": {
                "text": game + " Auto Check-in"
            }
        }

    def send(self, game):
        headers = {"Content-Type": "application/json"}
        embed = self._generateEmbed(game)
        payload = {
            "embeds": [embed],
            "username": "Auto check-in bot",
        }

        try:
            res = requests.post(self.webhookURL, data=json.dumps(payload), headers=headers)

            if res.status_code == 204:
                logging.info("Successfully sent to discord webhook!")
            else:
                logging.error(f"Failed to send to Discord, status code: {res.status_code}")
         
        except requests.exceptions.RequestException as e:
            logging.error(f"Discord webhook error: ': {e}")

class CheckIn:
    def __init__(self):
        self.cookie = os.getenv("COOKIE")
        self.userAgent = "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36"
        self.discord = DiscordWebhook()

        if not self.cookie:
            logging.error("COOKIE not provided in environment variables")
            raise ValueError("Missing required environment variable: COOKIE")
    
    def sign(self, game, endpoint):
        parsed = urlparse(endpoint)
        act_id = parse_qs(parsed.query).get("act_id", [None])[0]
        if not act_id:
            raise ValueError(f"Missing act_id for {game}")

        payload = {
            "act_id": act_id,
            "lang": "en-us"
        }

        headers = {
            "User-Agent": self.userAgent,
            "Cookie": self.cookie,
            "Content-Type": "application/json;charset=UTF-8",
            "Origin": "https://act.hoyolab.com",
            "Referer": "https://act.hoyolab.com",
            "x-rpc-signgame": HTTP_GAME_HEADER[game]
        }

        try:
            res = requests.post(endpoint, headers=headers, json=payload)
            if res.status_code != 200:
                logging.error(f"HTTP error: {res.status_code}")
                return

            body = res.json()
            code = str(body.get("retcode", ""))
            if code == "0":
                logging.info("Check-in successful!")
                self.discord.send(game)
            elif code == "-5003":
                logging.info("Already checked in today.")
                self.discord.send(game)
            else:
                logging.error(f"API error: {body.get('message')}")
                logging.error(f"Full response: {json.dumps(body, indent=2)}")
        except Exception as e:
            logging.error(f"Check-in error: {e}")

if __name__ == "__main__":
    checker = CheckIn()
    for game, endpoint in API_ENDPOINTS.items():
        logging.info(f"--- Checking in for {game} ---")
        checker.sign(game, endpoint)
    
    logging.info("--- Script completed, exiting now ---")
