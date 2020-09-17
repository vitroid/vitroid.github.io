build: parse
	cd ..; bundle exec jekyll build --verbose --incremental
parse:
	python make.py
force:
	python make.py -f
serve:
	cd ..; bundle exec jekyll serve --incremental --watch
prepare:
	python unscrapbox.py *json
push:
	git add -A
	git commit -m.
	git push

prepare-wiki:
#	rsync -av --exclude 'CVS/*' chemist@www.chem.okayama-u.ac.jp:/home/theochem/wiki-data/data/matto/  wiki/
	rsync -av chemist@www.chem.okayama-u.ac.jp:/home/theochem/wiki-data/attach/matto _attach/

# transfer files converted from wiki attachments via attachconv.py
xfer-attach:
	rsync -av _conv/ theochem@www.chem.okayama-u.ac.jp:Sites/vitroid/


# 間違ったtagを消したい場合は、/と/_refの両方を消す。
