import os
import re
import time

import requests
from flask import Flask, render_template

app = Flask(__name__)

# ---------------------------------------------------------------------------
# HIER PASST DU DEINE DATEN AN
# ---------------------------------------------------------------------------

# Deine YouTube-Kanal-ID (für @max-lukatv bereits eingetragen).
# Falls du sie für einen anderen Kanal brauchst: Kanal öffnen -> Rechtsklick
# -> "Seitenquelltext anzeigen" -> nach "channelId" suchen.
CHANNEL_ID = "UCsPV0AoF_XE0paQPl85l8Bg"

# Deinen kostenlosen YouTube-API-Key hier eintragen (siehe README, Abschnitt
# "YouTube API-Key einrichten"). Alternativ als Umgebungsvariable setzen:
# Windows PowerShell:  $env:YOUTUBE_API_KEY = "dein-key"
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", "AIzaSyDEe8XyC8sSW23MJIWOiQnC3I7GsA-FKmo")

CHANNEL = {
    "name": "Max-Luka TV",
    "tagline": "Alles rund um meinen YouTube-Kanal - News, Videos und Community.",
    "bio": (
        "Hey, ich bin Max-Luka! Hier auf Max-Luka TV findest du alle Infos zu "
        "meinem YouTube-Kanal: meine neuesten Videos, die beliebtesten Uploads "
        "und wie du Teil der Community wirst. Schau vorbei und abonniere den Kanal!"
    ),
    "status": "AKTIV",
}

LINKS = [
    {
        "name": "YouTube",
        "url": "https://www.youtube.com/@max-lukatv",
        "handle": "@max-lukatv",
        "description": "Alle Videos & Uploads",
        "icon": "youtube",
    },
    {
        "name": "Instagram",
        "url": "https://www.instagram.com/max_luka_tv/",
        "handle": "@max_luka_tv",
        "description": "Mein Hauptaccount - Behind the Scenes",
        "icon": "instagram",
    },
    {
        "name": "Instagram: Schiene & Weiche",
        "url": "https://www.instagram.com/schiene_und_weiche/",
        "handle": "@schiene_und_weiche",
        "description": "Modellbahn-Content & Community",
        "icon": "instagram",
        "featured": True,
    },
    {
        "name": "WhatsApp Community",
        "url": "https://chat.whatsapp.com/JeiNjBWYGNe3rXNjxwJ2hA?s=cl&p=a&ilr=2",
        "handle": "Schiene und Weiche",
        "description": "Community beitreten & News zuerst",
        "icon": "whatsapp",
        "featured": True,
    },
]

# Events. Leer lassen, wenn gerade nichts geplant ist - die Seite zeigt dann
# automatisch einen freundlichen "aktuell keine Events"-Hinweis an.
# Beispiel für einen Eintrag:
# {
#     "date": "15.09.2026",
#     "title": "Livestream: Fragen & Antworten",
#     "description": "Ich beantworte eure Fragen live auf YouTube.",
#     "link": "https://www.youtube.com/@max-lukatv",
# },
EVENTS = []

# News/Ankündigungen für die eigene News-Seite. Neuester Eintrag zuerst.
NEWS_ITEMS = [
    {
        "date": "18.08.2026",
        "tag": "NEUES VIDEO",
        "title": "Neues Video ist online!",
        "text": "Schaut unbedingt vorbei und lasst gerne ein Like da.",
    },
    {
        "date": "10.08.2026",
        "tag": "COMMUNITY",
        "title": "WhatsApp Community gestartet",
        "text": "Ab sofort gibt's die WhatsApp-Gruppe 'Schiene und Weiche' fuer News, Umfragen und direkten Austausch.",
    },
    {
        "date": "01.08.2026",
        "tag": "ANKÜNDIGUNG",
        "title": "Neuer Upload-Plan",
        "text": "Ab jetzt gibt es regelmaessig neue Inhalte - bleibt gespannt, was als Naechstes kommt!",
    },
]

# Ziel-Marke für die Abonnenten-Fortschrittsanzeige
SUBSCRIBER_GOAL = 5000

# Link zu deinem Google Formular für Video-Einsendungen. Trage hier den
# Link ein, sobald du das Formular erstellt hast (Anleitung dazu hat dir
# Claude im Chat gegeben). Bis dahin zeigt der Button einen Hinweis an.
EINSENDUNG_FORM_URL = "https://forms.gle/Y6D38VwWpqJV5RW97"

# Schnellzugriff-Navigation (erscheint als Buttonleiste auf jeder Seite)
NAV_ITEMS = [
    {"label": "Videos", "href": "/#latest-videos"},
    {"label": "Shorts", "href": "/#latest-shorts"},
    {"label": "Playlists", "href": "/#playlists"},
    {"label": "Events", "href": "/event"},
    {"label": "News", "href": "/news"},
    {"label": "Einsendung", "href": "/einsendung"},
    {"label": "Kanäle", "href": "/#links"},
]

# Wie viele Videos/Shorts/Playlists jeweils angezeigt werden
LATEST_VIDEOS_COUNT = 5
TOP_VIDEOS_COUNT = 5
LATEST_SHORTS_COUNT = 8
TOP_SHORTS_COUNT = 8
PLAYLISTS_COUNT = 6

# Videos bis zu dieser Länge (in Sekunden) gelten als "Short". YouTube selbst
# erlaubt Shorts bis zu 3 Minuten (180 Sekunden) - die API liefert kein
# direktes "ist Short"-Flag, das ist also eine Näherung anhand der Länge.
SHORT_MAX_SECONDS = 180

# Wie viele "Seiten" à 50 Videos maximal durchsucht werden, um die
# Top-Listen zu berechnen (YouTube liefert max. 50 Videos pro Anfrage,
# hier wird so oft "nachgeblättert", bis entweder der ganze Kanal erfasst
# ist oder dieses Limit erreicht wird). 20 Seiten = bis zu 1000 Videos -
# für die allermeisten Kanäle mehr als genug, um wirklich ALLE Videos für
# die Top-Listen zu berücksichtigen, nicht nur die letzten 50 Uploads.
MAX_PAGES_TO_SCAN = 20

# Wie lange Ergebnisse zwischengespeichert werden (Sekunden), damit nicht bei
# jedem Seitenaufruf neu bei YouTube abgefragt wird (spart API-Kontingent)
CACHE_SECONDS = 600  # 10 Minuten

# ---------------------------------------------------------------------------
# YouTube-Anbindung (ab hier musst du normalerweise nichts mehr ändern)
# ---------------------------------------------------------------------------

_cache = {
    "channel_info": None,
    "channel_info_fetched_at": 0,
    "videos": None,
    "videos_fetched_at": 0,
    "playlists": None,
    "playlists_fetched_at": 0,
}


def _api_key_configured():
    return bool(YOUTUBE_API_KEY) and YOUTUBE_API_KEY != "DEIN_API_KEY_HIER"


def _parse_iso8601_duration(duration):
    """Wandelt z.B. 'PT4M13S' oder 'PT45S' in Sekunden um."""
    match = re.match(
        r"^PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?$", duration or ""
    )
    if not match:
        return 0
    hours, minutes, seconds = (int(x) if x else 0 for x in match.groups())
    return hours * 3600 + minutes * 60 + seconds


def _get_channel_info():
    """Kanal-Stammdaten: Profilbild, Titel, Abonnentenzahl, Uploads-Playlist-ID.
    Wird gecached, damit nicht bei jedem Seitenaufruf neu abgefragt wird."""
    now = time.time()
    if _cache["channel_info"] is not None and (now - _cache["channel_info_fetched_at"]) < CACHE_SECONDS:
        return _cache["channel_info"]

    resp = requests.get(
        "https://www.googleapis.com/youtube/v3/channels",
        params={
            "part": "snippet,statistics,contentDetails",
            "id": CHANNEL_ID,
            "key": YOUTUBE_API_KEY,
        },
        timeout=10,
    )
    resp.raise_for_status()
    data = resp.json()
    items = data.get("items", [])
    if not items:
        raise ValueError("Kanal nicht gefunden - CHANNEL_ID prüfen.")

    item = items[0]
    snippet = item.get("snippet", {})
    stats = item.get("statistics", {})
    thumbnails = snippet.get("thumbnails", {})
    thumb = (
        thumbnails.get("high")
        or thumbnails.get("medium")
        or thumbnails.get("default")
        or {}
    )

    info = {
        "uploads_playlist_id": item["contentDetails"]["relatedPlaylists"]["uploads"],
        "avatar": thumb.get("url", ""),
        "title": snippet.get("title", ""),
        "subscriber_count": (
            None
            if stats.get("hiddenSubscriberCount")
            else int(stats.get("subscriberCount", 0))
        ),
    }
    _cache["channel_info"] = info
    _cache["channel_info_fetched_at"] = now
    return info


def _get_uploads_playlist_id():
    return _get_channel_info()["uploads_playlist_id"]


def _fetch_recent_videos_with_stats():
    """Holt ALLE Uploads (bis MAX_PAGES_TO_SCAN Seiten) inkl. Aufrufzahlen &
    Länge, gecached für CACHE_SECONDS. Blättert dafür durch die komplette
    Upload-Playlist, damit die Top-Listen wirklich die meistgesehenen
    Videos des ganzen Kanals zeigen - nicht nur unter den letzten Uploads."""
    now = time.time()
    if _cache["videos"] is not None and (now - _cache["videos_fetched_at"]) < CACHE_SECONDS:
        return _cache["videos"]

    playlist_id = _get_uploads_playlist_id()

    # Schritt 1: alle Video-IDs einsammeln (mehrere Seiten à 50)
    video_ids = []
    page_token = None
    for _ in range(MAX_PAGES_TO_SCAN):
        params = {
            "part": "snippet",
            "playlistId": playlist_id,
            "maxResults": 50,
            "key": YOUTUBE_API_KEY,
        }
        if page_token:
            params["pageToken"] = page_token

        resp = requests.get(
            "https://www.googleapis.com/youtube/v3/playlistItems",
            params=params,
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        items = data.get("items", [])
        video_ids.extend(it["snippet"]["resourceId"]["videoId"] for it in items)

        page_token = data.get("nextPageToken")
        if not page_token:
            break

    if not video_ids:
        _cache["videos"] = []
        _cache["videos_fetched_at"] = now
        return []

    # Reihenfolge der Uploads merken (playlistItems liefert neueste zuerst)
    order = {vid: i for i, vid in enumerate(video_ids)}

    # Schritt 2: Details/Statistiken in 50er-Blöcken abrufen (API-Limit)
    videos = []
    for batch_start in range(0, len(video_ids), 50):
        batch_ids = video_ids[batch_start : batch_start + 50]

        details_resp = requests.get(
            "https://www.googleapis.com/youtube/v3/videos",
            params={
                "part": "snippet,statistics,contentDetails",
                "id": ",".join(batch_ids),
                "key": YOUTUBE_API_KEY,
            },
            timeout=10,
        )
        details_resp.raise_for_status()

        for v in details_resp.json().get("items", []):
            vid = v["id"]
            snippet = v.get("snippet", {})
            thumbnails = snippet.get("thumbnails", {})
            thumb = (
                thumbnails.get("high")
                or thumbnails.get("medium")
                or thumbnails.get("default")
                or {}
            )
            duration_seconds = _parse_iso8601_duration(
                v.get("contentDetails", {}).get("duration")
            )
            videos.append(
                {
                    "id": vid,
                    "title": snippet.get("title", ""),
                    "published_at": snippet.get("publishedAt", "")[:10],
                    "thumbnail": thumb.get("url", ""),
                    "url": (
                        f"https://www.youtube.com/shorts/{vid}"
                        if duration_seconds and duration_seconds <= SHORT_MAX_SECONDS
                        else f"https://www.youtube.com/watch?v={vid}"
                    ),
                    "views": int(v.get("statistics", {}).get("viewCount", 0)),
                    "duration_seconds": duration_seconds,
                    "is_short": bool(duration_seconds) and duration_seconds <= SHORT_MAX_SECONDS,
                }
            )

    videos.sort(key=lambda v: order.get(v["id"], 0))
    _cache["videos"] = videos
    _cache["videos_fetched_at"] = now
    return videos


def get_latest_videos():
    videos = [v for v in _fetch_recent_videos_with_stats() if not v["is_short"]]
    return videos[:LATEST_VIDEOS_COUNT]


def get_top_videos():
    videos = [v for v in _fetch_recent_videos_with_stats() if not v["is_short"]]
    return sorted(videos, key=lambda v: v["views"], reverse=True)[:TOP_VIDEOS_COUNT]


def get_latest_shorts():
    shorts = [v for v in _fetch_recent_videos_with_stats() if v["is_short"]]
    return shorts[:LATEST_SHORTS_COUNT]


def get_top_shorts():
    shorts = [v for v in _fetch_recent_videos_with_stats() if v["is_short"]]
    return sorted(shorts, key=lambda v: v["views"], reverse=True)[:TOP_SHORTS_COUNT]


def get_playlists():
    now = time.time()
    if _cache["playlists"] is not None and (now - _cache["playlists_fetched_at"]) < CACHE_SECONDS:
        return _cache["playlists"]

    resp = requests.get(
        "https://www.googleapis.com/youtube/v3/playlists",
        params={
            "part": "snippet,contentDetails",
            "channelId": CHANNEL_ID,
            "maxResults": PLAYLISTS_COUNT,
            "key": YOUTUBE_API_KEY,
        },
        timeout=10,
    )
    resp.raise_for_status()

    playlists = []
    for pl in resp.json().get("items", []):
        snippet = pl.get("snippet", {})
        thumbnails = snippet.get("thumbnails", {})
        thumb = (
            thumbnails.get("high")
            or thumbnails.get("medium")
            or thumbnails.get("default")
            or {}
        )
        playlists.append(
            {
                "id": pl["id"],
                "title": snippet.get("title", ""),
                "thumbnail": thumb.get("url", ""),
                "url": f"https://www.youtube.com/playlist?list={pl['id']}",
                "item_count": pl.get("contentDetails", {}).get("itemCount", 0),
            }
        )

    _cache["playlists"] = playlists
    _cache["playlists_fetched_at"] = now
    return playlists


def _get_channel_avatar_safe():
    """Holt das Profilbild für den Header/Unterseiten, ohne bei Fehlern
    die ganze Seite zum Absturz zu bringen (z.B. wenn YouTube gerade nicht
    erreichbar ist oder kein API-Key eingetragen wurde)."""
    if not _api_key_configured():
        return None
    try:
        return _get_channel_info()["avatar"]
    except Exception as e:
        print("YOUTUBE-FEHLER (Avatar):", repr(e))
        return None


@app.route("/ping")
def ping():
    # Leichter Endpunkt für kostenlose Wach-halte-Dienste (z.B. UptimeRobot),
    # damit die Seite bei Render nicht einschläft - ruft KEINE YouTube-API auf.
    return "OK", 200


@app.route("/")
def index():
    latest_videos = []
    top_videos = []
    latest_shorts = []
    top_shorts = []
    playlists = []
    channel_avatar = None
    subscriber_count = None
    videos_error = None

    if not _api_key_configured():
        videos_error = (
            "Kein YouTube-API-Key eingerichtet. Trage deinen Key in app.py "
            "(YOUTUBE_API_KEY) ein - Anleitung dazu in der README."
        )
    else:
        try:
            channel_info = _get_channel_info()
            channel_avatar = channel_info["avatar"]
            subscriber_count = channel_info["subscriber_count"]
            latest_videos = get_latest_videos()
            top_videos = get_top_videos()
            latest_shorts = get_latest_shorts()
            top_shorts = get_top_shorts()
            playlists = get_playlists()
        except requests.RequestException as e:
            print("YOUTUBE-FEHLER (Verbindung):", repr(e))
            videos_error = "Videos konnten gerade nicht geladen werden (keine Verbindung zu YouTube)."
        except Exception as e:
            print("YOUTUBE-FEHLER (Sonstiges):", repr(e))
            videos_error = "Videos konnten gerade nicht geladen werden. Prüfe API-Key und Kanal-ID."

    subscriber_remaining = None
    subscriber_progress_percent = 0
    if subscriber_count is not None:
        subscriber_remaining = max(SUBSCRIBER_GOAL - subscriber_count, 0)
        subscriber_progress_percent = min(
            100, round(subscriber_count / SUBSCRIBER_GOAL * 100)
        )

    return render_template(
        "index.html",
        channel=CHANNEL,
        links=LINKS,
        nav_items=NAV_ITEMS,
        events=EVENTS,
        latest_videos=latest_videos,
        top_videos=top_videos,
        latest_shorts=latest_shorts,
        top_shorts=top_shorts,
        playlists=playlists,
        channel_avatar=channel_avatar,
        subscriber_count=subscriber_count,
        subscriber_goal=SUBSCRIBER_GOAL,
        subscriber_remaining=subscriber_remaining,
        subscriber_progress_percent=subscriber_progress_percent,
        videos_error=videos_error,
    )


@app.route("/news")
def news():
    return render_template(
        "news.html",
        channel=CHANNEL,
        links=LINKS,
        nav_items=NAV_ITEMS,
        news_items=NEWS_ITEMS,
        channel_avatar=_get_channel_avatar_safe(),
    )


@app.route("/event")
def event():
    return render_template(
        "event.html",
        channel=CHANNEL,
        links=LINKS,
        nav_items=NAV_ITEMS,
        events=EVENTS,
        channel_avatar=_get_channel_avatar_safe(),
    )


@app.route("/einsendung")
def einsendung():
    return render_template(
        "einsendung.html",
        channel=CHANNEL,
        links=LINKS,
        nav_items=NAV_ITEMS,
        form_url=EINSENDUNG_FORM_URL,
        channel_avatar=_get_channel_avatar_safe(),
    )


if __name__ == "__main__":
    # 0.0.0.0 damit cloudflared den lokalen Server erreichen kann
    app.run(host="0.0.0.0", port=5050, debug=True)
