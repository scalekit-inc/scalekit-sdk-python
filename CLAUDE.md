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

## Release notes and releases

- Package: `scalekit-sdk-python` on PyPI. Workflow: `.github/workflows/release.yml`.
- Every change that users can notice adds a release-notes file under `.changes/unreleased/`.
- Never hand-edit the version (`scalekit/_version.py`) or `CHANGELOG.md` sections: release
  tooling bumps the version and renders the CHANGELOG section from those files.
- Publishing a GitHub Release for a merged version starts the release workflow. It waits for
  an approval on the `release` environment from someone other than the person who started
  it, then publishes to PyPI.
