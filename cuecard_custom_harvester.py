import json
import re
import os
import time
import random
import urllib.parse
from datetime import datetime
import pandas as pd
import requests
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def get_wikipedia_summary(keyword):
    """Fetches clean, verified summary abstracts from Wikipedia's open REST engine."""
    formatted_kw = keyword.strip().title().replace(" ", "_")
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{formatted_kw}"
    try:
        res = requests.get(url, headers={"User-Agent": "CueCardMediaBot/2.0 (editorial@cuecard.media)"}, timeout=3)
        if res.status_code == 200:
            return res.json().get("extract", "")[:180] + "..."
    except Exception:
        pass
    
    try:
        ddg_url = f"https://api.duckduckgo.com/?q={keyword}&format=json&no_html=1"
        res = requests.get(ddg_url, headers={"User-Agent": "CueCardBot/2.0"}, timeout=3)
        if res.status_code == 200:
            abstract = res.json().get("AbstractText", "").strip()
            if abstract: return abstract[:180] + "..."
    except Exception:
        pass
    return "Trending real-time news topic. See live hyperlinked social media and news tracking nodes."

def fetch_comparison_vs_hook(keyword):
    """Pings the auto-suggest matrix to extract real-world competitive comparison metrics."""
    encoded = urllib.parse.quote(f"{keyword} vs")
    url = f"https://suggestqueries.google.com/complete/search?client=youtube&ds=yt&q={encoded}"
    try:
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=3)
        if res.status_code == 200:
            match = re.search(r'\[.*\]', res.text)
            if match:
                return json.loads(match.group())[1][0][0]
    except Exception:
        pass
    return "N/A"

def fetch_reddit_discussion_angle(keyword):
    """Harvests community discussion points safely using updated browser mimicking and strict timeouts."""
    encoded = urllib.parse.quote(keyword)
    url = f"https://www.reddit.com/search.json?q={encoded}&sort=relevance&limit=2"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        res = requests.get(url, headers=headers, timeout=2)
        if res.status_code == 200:
            children = res.json().get("data", {}).get("children", [])
            if children:
                title = children[0].get("data", {}).get("title", "")
                subreddit = children[0].get("data", {}).get("subreddit", "reddit")
                return f"r/{subreddit}: {title[:65]}..."
    except Exception:
        pass
    return "No active community threads cached. Refer to breaking journalism feeds."

def harvest_youtube_intent(keyword):
    url = f"https://suggestqueries.google.com/complete/search?client=youtube&ds=yt&q={keyword}"
    try:
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=3)
        if res.status_code == 200:
            match = re.search(r'\[.*\]', res.text)
            if match: return json.loads(match.group())[1][0][0]
    except Exception: pass
    return "N/A"

def fetch_live_youtube_video_link(keyword):
    """Pulls live video links from YouTube XML feed, with a fail-safe HTML scrape backup."""
    encoded_kw = urllib.parse.quote(keyword)
    
    # --- PATHWAY A: XML Feed Protocol ---
    url_xml = f"https://www.youtube.com/feeds/videos.xml?search_query={encoded_kw}"
    try:
        res = requests.get(url_xml, headers={"User-Agent": "Mozilla/5.0"}, timeout=3)
        if res.status_code == 200:
            video_ids = re.findall(r'<yt:videoId>(.*?)</yt:videoId>', res.text)
            titles = re.findall(r'<title>(.*?)</title>', res.text)
            if video_ids and len(titles) > 1:
                clean_title = titles[1].replace('"', "'")[:35]
                return f'=HYPERLINK("https://www.youtube.com/watch?v={video_ids[0]}", "YT: {clean_title}...")'
    except Exception:
        pass

    # --- PATHWAY B: Fail-safe HTML Backup (Triggers if Feed is empty/throttled) ---
    url_web = f"https://www.youtube.com/results?search_query={encoded_kw}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    try:
        res = requests.get(url_web, headers=headers, timeout=3)
        if res.status_code == 200:
            video_ids = re.findall(r'"videoId":"([^"]+)"', res.text)
            if video_ids:
                valid_ids = [vid for vid in video_ids if len(vid) == 11]
                if valid_ids:
                    return f'=HYPERLINK("https://www.youtube.com/watch?v={valid_ids[0]}", "YT: Click to Watch...")'
    except Exception:
        pass

    return "N/A"

def proxy_meta_social_videos(keyword, platform="instagram.com/reel"):
    query = f"site:{platform} {keyword}"
    encoded_query = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-IN&gl=IN&ceid=IN:en"
    try:
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=3)
        if res.status_code == 200:
            links = re.findall(r'<link>(.*?)</link>', res.text)
            items = re.findall(r'<item>(.*?)</item>', res.text, re.DOTALL)
            if links and items:
                title = re.search(r'<title>(.*?)</title>', items[0]).group(1).replace('"', "'")[:35]
                label = "IG" if "instagram" in platform else "FB"
                return f'=HYPERLINK("{links[0]}", "{label}: {title}...")'
    except Exception: pass
    return "N/A"

def fetch_news_hyperlink(keyword):
    url = f"https://news.google.com/rss/search?q={keyword}&hl=en-IN&gl=IN&ceid=IN:en"
    try:
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=3)
        if res.status_code == 200:
            items = re.findall(r'<item>(.*?)</item>', res.text, re.DOTALL)
            if items:
                title = re.search(r'<title>(.*?)</title>', items[0]).group(1).replace("&amp;", "&").replace('"', "'")
                if " - " in title: title = " - ".join(title.split(" - ")[:-1])
                return f'=HYPERLINK("{re.search(r"<link>(.*?)</link>", items[0]).group(1)}", "{title[:35]}...")'
    except Exception: pass
    return "N/A"

def fetch_audience_question(keyword):
    url = f"https://suggestqueries.google.com/complete/search?client=chrome&q=why {keyword}"
    try:
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=3)
        if res.status_code == 200:
            suggestions = res.json()[1]
            questions = [q for q in suggestions if any(x in q.lower() for x in ["why", "how", "what", "is"])]
            if questions: return questions[0]
    except Exception: pass
    return f"What is the latest update regarding {keyword}?"

def apply_master_formatting(ws, df):
    ws.views.sheetView[0].showGridLines = True
    HEADER_FILL = PatternFill(start_color="111827", end_color="111827", fill_type="solid")
    ZEBRA_FILL = PatternFill(start_color="F9FAFB", end_color="F9FAFB", fill_type="solid")
    
    font_h = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    font_b = Font(name="Calibri", size=11)
    font_link = Font(name="Calibri", size=11, underline="single", color="0284C7")
    thin_border = Border(left=Side(style='thin', color='E5E7EB'), right=Side(style='thin', color='E5E7EB'),
                         top=Side(style='thin', color='E5E7EB'), bottom=Side(style='thin', color='E5E7EB'))

    for col_idx in range(1, len(df.columns) + 1):
        cell = ws.cell(row=1, column=col_idx)
        cell.font = font_h
        cell.fill = HEADER_FILL
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = thin_border
    ws.row_dimensions[1].height = 28

    for row_idx in range(2, ws.max_row + 1):
        is_even = (row_idx % 2 == 0)
        ws.row_dimensions[row_idx].height = 22
        for col_idx in range(1, len(df.columns) + 1):
            cell = ws.cell(row=row_idx, column=col_idx)
            cell.border = thin_border
            if is_even: cell.fill = ZEBRA_FILL
            
            if col_idx in [1, 12]:
                cell.alignment = Alignment(horizontal="center", vertical="center")
            else:
                cell.alignment = Alignment(horizontal="left", vertical="center")
                
            # Treat formula text dynamically as clickable link objects
            if col_idx in [5, 6, 7, 8] and str(cell.value).startswith("="):
                cell.font = font_link
            else:
                cell.font = font_b

    for col in ws.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        col_letter = get_column_letter(col[0].column)
        ws.column_dimensions[col_letter].width = min(max(max_len + 3, 14), 48)

def main():
    print("================================================================")
    print("🧠 CUE CARD MEDIA - AUTOMATED INPUT PIPELINE V2 (DEEP EXTENSION)")
    print("================================================================\n")
    
    txt_source = "keywords_input.txt"
    excel_dest = "CueCard_Custom_Intelligence.xlsx"
    
    # Strictly matching schema matrix boundaries 
    MASTER_COLUMNS = [
        "Tracking ID", "Target Keyword", "Context Summary (Wiki/DDG)", 
        "YouTube Auto Intent", "Live YouTube Link", "Live Instagram Reel", 
        "Live Facebook Video", "Live News Brief", "High-Click Comparison Hook ('VS')", 
        "Reddit Community Sentiment Pulse", "Audience Inquiry Question", "Synced Timestamp"
    ]
    
    if not os.path.exists(txt_source):
        with open(txt_source, "w", encoding="utf-8") as f: pass
        print(f"📝 Created empty '{txt_source}' layout container. Insert tracking handles.")
        return

    with open(txt_source, "r", encoding="utf-8") as f:
        keywords = [line.strip() for line in f if line.strip()]

    if not keywords:
        print("⚠️ Input text layer empty. Populate keywords to trigger script execution parameters.")
        return

    print(f"🎯 Parsing details across {len(keywords)} Custom Targets...\n")
    current_run_rows = []
    
    for idx, kw in enumerate(keywords, 1):
        print(f" 📡 Processing [{idx}/{len(keywords)}] -> '{kw}'")
        
        # Pull Upgraded Free Components
        context = get_wikipedia_summary(kw)
        vs_hook = fetch_comparison_vs_hook(kw)
        reddit_pulse = fetch_reddit_discussion_angle(kw)
        
        # Core Infrastructure Pulls
        yt_intent = harvest_youtube_intent(kw)
        yt_video = fetch_live_youtube_video_link(kw)
        ig_reel = proxy_meta_social_videos(kw, "instagram.com/reel")
        fb_video = proxy_meta_social_videos(kw, "facebook.com/watch")
        news_link = fetch_news_hyperlink(kw)
        question = fetch_audience_question(kw)
        
        current_run_rows.append({
            "Tracking ID": idx,
            "Target Keyword": kw,
            "Context Summary (Wiki/DDG)": context,
            "YouTube Auto Intent": yt_intent,
            "Live YouTube Link": yt_video,
            "Live Instagram Reel": ig_reel,
            "Live Facebook Video": fb_video,
            "Live News Brief": news_link,
            "High-Click Comparison Hook ('VS')": vs_hook,
            "Reddit Community Sentiment Pulse": reddit_pulse,
            "Audience Inquiry Question": question,
            "Synced Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        time.sleep(random.uniform(0.3, 0.5))

    latest_df = pd.DataFrame(current_run_rows)
    latest_df = latest_df.reindex(columns=MASTER_COLUMNS)
    latest_df["Tracking ID"] = range(1, len(latest_df) + 1)

    if os.path.exists(excel_dest):
        try:
            historic_df = pd.read_excel(excel_dest, sheet_name="Historic Data")
            # Force historic index configuration alignment
            historic_df = historic_df.reindex(columns=MASTER_COLUMNS)
            
            combined_df = pd.concat([historic_df, latest_df], ignore_index=True)
            historic_df = combined_df.drop_duplicates(subset=["Target Keyword"], keep="last")
        except Exception: 
            historic_df = latest_df
    else:
        historic_df = latest_df

    # Recalculate IDs chronological presentation ordering 
    historic_df = historic_df.sort_values(by="Synced Timestamp", ascending=False)
    historic_df = historic_df.reindex(columns=MASTER_COLUMNS)
    historic_df["Tracking ID"] = range(1, len(historic_df) + 1)

    with pd.ExcelWriter(excel_dest, engine='openpyxl') as writer:
        latest_df.to_excel(writer, sheet_name="Latest Data", index=False)
        apply_master_formatting(writer.sheets["Latest Data"], latest_df)
        
        historic_df.to_excel(writer, sheet_name="Historic Data", index=False)
        apply_master_formatting(writer.sheets["Historic Data"], historic_df)

    try:
        with open(txt_source, "w", encoding="utf-8") as f: pass
        print(f"\n🧹 Cleaned up input script: '{txt_source}' has been successfully reset.")
    except Exception as e: print(f"⚠️ Text cleanup error: {e}")

    print("\n================================================================")
    print("🛰️  SYSTEM COMPLETION SUCCESS: Extended Editorial Blueprint Ready!")
    print("================================================================")

if __name__ == "__main__":
    main()