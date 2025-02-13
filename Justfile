import? '.gists/just-gh/Justfile'
import? '.gists/just-scriv/Justfile'
import? '.gists/just-version/Justfile'

gist_owner := "makukha"


# list available commands
default:
    @just --list

# initialize dev environment
[group('initialize')]
[macos]
init:
    #!/usr/bin/env bash
    set -euo pipefail
    sudo port install gh git uv yq
    just sync
    # install pre-commit hook
    echo -e "#!/usr/bin/env bash\njust pre-commit" > .git/hooks/pre-commit
    chmod a+x .git/hooks/pre-commit

# clone gists
[group('initialize')]
gist desc:
    #!/usr/bin/env bash
    set -euo pipefail
    mkdir -p .gists
    gist="$(gh api gists | yq '.[] | select(.description=="'"{{desc}}"'") | .id')"
    [ -d .gists/{{desc}} ] || /opt/local/bin/git submodule add "https://gist.github.com/{{gist_owner}}/$gist" ".gists/{{desc}}"
    /opt/local/bin/git submodule update ".gists/{{desc}}"

# synchronize dev environment
[group('initialize')]
sync:
    uv sync --all-extras --all-groups
    just gist just-gh
    just gist just-scriv
    just gist just-version

# update dev environment
[group('initialize')]
upd:
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
pre-merge: lint test docs

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
    just bump
    just changelog
    echo -n "\nProofread the changelog, then press enter: "
    just pre-merge
    echo -n "\nCommit changes, then press enter: "
    just gh-pr
    echo -n "\nMerge pull request, then press enter: "
    just gh-release
    echo -n "\nPublish GitHub release, then press enter: "
    just pypi-publish
