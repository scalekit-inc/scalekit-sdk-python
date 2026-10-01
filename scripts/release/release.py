#!/usr/bin/env python3
"""Release tooling shared by the Scalekit SDKs.

Canonical copy: scalekit-sdks-wrapper/tools/release/release.py. Each SDK repo vendors an
identical copy at scripts/release/release.py; `make release-tool-check` in the wrapper
repo fails if a vendored copy drifts.

Fragments are changie-format YAML files in `.changes/unreleased/` (see
standards/release-notes.md §4). This tool validates them, computes the next version,
bumps every version location listed in `release.toml`, renders the CHANGELOG section in
the layout required by standards/release-notes.md §5, and checks pull requests.

Commands:
  check     Validate pending fragments.
  new       Write a fragment non-interactively.
  next      Print the version the pending fragments would release as.
  status    Print release state as JSON (used by /sdk-release).
  prepare   Consume fragments: bump versions, render CHANGELOG section, delete fragments.
  verify    Pull-request check: label, version, CHANGELOG and fragment consistency.
  notes     Print the GitHub Release body for a version.

Exit codes: 0 success, 1 validation failure, 2 usage or environment error.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import fnmatch
import json
import os
import re
import subprocess
import sys
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover - exercised only without PyYAML installed
    sys.stderr.write("release.py needs PyYAML: pip install 'pyyaml>=6'\n")
    sys.exit(2)

TOOL_VERSION = "1.0.0"

KINDS = ("added", "changed", "deprecated", "removed", "fixed", "security")
SECTION_ORDER = (
    ("breaking", "⚠️ Breaking changes"),
    ("deprecated", "Deprecated"),
    ("added", "Added"),
    ("changed", "Changed"),
    ("fixed", "Fixed"),
    ("security", "Security"),
)
LEVELS = {"patch": 0, "minor": 1, "major": 2}
RELEASE_LABEL = "release"
SKIP_LABEL = "skip-release"
NO_CHANGELOG_LABEL = "no-changelog"

SEMVER_RE = re.compile(
    r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)"
    r"(?:-(?P<pre>[0-9A-Za-z.-]+))?$"
)
TICKET_RE = re.compile(r"^[A-Z][A-Z0-9]+-\d+$")
SECTION_HEADER_RE = re.compile(
    r"^## \[(?P<version>[^\]]+)\](?: - (?P<date>\d{4}-\d{2}-\d{2}))?\s*$"
)
LINK_REF_RE = re.compile(r"^\[(?P<version>[^\]]+)\]: \S+\s*$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
# Prose-only checks (RN-7): internal jargon must not reach the reader.
JARGON_PATTERNS = (
    (
        re.compile(r"\b(?:SK|WF)-\d+\b"),
        "ticket ID in the body (put it in custom.Ticket)",
    ),
    (re.compile(r"(?<![\w/])#\d+\b"), "PR/issue number in the body"),
    (re.compile(r"(?<![\w.`])@[a-z][\w-]*\b"), "@-mention in the body"),
    (
        re.compile(r"^\s*(feat|fix|chore|refactor|docs|test)(\([^)]*\))?!?:", re.I),
        "commit-style prefix",
    ),
    (
        re.compile(
            r"^\s*(misc|minor|various)\b.*\b(fix|fixes|changes|improvements|updates)\b",
            re.I,
        ),
        "vague entry; describe the user-visible change",
    ),
)


class ReleaseError(Exception):
    """A validation or state error that should be reported to the user."""


# --------------------------------------------------------------------------- versions


@dataclass(frozen=True, order=False)
class Version:
    major: int
    minor: int
    patch: int
    pre: str | None = None

    @classmethod
    def parse(cls, text: str) -> "Version":
        m = SEMVER_RE.match(text.strip().removeprefix("v"))
        if not m:
            raise ReleaseError(f"not a semantic version: {text!r}")
        return cls(int(m["major"]), int(m["minor"]), int(m["patch"]), m["pre"])

    def key(self) -> tuple:
        # A pre-release sorts before its release (semver §11, simplified to string compare).
        return (self.major, self.minor, self.patch, self.pre is None, self.pre or "")

    def __lt__(self, other: "Version") -> bool:
        return self.key() < other.key()

    def __le__(self, other: "Version") -> bool:
        return self.key() <= other.key()

    def __gt__(self, other: "Version") -> bool:
        return self.key() > other.key()

    def __ge__(self, other: "Version") -> bool:
        return self.key() >= other.key()

    def bump(self, level: str) -> "Version":
        if level == "major":
            return Version(self.major + 1, 0, 0)
        if level == "minor":
            return Version(self.major, self.minor + 1, 0)
        if level == "patch":
            return Version(self.major, self.minor, self.patch + 1)
        raise ReleaseError(f"unknown bump level {level!r}")

    def __str__(self) -> str:
        base = f"{self.major}.{self.minor}.{self.patch}"
        return f"{base}-{self.pre}" if self.pre else base


# --------------------------------------------------------------------------- config


@dataclass
class VersionFile:
    path: str
    pattern: str | None = None
    json_pointers: list[str] = field(default_factory=list)
    count: int | None = None


@dataclass
class Config:
    root: Path
    name: str
    repo: str
    language: str
    tag_prefix: str
    changelog: Path
    fragments_dir: Path
    version_files: list[VersionFile]
    post_bump: list[list[str]]
    shipped: list[str]
    install: str
    install_lang: str
    max_major: int | None

    @classmethod
    def load(cls, root: Path) -> "Config":
        path = root / "release.toml"
        if not path.exists():
            raise ReleaseError(f"{path} not found")
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        project = data.get("project", {})
        for key in ("name", "repo", "language"):
            if key not in project:
                raise ReleaseError(f"release.toml: [project].{key} is required")
        files = []
        for entry in data.get("version_files", []):
            vf = VersionFile(
                path=entry["path"],
                pattern=entry.get("pattern"),
                json_pointers=list(entry.get("json_pointers", [])),
                count=entry.get("count"),
            )
            if bool(vf.pattern) == bool(vf.json_pointers):
                raise ReleaseError(
                    f"release.toml: version file {vf.path} needs exactly one of pattern / json_pointers"
                )
            if vf.pattern and "(?P<version>" not in vf.pattern:
                raise ReleaseError(
                    f"release.toml: pattern for {vf.path} needs a (?P<version>...) group"
                )
            files.append(vf)
        if not files:
            raise ReleaseError(
                "release.toml: at least one [[version_files]] entry is required"
            )
        release = data.get("release", {})
        return cls(
            root=root,
            name=project["name"],
            repo=project["repo"],
            language=project["language"],
            tag_prefix=project.get("tag_prefix", "v"),
            changelog=root / project.get("changelog", "CHANGELOG.md"),
            fragments_dir=root / project.get("fragments_dir", ".changes/unreleased"),
            version_files=files,
            post_bump=[list(cmd["run"]) for cmd in data.get("post_bump", [])],
            shipped=list(data.get("paths", {}).get("shipped", [])),
            install=release.get("install", ""),
            install_lang=release.get("install_lang", "bash"),
            max_major=project.get("max_major"),
        )


# --------------------------------------------------------------------------- git


def git(cfg_root: Path, *args: str, check: bool = True) -> str:
    proc = subprocess.run(
        ["git", *args], cwd=cfg_root, capture_output=True, text=True, check=False
    )
    if check and proc.returncode != 0:
        raise ReleaseError(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout


def latest_tag(cfg: Config) -> Version | None:
    tags = git(cfg.root, "tag", "--list", f"{cfg.tag_prefix}*").split()
    versions = []
    for tag in tags:
        try:
            versions.append(Version.parse(tag[len(cfg.tag_prefix) :]))
        except ReleaseError:
            continue
    return max(versions, key=Version.key) if versions else None


def tag_exists(cfg: Config, version: Version) -> bool:
    return bool(git(cfg.root, "tag", "--list", f"{cfg.tag_prefix}{version}").strip())


def show_file(cfg: Config, ref: str, rel: str) -> str | None:
    proc = subprocess.run(
        ["git", "show", f"{ref}:{rel}"],
        cwd=cfg.root,
        capture_output=True,
        text=True,
        check=False,
    )
    return proc.stdout if proc.returncode == 0 else None


def changed_files(cfg: Config, base: str) -> list[tuple[str, str]]:
    out = git(cfg.root, "diff", "--name-status", "--no-renames", f"{base}...HEAD")
    result = []
    for line in out.splitlines():
        if not line.strip():
            continue
        status, _, path = line.partition("\t")
        result.append((status[0], path))
    return result


# --------------------------------------------------------------------------- version files


def _json_get(doc: Any, pointer: str) -> Any:
    node = doc
    for part in pointer.split("/")[1:]:
        part = part.replace("~1", "/").replace("~0", "~")
        node = node[part]
    return node


def _json_set(doc: Any, pointer: str, value: Any) -> None:
    parts = [p.replace("~1", "/").replace("~0", "~") for p in pointer.split("/")[1:]]
    node = doc
    for part in parts[:-1]:
        node = node[part]
    node[parts[-1]] = value


def read_versions(cfg: Config, text_of: Any = None) -> dict[str, str]:
    """Return {location: version} for every configured version location.

    text_of(path) -> str | None lets callers read from another git ref.
    """
    found: dict[str, str] = {}
    for vf in cfg.version_files:
        text = text_of(vf.path) if text_of else _read(cfg.root / vf.path)
        if text is None:
            raise ReleaseError(f"version file {vf.path} not found")
        if vf.pattern:
            matches = list(re.finditer(vf.pattern, text, re.MULTILINE))
            if not matches:
                raise ReleaseError(f"{vf.path}: version pattern did not match")
            if vf.count is not None and len(matches) != vf.count:
                raise ReleaseError(
                    f"{vf.path}: expected {vf.count} version matches, found {len(matches)}"
                )
            for i, m in enumerate(matches):
                found[f"{vf.path}#{i + 1}"] = m["version"]
        else:
            doc = json.loads(text)
            for pointer in vf.json_pointers:
                try:
                    found[f"{vf.path}{pointer}"] = str(_json_get(doc, pointer))
                except (KeyError, TypeError) as exc:
                    raise ReleaseError(
                        f"{vf.path}: JSON pointer {pointer} not found"
                    ) from exc
    return found


def source_version(cfg: Config, text_of: Any = None) -> Version:
    versions = read_versions(cfg, text_of)
    distinct = set(versions.values())
    if len(distinct) != 1:
        detail = ", ".join(f"{k}={v}" for k, v in sorted(versions.items()))
        raise ReleaseError(f"version locations disagree: {detail}")
    return Version.parse(distinct.pop())


def write_version(cfg: Config, version: Version) -> list[str]:
    touched = []
    for vf in cfg.version_files:
        path = cfg.root / vf.path
        text = path.read_text(encoding="utf-8")
        if vf.pattern:

            def repl(m: re.Match) -> str:
                start, end = m.span("version")
                s0 = m.start()
                return m.group(0)[: start - s0] + str(version) + m.group(0)[end - s0 :]

            new = re.sub(vf.pattern, repl, text, flags=re.MULTILINE)
        else:
            doc = json.loads(text)
            for pointer in vf.json_pointers:
                _json_set(doc, pointer, str(version))
            new = json.dumps(doc, indent=2, ensure_ascii=False) + "\n"
        if new != text:
            path.write_text(new, encoding="utf-8")
            touched.append(vf.path)
    for cmd in cfg.post_bump:
        run = [part.replace("{version}", str(version)) for part in cmd]
        proc = subprocess.run(
            run, cwd=cfg.root, capture_output=True, text=True, check=False
        )
        if proc.returncode != 0:
            raise ReleaseError(
                f"post_bump {' '.join(run)} failed: {proc.stderr.strip()}"
            )
    return touched


def _read(path: Path) -> str | None:
    return path.read_text(encoding="utf-8") if path.exists() else None


# --------------------------------------------------------------------------- fragments


@dataclass
class Fragment:
    path: Path
    kind: str
    body: str
    breaking: bool
    ticket: str
    migration: str
    time: str

    @property
    def level(self) -> str:
        if self.breaking or self.kind == "removed":
            return "major"
        if self.kind in ("added", "deprecated"):
            return "minor"
        return "patch"

    @property
    def section(self) -> str:
        return "breaking" if (self.breaking or self.kind == "removed") else self.kind


def _prose_lines(markdown: str) -> list[str]:
    """Lines outside fenced code blocks, with inline code removed."""
    lines, in_fence = [], False
    for line in markdown.splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if not in_fence:
            lines.append(re.sub(r"`[^`]*`", "``", line))
    return lines


def parse_fragment(path: Path) -> tuple[Fragment | None, list[str]]:
    errors: list[str] = []
    rel = path.name
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        return None, [f"{rel}: invalid YAML: {exc}"]
    if not isinstance(data, dict):
        return None, [f"{rel}: expected a mapping"]
    kind = data.get("kind")
    body = data.get("body")
    custom = data.get("custom") or {}
    if kind not in KINDS:
        errors.append(f"{rel}: kind must be one of {', '.join(KINDS)} (got {kind!r})")
    if not isinstance(body, str) or len(body.strip()) < 20:
        errors.append(f"{rel}: body must be at least 20 characters of Markdown")
        body = body if isinstance(body, str) else ""
    breaking_raw = custom.get("Breaking")
    if breaking_raw not in ("Yes", "No"):
        errors.append(
            f'{rel}: custom.Breaking must be the quoted string "Yes" or "No" (got {breaking_raw!r})'
        )
    breaking = breaking_raw == "Yes"
    ticket = str(custom.get("Ticket") or "")
    if not TICKET_RE.match(ticket):
        errors.append(f"{rel}: custom.Ticket must look like SK-1234 (got {ticket!r})")
    migration = custom.get("Migration") or ""
    if not isinstance(migration, str):
        errors.append(f"{rel}: custom.Migration must be a string")
        migration = ""
    if kind == "removed" and not breaking:
        errors.append(
            f"{rel}: kind 'removed' is always breaking; set custom.Breaking: \"Yes\""
        )
    if breaking:
        if not migration.strip():
            errors.append(
                f"{rel}: breaking change needs custom.Migration (steps + before/after code)"
            )
        elif not any(FENCE_RE.match(line) for line in migration.splitlines()):
            errors.append(
                f"{rel}: custom.Migration needs before/after code in a fenced block"
            )
    elif migration.strip():
        errors.append(
            f'{rel}: custom.Migration must be empty when custom.Breaking is "No"'
        )
    for line in _prose_lines(body):
        for regex, message in JARGON_PATTERNS:
            if regex.search(line):
                errors.append(f"{rel}: {message}: {line.strip()[:80]!r}")
    if errors:
        return None, errors
    return Fragment(
        path=path,
        kind=str(kind),
        body=body.rstrip("\n"),
        breaking=breaking,
        ticket=ticket,
        migration=migration.rstrip("\n"),
        time=str(data.get("time", "")),
    ), []


def load_fragments(cfg: Config) -> tuple[list[Fragment], list[str]]:
    if not cfg.fragments_dir.exists():
        return [], []
    frags, errors = [], []
    for path in sorted(cfg.fragments_dir.glob("*.yaml")) + sorted(
        cfg.fragments_dir.glob("*.yml")
    ):
        frag, errs = parse_fragment(path)
        errors.extend(errs)
        if frag:
            frags.append(frag)
    frags.sort(key=lambda f: (f.time, f.path.name))
    return frags, errors


def required_level(frags: list[Fragment]) -> str | None:
    if not frags:
        return None
    return max((f.level for f in frags), key=LEVELS.__getitem__)


def compute_next(cfg: Config, frags: list[Fragment]) -> Version | None:
    level = required_level(frags)
    if level is None:
        return None
    base = latest_tag(cfg) or Version(0, 0, 0)
    nxt = base.bump(level)
    _check_major(cfg, nxt)
    return nxt


def _check_major(cfg: Config, version: Version) -> None:
    if cfg.max_major is not None and version.major > cfg.max_major:
        raise ReleaseError(
            f"{version} would cross major version {cfg.max_major}. For Go this means a new module "
            f"path (/v{version.major}) and an import-path change for every caller; it is not a "
            "routine release. Use a deprecation path inside the current major instead."
        )


# --------------------------------------------------------------------------- rendering


def _indent(text: str, prefix: str = "  ") -> str:
    return "\n".join(
        prefix + line if line.strip() else "" for line in text.splitlines()
    )


def render_entry(frag: Fragment) -> str:
    lines = frag.body.splitlines()
    out = "- " + lines[0]
    if len(lines) > 1:
        out += "\n" + _indent("\n".join(lines[1:]))
    if frag.section == "breaking":
        out += "\n\n  **Migration**\n\n" + _indent(frag.migration)
    return out


def render_section(
    version: Version, date: str, frags: list[Fragment], highlights: str = ""
) -> str:
    parts = [f"## [{version}] - {date}"]
    if highlights.strip():
        parts.append(highlights.strip())
    for key, title in SECTION_ORDER:
        entries = [render_entry(f) for f in frags if f.section == key]
        if entries:
            parts.append(f"### {title}")
            parts.append("\n\n".join(entries))
    return "\n\n".join(parts) + "\n"


CHANGELOG_HEADER = """# Changelog

All notable changes to this SDK are documented in this file. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) with the layout defined in the
Scalekit release-notes standard, and versions follow [Semantic Versioning](https://semver.org/).
"""


def insert_section(changelog: str, section: str, link_ref: str | None) -> str:
    if not changelog.strip():
        changelog = CHANGELOG_HEADER
    lines = changelog.rstrip("\n").split("\n")
    first_section = next(
        (i for i, ln in enumerate(lines) if SECTION_HEADER_RE.match(ln)), None
    )
    first_ref = next((i for i, ln in enumerate(lines) if LINK_REF_RE.match(ln)), None)
    if first_section is None:
        cut = first_ref if first_ref is not None else len(lines)
        head, tail = lines[:cut], lines[cut:]
        while head and not head[-1].strip():
            head.pop()
        new = head + ["", section.rstrip("\n"), ""] + tail
    else:
        new = (
            lines[:first_section]
            + section.rstrip("\n").split("\n")
            + [""]
            + lines[first_section:]
        )
    text = "\n".join(new).rstrip("\n") + "\n"
    if link_ref:
        body = text.rstrip("\n").split("\n")
        ref_idx = next((i for i, ln in enumerate(body) if LINK_REF_RE.match(ln)), None)
        if ref_idx is None:
            body += ["", link_ref]
        else:
            body.insert(ref_idx, link_ref)
        text = "\n".join(body) + "\n"
    return text


def find_section(changelog: str, version: str) -> str | None:
    lines = changelog.split("\n")
    start = None
    for i, line in enumerate(lines):
        m = SECTION_HEADER_RE.match(line)
        if m and m["version"] == version:
            start = i
            continue
        if start is not None and (
            SECTION_HEADER_RE.match(line) or LINK_REF_RE.match(line)
        ):
            return "\n".join(lines[start:i]).strip("\n")
    if start is not None:
        return "\n".join(lines[start:]).strip("\n")
    return None


def section_level(section: str) -> str | None:
    headings = {
        m.group(1).strip() for m in re.finditer(r"^### (.+)$", section, re.MULTILINE)
    }
    if not headings:
        return None
    if any("Breaking" in h for h in headings):
        return "major"
    if headings & {"Added", "Deprecated"}:
        return "minor"
    return "patch"


def section_versions(changelog: str) -> list[Version]:
    out = []
    for line in changelog.split("\n"):
        m = SECTION_HEADER_RE.match(line)
        if m:
            try:
                out.append(Version.parse(m["version"]))
            except ReleaseError:
                continue
    return out


# --------------------------------------------------------------------------- commands


def cmd_check(cfg: Config, args: argparse.Namespace) -> int:
    frags, errors = load_fragments(cfg)
    for err in errors:
        print(f"error: {err}")
    if not errors:
        print(f"ok: {len(frags)} pending fragment(s) valid")
    return 1 if errors else 0


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:40] or "change"


def cmd_new(cfg: Config, args: argparse.Namespace) -> int:
    body = (
        Path(args.body_file).read_text(encoding="utf-8")
        if args.body_file
        else args.body
    )
    migration = (
        Path(args.migration_file).read_text(encoding="utf-8")
        if args.migration_file
        else ""
    )
    now = _dt.datetime.now(_dt.timezone.utc).astimezone()
    data = {
        "kind": args.kind,
        "body": body.rstrip("\n") + "\n",
        "time": now.isoformat(),
        "custom": {
            "Breaking": args.breaking,
            "Ticket": args.ticket,
            "Migration": migration,
        },
    }
    cfg.fragments_dir.mkdir(parents=True, exist_ok=True)
    name = f"{args.kind}-{now.strftime('%Y%m%d-%H%M%S')}-{_slug(args.slug or body.splitlines()[0])}.yaml"
    path = cfg.fragments_dir / name

    class _Literal(str):
        pass

    def _literal(dumper: yaml.Dumper, value: str) -> yaml.Node:
        return dumper.represent_scalar(
            "tag:yaml.org,2002:str", value, style="|" if "\n" in value else None
        )

    yaml.add_representer(_Literal, _literal)
    data["body"] = _Literal(data["body"])
    data["custom"]["Migration"] = _Literal(migration) if migration else ""
    path.write_text(
        yaml.dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8"
    )
    frag, errors = parse_fragment(path)
    if errors:
        path.unlink()
        for err in errors:
            print(f"error: {err}")
        return 1
    print(path.relative_to(cfg.root))
    return 0


def cmd_next(cfg: Config, args: argparse.Namespace) -> int:
    frags, errors = load_fragments(cfg)
    if errors:
        for err in errors:
            print(f"error: {err}")
        return 1
    nxt = compute_next(cfg, frags)
    print(nxt if nxt else "none")
    return 0


def cmd_status(cfg: Config, args: argparse.Namespace) -> int:
    frags, errors = load_fragments(cfg)
    tag = latest_tag(cfg)
    try:
        src = str(source_version(cfg))
        src_error = None
    except ReleaseError as exc:
        src, src_error = None, str(exc)
    changelog = _read(cfg.changelog) or ""
    try:
        nxt = str(compute_next(cfg, frags)) if frags and not errors else None
        next_error = None
    except ReleaseError as exc:
        nxt, next_error = None, str(exc)
    status = {
        "tool_version": TOOL_VERSION,
        "name": cfg.name,
        "latest_tag": f"{cfg.tag_prefix}{tag}" if tag else None,
        "source_version": src,
        "source_version_error": src_error,
        "bumped_untagged": bool(src and tag and Version.parse(src) > tag),
        "changelog_has_source_section": bool(src and find_section(changelog, src)),
        "pending_fragments": [
            {
                "file": f.path.name,
                "kind": f.kind,
                "breaking": f.breaking,
                "ticket": f.ticket,
            }
            for f in frags
        ],
        "fragment_errors": errors,
        "next_version": nxt,
        "next_version_error": next_error,
    }
    print(json.dumps(status, indent=2))
    return 0


def cmd_prepare(cfg: Config, args: argparse.Namespace) -> int:
    frags, errors = load_fragments(cfg)
    if errors:
        for err in errors:
            print(f"error: {err}")
        return 1
    if not frags:
        raise ReleaseError(
            f"no pending fragments in {cfg.fragments_dir.relative_to(cfg.root)}; nothing to release"
        )
    tag = latest_tag(cfg)
    base = tag or Version(0, 0, 0)
    src = source_version(cfg)
    computed = base.bump(required_level(frags))  # type: ignore[arg-type]
    changelog = _read(cfg.changelog) or ""

    if args.version_from_source:
        if args.version:
            raise ReleaseError(
                "--version and --version-from-source are mutually exclusive"
            )
        if tag and not src > tag:
            raise ReleaseError(
                f"--version-from-source: source version {src} is not ahead of latest tag {tag}"
            )
        version = src
    elif args.version:
        version = Version.parse(args.version)
    else:
        version = computed
    if version < computed:
        raise ReleaseError(
            f"{version} is lower than {computed}, which the pending changes require "
            f"(latest tag {tag or 'none'}, highest change: {required_level(frags)})"
        )
    if tag and not version > tag:
        raise ReleaseError(f"{version} is not ahead of the latest tag {tag}")
    if tag_exists(cfg, version):
        raise ReleaseError(f"tag {cfg.tag_prefix}{version} already exists")
    if src > base and src != version and not args.version_from_source:
        raise ReleaseError(
            f"source already says {src} (ahead of tag {tag}) but the release would be {version}. "
            "Use --version-from-source to release the version already in source, or --version to choose."
        )
    if find_section(changelog, str(version)):
        raise ReleaseError(f"{cfg.changelog.name} already has a section for {version}")
    _check_major(cfg, version)

    date = args.date or _dt.date.today().isoformat()
    section = render_section(version, date, frags)
    link_ref = (
        f"[{version}]: https://github.com/{cfg.repo}/compare/{cfg.tag_prefix}{tag}...{cfg.tag_prefix}{version}"
        if tag
        else f"[{version}]: https://github.com/{cfg.repo}/releases/tag/{cfg.tag_prefix}{version}"
    )
    summary = {
        "version": str(version),
        "previous_tag": f"{cfg.tag_prefix}{tag}" if tag else None,
        "level": required_level(frags),
        "fragments": [f.path.name for f in frags],
        "version_files": [],
        "dry_run": bool(args.dry_run),
    }
    if args.dry_run:
        print(section)
        print(json.dumps(summary, indent=2), file=sys.stderr)
        return 0
    if version != src:
        summary["version_files"] = write_version(cfg, version)
    elif cfg.post_bump:
        write_version(cfg, version)
    cfg.changelog.write_text(
        insert_section(changelog, section, link_ref), encoding="utf-8"
    )
    for frag in frags:
        frag.path.unlink()
    print(json.dumps(summary, indent=2))
    return 0


def _matches_any(path: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(path, pat) for pat in patterns)


def cmd_verify(cfg: Config, args: argparse.Namespace) -> int:
    problems: list[str] = []
    labels = {lb.strip() for lb in (args.labels or "").split(",") if lb.strip()}
    changes = changed_files(cfg, args.base)
    changed = {p for _, p in changes}
    frag_rel = str(cfg.fragments_dir.relative_to(cfg.root))
    changelog_rel = str(cfg.changelog.relative_to(cfg.root))
    version_rels = {vf.path for vf in cfg.version_files}
    shipped_changed = sorted(
        p
        for p in changed
        if _matches_any(p, cfg.shipped) and not p.startswith(frag_rel)
    )
    added_frags = [
        p
        for s, p in changes
        if s == "A" and p.startswith(frag_rel + "/") and p.endswith((".yaml", ".yml"))
    ]

    frags, frag_errors = load_fragments(cfg)
    problems.extend(frag_errors)

    def at_base(rel: str) -> str | None:
        return show_file(cfg, args.base, rel)

    head_version = source_version(cfg)
    base_version = source_version(cfg, at_base)
    tag = latest_tag(cfg)
    changelog = _read(cfg.changelog) or ""
    base_changelog = at_base(changelog_rel) or ""

    if NO_CHANGELOG_LABEL in labels:
        if shipped_changed:
            problems.append(
                f"'{NO_CHANGELOG_LABEL}' is only allowed when no shipped code changes; changed: "
                + ", ".join(shipped_changed[:10])
            )
        if head_version != base_version or changelog_rel in changed:
            problems.append(
                f"'{NO_CHANGELOG_LABEL}' PRs must not change the version or {changelog_rel}"
            )
        return _report(problems, "no-changelog PR")

    intent = labels & {RELEASE_LABEL, SKIP_LABEL}
    if len(intent) != 1:
        problems.append(
            f"label the PR with exactly one of '{RELEASE_LABEL}' or '{SKIP_LABEL}' "
            f"(or '{NO_CHANGELOG_LABEL}' for changes that ship nothing); found: {sorted(labels) or 'none'}"
        )
        return _report(problems, "release intent")

    if RELEASE_LABEL in intent:
        # The version may equal the base when the base is already bumped but never tagged
        # (released with `prepare --version-from-source`); it may never go down.
        if head_version < base_version:
            problems.append(
                f"release PR lowers the version: base {base_version}, head {head_version}"
            )
        elif (
            head_version == base_version and tag is not None and not base_version > tag
        ):
            problems.append(
                f"release PR must bump the version: base {base_version} is already tagged"
            )
        if tag and not head_version > tag:
            problems.append(
                f"version {head_version} is not ahead of the latest tag {tag}"
            )
        if tag_exists(cfg, head_version):
            problems.append(f"tag {cfg.tag_prefix}{head_version} already exists")
        if cfg.max_major is not None and head_version.major > cfg.max_major:
            problems.append(
                f"{head_version} crosses major {cfg.max_major} (module path change); not allowed"
            )
        section = find_section(changelog, str(head_version))
        if not section:
            problems.append(f"{changelog_rel} has no section for {head_version}")
        elif find_section(base_changelog, str(head_version)):
            problems.append(
                f"{changelog_rel} section for {head_version} already existed on the base branch"
            )
        else:
            level = section_level(section)
            if level is None:
                problems.append(
                    f"{changelog_rel} section for {head_version} has no entries"
                )
            elif tag:
                minimum = tag.bump(level)
                if head_version < minimum:
                    problems.append(
                        f"{head_version} is too low for a release containing {level}-level changes "
                        f"(minimum {minimum} after {tag})"
                    )
        if frags:
            problems.append(
                "pending fragments must be consumed by `release.py prepare` in a release PR: "
                + ", ".join(f.path.name for f in frags)
            )
    else:
        if head_version != base_version:
            problems.append(
                f"'{SKIP_LABEL}' PR must not change the version ({base_version} → {head_version})"
            )
        if changelog != base_changelog:
            problems.append(
                f"'{SKIP_LABEL}' PR must not edit {changelog_rel}; add a fragment instead"
            )
        if shipped_changed and not added_frags:
            problems.append(
                "this PR changes shipped code but adds no release-notes fragment in "
                f"{frag_rel}/ (run `python scripts/release/release.py new ...`)"
            )
        touched_versions = sorted(version_rels & changed)
        if touched_versions:
            problems.append(
                f"'{SKIP_LABEL}' PR must not edit version files: {', '.join(touched_versions)}"
            )
    return _report(
        problems, f"{'release' if RELEASE_LABEL in intent else 'skip-release'} PR"
    )


def _report(problems: list[str], what: str) -> int:
    if problems:
        print(f"release verify failed for {what}:")
        for p in problems:
            print(f"  - {p}")
        return 1
    print(f"release verify passed for {what}")
    return 0


def cmd_notes(cfg: Config, args: argparse.Namespace) -> int:
    version = Version.parse(args.version)
    changelog = _read(cfg.changelog) or ""
    section = find_section(changelog, str(version))
    if not section:
        raise ReleaseError(f"{cfg.changelog.name} has no section for {version}")
    body = "\n".join(section.split("\n")[1:]).strip("\n")
    previous = [v for v in section_versions(changelog) if v < version and v.pre is None]
    prev = max(previous, key=Version.key) if previous else None
    parts = [body]
    if cfg.install:
        parts.append(
            "### Install / upgrade\n\n"
            f"```{cfg.install_lang}\n{cfg.install.replace('{version}', str(version))}\n```"
        )
    if args.also:
        parts.append("**Also released:** " + " · ".join(args.also))
    if prev:
        parts.append(
            f"**Full diff:** https://github.com/{cfg.repo}/compare/"
            f"{cfg.tag_prefix}{prev}...{cfg.tag_prefix}{version}"
        )
    print("\n\n".join(parts))
    return 0


# --------------------------------------------------------------------------- main


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="release.py", description=__doc__.split("\n\n")[0]
    )
    parser.add_argument(
        "--root", default=os.environ.get("RELEASE_ROOT", "."), help="SDK repo root"
    )
    parser.add_argument(
        "--version-info", action="version", version=f"release.py {TOOL_VERSION}"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("check", help="validate pending fragments")

    p_new = sub.add_parser("new", help="write a fragment")
    p_new.add_argument("--kind", required=True, choices=KINDS)
    p_new.add_argument("--breaking", default="No", choices=("Yes", "No"))
    p_new.add_argument("--ticket", required=True)
    body = p_new.add_mutually_exclusive_group(required=True)
    body.add_argument("--body")
    body.add_argument("--body-file")
    p_new.add_argument("--migration-file")
    p_new.add_argument("--slug")

    sub.add_parser("next", help="print the next version")
    sub.add_parser("status", help="print release state as JSON")

    p_prep = sub.add_parser("prepare", help="consume fragments into a release")
    p_prep.add_argument(
        "--version", help="release as this version (must be >= the computed version)"
    )
    p_prep.add_argument(
        "--version-from-source",
        action="store_true",
        help="release the version already in source (bumped but never tagged)",
    )
    p_prep.add_argument("--date", help="release date YYYY-MM-DD (default: today)")
    p_prep.add_argument(
        "--dry-run", action="store_true", help="print the section, change nothing"
    )

    p_ver = sub.add_parser("verify", help="pull-request check")
    p_ver.add_argument("--base", required=True, help="base ref, e.g. origin/main")
    p_ver.add_argument("--labels", default="", help="comma-separated PR labels")

    p_notes = sub.add_parser(
        "notes", help="print the GitHub Release body for a version"
    )
    p_notes.add_argument("version")
    p_notes.add_argument(
        "--also", action="append", default=[], help="'[Go v2.9.0](url)' sibling link"
    )
    return parser


COMMANDS = {
    "check": cmd_check,
    "new": cmd_new,
    "next": cmd_next,
    "status": cmd_status,
    "prepare": cmd_prepare,
    "verify": cmd_verify,
    "notes": cmd_notes,
}


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        cfg = Config.load(Path(args.root).resolve())
        return COMMANDS[args.command](cfg, args)
    except ReleaseError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except (OSError, KeyError, tomllib.TOMLDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
