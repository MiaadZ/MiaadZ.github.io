#!/usr/bin/env python3
"""Phase 4 identity/topics/activity checks; no extra Python dependencies.
Usage: python3 docs/verify-phase4.py [generated-site]
In-memory Ruby fixtures verify future collections; no content files are created.
"""
from pathlib import Path
from html.parser import HTMLParser
import json
import re
import subprocess
import sys
from urllib.parse import urlsplit

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
review = json.loads(Path("docs/topic-evidence.json").read_text())
corrections = json.loads(Path("docs/editorial-corrections.json").read_text())["writeups"]
manifest = json.loads(Path("docs/legacy-manifest.yml").read_text())
narrative = "I started in software development, moved deeper into Linux and infrastructure, and eventually into security. This notebook is where I document the parts worth keeping: writeups, notes, research, experiments and tools."

class Node:
    def __init__(self, tag="", attrs=None):
        self.tag, self.attrs, self.children = tag, attrs or {}, []
    def walk(self):
        yield self
        for child in self.children:
            if isinstance(child, Node):
                yield from child.walk()
    def find(self, tag=None, cls=None, **attrs):
        return [n for n in self.walk() if (tag is None or n.tag == tag) and (cls is None or cls in n.attrs.get("class", "").split()) and all(n.attrs.get(k) == v for k, v in attrs.items())]
    def text(self):
        return "".join(c.text() if isinstance(c, Node) else c for c in self.children)

class Tree(HTMLParser):
    VOID = {"meta", "link", "img", "br", "hr", "input", "source", "wbr", "area", "base", "col", "embed", "param", "track"}
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.root = Node()
        self.stack = [self.root]
        self.feed(path.read_text())
    def handle_starttag(self, tag, attrs):
        node = Node(tag, dict(attrs))
        self.stack[-1].children.append(node)
        if tag not in self.VOID:
            self.stack.append(node)
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID:
            self.handle_endtag(tag)
    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                self.stack = self.stack[:i]
                break
    def handle_data(self, data):
        self.stack[-1].children.append(data)

ruby = r'''
require "yaml"; require "date"; require "json"
types = {"writeups"=>"writeup", "notes"=>"note", "research"=>"research", "projects"=>"project"}
records = types.flat_map do |collection, type|
  Dir["_#{collection}/*.md"].filter_map do |path|
    raw = File.read(path)
    data = YAML.safe_load(raw.match(/\A---\n(.*?)\n---\n/m)[1], permitted_classes:[Date,Time])
    next if data["published"] == false || data["status"] == "draft" || data["date"].to_date > Date.today
    data.merge("type" => data.fetch("type", type), "date" => data["date"].to_date.to_s, "path" => path)
  end
end
topics = Dir["_topics/*.md"].filter_map do |path|
  raw = File.read(path)
  data = YAML.safe_load(raw.match(/\A---\n(.*?)\n---\n/m)[1], permitted_classes:[Date,Time])
  next if data["published"] == false
  data
end
puts JSON.generate({"entries"=>records, "topics"=>topics})
'''
source = json.loads(subprocess.check_output(["ruby", "-e", ruby]))
records, published_topics = source["entries"], source["topics"]
records.sort(key=lambda r: (-int(r["date"].replace("-", "")), r["title"].lower(), r["permalink"]))
home = Tree(root / "index.html").root
assert narrative in " ".join(home.text().split())
assert "Breaking, building and understanding systems." in home.text()
assert not any(p in home.text().lower() for p in ("cybersecurity enthusiast", "aspiring security", "available for work", "hire me", "linkedin"))
assert all(n.attrs.get("aria-hidden") == "true" for n in home.find(cls="glitch-layer") + home.find(cls="binary"))
assert "01010011 00110011 01011010 00110100 01010010" in home.find(cls="binary")[0].text()

def section(name):
    return next(n for n in home.find("section") if n.attrs.get("aria-labelledby") == name)

def entry_urls(node):
    return [n.find("h3")[0].find("a")[0].attrs["href"] for n in node.find("li", cls="content-entry")]

assert entry_urls(section("featured-title")) == [r["permalink"] for r in records if r.get("starred")][:3]
assert all(n.find(cls="featured-label") for n in section("featured-title").find("li", cls="content-entry"))
assert entry_urls(section("latest-title")) == [r["permalink"] for r in records[:6]]
assert [n.text().strip().upper() for n in section("latest-title").find("li", cls="content-type")] == [r["type"].upper() for r in records[:6]]
nav = home.find("ul", cls="nav-list")[0]
expected_nav = ["/writeups/", "/topics/"] + ["/" + c + "/" for c, t in (("notes","note"),("research","research"),("projects","project")) if any(r["type"] == t for r in records)]
assert [n.attrs["href"] for n in nav.find("a")] == expected_nav
assert {n.attrs["href"] for n in home.find("a") if urlsplit(n.attrs["href"]).scheme} == {"https://tryhackme.com/p/S3Z4R"}

assert {t["slug"] for t in review["topics"]}.issubset({t["slug"] for t in published_topics})
home_topic_urls = {n.attrs["href"] for n in section("explore-title").find("h3") for n in n.find("a")}
assert home_topic_urls == {t["permalink"] for t in published_topics if t.get("featured")}
topic_rows = Tree(root / "topics/index.html").root.find("li", cls="topic-entry")
assert len(topic_rows) == len(published_topics)
source_routes = {Path(e["target_source_path"]).name: e["permalink"] for e in manifest["writeups"]}
for topic in published_topics:
    tree = Tree(root / topic["permalink"].lstrip("/") / "index.html").root
    assert topic["description"] in tree.text()
    related = [r for type_ in ("note","writeup","research","project") for r in records if r["type"] == type_ and topic["slug"] in r.get("topics", [])]
    assert entry_urls(tree) == [r["permalink"] for r in related], topic["slug"]
    assert str(len(related)) + (" entry" if len(related) == 1 else " entries") + " in the notebook" in " ".join(tree.text().split())
    groups = tree.find("section", cls="topic-group")
    assert len(groups) == len({r["type"] for r in related}), topic["slug"]
    assert all(g.find("li", cls="content-entry") for g in groups)
for topic in review["topics"]:
    assert len(topic["members"]) >= 2
    for source, anchor, reason in topic["members"]:
        doc = Tree(root / source_routes[source].lstrip("/")).root
        assert any(n.attrs.get("id") == anchor for n in doc.walk()), (source, anchor)
        assert reason.strip()
for entry in manifest["writeups"]:
    path = entry["target_source_path"]
    current = Path(path).read_bytes()
    prior = subprocess.check_output(["git", "show", "HEAD:" + path])
    def without_topics(data):
        match = re.match(br"\A---\r?\n.*?\r?\n---(?:\r?\n|$)", data, re.S)
        return re.sub(br"(?m)^topics:.*\r?\n", b"", data[:match.end()]) + data[match.end():]
    for correction in corrections.get(path, []):
        old, new = correction["old"].encode(), correction["new"].encode()
        if old in prior:
            assert prior.count(old) == 1
            prior = prior.replace(old, new, 1)
    assert without_topics(current) == without_topics(prior), path
assert Path("_templates/ctf-template.md").read_bytes() == subprocess.check_output(["git", "show", "HEAD:_templates/ctf-template.md"])
assert not any(root.rglob("*.js"))
assert all(not Tree(p).root.find("script") for p in root.rglob("*.html"))
print("PASS: exact narrative, real featured/latest selection, content labels, conditional navigation, curated topic membership/counts/anchors and decorative ARIA")
print("PASS: all 20 sources match HEAD except reviewed topics metadata and exact Phase 6 editorial corrections; template unchanged; no frontend JavaScript")

# Build-only in-memory fixtures: no fake Notes/Research/Projects source or HTML files.
fixture = r'''
require "jekyll"; require "date"; require "time"; require "json"
Liquid::Template.register_filter(Jekyll::Filters)
site = Jekyll::Site.new(Jekyll.configuration({"source"=>Dir.pwd,"quiet"=>true,"disable_disk_cache"=>true}))
site.read
generator = Notebook::Foundation.new
generator.generate(site)
baseline_count = site.config["notebook_entries"].length
actual = site.collections["writeups"].docs.first
Fixture = Struct.new(:data,:url,:path,:collection) do
  def date; Time.parse(data["date"].to_s); end
  def to_liquid; data.merge("url"=>url); end
end
fixtures = []
{"notes"=>"note","research"=>"research","projects"=>"project"}.each do |name,type|
  data = actual.data.dup.merge("type"=>type, "date"=>Time.local(site.time.year,site.time.month,site.time.day))
  item = Fixture.new(data,"/__fixture__/#{type}/","in-memory-only",site.collections[name])
  site.collections[name].docs << item
  fixtures << item
end
generator.generate(site)
latest = site.config["notebook_entries"].first(6)
abort "Mixed activity missing a type" unless %w[writeup note research project].all? { |type| latest.any? { |d| d.data["type"]==type } }
labels = Liquid::Template.parse(File.read("_includes/content-list.html")).render!({"include"=>{"entries"=>latest}},registers:{site:site})
%w[writeup note research project].each { |type| abort "Missing content label" unless labels.include?(">#{type}</li>") }
nav = Liquid::Template.parse(File.read("_includes/header.html")).render!({"site"=>site.site_payload["site"],"page"=>{"url"=>"/"}},registers:{site:site})
%w[notes research projects].each { |name| abort "Populated navigation hidden" unless nav.include?('href="/'+name+'/"') }
fixtures.each { |item| item.data["published"]=false }
generator.generate(site)
abort "Unpublished fixtures included" unless site.config["notebook_entries"].length==baseline_count
puts "PASS: in-memory Notes/Research/Projects automatically enter Latest and primary navigation; unpublished entries stay excluded; no files created"
'''
env = dict(__import__("os").environ)
env["BUNDLE_FROZEN"] = "true"
if not env.get("BUNDLE_PATH"):
    env["BUNDLE_PATH"] = str(Path("docs/vendor/bundle").resolve()) if Path("docs/vendor/bundle").exists() else str(Path("vendor/bundle").resolve())
subprocess.run(["bundle", "exec", "ruby", "-e", fixture], env=env, check=True)
