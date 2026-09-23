# PyPI name aliases

Metadata-only packages that reserve names people and coding agents guess for
this SDK. Each one depends on `scalekit-sdk-python` and ships no code.

| PyPI name      | Why                                                         |
| -------------- | ----------------------------------------------------------- |
| `scalekit`     | Matches the import name. Older docs told readers to install it. |
| `scalekit-sdk` | Used by an older cookbook.                                   |

Publish with the **Publish PyPI aliases** workflow
(`.github/workflows/publish-aliases.yml`, run manually). It builds and checks
the alias in one job, then publishes the checked files from a second job. Only
that second job can request a PyPI token. Pull requests that change `aliases/`
run the build and check, without publishing.

Before the first run, a PyPI owner must add a pending trusted publisher for
each name:

- Owner: `scalekit-inc`
- Repository: `scalekit-sdk-python`
- Workflow: `publish-aliases.yml`
- Environment: `release`

Bump `version` in an alias's `pyproject.toml` only when its metadata changes.
It doesn't need to track the SDK version.
