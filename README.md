# hoyo-auto-checkin

[![Hoyo auto check-in](https://github.com/jlgsjlgs/hoyo-auto-checkin/actions/workflows/main.yml/badge.svg)](https://github.com/jlgsjlgs/hoyo-auto-checkin/actions/workflows/main.yml)

A lightweight python script that performs automatic daily check-ins for HoYoverse games. Script currently supports HSR and ZZZ, but remains easily scalable for future additions.

## Features

- Runs daily using GitHub Actions cron scheduling  
- Sends requests to relevant HoYoverse API endpoints with necessary authentication cookies to perform automatic check-ins

## Environment Variables

These can be set locally or through GitHub Actions secrets.

| Variable    | Description                            |
|-------------|------------------------------------|
| COOKIE      | Your Hoyolab authentication cookie, ltoken_v2 and ltuid_v2|
| WEBHOOK_URL | Discord Webhook URL for notifications |

## Logging

The script uses Python’s logging module to provide structured logs:

- Success and error responses from Hoyolab’s API  
- Success and error responses from Discord Webhook

Logs are visible in the GitHub Actions job output.
