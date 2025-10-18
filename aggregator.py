import feedparser, PyRSS2Gen, datetime

# list of source feeds
FEEDS = [
    "https://news.ycombinator.com/rss",
    "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
    "https://www.reddit.com/r/energy/.rss"
]

entries = []
for url in FEEDS:
    d = feedparser.parse(url)
    for e in d.entries:
        entries.append({
            "title": e.title,
            "link": e.link,
            "description": getattr(e, "summary", ""),
            "pubDate": getattr(e, "published_parsed", datetime.datetime.now(datetime.timezone.utc).timetuple())
        })

# sort by date, newest first
entries.sort(key=lambda x: x["pubDate"], reverse=True)
entries = entries[:50]  # limit output

rss = PyRSS2Gen.RSS2(
    title="Dillon's Aggregated Feed",
    link="https://example.com",
    description="Merged RSS feed",
    lastBuildDate=datetime.datetime.now(datetime.timezone.utc),
    items=[
        PyRSS2Gen.RSSItem(
            title=e["title"],
            link=e["link"],
            description=e["description"],
            pubDate=datetime.datetime(*e["pubDate"][:6])
        ) for e in entries
    ]
)

rss.write_xml(open("aggregated_feed.xml", "w", encoding="utf-8"))
