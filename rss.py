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

# 結果保存用辞書オブジェクト
dict = {}

# 記事の情報をひとつずつ取り出す
for entry in feed.entries:

    # pprint( entry ) # ダンプ

    # URLにアクセスする 戻り値にはアクセスした結果やHTMLなどが入ったinstanceが帰ってきます
    # instance = urllib2.urlopen(url)
    instance = urllib.request.urlopen( entry.link )

    # instanceからHTMLを取り出して、BeautifulSoupで扱えるようにパースします
    soup = BeautifulSoup(instance, "html.parser")

    # pprint( soup ) # ダンプ

    # 1日1回RSSを取得してリンクとIDと更新日時をDBに登録する
    # リンクとIDと更新日時。画像も取得してサムネイル作成に使用する

    # サムネイル画像になりそうなimgタグが属す要素
    imgParentDom = soup.find( id="main_body" ) # TODO RSSによって変化するため変数にする
    # pprint( imgParentDom )

    imgTag = None
    if imgParentDom is not None:
        imgTag = imgParentDom.find( "img" )

    imgSrc = None
    if imgTag is not None:
        imgSrc = imgTag['src']

    pprint( { "img dom" : imgTag } )
    pprint( { "img src" : imgSrc } )

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


    pprint( entry.id ) # 結果をダンプ出力
    dict[ entry.id ] = result # TODO 同一キーなら更新日時が新しいフィードを残す
    # break #デバッグ時は１要素で十分

# ループ抜けてからダンプ
# pprint( dict )
