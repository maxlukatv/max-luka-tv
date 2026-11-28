import os
import re
import time
from datetime import datetime

import requests
from flask import Flask, render_template, jsonify

import signale_daten

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
EVENTS = []

# Manuelle Sonder-Ankündigungen (z.B. für Dinge, die nichts mit einem
# einzelnen Video zu tun haben). Neuester Eintrag zuerst.
NEWS_ITEMS = [
    {
        "date": "10.08.2026",
        "tag": "COMMUNITY",
        "title": "WhatsApp Community gestartet",
        "text": "Ab sofort gibt's die WhatsApp-Gruppe 'Schiene und Weiche' fuer News, Umfragen und direkten Austausch.",
    },
]

# Wie viele automatisch generierte Video/Short-News maximal angezeigt werden
AUTO_NEWS_COUNT = 12


def _format_date_de(iso_date_str):
    """Wandelt 'YYYY-MM-DD' in 'DD.MM.YYYY' um, fuer einheitliche Anzeige."""
    try:
        return datetime.strptime(iso_date_str, "%Y-%m-%d").strftime("%d.%m.%Y")
    except (ValueError, TypeError):
        return iso_date_str


def _parse_de_date(date_str):
    """Wandelt 'DD.MM.YYYY' in ein datetime-Objekt um, fuer die Sortierung."""
    try:
        return datetime.strptime(date_str, "%d.%m.%Y")
    except (ValueError, TypeError):
        return datetime.min


def get_news_items():
    auto_items = []
    try:
        for video in get_latest_videos():
            auto_items.append(
                {
                    "date": _format_date_de(video["published_at"]),
                    "tag": "NEUES VIDEO",
                    "title": video["title"],
                    "text": "Ein neues Video ist online - schau unbedingt vorbei und lass gerne ein Like da!",
                    "link": video["url"],
                }
            )
        for short in get_latest_shorts():
            auto_items.append(
                {
                    "date": _format_date_de(short["published_at"]),
                    "tag": "NEUER SHORT",
                    "title": short["title"],
                    "text": "Ein neuer Short ist online - schau ihn dir an!",
                    "link": short["url"],
                }
            )
    except Exception as e:
        print("NEWS-FEHLER (automatische Videos):", repr(e))

    all_items = list(NEWS_ITEMS) + auto_items
    all_items.sort(key=lambda item: _parse_de_date(item["date"]), reverse=True)
    return all_items[:AUTO_NEWS_COUNT]

# Ziel-Marke für die Abonnenten-Fortschrittsanzeige
SUBSCRIBER_GOAL = 5000

# Link zu deinem Google Formular für Video-Einsendungen.
EINSENDUNG_FORM_URL = "https://forms.gle/Y6D38VwWpqJV5RW97"

# Schnellzugriff-Navigation oben (OHNE Impressum und Datenschutz)
NAV_ITEMS = [
    {"label": "Videos", "href": "/#latest-videos"},
    {"label": "Shorts", "href": "/#latest-shorts"},
    {"label": "Playlists", "href": "/#playlists"},
    {"label": "Events", "href": "/event"},
    {"label": "Weihnachten", "href": "/event/weinachten"},
    {"label": "News", "href": "/news"},
    {"label": "Einsendung", "href": "/einsendung"},
    {"label": "Schiene & Weiche", "href": "/schiene_und_weiche"},
    {"label": "Signale lernen", "href": "/signale_lernen"},
    {"label": "Kanäle", "href": "/#links"},
]

# ---------------------------------------------------------------------------
# Community-Seite "Schiene und Weiche"
# ---------------------------------------------------------------------------

SCHIENE_UND_WEICHE = {
    "name": "Schiene und Weiche",
    "tagline": "Die WhatsApp-Community rund um Züge, Bahn und Eisenbahn-Content.",
    "bio": (
        "Schiene und Weiche ist unsere WhatsApp-Community für alle, die Züge "
        "und Bahn genauso lieben wie ich. Hier tauschen wir uns aus, teilen "
        "Aufnahmen und bleiben gemeinsam auf dem Laufenden."
    ),
    "member_count": 30,
    "whatsapp_link": "https://chat.whatsapp.com/JeiNjBWYGNe3rXNjxwJ2hA?s=cl&p=a&ilr=2",
    "instagram_link": "https://www.instagram.com/schiene_und_weiche/",
    "instagram_handle": "@schiene_und_weiche",
    "contact_email": "schieneundweiche9@gmail.com",
}

SCHIENE_ANGEBOTE = [
    {
        "title": "Chatten & Austauschen",
        "text": "Quatscht mit Gleichgesinnten über alles rund um Züge und Bahn.",
    },
    {
        "title": "Zug-Fotos & Videos teilen",
        "text": "Teilt eure eigenen Aufnahmen und schaut euch die der anderen an.",
    },
    {
        "title": "Bahn-Störungen sofort",
        "text": "Wir informieren euch schnell über aktuelle Störungen im Bahnverkehr.",
    },
    {
        "title": "Sonderzug-Fahrpläne",
        "text": "Infos zu Sonderzügen und ihren Fahrplänen aus erster Hand.",
    },
    {
        "title": "Regelmäßige Events",
        "text": "Von gemeinsamen Aktionen bis zu Community-Terminen ist immer was los.",
    },
]

SCHIENE_ADMINS = [
    {"name": "Max-Luka TV", "role": "Owner"},
    {"name": "Louis", "role": "Admin - Management Leiter"},
    {"name": "Thomas", "role": "Head Admin"},
    {"name": "‹Ul®|CH›", "role": "General Admin"},
]

SCHIENE_REGELN = [
    {
        "title": "Respekt und Höflichkeit",
        "text": "Bitte behandle alle Mitglieder mit Respekt. Beleidige und diskriminiere niemanden.",
    },
    {
        "title": "Themenbezogene Beiträge",
        "text": "Schreibe bitte nur themenbezogene Beiträge in die jeweiligen Gruppen.",
    },
    {
        "title": "Keine Werbung",
        "text": "Bitte mache keine Werbung für Produkte, Dienstleistungen oder andere Gruppen/Communitys/Kanäle.",
    },
    {
        "title": "Privatsphäre respektieren",
        "text": "Teile bitte keine persönlichen Informationen von und über andere ohne deren Zustimmung.",
    },
    {
        "title": "Keine Spam-Nachrichten",
        "text": "Vermeide das Senden von Kettenbriefen, schicke nicht unnötig viele Sticker und übertreibe nicht mit Nachrichten.",
    },
    {
        "title": "Kritik gegenüber Admins und Mitgliedern",
        "text": "Wenn du Kritik übst, bleibe immer respektvoll und konstruktiv.",
    },
    {
        "title": "Respektiere die Admins",
        "text": "Widersetze dich nicht den Admins und diskutiere nicht mit ihnen.",
    },
    {
        "title": "Keine illegalen Inhalte",
        "text": "Sende bitte keine illegalen, obszönen oder unangemessenen Nachrichten.",
    },
    {
        "title": "Nachrichten in den Chats",
        "text": "Verwende bitte immer eine angemessene Sprache und beleidige keine Mitglieder.",
    },
    {
        "title": "Probleme/Streitereien melden",
        "text": "Bei Anregungen oder Streitereien melde dich bitte bei einem Admin. Melde uns auch Regelverstöße.",
    },
    {
        "title": "Mitgliederlabel",
        "text": "Bitte verwende keine bösen oder obszönen Inhalte - nutze am besten deinen Künstlernamen oder ein Kürzel.",
    },
    {
        "title": "Chat-Sperrungen",
        "text": "Bitte beachte Chatsperren und schreibe während einer aktiven Sperre nicht in andere Gruppen.",
    },
]

SCHIENE_STRAFEN_HINWEIS = (
    "Bei Nichtbeachten der Regeln droht eine Verwarnung, eine schwere "
    "Verwarnung oder der Ausschluss aus unserer Community. Eine Verwarnung "
    "dauert zwischen 2 und 24 Stunden an - bei einer erneuten Verwarnung "
    "während dieser Zeit werden 24 Stunden addiert. Eine schwere Verwarnung "
    "dauert 1-3 Wochen an; bei einer erneuten Verwarnung während dieser "
    "Zeit folgt der Ausschluss."
)

# ---------------------------------------------------------------------------
# Weihnachts-Seite: Adventskranz & Adventskalender
# ---------------------------------------------------------------------------

# Optional für Tests: z. B. XMAS_TEST_MONTH = 12, XMAS_TEST_DAY = 10
# Im Normalbetrieb auf None lassen, damit das echte Datum genutzt wird.
XMAS_TEST_MONTH = None
XMAS_TEST_DAY = None

ADVENT_CALENDAR_DOORS = [
    {"day": 1, "title": "Start ins Signalbuch", "text": "Das erste Türchen ist offen! Kennst du den Unterschied zwischen Haupt- und Vorsignal?"},
    {"day": 2, "title": "Winterliche Stellwerke", "text": "Wenn draußen Frost liegt, müssen Weichenheizungen zuverlässig arbeiten."},
    {"day": 3, "title": "Blick an die Strecke", "text": "Manchmal sind es die ruhigen Wintermomente am Gleis, die am besten in Erinnerung bleiben."},
    {"day": 4, "title": "Modellbahn-Werkstatt", "text": "Perfektes Wetter, um an Modulen, Signalen oder der Beleuchtung zu tüfteln."},
    {"day": 5, "title": "Sonderzug-Fieber", "text": "Besondere Züge im Winterlicht sorgen auf dem Kanal immer für Highlights."},
    {"day": 6, "title": "Nikolaus-Gruß", "text": "Frohen Nikolaustag an alle aus der Community – danke fürs Dabeisein!"},
    {"day": 7, "title": "Form- oder Lichtsignal?", "text": "Beide haben ihren ganz eigenen Charme – im Quiz kannst du dein Wissen testen."},
    {"day": 8, "title": "Pünktlichkeit & Takt", "text": "Schon kleine Verspätungen können im Fahrplan spürbare Wellen schlagen."},
    {"day": 9, "title": "Kamera bereit", "text": "Gutes Licht im Dezember ist oft kurz – also rechtzeitig an den Spot fahren."},
    {"day": 10, "title": "Community-Moment", "text": "Austausch, Fotos und Störungsmeldungen halten Schiene & Weiche lebendig."},
    {"day": 11, "title": "Freie Fahrt voraus", "text": "Halbzeit bis Heiligabend – schon elf Türchen sind geöffnet!"},
    {"day": 12, "title": "Streckenkunde", "text": "Jede Haupt- und Nebenbahn erzählt ihre eigene Geschichte."},
    {"day": 13, "title": "Dämmerung am Gleis", "text": "Wenn Signale und Zugspitzenlichter im Dunkeln besonders klar leuchten."},
    {"day": 14, "title": "Kleine Rückschau", "text": "Welche Videos und Shorts von Max-Luka TV haben dir dieses Jahr am besten gefallen?"},
    {"day": 15, "title": "Weiche gestellt", "text": "Manchmal braucht es nur den richtigen Impuls zur richtigen Zeit."},
    {"day": 16, "title": "Kurz vor dem Endspurt", "text": "Zwei Drittel des Adventskalenders sind geschafft!"},
    {"day": 17, "title": "Soundcheck", "text": "Das Signalhorn in der Ferne – eines der markantesten Geräusche überhaupt."},
    {"day": 18, "title": "Gleisgeflüster", "text": "Noch sechs Tage bis zum großen Fest – genießt die Adventszeit."},
    {"day": 19, "title": "Winterfahrplan", "text": "Kälte, Dunkelheit und besondere Umläufe prägen den Dezember."},
    {"day": 20, "title": "Alle vier Kerzen", "text": "Spätestens jetzt leuchtet der Adventskranz in voller Pracht."},
    {"day": 21, "title": "Fast geschafft", "text": "Nur noch drei Türchen bis Heiligabend!"},
    {"day": 22, "title": "Vorfreude", "text": "Die letzten Tage vor Weihnachten laufen – danke für euren Support!"},
    {"day": 23, "title": "Letzter Tag davor", "text": "Morgen ist es soweit: Türchen 24 wartet schon."},
    {"day": 24, "title": "Frohe Weihnachten!", "text": "Alles Gute zum Weihnachtsfest wünscht Max-Luka TV & Schiene und Weiche!"},
]


def _get_effective_now():
    real_now = datetime.now()
    if XMAS_TEST_MONTH is not None and XMAS_TEST_DAY is not None:
        return real_now.replace(month=XMAS_TEST_MONTH, day=XMAS_TEST_DAY)
    return real_now


def _count_lit_candles(dt):
    """Berechnet, wie viele der 4 Adventskerzen am gegebenen Datum brennen."""
    year = dt.year
    christmas_eve = datetime(year, 12, 24)
    days_since_sunday = (christmas_eve.weekday() + 1) % 7
    fourth_advent = datetime(year, 12, 24 - days_since_sunday)
    first_advent = datetime(fourth_advent.year, fourth_advent.month, fourth_advent.day - 21)
    second_advent = datetime(fourth_advent.year, fourth_advent.month, fourth_advent.day - 14)
    third_advent = datetime(fourth_advent.year, fourth_advent.month, fourth_advent.day - 7)

    current_day = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    if current_day >= fourth_advent:
        return 4
    if current_day >= third_advent:
        return 3
    if current_day >= second_advent:
        return 2
    if current_day >= first_advent:
        return 1
    return 0


def get_christmas_context():
    now = _get_effective_now()
    month = now.month
    day = now.day

    is_xmas_season = (month == 11 and day >= 25) or (month == 12) or (month == 1 and day <= 6)

    if month == 12:
        unlocked_door = min(day, 24)
    elif month == 1 and day <= 6:
        unlocked_door = 24
    else:
        unlocked_door = 0

    lit_candles = _count_lit_candles(now)

    doors = []
    for item in ADVENT_CALENDAR_DOORS:
        is_unlocked = item["day"] <= unlocked_door
        doors.append(
            {
                "day": item["day"],
                "unlocked": is_unlocked,
                "is_today": month == 12 and item["day"] == day and item["day"] <= 24,
                "title": item["title"] if is_unlocked else "Noch verschlossen",
                "text": item["text"] if is_unlocked else f"Öffnet am {item['day']}. Dezember.",
            }
        )

    return {
        "is_xmas_season": is_xmas_season,
        "month": month,
        "day": day,
        "unlocked_door": unlocked_door,
        "lit_candles": lit_candles,
        "doors": doors,
    }


LATEST_VIDEOS_COUNT = 5
TOP_VIDEOS_COUNT = 5
LATEST_SHORTS_COUNT = 8
TOP_SHORTS_COUNT = 8
PLAYLISTS_COUNT = 6
SHORT_MAX_SECONDS = 180
MAX_PAGES_TO_SCAN = 20
CACHE_SECONDS = 600

# ---------------------------------------------------------------------------
# YouTube-Anbindung
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
    match = re.match(
        r"^PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?$", duration or ""
    )
    if not match:
        return 0
    hours, minutes, seconds = (int(x) if x else 0 for x in match.groups())
    return hours * 3600 + minutes * 60 + seconds


def _get_channel_info():
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
    now = time.time()
    if _cache["videos"] is not None and (now - _cache["videos_fetched_at"]) < CACHE_SECONDS:
        return _cache["videos"]

    playlist_id = _get_uploads_playlist_id()

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

    order = {vid: i for i, vid in enumerate(video_ids)}

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
            published_at_str = snippet.get("publishedAt", "")[:10]
            is_new = False
            if published_at_str:
                try:
                    published_date = datetime.strptime(published_at_str, "%Y-%m-%d")
                    is_new = (datetime.now() - published_date).days < 7
                except ValueError:
                    is_new = False
            videos.append(
                {
                    "id": vid,
                    "title": snippet.get("title", ""),
                    "published_at": published_at_str,
                    "thumbnail": thumb.get("url", ""),
                    "url": (
                        f"https://www.youtube.com/shorts/{vid}"
                        if duration_seconds and duration_seconds <= SHORT_MAX_SECONDS
                        else f"https://www.youtube.com/watch?v={vid}"
                    ),
                    "views": int(v.get("statistics", {}).get("viewCount", 0)),
                    "duration_seconds": duration_seconds,
                    "is_short": bool(duration_seconds) and duration_seconds <= SHORT_MAX_SECONDS,
                    "is_new": is_new,
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
    if not _api_key_configured():
        return None
    try:
        return _get_channel_info()["avatar"]
    except Exception as e:
        print("YOUTUBE-FEHLER (Avatar):", repr(e))
        return None


@app.route("/ping")
def ping():
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
        xmas=get_christmas_context(),
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
        news_items=get_news_items(),
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
        xmas=get_christmas_context(),
        channel_avatar=_get_channel_avatar_safe(),
    )


@app.route("/event/weinachten")
def event_weinachten():
    return render_template(
        "event_weinachten.html",
        channel=CHANNEL,
        nav_items=NAV_ITEMS,
        xmas=get_christmas_context(),
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


@app.route("/schiene_und_weiche")
def schiene_und_weiche():
    return render_template(
        "schiene_und_weiche.html",
        channel=CHANNEL,
        nav_items=NAV_ITEMS,
        community=SCHIENE_UND_WEICHE,
        angebote=SCHIENE_ANGEBOTE,
        admins=SCHIENE_ADMINS,
        regeln=SCHIENE_REGELN,
        strafen_hinweis=SCHIENE_STRAFEN_HINWEIS,
        channel_avatar=_get_channel_avatar_safe(),
    )


@app.route("/signale_lernen")
def signale_lernen():
    return render_template(
        "signale_lernen.html",
        channel=CHANNEL,
        nav_items=NAV_ITEMS,
        fragen_pro_runde=signale_daten.FRAGEN_PRO_RUNDE,
        sound_max=signale_daten.SOUND_MAX_ABSPIELEN,
        katalog=signale_daten.baue_katalog(),
        channel_avatar=_get_channel_avatar_safe(),
    )


@app.route("/signale_lernen/fragen")
def signale_lernen_fragen():
    return jsonify(signale_daten.baue_fragen())


# --- Routen für Impressum & Datenschutz (für den Footer) ---

@app.route("/impressum")
def impressum():
    return render_template(
        "impressum.html",
        channel=CHANNEL,
        nav_items=NAV_ITEMS,
        channel_avatar=_get_channel_avatar_safe(),
    )


@app.route("/datenschutz")
def datenschutz():
    return render_template(
        "datenschutz.html",
        channel=CHANNEL,
        nav_items=NAV_ITEMS,
        channel_avatar=_get_channel_avatar_safe(),
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)