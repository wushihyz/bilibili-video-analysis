import requests, csv, time, os
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://www.bilibili.com/"
}

ALL_ENDPOINTS = []

# 1) 热门榜单多页
for page in range(1, 11):
    ALL_ENDPOINTS.append(("popular", f"https://api.bilibili.com/x/web-interface/popular?pn={page}&ps=50", 0.3))

# 2) 每周必看 (近几期)
for series in range(1, 5):
    ALL_ENDPOINTS.append(("weekly", f"https://api.bilibili.com/x/web-interface/popular/series/one?number={series}", 0.3))

def fetch(url):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=8)
        data = resp.json()
        if data.get("code") == 0:
            return data["data"].get("list", []) or data["data"].get("videos", [])
    except:
        pass
    return []

def parse_video(v):
    stat = v.get("stat", {})
    owner = v.get("owner", {})
    return {
        "bvid": v.get("bvid", ""),
        "title": v.get("title", "").strip(),
        "description": (v.get("description", "") or "").strip()[:150],
        "category_name": v.get("tname", ""),
        "upload_time": datetime.fromtimestamp(v.get("pubdate", 0)).strftime("%Y-%m-%d %H:%M:%S"),
        "upload_date": datetime.fromtimestamp(v.get("pubdate", 0)).strftime("%Y-%m-%d"),
        "upload_hour": datetime.fromtimestamp(v.get("pubdate", 0)).hour,
        "duration": v.get("duration", 0),
        "up_name": owner.get("name", ""),
        "views": stat.get("view", 0),
        "danmaku": stat.get("danmaku", 0),
        "likes": stat.get("like", 0),
        "coins": stat.get("coin", 0),
        "favorites": stat.get("favorite", 0),
        "shares": stat.get("share", 0),
        "reply": stat.get("reply", 0),
    }

def main():
    all_videos = {}
    print("=" * 50)
    print("B站热门视频数据采集器 v2")
    print("=" * 50)

    for source, url, delay in ALL_ENDPOINTS:
        videos = fetch(url)
        for v in videos:
            parsed = parse_video(v)
            if parsed["views"] > 0:  # 过滤无效数据
                all_videos[parsed["bvid"]] = parsed
        label = "热门" if source == "popular" else "每周必看"
        print(f"  [{label}] {len(videos)} 条")
        time.sleep(delay)

    output_path = os.path.join(os.path.dirname(__file__), "data", "bilibili_videos.csv")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    fieldnames = [
        "bvid","title","description","category_name",
        "upload_time","upload_date","upload_hour","duration",
        "up_name","views","danmaku","likes","coins","favorites","shares","reply"
    ]
    with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_videos.values())

    print(f"\n{'=' * 50}")
    print(f"采集完成！共 {len(all_videos)} 条视频数据")
    print(f"已保存至: {output_path}")
    print(f"{'=' * 50}")

if __name__ == "__main__":
    main()