SHELL=/bin/bash -euo pipefail


.PHONY: build
build: dist

dist: src/**/* pyproject.toml README.md uv.lock
	uv lock
	rm -rf $@
	cd $(@D) && uv build -o dist


.PHONY: docs
docs: \
	docs/_build \
	docs/requirements.txt \
	docs/_static/badge-coverage.svg \
	docs/_static/badge-tests.svg \
	README.md


docs/_build: docs/usage.md docs/**/*.* src/**/*.*
	rm -rf $@
	cd docs && uv run sphinx-build -b html . _build

docs/requirements.txt: pyproject.toml uv.lock
	uv export --only-group docs --no-emit-project > $@

docs/_static/badge-coverage.svg: .tmp/coverage.xml
	uv run genbadge coverage --local -i $< -o $@

docs/_static/badge-tests.svg: .tmp/junit.xml
	uv run genbadge tests --local -i $< -o $@

docs/usage.md: FORCE
	uv run docsub sync -i $@

README.md: docs/usage.md FORCE
	uv run docsub sync -i $@


FORCE:
