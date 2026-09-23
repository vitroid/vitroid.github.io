wikiやscrapboxファイルはできるだけさわらない。

何か更新した場合は
make

そしてローカルでチェックする場合は
make serve

deployする場合は
make push

ソースは MD/、生成ページは _wiki/。
被リンクは毎 make で本文から作り直す。
画像サムネイルのキャッシュは _cache/（git 管理外）。
