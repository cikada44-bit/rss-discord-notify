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
    "https://civitai.com/api/v1/models?types=checpoint&nsfw=true&token=5b182d04bf7467cdb49e2ff5667ba621&feed.xml",
    "https://civitai.com/api/rss/models?sort=Newest",
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

def send_embed_to_discord(title, link, summary):
    # 本文はコードブロック化して翻訳対象外にする
    description = f"```\n{summary[:1500]}\n```"  # Discord の制限に合わせて長さ調整

    embed = {
        "title": title,
        "url": link,
        "description": description,
        "color": 0x00AEEF,  # 好きな色に変更可能
    }

    payload = {"embeds": [embed]}
    requests.post(WEBHOOK, json=payload)

def main():
    seen = load_seen()
    new_seen = set(seen)

    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            uid = entry.get("id") or entry.get("link")
            if uid not in seen:
                title = entry.title
                link = entry.link
                summary = entry.get("summary", "No description available.")

                send_embed_to_discord(title, link, summary)
                new_seen.add(uid)

    save_seen(list(new_seen))

if __name__ == "__main__":
    main()
