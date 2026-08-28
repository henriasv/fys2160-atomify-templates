#!/usr/bin/env python3
"""Validate examples.json against the files in this repository.

Run it before pushing:   python check_examples.py
Check the published URLs: python check_examples.py --remote

Every relative path in examples.json is resolved by Atomify as
``{baseUrl}/{path}``.  With baseUrl pointing at this repository's ``main``
branch, that means every path must exist relative to this file.  Project
creation in Atomify is all-or-nothing: one missing file (HTTP 404) and neither
"Quick run" nor "Use as project" works for that example.
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
REQUIRED = ("id", "title", "description", "imageUrl", "inputScript", "files")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--remote", action="store_true",
                        help="also request every URL under baseUrl over HTTP")
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []
    urls: list[str] = []

    with open(os.path.join(ROOT, "examples.json")) as f:
        data = json.load(f)

    base_url = data.get("baseUrl", "")
    if not base_url.startswith("http"):
        errors.append(f"baseUrl should be an absolute URL, got {base_url!r}")
    elif "localhost" in base_url or "127.0.0.1" in base_url:
        warnings.append(f"baseUrl is {base_url!r}: fine for local testing, "
                        "change it back before committing")

    def local(path: str, what: str) -> None:
        urls.append(path)
        if not os.path.isfile(os.path.join(ROOT, path)):
            errors.append(f"{what}: {path!r} does not exist in the repository")

    if data.get("descriptionFile"):
        local(data["descriptionFile"], "descriptionFile")

    ids = [e.get("id") for e in data.get("examples", [])]
    for dup in {i for i in ids if ids.count(i) > 1}:
        errors.append(f"duplicate example id {dup!r}")

    for ex in data.get("examples", []):
        name = ex.get("id", "<no id>")
        for key in REQUIRED:
            if key not in ex:
                errors.append(f"{name}: missing required field {key!r}")
        if not re.fullmatch(r"[a-z0-9-]+", name):
            warnings.append(f"{name}: ids are conventionally lower-case [a-z0-9-]")

        file_names = [f.get("fileName") for f in ex.get("files", [])]
        for fn in file_names:
            if not fn or "/" in fn or "%" in fn:
                errors.append(f"{name}: fileName {fn!r} must be a plain file name without '/' or '%'")
        for dup in {fn for fn in file_names if file_names.count(fn) > 1}:
            errors.append(f"{name}: fileName {dup!r} listed twice")

        if ex.get("imageUrl"):
            local(ex["imageUrl"], f"{name}: imageUrl")
        for entry in ex.get("files", []):
            if "url" in entry:
                local(entry["url"], f"{name}: files[{entry.get('fileName')}]")
            elif "content" not in entry:
                errors.append(f"{name}: file {entry.get('fileName')!r} has neither url nor content")

        if ex.get("inputScript") and ex["inputScript"] not in file_names:
            errors.append(f"{name}: inputScript {ex['inputScript']!r} is not one of files[].fileName")

        # analysisScript is resolved as {baseUrl}/{analysisScript} and fetched at
        # project creation; a bare file name 404s unless the notebook sits at the
        # repository root.  Listing the notebook under files[] is enough.
        if ex.get("analysisScript"):
            local(ex["analysisScript"], f"{name}: analysisScript")
            if ex["analysisScript"] in file_names or os.path.basename(ex["analysisScript"]) in file_names:
                warnings.append(f"{name}: analysisScript duplicates a files[] entry; "
                                "Atomify will download the notebook twice")

        for fn in file_names:
            if fn and fn.endswith(".ipynb"):
                check_notebook(name, ex, fn, errors, warnings)

    if args.remote and base_url.startswith("http"):
        for path in urls:
            url = f"{base_url}/{path}"
            try:
                req = urllib.request.Request(url, method="HEAD")
                with urllib.request.urlopen(req, timeout=20) as resp:
                    status = resp.status
            except urllib.error.HTTPError as exc:
                status = exc.code
            except Exception as exc:  # noqa: BLE001
                status = str(exc)
            if status != 200:
                errors.append(f"remote: {url} -> {status}")
            else:
                print(f"ok   {url}")

    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"ERROR:   {e}")
    n = len(data.get("examples", []))
    if errors:
        print(f"\n{n} examples, {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"\n{n} examples OK ({len(warnings)} warning(s))")
    return 0


def check_notebook(name, ex, file_name, errors, warnings):
    entry = next(f for f in ex["files"] if f.get("fileName") == file_name)
    path = os.path.join(ROOT, entry.get("url", ""))
    if not os.path.isfile(path):
        return
    try:
        with open(path) as f:
            nb = json.load(f)
    except json.JSONDecodeError as exc:
        errors.append(f"{name}: {file_name} is not valid JSON ({exc})")
        return
    kernel = nb.get("metadata", {}).get("kernelspec", {}).get("name")
    if kernel != "python":
        warnings.append(f"{name}: {file_name} kernelspec.name is {kernel!r}; Atomify's "
                        "JupyterLite kernel is named 'python'")
    source = "\n".join(
        "".join(c.get("source", [])) if isinstance(c.get("source"), list) else c.get("source", "")
        for c in nb.get("cells", []) if c.get("cell_type") == "code"
    )
    if "/drive" in source:
        warnings.append(f"{name}: {file_name} uses sys.path '/drive'; use '%pip install lammps-logfile' instead")
    if re.search(r"""File\(\s*["']\.?/?log\.lammps["']""", source):
        warnings.append(f"{name}: {file_name} opens 'log.lammps' in the notebook directory; "
                        "Atomify writes it to runs/<run>/log.lammps (use glob('runs/*/log.lammps'))")
    if "lammps_logfile" in source and "lammps-logfile" not in source:
        warnings.append(f"{name}: {file_name} imports lammps_logfile without '%pip install lammps-logfile'")


if __name__ == "__main__":
    sys.exit(main())
