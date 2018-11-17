# coding: UTF-8
import feedparser
# import urllib2
# python3系では以下に書き換え
import urllib.request, urllib.error
from bs4 import BeautifulSoup

# デバッグ用にオブジェクトの中身を表示するpprint
from pprint import pprint

# 取得するRSSのURL
# RSS_URL = "https://headlines.yahoo.co.jp/rss/trendy-all.xml"
RSS_URL = "http://www.pref.kanagawa.jp/menu/4/menu4.xml"

# RSSから取得する
feed = feedparser.parse(RSS_URL)

dict = {}

# 記事の情報をひとつずつ取り出す
for entry in feed.entries:

    # ダンプ
    # pprint( entry )

    # タイトルを出力
    # print( entry.title )
    # print( entry.link )
    # print( entry.updated )

    # URLにアクセスする 戻り値にはアクセスした結果やHTMLなどが入ったinstanceが帰ってきます
    # instance = urllib2.urlopen(url)
    # instance = urllib.request.urlopen(url)

    # instance = urllib.request.urlopen( entry.url )
    instance = urllib.request.urlopen( entry.link )

    # instanceからHTMLを取り出して、BeautifulSoupで扱えるようにパースします
    soup = BeautifulSoup(instance, "html.parser")

    # 例としてタイトル要素のみを出力する
    # print(soup.title)

    # ダンプ
    # pprint( soup )

    # 1日1回RSSを取得してリンクとIDと更新日時をDBに登録する

    # リンクとIDと更新日時だけでOKか。
    # と思ったけど画像も取得してサムネイル作成に使用すればよいのでは

    # 画像
    # img = soup.find("img")
    # TDOD
    # imgタグが属すcss class名、img srcのパスのホスト名、などで取得する画像を判定する
    # imgParentDom = soup.find( "div", class_="img_cap")
    # imgParentDom = soup.find( "div", class_="main_box clearfix")
    # imgParentDom = soup.find( class_="clearfix" )
    imgParentDom = soup.find( id="main_body" )
    # pprint( imgParentDom )

    imgTag = None
    if imgParentDom is not None:
        imgTag = imgParentDom.find( "img" )

    imgSrc = None
    if imgTag is not None:
        imgSrc = imgTag['src']

    pprint( { "img dom" : imgTag } )
    pprint( { "img src" : imgSrc } )
    # これでもできるがセレクタでできないか
    # for child in imgParentDom.children:
    #     print(child)

    # 結果保存用変数
    result = {
                    "rss" : {
                                "id" : entry.id,
                                "title" : entry.title,
                                "link" : entry.link,
                                "updated" : entry.updated
                            },
                    "img dom" : imgTag,
                    "img src" : imgSrc
              }

    # 結果をダンプ出力
    pprint( entry.id )
    dict[ entry.id ] = result
    # break #デバッグ時は１要素で十分

# ループ抜けてからダンプ
# pprint( dict )
