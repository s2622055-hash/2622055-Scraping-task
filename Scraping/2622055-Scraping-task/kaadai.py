import time
import requests
import csv
from bs4 import BeautifulSoup

url = 'https://www.musashino-u.ac.jp'

res = requests.get(url)

time.sleep(1) 

res.encoding = 'utf-8'

from urllib.parse import urljoin, urldefrag

page_url = 'https://www.musashino-u.ac.jp'

href_list = [
    
    ]

for href in href_list:
    absolute_url = urljoin(page_url, href)
    clean_url = urldefrag(absolute_url).url

    print(f"{href}  →{clean_url}")


from urllib.parse import urlparse

parsed = urlparse(url)
print(f"スキーム：{parsed.scheme}")
print(f"ドメイン：{parsed.netloc}")
print(f"パス　　：{parsed.path}")

DOMAIN = 'www.musashino-u.ac.jp'

url_list = [

]

from urllib.parse import urljoin, urldefrag, urlparse
DOMAIN = urlparse(url).netloc 

print(f"ステータスコード：{res.status_code}")

html_soup = BeautifulSoup(res.content, 'html.parser')

# <title>がない場合や .string が None の場合に備えて、空文字にしておく
if html_soup.title is not None and html_soup.title.string is not None:
    # split()で空白・改行ごとに区切り、' '.join()で1つの空白でつなぎ直す
    # （タイトル内の改行や連続した空白を整理する）
    title = ' '.join(html_soup.title.string.split())
else:
    title = ''
print(f"タイトル：{title}")

# ページ内のリンクを集め、同一ドメインのものだけリストにする
# 見つけたURLを貯めるための空のリスト
link_list = []
for a in html_soup.find_all('a', href=True): 
 #href属性を持つ<a>タグだけをnext_urlとして置き換えた
    next_url = urldefrag(urljoin(url, a['href'])).url  
    #絶対URL化＋#除去
    parsed = urlparse(next_url)

      # http(s)で、同一ドメインで、まだリストにないものだけ追加
    if parsed.scheme in ('http', 'https') and parsed.netloc == DOMAIN:
        if next_url not in link_list:
            link_list.append(next_url)

print(f"見つかった同一ドメインのリンク数：{len(link_list)}")
for link in link_list[:10]:   # 先頭10件だけ表示
    print(link)

START_URL = 'https://www.musashino-u.ac.jp'
DOMAIN = urlparse(START_URL).netloc

SKIP_EXTENSIONS = ('.pdf', '.jpg', '.jpeg', '.png', '.gif', '.zip', '.docx', '.xlsx', '.pptx')

def is_target_url(url):
    """実習8の判定関数"""
    parsed = urlparse(url)
    if parsed.scheme not in ('http', 'https'):
        return False
    if parsed.netloc != DOMAIN:
        return False
    if parsed.path.lower().endswith(SKIP_EXTENSIONS):
        return False
    return True

sitemap = {}               # 結果：{URL: タイトル}　# 空の辞書を作る
to_visit = [START_URL]     # これから訪問するURLのリスト（待ち行列）# 辞書にデータを追加する、ページにアクセスしてタイトルを取得したら、辞書に次々と追加されていく
found = {START_URL}        # 一度でも待ち行列に入れたURLの集合（重複防止）# 中身を確認する

# 待ち行列が空になるまで繰り返す
while to_visit:

    url = to_visit.pop(0)  # 先頭のURLを取り出す（取り出したものはリストから消える）

    time.sleep(1)          # ★ 必ず待ってからアクセスする
    res = requests.get(url)

    # 正常に取得できなかったページは飛ばす
    if res.status_code != 200:
        print(f"スキップ（{res.status_code}）：{url}")
        continue
    # HTML以外（PDFなど）は飛ばす（実習1のレスポンスヘッダーを使う）
    if 'text/html' not in res.headers.get('Content-Type', ''):
        continue

    html_soup = BeautifulSoup(res.content, 'html.parser')

    # タイトルを取得して辞書に格納
    if html_soup.title is not None and html_soup.title.string is not None:
        title = ' '.join(html_soup.title.string.split())   # 改行・連続空白を整理
    else:
        title = ''
    sitemap[url] = title
    print(f"[{len(sitemap)}]{url} |{title}")

    # リンクを集めて、新しいものだけ待ち行列に追加
    for a in html_soup.find_all('a', href=True):
        next_url = urldefrag(urljoin(url, a['href'])).url
        if is_target_url(next_url) and next_url not in found:
            found.add(next_url)
            to_visit.append(next_url)

print(f"取得ページ数：{len(sitemap)} / 未訪問で残っているURL：{len(to_visit)}")


with open('sitemap.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['url', 'title'])      
    for url, title in sitemap.items():     
        writer.writerow([url, title])

with open('sitemap.csv', encoding='utf-8') as f:
    print(f.read())