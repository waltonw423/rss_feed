import feedparser, PyRSS2Gen, os
from datetime import datetime, timezone

# list of source feeds
FEEDS = [
    "https://news.ycombinator.com/rss",
    "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
    "https://www.reddit.com/r/energy/.rss",
    "https://feeds.bbci.co.uk/news/world/rss.xml",
    "https://www.theguardian.com/world/rss",
    "https://apnews.com/news-sitemap-content.xml",
    "https://www.washingtonpost.com/rss",
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
    "https://smallwarsjournal.com/feed/",
    "https://www.thediplomat.com/feed/",
    "https://www.chathamhouse.org/path/83/feed.xml",
    "https://www.chathamhouse.org/path/events.xml",
    "https://www.chathamhouse.org/path/news-releases.xml"
    "https://feeds.feedburner.com/CarnegieCouncilResourcesRssFeed",
    "https://feeds.feedburner.com/carnegiecouncil/newsFeed",
    "https://ecfr.eu/feed/",
    "https://foreignpolicyblogs.com/feed/",
    "https://www.fpri.org/feed/",
    "https://www.cjfp.org/rss/",
    "https://ucleuropeblog.com/category/foreign-policy-security/feed/",
    "https://blogs.fcdo.gov.uk/feed/",
    "https://medium.com/feed/tag/foreign-policy",
    "https://www.diplomatie.gouv.fr/spip.php?page=backend&id_rubrique=53404/feed",
    "https://www.thenation.com/subject/foreign-policy/feed/",
    "https://www.politico.eu/tag/foreign-policy/feed/",
    "https://www.foreignaffairs.com/rss.xml",
    "https://www.foreignpolicyjournal.com/feed/",
    "https://www.e-ir.info/feed/",
    "https://blogs.lse.ac.uk/internationalrelations/feed/",
    "https://www.internationalaffairs.org.au/feed/atom/",
    "https://medium.com/feed/international-affairs-blog",
    "https://blogs.kent.ac.uk/polir-news/feed/"
]

entries = []
for url in FEEDS:
    try:
        print(f"Parsing {url}...")
        d = feedparser.parse(url)
        if d.bozo:
            print(f"⚠️  Problem parsing {url}: {d.bozo_exception}")
            continue
        for e in d.entries:
            entries.append({
                "title": e.get("title", "No title"),
                "link": e.get("link", ""),
                "description": getattr(e, "summary", ""),
                "pubDate": getattr(e, "published_parsed", getattr(e, "updated_parsed", None))
            })
    except Exception as ex:
        print(f"❌ Error parsing {url}: {ex}")
        continue

# ✅ FIX: Safely handle missing or malformed date fields
from datetime import datetime

def get_entry_date(entry):
    pd = entry.get("pubDate")
    if pd:
        try:
            return datetime(*pd[:6])
        except Exception:
            pass
    # fallback: current UTC time if no valid date
    return datetime.now(timezone.utc)

entries.sort(key=get_entry_date, reverse=True)
entries = entries[:50]  # limit output

rss = PyRSS2Gen.RSS2(
    title="William's Aggregated Feed",
    link="https://example.com",
    description="Merged RSS feed",
    lastBuildDate=datetime.now(timezone.utc),
    items=[
        PyRSS2Gen.RSSItem(
            title=e["title"],
            link=e["link"],
            description=e["description"],
            guid=PyRSS2Gen.Guid(e["link"]),
            pubDate=get_entry_date(e)
        )
        for e in entries
    ]
)

rss.write_xml(open("aggregated_feed.xml", "w", encoding="utf-8"))
print("✅ Feed generated:", os.path.abspath("aggregated_feed.xml"))