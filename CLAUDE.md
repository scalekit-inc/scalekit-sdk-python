# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Session start

At the beginning of each session, if changes to code need to be made, ask the user: "Do you want me to cut a new branch from `main`, or continue working on the existing branch (`<current-branch>`)?"

## Commands

```bash
make setup   # Create/update .venv and install dependencies
make lint    # compileall on scalekit/ and tests/
make test    # unittest discover
make generate  # Regenerate from proto (needs buf)
```

## Release

Package: `scalekit-sdk-python` on PyPI. Workflow: `.github/workflows/release.yml`.

1. Bump `scalekit/_version.py`. Use a minor or patch bump. `setup.py` reads this file.
2. Review the unreleased changes. If proto or generated API files changed, extra generation steps apply. Those steps are not documented yet. Do not invent them. Ask before you regenerate.
3. Merge the release branch to `main`.
4. Create a git tag that matches the version (`v2.17.0` for `2.17.0`). Create and publish a GitHub Release for that tag.
5. After publication, the Release workflow starts automatically. Open the Actions run and obtain approval for the `release` environment.
6. After approval, the workflow publishes to PyPI.
