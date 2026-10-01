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

- Every PR that changes shipped code adds a release-notes fragment:
  `python3 scripts/release/release.py new --kind <added|changed|deprecated|removed|fixed|security> --ticket SK-1234 --body "..."`
  (or `changie new`). Write it for the developer upgrading; rules are in
  scalekit-sdks-wrapper `standards/release-notes.md`.
- Label every PR `release` or `skip-release` (`no-changelog` only when nothing shipped
  changes). The `release-notes` check enforces the label, the version and CHANGELOG rules.
- Never hand-edit the SDK version or `CHANGELOG.md`. A releasing PR runs
  `python3 scripts/release/release.py prepare`, which computes the version from the
  fragments, bumps every location in `release.toml` and renders the section.
- Merging a version bump to `main` starts `.github/workflows/release.yml`. It builds and
  tests, then waits for a human approval on the `release` environment (someone other than
  the person who merged) before tagging and publishing.
- Cross-SDK changes and release-only runs: `/sdk` and `/sdk-release` from
  scalekit-sdks-wrapper. Never edit `scripts/release/` or the release workflows here; they
  are vendored from that repo.
