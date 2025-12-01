#!/usr/bin/env python3
import os
import re
from html import unescape

import feedparser

# Medium kullanıcı adın – Türkçe karakter veya boşluk olmamalı
MEDIUM_USERNAME = "MustafaYusufDasdemir"
POSTS_COUNT = 5

FEED_URL = f"https://medium.com/feed/@{MEDIUM_USERNAME}"


def safe_text(s):
    if not s:
        return ""
    return unescape(re.sub(r'\s+', ' ', s)).strip()


def strip_html(text):
    """Basit HTML tag temizleyici."""
    return re.sub('<[^<]+?>', '', text)


def build_posts_md(entries, count=5):
    lines = []
    for e in entries[:count]:
        title = safe_text(e.get("title", "Untitled"))
        link = e.get("link")

        summary_raw = e.get("summary", "")
        summary = safe_text(strip_html(summary_raw))

        # Özet çok uzunsa kısalt
        if len(summary) > 120:
            summary = summary[:117].rsplit(" ", 1)[0] + "..."

        line = f"- [{title}]({link})"
        if summary:
            line += f" — {summary}"
        lines.append(line)

    if not lines:
        lines.append("- (Gösterilecek yazı bulunamadı.)")
    return "\n".join(lines)


def update_readme(md_block, readme_path="README.md"):
    start_marker = "<!-- MEDIUM_POSTS_START -->"
    end_marker = "<!-- MEDIUM_POSTS_END -->"

    if not os.path.isfile(readme_path):
        print(f"{readme_path} bulunamadı, yeni oluşturuluyor...")
        content = f"{start_marker}\n{md_block}\n{end_marker}\n"
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(content)
        return True

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    if start_marker in content and end_marker in content:
        pattern = re.compile(
            re.escape(start_marker) + r".*?" + re.escape(end_marker),
            flags=re.DOTALL | re.IGNORECASE
        )
        new_content = pattern.sub(f"{start_marker}\n{md_block}\n{end_marker}", content)
    else:
        new_content = content.rstrip() + f"\n\n{start_marker}\n{md_block}\n{end_marker}\n"

    if new_content == content:
        print("README zaten güncel.")
        return False

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("README güncellendi.")
    return True


def main():
    print("Feed URL:", FEED_URL)
    feed = feedparser.parse(FEED_URL)

    if feed.bozo:
        print("⚠️ Uyarı: Feed okunurken sorun oluştu. Kullanıcı adı doğru olmayabilir.")

    entries = feed.get("entries", [])

    md = build_posts_md(entries, POSTS_COUNT)
    changed = update_readme(md)

    print("Bitti.")


if __name__ == "__main__":
    main()
