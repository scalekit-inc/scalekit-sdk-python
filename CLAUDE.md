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

- Releases and cross-SDK changes are driven from scalekit-sdks-wrapper (`/sdk`, `/sdk-release`).
  Its release tool (`python3 tools/release/release.py --sdk <lang> ...`, run from the wrapper)
  writes release-notes fragments into `.changes/unreleased/`, bumps the version and renders
  `CHANGELOG.md`. Notes follow the wrapper's `standards/release-notes.md`.
- Never hand-edit the SDK version or `CHANGELOG.md` sections.
- `.github/workflows/release.yml` publishes a version after its release PR has merged. It is
  started with that version (by Claude from the wrapper, or by a maintainer), and waits for a
  human approval on the `release` environment from someone other than the person who started
  it. The workflow is generated in the wrapper; don't edit it here.
