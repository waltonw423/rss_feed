import feedparser, PyRSS2Gen, datetime

# list of source feeds
FEEDS = [
    "https://news.ycombinator.com/rss",
    "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
    "https://www.reddit.com/r/energy/.rss",
    "https://feeds.bbci.co.uk/news/world/rss.xml",
    "https://www.theguardian.com/world/rss",
    "https://apnews.com/news-sitemap-content.xml",
    "https://www.washingtonpost.com/rss",
    "https://www.wsj.com/rss/articles.xml",
    "https://www.politico.com/rss/politics.xml",
    "https://foreignpolicy.com/feed/",
    "https://warontherocks.com/feed/",
    "https://thediplomat.com/feed/",
    "https://www.rferl.org/api/zbgvmtl-vomx-tpeq_kmr",
    "https://www.rferl.org/api/zbqiml-vomx-tpeqkmy",
    "https://www.rferl.org/api/zmoiil-vomx-tpeykmp",
    "https://www.rferl.org/api/zpgimml-vomx-tpe_m_my",
    "https://www.themoscowtimes.com/rss/news",
    "https://www.bellingcat.com/feed/",
    "https://www.justsecurity.org/feed/",
    "https://smallwarsjournal.com/feed/"
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
    title="William's Aggregated Feed",
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
print("Feed generated:", os.path.abspath("aggregated_feed.xml"))
