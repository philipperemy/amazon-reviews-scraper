# Amazon Multi Language Reviews Scraper (Last update March 2017. Works!)
Yet another Multi Language Scraper for Amazon targeting reviews.
<br/>
<div align="center">
  <img src="http://static1.businessinsider.com/image/539f3ffbecad044276726c01-960/amazon-com-logo.jpg" width="200"><br><br>
</div>
## How to get started?
```
git clone git@github.com:philipperemy/amazon-reviews-scraper.git ars
cd ars
sudo pip install -r requirements.txt
python amazon_comments_scraper.py -s iPhone # will search iPhone on Amazon.co.jp and fetch many comments!
```

## Some examples on Amazon Japan

Item = `BOTANIST ボタニカルシャンプー 490ml ＆ トリートメント 490g　モイストセット`

### Data processed by the scraper
```
[...]
2017-02-27 16:52:47,347 - INFO - ***********************************************
2017-02-27 16:52:47,347 - INFO - TITLE    = スカルプ
2017-02-27 16:52:47,347 - INFO - RATING   = 4
2017-02-27 16:52:47,347 - INFO - CONTENT  = まだ1日しか使ってませんが以前モイストを使ってました。モイストと比べてシャンプーは泡立ちが少し悪いかもしれません。また香りも控えめで余り残らないです。さらにその香りも人によって好き嫌いに分かれるシトラスのキツめ？香りです。でもさすがボタニスト！髪の毛はサラサラになります。
2017-02-27 16:52:47,347 - INFO - ***********************************************

2017-02-27 16:52:47,347 - INFO - ***********************************************
2017-02-27 16:52:47,347 - INFO - TITLE    = いろいろ試しました
2017-02-27 16:52:47,348 - INFO - RATING   = 4
2017-02-27 16:52:47,348 - INFO - CONTENT  = スカルプ系のシャンプーは一通り試しましたが、一番自分に合っている気がします。価格も他のスカルプ系のシャンプーに比べると安いと思います。
2017-02-27 16:52:47,348 - INFO - ***********************************************
```

### Content on amazon.co.jp
<div align="center">
  <img src="fig/img1.png"><br><br>
</div>
<div align="center">
  <img src="fig/img2.png"><br><br>
</div>
