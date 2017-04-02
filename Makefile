log.log: parse.py py.py
	python parse.py < py.py > log.log && tail $(TAIL) $@
