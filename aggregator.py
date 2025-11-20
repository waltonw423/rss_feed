import feedparser, os
from email.utils import format_datetime
from datetime import datetime, timezone
import time

FEEDS = [
    # ... your feeds unchanged ...
]

KEYWORDS = [
    "op-ed", "opinion", "commentary", "analysis", "essay", "investigation",
    "report", "long read", "explainer", "policy brief", "research", "think tank",
    "paper", "review", "insight", "perspective", "viewpoint"
]

REGION_KEYWORDS = [
    "russia", "ukraine", "eurasia", "central asia", "kazakhstan", "kyrgyzstan",
    "uzbekistan", "tajikistan", "turkmenistan", "post-soviet", "nato",
    "security", "sanctions", "diplomacy", "foreign policy"
]

###########################################################
# ✔ Guaranteed pubDate extraction
###########################################################
def get_pubdate(e):
    if hasattr(e, "published_parsed") and e.published_parsed:
        dt = datetime.fromtimestamp(time.mktime(e.published_parsed), tz=timezone.utc)
        return format_datetime(dt)

    if hasattr(e, "updated_parsed") and e.updated_parsed:
        dt = datetime.fromtimestamp(time.mktime(e.updated_parsed), tz=timezone.utc)
        return format_datetime(dt)

    # raw published string
    if hasattr(e, "published") and e.published:
        return e.published

    if hasattr(e, "updated") and e.updated:
        return e.updated

    return format_datetime(datetime.now(timezone.utc))


###########################################################
# ✔ Priority computation using your keyword scheme
###########################################################
def compute_priority(entry):
    text = (entry.get("description", "") or "").lower()
    analysis_hits = sum(k in text for k in KEYWORDS)
    region_hits = sum(k in text for k in REGION_KEYWORDS)
    return analysis_hits * 2 + region_hits


entries = []

###########################################################
# ✔ Parse each feed
###########################################################
for url in FEEDS:
    print(f"Parsing {url}...")
    try:
        d = feedparser.parse(url, request_headers={
            "User-Agent": "Mozilla/5.0 (RSS aggregator)"
        })
    except Exception as e:
        print(f"⚠ Request failed: {e}")
        continue

    if d.bozo:
        print(f"⚠ Parse problem: {d.bozo_exception}")
        continue

    for e in d.entries:
        pub_date = get_pubdate(e)

        entries.append({
            "title": e.get("title", "No title"),
            "link": e.get("link", ""),
            "description": e.get("summary", ""),
            "pubDate": pub_date
        })

###########################################################
# ✔ Sort by (priority, pubDate)
###########################################################
def parse_date_str(s):
    try:
        return datetime(*feedparser._parse_date(s)[:6])
    except:
        return datetime.now()

entries.sort(
    key=lambda x: (compute_priority(x), parse_date_str(x["pubDate"])),
    reverse=True
)

entries = entries[:50]

###########################################################
# ✔ Build final RSS XML manually (your requested method)
###########################################################
items_xml = ""

for entry in entries:
    title = entry["title"]
    link = entry["link"]
    summary = entry["description"]
    guid = link
    pub_date = entry["pubDate"]

    # 🔥 THIS IS WHERE YOUR BLOCK BELONGS 🔥
    item_xml = f"""
    <item>
        <title>{title}</title>
        <link>{link}</link>
        <description><![CDATA[{summary}]]></description>
        <guid>{guid}</guid>
        <pubDate>{pub_date}</pubDate>
    </item>
    """

    items_xml += item_xml


###########################################################
# ✔ Write final RSS file
###########################################################
rss_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
    <title>William's Aggregated Feed</title>
    <link>https://example.com</link>
    <description>Merged RSS feed</description>
    <lastBuildDate>{format_datetime(datetime.now(timezone.utc))}</lastBuildDate>

    {items_xml}

</channel>
</rss>
"""

with open("aggregated_feed.xml", "w", encoding="utf-8") as f:
    f.write(rss_xml)

print("✅ Feed generated:", os.path.abspath("aggregated_feed.xml"))
