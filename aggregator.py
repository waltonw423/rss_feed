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
    "https://blogs.kent.ac.uk/polir-news/feed/",
    "https://www.atlanticcouncil.org/feed/",
    "https://www.csis.org/rss.xml",
    "https://www.rusi.org/rss/latest-commentary.xml",
    "https://www.rusi.org/rss/latest-publications.xml",
    "https://foreignpolicy.com/category/the-reading-list/feed/",
    "https://foreignpolicy.com/category/world-brief/feed/",
    "https://foreignpolicy.com/category/situation-report/feed/",
    "https://foreignpolicy.com/tag/editors-picks/feed/",
    "https://www.crisisgroup.org/rss/139",
    "https://www.crisisgroup.org/rss",
    "https://www.crisisgroup.org/rss/56",
    "https://www.justsecurity.org/feed/",
    "https://kyivindependent.com/news-archive/rss/",
    "https://www.nytimes.com/svc/collections/v1/publish/https://www.nytimes.com/topic/destination/ukraine/rss.xml",
    "https://eurasianet.org/rss",
    "https://theconversation.com/us/world/articles.atom",
    "https://jamestown.org/feed/"
]
# keywords that indicate analysis, commentary, or academic content
KEYWORDS = [
    "op-ed", "opinion", "commentary", "analysis", "essay", "investigation",
    "report", "long read", "explainer", "policy brief", "research", "think tank",
    "paper", "review", "insight", "perspective", "viewpoint"
]

# region or topic keywords for filtering
REGION_KEYWORDS = [
    "russia", "ukraine", "eurasia", "central asia", "kazakhstan", "kyrgyzstan",
    "uzbekistan", "tajikistan", "turkmenistan", "post-soviet", "nato",
    "security", "sanctions", "diplomacy", "foreign policy"
]

entries = []
for url in FEEDS:
    print(f"Parsing {url}...")
    d = feedparser.parse(url)
    if d.bozo:
        print(f"⚠️  Problem parsing {url}: {d.bozo_exception}")
        continue
    for e in d.entries:
        try:
            pub_date = getattr(e, "published_parsed", None)
            if not pub_date:
                pub_date = getattr(e, "updated_parsed", None)
            entries.append({
                "title": e.get("title", "No title"),
                "link": e.get("link", ""),
                "description": getattr(e, "summary", ""),
                "pubDate": pub_date
            })
        except Exception as ex:
            print(f"❌ Error parsing entry from {url}: {ex}")
            continue
# removed duplicate import (already imported at top)

def get_entry_date(entry):
    pd = entry.get("pubDate")
    if pd:
        try:
            # ensure timezone-aware datetime for consistent comparisons
            return datetime(*pd[:6], tzinfo=timezone.utc)
        except Exception:
            pass
    # fallback: current UTC time if no valid date
    return datetime.now(timezone.utc)


def compute_priority(entry):
    """Higher score for entries whose description contains keywords.
    Analysis keywords are weighted higher than region keywords.
    """
    text = (entry.get("description", "") or "").lower()
    analysis_hits = sum(1 for k in KEYWORDS if k in text)
    region_hits = sum(1 for k in REGION_KEYWORDS if k in text)
    return analysis_hits * 2 + region_hits

# prioritize by keyword score first, then by recency
entries.sort(key=lambda e: (compute_priority(e), get_entry_date(e)), reverse=True)
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