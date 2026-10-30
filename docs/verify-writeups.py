#!/usr/bin/env python3
"""Verify immutable legacy content plus normalized publishing output.
Run from repository root:
    python3 docs/verify-writeups.py [generated-site] [pre-migration-output]
No writes, external requests or third-party Python dependencies.
Requires Git and Ruby standard libraries for independent YAML parsing.
"""
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urljoin, urlsplit

MANIFEST = json.loads(Path("docs/legacy-manifest.yml").read_text())
BASELINE = json.loads(Path("docs/phase2-verification.json").read_text())
TOKENS = {
    b"{{ page.machine_url }}": b"{{ page.source_url }}",
    b"{{ page.link }}": b"{{ page.source_url }}",
    b"{{ page.parent }}": b"{{ page.platform }}",
}
sha = lambda data: hashlib.sha256(data).hexdigest()

def body_bytes(data):
    delimiter = re.match(br"\A---\r?\n.*?\r?\n---(?:\r?\n|$)", data, re.S)
    assert delimiter, "Missing front-matter delimiters"
    return data[delimiter.end():]

for entry in MANIFEST["writeups"]:
    assert entry["expected_current_url"] == entry["permalink"] == entry["desired_canonical_url"], entry["target_source_path"]
    assert not Path(entry["source_path"]).exists(), entry["source_path"]
    original = subprocess.check_output(["git", "show", MANIFEST["baseline_git_head"] + ":" + entry["source_path"]])
    assert sha(original) == entry["source_sha256"], entry["source_path"]
    original_body = original[entry["body_offset_bytes"]:]
    assert sha(original_body) == entry["body_sha256"]
    expected = original_body
    for old, new in TOKENS.items():
        expected = expected.replace(old, new)
    actual = Path(entry["target_source_path"]).read_bytes()
    assert body_bytes(actual) == expected, f"Unexpected body edit: {entry['target_source_path']}"
    for asset in entry["referenced_local_assets"]:
        assert sha(Path(asset["source_path"]).read_bytes()) == asset["sha256"], asset["source_path"]

assert len(MANIFEST["writeups"]) == 20
assert not list(Path("TryHackMe").glob("*.md"))
assert not [p for p in Path("_writeups").rglob("*.md") if p.parent != Path("_writeups")], "Nested writeup source"
for p in Path("_writeups").glob("*.md"):
    assert re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)+\.md", p.name), p
print("PASS: all 20 original bodies match exactly after only approved Liquid substitutions; all screenshot hashes unchanged")

ruby = r'''
require "yaml"
require "date"
require "json"
require "uri"
m = YAML.safe_load_file("docs/legacy-manifest.yml")
records = {}
Dir["_writeups/*.md"].sort.each do |path|
  raw = File.binread(path)
  match = raw.match(/\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)/m)
  abort "Missing front matter: #{path}" unless match
  data = YAML.safe_load(match[1], permitted_classes: [Date])
  abort "Missing title/platform/date: #{path}" unless %w[title platform].all? { |key| data[key].is_a?(String) && !data[key].strip.empty? } && data["date"].is_a?(Date)
  abort "Invalid type: #{path}" unless data["type"] == "writeup"
  abort "Invalid tags/starred: #{path}" unless data.fetch("tags", []).is_a?(Array) && [true, false].include?(data.fetch("starred", false))
  abort "Missing explicit permalink: #{path}" unless data["permalink"].is_a?(String) && data["permalink"].start_with?("/") && !data["permalink"].start_with?("//")
  abort "Legacy field remains: #{path}" unless (data.keys & %w[parent link machine_url toc_sticky toc_icon]).empty?
  source = data["source_url"]
  if source && !source.empty?
    uri = URI.parse(source)
    abort "Invalid source URL: #{path}" unless %w[http https].include?(uri.scheme) && uri.host && !uri.userinfo
  end
  records[path] = data
end
m["writeups"].each do |entry|
  data = records.fetch(entry["target_source_path"])
  %w[title os difficulty tags starred].each { |key| abort "Changed #{key}: #{entry["target_source_path"]}" unless data[key] == entry[key] }
  abort "Changed date" unless data["date"].to_s == entry["date"]
  abort "Changed source" unless data["source_url"] == entry["external_source_url"]
  abort "Changed platform" unless data["platform"] == entry["platform"]
  abort "Changed permalink" unless data["permalink"] == entry["permalink"]
  abort "Unexpected presentation" unless data["layout"] == "article" && data["legacy_body_header"] == true
  %w[toc toc_label].each { |key| abort "Changed TOC" unless data[key] == entry["original_front_matter"][key] }
  expected_keys = %w[layout title type platform source_url os difficulty date tags starred toc toc_label permalink legacy_body_header]
  abort "Unexpected enrichment: #{entry["target_source_path"]}" unless data.keys.sort == expected_keys.sort
end
puts JSON.generate(records.transform_values { |data| data.merge("date" => data["date"].to_s) })
'''
metadata = json.loads(subprocess.check_output(["ruby", "-e", ruby]))
print("PASS: all 20 original titles/dates/platforms/OS/difficulties/tags/starred/source URLs preserved; normalized schema and useful TOC settings verified")

class Document(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids, self.links, self.assets, self.tags, self.canonicals, self.headings = [], [], [], [], [], []
        self.list_depth = None
        self.depth = 0
        self.archive_links = []
        self.heading_tag = None
        self.heading_text = []
        self.pre_texts = []
        self.pre_parts = None
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append(tag)
        if tag == "pre":
            self.pre_parts = []
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "ul":
            self.depth += 1
            if "content-list" in attrs.get("class", "").split():
                self.list_depth = self.depth
        if tag == "a" and "href" in attrs:
            self.links.append(attrs["href"])
            if self.list_depth is not None and self.depth == self.list_depth:
                self.archive_links.append(attrs["href"])
        if tag in ("img", "script") and attrs.get("src"):
            self.assets.append(attrs["src"])
        if tag == "link" and attrs.get("rel") == "stylesheet":
            self.assets.append(attrs["href"])
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonicals.append(attrs["href"])
        if re.fullmatch(r"h[1-6]", tag):
            self.heading_tag = tag
            self.heading_text = []

    def handle_endtag(self, tag):
        if tag == "pre" and self.pre_parts is not None:
            self.pre_texts.append("".join(self.pre_parts))
            self.pre_parts = None
        if tag == "ul":
            if self.list_depth == self.depth:
                self.list_depth = None
            self.depth -= 1
        if tag == self.heading_tag:
            self.headings.append((tag, "".join(self.heading_text)))
            self.heading_tag = None

    def handle_data(self, data):
        if self.pre_parts is not None:
            self.pre_parts.append(data)
        if self.heading_tag:
            self.heading_text.append(data)

if len(sys.argv) > 1:
    root = Path(sys.argv[1])
    documents = {p: Document(p.read_text()) for p in root.rglob("*.html")}
    assert documents, "No generated HTML found"
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
                if path.relative_to(root).as_posix() == "TryHackMe/h4cked.html" and link == "10.10.10.10":
                    warnings.append("Existing h4cked relative link 10.10.10.10 remains unchanged.")
                    continue
                raise AssertionError(f"Missing link: {path.relative_to(root)} -> {link}")
            if resolved.fragment and target in documents:
                assert unquote(resolved.fragment) in documents[target].ids, f"Missing fragment: {link}"
    baseline_routes = {e["original_source"]: e for e in BASELINE["baseline_routes"]}
    for entry in MANIFEST["writeups"]:
        document = documents[root / entry["permalink"].lstrip("/")]
        assert len(document.canonicals) == 1 and urlsplit(document.canonicals[0]).path == entry["permalink"], entry["permalink"]
        assert set(baseline_routes[entry["source_path"]]["preserved_heading_ids"]).issubset(document.ids), entry["target_source_path"]
        assert entry["external_source_url"] in document.links, entry["target_source_path"]
        for asset in entry["referenced_local_assets"]:
            if asset["url"] not in document.assets:
                # Confirmed in the pre-migration render; source Markdown remains protected.
                literal_image = "![Sending the shell of our own](/assets/images/h4cked/put.png)"
                assert entry["title"] == "h4cked" and asset["url"] == "/assets/images/h4cked/put.png" and any(literal_image in block for block in document.pre_texts), asset["url"]
                warnings.append("Existing h4cked put.png reference renders literally as code; eight images render, all nine asset hashes are preserved.")
            assert sha((root / asset["url"].lstrip("/")).read_bytes()) == asset["sha256"]

    if len(sys.argv) > 2:
        before = Path(sys.argv[2])
        for entry in MANIFEST["writeups"]:
            old_document = Document((before / entry["permalink"].lstrip("/")).read_text())
            new_document = documents[root / entry["permalink"].lstrip("/")]
            assert old_document.pre_texts == new_document.pre_texts, f"Rendered command/code change: {entry['target_source_path']}"
            assert sorted(old_document.assets) == sorted(new_document.assets), f"Rendered asset change: {entry['target_source_path']}"
        print("PASS: all rendered code/command-output blocks and runtime asset references match the pre-migration build")

    ordered = sorted(metadata, key=lambda p: (-int(metadata[p]["date"].replace("-", "")), metadata[p]["title"].lower(), metadata[p]["permalink"]))
    expected_urls = [metadata[p]["permalink"] for p in ordered]
    actual = documents[root / "writeups/index.html"].archive_links
    assert actual == expected_urls, "Writeup archive contents or sort mismatch"
    thm = [metadata[p]["permalink"] for p in ordered if metadata[p]["platform"] == "TryHackMe"]
    assert documents[root / "tryhackme/index.html"].archive_links == thm, "Platform archive mismatch"
    assert documents[root / "hackthebox/index.html"].archive_links == [], "Unexpected HTB content"
    assert "No entries published yet." in (root / "hackthebox/index.html").read_text()
    for excluded in ("docs", "AGENTS.md", "README.md", "Gemfile", "Gemfile.lock", "vendor", ".obsidian", "_plugins"):
        assert not (root / excluded).exists(), f"Published development artifact: {excluded}"
    assert not list(root.rglob("*.map")), "Published source map"
    print(f"PASS: {len(documents)} HTML pages; all 20 exact legacy/canonical routes, heading anchors and source links preserved")
    print("PASS: newest-first normalized writeup archive, TryHackMe metadata filtering, clean HackTheBox empty state, Tools links/anchors, landmarks and publishing exclusions")
    for warning in sorted(set(warnings)):
        print("REVIEW:", warning)
