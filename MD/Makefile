prepare:
	python unscrapbox.py *json
push:
	git add -A
	git commit -m.
	git push

prepare-wiki:
	rsync -av --exclude 'CVS/*' chemist@www.chem.okayama-u.ac.jp:/home/theochem/wiki-data/data/matto/  wiki/



