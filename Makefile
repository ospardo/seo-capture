.PHONY: all
all:
	$(info "There is no need to build anything!")

.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: tests
tests:
	$(info "Tests are not currently implemented")

.PHONY: docs
docs:
	pip install -q -r docs/requirements.txt
	$(info "Doc generation using pdoc not currently implemented")

.PHONY: clean
clean:
	rm -rf seo-capture/__pycache__
