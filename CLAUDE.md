# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Session start

At the beginning of each session, if changes to code need to be made, ask the user: "Do you want me to cut a new branch from `main`, or continue working on the existing branch (`<current-branch>`)?"

## Commands

```bash
make setup   # Create .venv and install the SDK
make lint    # compileall on scalekit/ and tests/
make test    # unittest discover
make generate  # Regenerate from proto (needs buf)
```

## Release

Package: `scalekit-sdk-python` on PyPI. Workflow: `.github/workflows/release.yml`.

1. Bump `scalekit/_version.py`. Use a minor or patch bump. `setup.py` reads this file.
2. Review the unreleased changes. If proto or generated API files changed, extra generation steps apply. Those steps are not documented yet. Do not invent them. Ask before you regenerate.
3. Merge the release branch to `main`.
4. Create a git tag that matches the version (`v2.17.0` for `2.17.0`). Draft a GitHub Release for that tag.
5. Publishing does not start on its own. Open the Actions run for the release workflow. Any peer can approve it. The `release` environment gates deploy.
6. After approval, the workflow publishes to PyPI.
