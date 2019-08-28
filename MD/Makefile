parse:
	python make.py
build:
	cd ..; bundle exec jekyll build --verbose
serve:
	cd ..; bundle exec jekyll serve --incremental
prepare:
	python unscrapbox.py *json
push:
	git add -A
	git commit -m.
	git push

prepare-wiki:
#	rsync -av --exclude 'CVS/*' chemist@www.chem.okayama-u.ac.jp:/home/theochem/wiki-data/data/matto/  wiki/
	rsync -av chemist@www.chem.okayama-u.ac.jp:/home/theochem/wiki-data/attach/matto _attach/



