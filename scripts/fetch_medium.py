#!/usr/bin/env python3
import os
import re
import sys
from html import unescape

try:
    import feedparser
except Exception as e:
    print("Eksik paket: feedparser. Lütfen 'pip install feedparser' yapın.")
    raise

# Kullanıcı adı sabit (myusufd)
MEDIUM_USERNAME = "myusufd"
POSTS_COUNT = 5  # İstediğin sayıyı değiştirebilirsin

# Feed URL
FEED_URL = f"https://medium.com/feed/@{MEDIUM_USERNAME}"

def safe_text(s):
    if not s:
        return ""
    return unescape(re.sub(r'\s+', ' ', s)).strip()

def build_posts_md(entries, count=5):
    lines = []
    for e in entries[:count]:
        title = safe_text(e.get("title", "Untitled"))
        link = e.get("link")
        summary = re.sub('<[^<]+?>', '', e.get("summary", ""))  # HTML etiketlerini kaldır
        summary = safe_text(summary)
        if summary and len(summary) > 120:
            summary = summary[:117].rsplit(' ', 1)[0] + "..."
        if link:
            lines.append(f"- [{title}]({link}){' — ' + summary if summary else ''}")
        else:
            lines.append(f"- {title}{' — ' + summary if summary else ''}")
    if not lines:
        lines.append("- (Gösterilecek yazı bulunamadı.)")
    return "\n".join(lines)

def update_readme(md_block, readme_path="README.md"):
    start_marker = "<!-- MEDIUM_POSTS_START -->"
    end_marker = "<!-- MEDIUM_POSTS_END -->"

    if not os.path.isfile(readme_path):
        print(f"{readme_path} bulunamadı; yeni bir dosya oluşturulacak.")
        content = f"{start_marker}\n{md_block}\n{end_marker}\n"
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(content)
        return True

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    if start_marker in content and end_marker in content:
        pattern = re.compile(
            re.escape(start_marker) + r'.*?' + re.escape(end_marker),
            flags=re.DOTALL | re.IGNORECASE
        )
        new_section = f"{start_marker}\n{md_block}\n{end_marker}"
        new_content = pattern.sub(new_section, content)
    else:
        # Marker yoksa README sonuna ekle
        new_content = content.rstrip() + "\n\n" + start_marker + "\n" + md_block + "\n" + end_marker + "\n"

    if new_content == content:
        print("README zaten güncel. Değişiklik yok.")
        return False

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("README güncellendi.")
    return True

def main():
    print("Feed URL:", FEED_URL)
    feed = feedparser.parse(FEED_URL)
    if feed.bozo:
        print("Feed okunurken bir hata oluştu veya feed bozuk olabilir.")
    entries = feed.get("entries", [])
    md = build_posts_md(entries, POSTS_COUNT)
    changed = update_readme(md)
    if changed:
        print("README başarıyla güncellendi.")
    else:
        print("Değişiklik yapılmadı.")

if __name__ == "__main__":
    main()
