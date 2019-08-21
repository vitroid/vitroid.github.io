---
---
    :root {
    }
    /* 二重括弧による強調を蛍光マーカーっぽくする */
    .line strong:not([class]) { 
      background: #E0FF80;
      padding: 0 3px;
      margin: 0 1px;
    }
    a[type="hashTag"] {
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
    .container {
      max-width: none;
      }
## Linked from

* [Settings](Settings.md)


----
[Edit](https://github.com/vitroid/vitroid.github.io/edit/master/MD/Settings.md)
