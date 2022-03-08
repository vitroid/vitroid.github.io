build: parse
	cd ..; bundle exec jekyll build --verbose --incremental
parse:
	python3 make.py
force:
	python3 make.py -f
serve:
	cd ..; bundle exec jekyll serve --incremental --watch & open http://localhost:4000
prepare:
	python3 unscrapbox.py *json
deploy: push
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
