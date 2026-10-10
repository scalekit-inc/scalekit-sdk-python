"""Progress reported by ``ActionClient.upload_resumable``."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class UploadProgress:
    """How much of a resumable upload the server has confirmed as stored.

    Passed to the ``on_progress`` callback of
    ``client.actions.upload_resumable`` each time the committed offset
    advances, and once more when the upload completes. A zero-length upload
    reports a single ``UploadProgress(0, 0)``.

    Attributes:
        bytes_committed: Bytes the server has confirmed so far.
        total_bytes: Total size of the upload, or ``None`` while it is not
            known yet (a stream of unknown length that has not reached its
            end). The completion call always carries the total.

    Example:
        >>> def show(p: UploadProgress) -> None:
        ...     if p.total_bytes:
        ...         print(f"{p.bytes_committed / p.total_bytes:.0%}")
        ...     else:
        ...         print(f"{p.bytes_committed} bytes")
    """

    bytes_committed: int
    total_bytes: int | None
