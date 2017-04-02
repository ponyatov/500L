log.log: 500L.py parse.py
	python parse.py < $< > $@ && tail $(TAIL) $@
