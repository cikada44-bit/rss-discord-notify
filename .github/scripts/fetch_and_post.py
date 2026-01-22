import feedparser
import json
import os
import requests
from pathlib import Path

RSS_FEEDS = [
    "https://www.reddit.com/r/comfyui/.rss",
    "https://www.reddit.com/r/StableDiffusion/.rss",
    "https://huggingface.co/blog/feed.xml",
    "https://github.com/comfyanonymous/ComfyUI/releases.atom",
    "https://civitai.com/api/rss/models?sort=Newest",
    "https://civitai.com/api/v1/models?types=LORA&feed.xml",
]

SEEN_FILE = Path("data/seen.json")
WEBHOOK = os.getenv("DISCORD_WEBHOOK")

def load_seen():
    if SEEN_FILE.exists():
        return json.loads(SEEN_FILE.read_text())
    return []

def save_seen(seen):
    SEEN_FILE.parent.mkdir(exist_ok=True)
    SEEN_FILE.write_text(json.dumps(seen, indent=2))

def send_to_discord(title, link):
    payload = {"content": f"**{title}**\n{link}"}
    requests.post(WEBHOOK, json=payload)

def main():
    seen = load_seen()
    new_seen = set(seen)

    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            uid = entry.get("id") or entry.get("link")
            if uid not in seen:
                send_to_discord(entry.title, entry.link)
                new_seen.add(uid)

    save_seen(list(new_seen))

if __name__ == "__main__":
    main()



