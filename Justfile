import? '.jist/gh.just'
import? '.jist/manage.just'
import? '.jist/scriv.just'
import? '.jist/version.just'

jist := "https://gist.github.com/makukha/34b318222a015eca1be6920d0e13532e"


# list available commands
default:
    @just --list

# initialize dev environment
[group('initialize')]
[macos]
init:
    sudo port install gh git uv yq
    just pre-commit-init
    just sync

# synchronize dev environment
[group('initialize')]
sync:
    git submodule update --remote .jist
    uv sync --all-extras --all-groups

# update dev environment
[group('initialize')]
upgrade:
    uv sync --all-extras --all-groups --upgrade

# develop

# run linters
[group('develop')]
lint:
    uv run mypy .
    uv run ruff check
    uv run ruff format --check

# run tests
[group('develop')]
test *toxargs: build
    time docker compose run --rm -it tox \
        {{ if toxargs == "" { "run-parallel" } else { "run" } }} \
         --installpkg="$(find dist -name '*.whl')" {{toxargs}}
    make badges

# enter testing docker container
[group('develop')]
shell:
    docker compose run --rm -it --entrypoint bash tox

# build python package
[group('develop')]
build: sync
    make build

# build docs
[group('develop')]
docs:
    make docs

# publish

# publish package on PyPI
[group('publish')]
pypi-publish: build
    uv publish

#
# Operations
#

# run pre-commit hook
[group('manage')]
pre-commit: lint docs

# run pre-merge
[group('manage')]
pre-merge: pre-commit test

# merge
[group('manage')]
merge:
    #!/usr/bin/env bash
    set -euo pipefail
    just pre-merge
    just gh-push
    just gh-pr

# release
[group('manage')]
release:
    #!/usr/bin/env bash
    set -euo pipefail
    just pre-merge
    #just bump
    just changelog
    just prompt "Proofread the changelog"
    just pre-merge
    just prompt "Commit changes"
    just gh-pr
    just prompt "Merge pull request"
    just gh-release
    just prompt "Publish GitHub release"
    just pypi-publish
