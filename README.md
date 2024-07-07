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
    "name": "noname",
    "http": "<addr>",
    "https": "<addr>"
  }
]
```
- Create `twitter.json` file with at least one account cookies if you consider running for Twitter
```json
[
  {
    "auth_token":"<auth token>",
    "ct0":"<csrf token>"
  }
]
```
- Run
```
python3 main.py
```