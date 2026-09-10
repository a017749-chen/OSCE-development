"""Deploy canonical Context Repo skill; dry-run by default. Python 3.10+."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import uuid

STATE = ".sync-state.json"
LOCAL = "deployment.local.json"
SKILL = ".agents/skills/osce-item-development"

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read_registry(path):
    text = path.read_text(encoding="utf-8-sig")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        try:
            import yaml
        except ImportError as exc:
            raise ValueError("YAML registry requires PyYAML; install requirements.txt") from exc
        return yaml.safe_load(text)

def roots(context):
    result = {}
    for name in ("SYSTEM_REGISTRY.yaml", "SYSTEM_REGISTRY.local.yaml"):
        path = context / name
        if path.exists():
            result.update(read_registry(path).get("logical_roots", {}))
    return result

def context_root(explicit=None):
    if explicit:
        path = Path(explicit).expanduser().resolve()
        if not (path / SKILL / "SKILL.md").is_file():
            raise ValueError(f"Canonical skill missing: {path}")
        return path
    configured = os.environ.get("YICHAN_CONTEXT_ROOT")
    if configured:
        return context_root(configured)
    candidates = [Path.home() / "Documents/YiChan-Context-Repo",
                  Path.home() / "YiChan-Context-Repo"]
    found = [p.resolve() for p in candidates if (p / SKILL / "SKILL.md").is_file()]
    if len(found) != 1:
        raise ValueError("Set -ContextRoot / --context-root or YICHAN_CONTEXT_ROOT explicitly.")
    return found[0]

def checked_path(path):
    path = Path(path).absolute()
    for item in (path, *path.parents):
        if item.is_symlink() or (hasattr(item, "is_junction") and item.is_junction()):
            raise ValueError(f"Linked path requires manual review: {item}")
    return path.resolve()

def inventory(source):
    result = {}
    for p in source.rglob("*"):
        checked_path(p)
        if p.is_file() and p.name not in (STATE, LOCAL) and ".sync-backups" not in p.parts:
            result[p.relative_to(source).as_posix()] = p
    if "SKILL.md" not in result:
        raise ValueError("Canonical source has no SKILL.md")
    return result

def deploy(source, targets, metadata, apply=False):
    source = checked_path(source)
    files = inventory(source)
    plans = []
    conflicts = []
    resolved = [checked_path(p) for p in targets]
    if len(set(resolved)) != len(resolved):
        raise ValueError("Duplicate targets")
    for i, target in enumerate(resolved):
        if target == source or target in source.parents or source in target.parents:
            raise ValueError("Source and target must not overlap")
        if target == Path.home().resolve() or target == Path(target.anchor):
            raise ValueError("Refusing broad target")
        if any(other in target.parents or target in other.parents for other in resolved[:i]):
            raise ValueError("Targets must not overlap")
        state_path = checked_path(target / STATE)
        previous = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {}
        previous_hashes = previous.get("files", {})
        changes = []
        for rel, src in files.items():
            dst = checked_path(target / rel)
            wanted = digest(src)
            actual = digest(dst) if dst.is_file() else None
            if actual == wanted:
                continue
            # First adoption requires identical content or a missing target.
            if actual is not None and actual != previous_hashes.get(rel):
                conflicts.append(str(dst))
            changes.append((rel, src, dst, actual, wanted))
        extras = []
        if target.exists():
            for p in target.rglob("*"):
                checked_path(p)
                rel = p.relative_to(target).as_posix()
                if p.is_file() and rel not in files and p.name not in (STATE, LOCAL) and ".sync-backups" not in p.parts:
                    extras.append(rel)
        plans.append((target, changes, extras))
    for target, changes, extras in plans:
        print(json.dumps({"target": str(target), "changes": [r[0] for r in changes],
                          "preserved_extras": extras}, ensure_ascii=False))
    if conflicts:
        raise ValueError("Local edits/unmanaged differences; no files written: " + ", ".join(conflicts))
    if not apply:
        return
    # Preflight all targets before writes; backup overwritten files, retain extras.
    run = uuid.uuid4().hex
    for target, changes, extras in plans:
        for rel, src, dst, before, wanted in changes:
            actual = digest(dst) if dst.is_file() else None
            if actual != before or digest(src) != wanted:
                raise ValueError("Concurrent edit detected; prior backups retained")
            if before is not None:
                backup = target / ".sync-backups" / run / rel
                backup.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(dst, backup)
            dst.parent.mkdir(parents=True, exist_ok=True)
            tmp = dst.with_name(dst.name + "." + run + ".tmp")
            shutil.copy2(src, tmp)
            tmp.replace(dst)
        # Verify against source, including unchanged files, before recording baseline.
        hashes = {rel: digest(src) for rel, src in files.items()}
        if any(not (target / rel).is_file() or digest(target / rel) != sha for rel, sha in hashes.items()):
            raise ValueError("Post-copy verification failed; previous baseline retained")
        target.mkdir(parents=True, exist_ok=True)
        for name, data in ((LOCAL, metadata), (STATE, {"schema_version": 1, "files": hashes})):
            tmp = target / (name + "." + run + ".tmp")
            tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            tmp.replace(target / name)

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--context-root")
    parser.add_argument("--target", action="append")
    parser.add_argument("--template-root")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args(argv)
    try:
        context = context_root(args.context_root)
        logical = roots(context)
        cloud = logical.get("cloud")
        runtime = logical.get("runtime")
        if not isinstance(cloud, str) or not Path(cloud).is_dir():
            raise ValueError("Configure an existing logical_roots.cloud in local registry")
        if not isinstance(runtime, str) or not Path(runtime).is_absolute():
            raise ValueError("Configure absolute logical_roots.runtime in local registry")
        repo = Path(__file__).resolve().parents[1]
        cloud_templates = Path(cloud) / "OSCE/OSCE教案開發教學/4.試題開發格式"
        template_dir = Path(args.template_root) if args.template_root else (
            cloud_templates if cloud_templates.is_dir() else repo / "templates")
        if not template_dir.is_dir() or len(list(template_dir.glob("*.docx"))) < 4:
            raise ValueError(f"Four station templates required: {template_dir}")
        targets = args.target or [
            str(Path.home() / ".claude/skills/osce-item-development"),
            str(Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "skills/osce-item-development")]
        metadata = {"context_root": str(context), "template_dir": str(template_dir.resolve()),
                    "output_dir": str(Path(cloud) / "OSCE/OSCE教案開發教學"),
                    "runtime_dir": str(Path(runtime) / "osce")}
        deploy(context / SKILL, targets, metadata, args.apply)
        return 0
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2

if __name__ == "__main__":
    sys.exit(main())
