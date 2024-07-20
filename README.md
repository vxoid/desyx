# Desyx
Desyx is a tool for finding available to register OG names for services such as Discord, Instagram, Telegram, with python OG library coming inside of it.
# Credits
All develepment was done by [VXOID](https://www.instagram.com/vxoid.lostmyself/), if you're redistributing this project you MUST either credit me as @VXOID or leave link on my social media like [IG](https://www.instagram.com/vxoid.lostmyself/).
# Usage
- Go to project folder
- Install required pip packages (`requirements.txt`)
```
pip3 install -r requirements.txt
```
- Create `proxies.json` file with proxies if needed
```json
[
  {
    "name": "idk, a name",
    "scheme": "socks5 | socks4 | http",
    "hostname": "<hostname>",
    "port": 80,
    "username": "",
    "password": "",
    "trusted": true
  }
]
```
- Create `twitter_accounts.json` file with at least one account cookies if you consider running for Twitter
```json
[
  {
    "auth_token":"<auth token>",
    "ct0":"<csrf token>"
  }
]
```
- Create `telegram_accounts.json` file with at least one account credentials or folder `./sessions` with active session if you consider running for Telegram
```json
[
  {
    "session_name": "name",
    "api_id": "<apiid>",
    "api_hash": "<apihash>",
    "phone_number": "<phonenum>",
    "2fa_pass": "123456"
  }
]
```
- Setup `telegram_loggers.json` if needed
```json
[
  {
    "token": "<your telegram bot token>",
    "chat_id": "<chat id>"
  }
]
```
- Run
```
python3 main.py
```