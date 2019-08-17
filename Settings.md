# Settings



[](https://gyazo.com/641dfa2be02c3674241a26f4d64af4e8)

[/progfay-pub/Settings](/progfay-pub/Settings.md)を参考に。

[[color theme]([color theme.md)]

[[https://gyazo.com/2d7af113e5d77a76ff03396a12c37979]([https://gyazo.com/2d7af113e5d77a76ff03396a12c37979.md)]

    :root {
   		--bg-color:  #FFFFFF;
   		--fg-color:  #252525;
   		--highlight: #6BA6DE;
   		--default:   #999999;
    }

[[マーカー]([マーカー.md)]

    /* 二重括弧による強調を蛍光マーカーっぽくする */
    .line strong:not([class]) { 
      background: #E0FF80;
      padding: 0 3px;
      margin: 0 1px;
    }

[[#で始まるタグをラベル風にする ]([#で始まるタグをラベル風にする .md)]

    a[type="hashTag"] {
   		display: inline-block;
      	padding: 2px 8px;
        margin: 0 8px 10px 0;
        background: rgba(0, 0, 0, 0);
        font-size: 0.8em;
        border: 1px solid #0085de;
        border-radius: 3px;
    }
    a[type="hashTag"].empty-page-link {
    	border: 1px solid #f27e48;
    }
    a.page-link[type=hashTag] > span:first-child {
    	visibility: hidden;
      	position: absolute;
    }
    div.cursor-line a.page-link[type=hashTag] > span:first-child {
      visibility: visible;
      position: relative;
    }
   [[トップページのタイルの数を増やす]] [/forum-jp/Webブラウザ横幅いっぱい表示させてほしい]
    .container {
      max-width: none;
      }



----
[Edit](https://github.com/vitroid/vitroid.github.io/blob/master/MD/Settings.md)
