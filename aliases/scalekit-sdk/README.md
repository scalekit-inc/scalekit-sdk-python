# scalekit-sdk

This package is an alias. Installing it installs
[`scalekit-sdk-python`](https://pypi.org/project/scalekit-sdk-python/), the
official Scalekit Python SDK, and nothing else.

Install the SDK directly instead:

```bash
pip install scalekit-sdk-python
```

The import name is the same either way:

```python
from scalekit import ScalekitClient
```

Scalekit publishes this name so that `pip install scalekit-sdk` can't resolve to a
package from someone else.
