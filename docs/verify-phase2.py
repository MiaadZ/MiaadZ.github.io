#!/usr/bin/env python3
"""Phase 2 preservation/output checks; Python/Ruby standard libraries and Git only.
Usage: python3 docs/verify-phase2.py /path/to/generated/site
Run from the repository root. Does not write or contact external services.
"""
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urljoin, urlsplit

manifest = json.loads(Path("docs/legacy-manifest.yml").read_text())
sha = lambda data: hashlib.sha256(data).hexdigest()
pilot = next(e for e in manifest["writeups"] if e["title"] == "h4cked")
assert not Path(pilot["source_path"]).exists()
assert sorted(str(p) for p in Path("_writeups").glob("*.md")) == [pilot["target_source_path"]]
for entry in manifest["writeups"]:
    if entry is pilot:
        original = subprocess.check_output(["git", "show", manifest["baseline_git_head"] + ":" + entry["source_path"]])
        assert sha(original) == entry["source_sha256"]
        migrated = Path(entry["target_source_path"]).read_bytes()
        delimiter = re.match(br"\A---\r?\n.*?\r?\n---(?:\r?\n|$)", migrated, re.S)
        assert delimiter
        body = migrated[delimiter.end():]
        original_body = original[entry["body_offset_bytes"]:]
        assert original_body.count(b"{{ page.machine_url }}") == 1
        assert body == original_body.replace(b"{{ page.machine_url }}", b"{{ page.source_url }}")
    else:
        assert sha(Path(entry["source_path"]).read_bytes()) == entry["source_sha256"], entry["source_path"]
    for asset in entry["referenced_local_assets"]:
        assert sha(Path(asset["source_path"]).read_bytes()) == asset["sha256"], asset["source_path"]
subprocess.run(["ruby", "-e", "require \"yaml\"; require \"date\"; m=YAML.safe_load_file(\"docs/legacy-manifest.yml\"); e=m[\"writeups\"].find { |x| x[\"title\"]==\"h4cked\" }; s=File.binread(e[\"target_source_path\"]); fm=s.match(/\\A---\\r?\\n(.*?)\\r?\\n---(?:\\r?\\n|$)/m)[1]; a=YAML.safe_load(fm, permitted_classes:[Date]); %w[title difficulty os starred tags].each { |k| abort \"Changed pilot metadata: #{k}\" unless a[k]==e[k] }; abort \"Changed date\" unless a[\"date\"].to_s==e[\"date\"]; abort \"Changed source\" unless a[\"source_url\"]==e[\"external_source_url\"]; abort \"Changed platform\" unless a[\"platform\"]==e[\"platform\"]; abort \"Changed route\" unless a[\"permalink\"]==e[\"permalink\"]; %w[toc toc_sticky toc_label toc_icon].each { |k| abort \"Changed TOC field: #{k}\" unless a[k]==e[\"original_front_matter\"][k] }; abort \"Unexpected metadata enrichment\" unless (a.keys & %w[summary topics techniques tools updated]).empty?"], check=True)
print("PASS: one pilot, exact approved body-token change, 19 untouched writeups, unchanged screenshot bytes")
print("PASS: pilot factual/routing/TOC metadata unchanged; no invented enrichment")

class Document(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids, self.links, self.assets, self.tags = [], [], [], []
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append(tag)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "a" and "href" in attrs:
            self.links.append(attrs["href"])
        if tag in ("img", "script") and attrs.get("src"):
            self.assets.append(attrs["src"])
        if tag == "link" and attrs.get("rel") == "stylesheet":
            self.assets.append(attrs["href"])

if len(sys.argv) > 1:
    root = Path(sys.argv[1])
    documents = {p: Document(p.read_text()) for p in root.rglob("*.html")}
    warnings = []
    for path, document in documents.items():
        assert len(document.ids) == len(set(document.ids)), f"Duplicate IDs: {path}"
        assert document.tags.count("main") == document.tags.count("h1") == 1, path
        for asset in document.assets:
            assert not urlsplit(asset).scheme and not urlsplit(asset).netloc, f"External runtime asset: {asset}"
        for link in document.links + document.assets:
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc:
                continue
            resolved = urlsplit(urljoin("/" + str(path.relative_to(root)), link))
            target = root / unquote(resolved.path).lstrip("/")
            if target.is_dir():
                target /= "index.html"
            if not target.exists():
                # Preserved existing technical prose; do not silently rewrite it.
                if path.relative_to(root).as_posix() == "TryHackMe/h4cked.html" and link == "10.10.10.10":
                    warnings.append("Existing h4cked relative link 10.10.10.10 remains unchanged.")
                    continue
                raise AssertionError(f"Missing link: {path.relative_to(root)} -> {link}")
            if resolved.fragment and target in documents:
                assert unquote(resolved.fragment) in documents[target].ids, f"Missing fragment: {link}"
    for entry in manifest["writeups"]:
        assert (root / entry["permalink"].lstrip("/")).is_file(), entry["permalink"]
    for excluded in ("docs", "AGENTS.md", "README.md", "Gemfile", "Gemfile.lock", "vendor", ".obsidian", "_plugins"):
        assert not (root / excluded).exists(), f"Published development artifact: {excluded}"
    assert not list(root.rglob("*.map")), "Published source map"
    print(f"PASS: {len(documents)} HTML pages; all 20 legacy routes; links/fragments; unique IDs; landmarks; local assets; exclusions")
    for warning in warnings:
        print("REVIEW:", warning)
