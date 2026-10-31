#!/usr/bin/env python3
"""Dependency-free publication policy checks; Ruby/Psych parses workflow YAML."""
import json
import os
from pathlib import Path
import re
import subprocess
from urllib.parse import urlsplit


def yaml(path):
    return json.loads(subprocess.check_output([
        "ruby", "-ryaml", "-rjson", "-rdate", "-e",
        "puts JSON.generate(YAML.safe_load_file(ARGV[0], permitted_classes: [Date, Time]))", path
    ], text=True))

w = yaml(".github/workflows/pages.yml")
assert set(w["on"]) == {"push", "pull_request", "workflow_dispatch"}
for event in ("push", "pull_request"):
    assert w["on"][event]["branches"] == ["main"]
assert w["on"]["workflow_dispatch"]["inputs"]["deploy"]["default"] is False
assert w["permissions"] == {}
b, d = w["jobs"]["build"], w["jobs"]["deploy"]
assert b["permissions"] == {"contents": "read", "pages": "read"}
assert d["permissions"] == {"contents": "read", "pages": "write", "id-token": "write"}
assert d["needs"] == "build" and d["environment"]["name"] == "github-pages"
assert d["concurrency"] == {"group": "pages", "cancel-in-progress": False}
guard = "github.ref == 'refs/heads/main' && (github.event_name == 'push' || (github.event_name == 'workflow_dispatch' && inputs.deploy))"
assert d["if"] == guard
steps = b["steps"]
assert steps[0]["with"] == {"fetch-depth": 0, "persist-credentials": False}
assert steps[1]["if"] == guard and steps[1]["with"] == {"enablement": False}
assert steps[2]["with"] == {"bundler": "Gemfile.lock", "bundler-cache": True}
assert steps[-1]["with"]["path"] == "_site"
for job in (b, d):
    for step in job["steps"]:
        if "uses" in step:
            assert re.fullmatch(r"(?:actions/(?:checkout|configure-pages|upload-pages-artifact|deploy-pages)|ruby/setup-ruby)@[0-9a-f]{40}", step["uses"])
        if "run" in step:
            assert "${{" not in step["run"], "Pass event values through quoted environment variables"
assert w["env"] == {"BUNDLE_FROZEN": "true", "JEKYLL_ENV": "production"}
c = yaml("_config.yml")
assert c.get("baseurl", "") == "" and os.environ.get("PAGES_BASE_PATH", "") == "", "User-site legacy routes require a root base path"
u = urlsplit(c["url"])
assert u.scheme == "https" and u.hostname and u.path in ("", "/")
assert not Path("CNAME").exists(), "Custom domain requires a separately reviewed phase"
subprocess.run(["git", "diff", "--check"], check=True)
# Check introduced whitespace on CI commits, without shell evaluation of event data.
event_path = os.environ.get("GITHUB_EVENT_PATH")
if event_path:
    event = json.loads(Path(event_path).read_text())
    base = event.get("pull_request", {}).get("base", {}).get("sha") or event.get("before")
    if base and re.fullmatch(r"[0-9a-f]{40}", base) and base != "0" * 40:
        exists = subprocess.run(["git", "cat-file", "-e", base + "^{commit}"], capture_output=True).returncode == 0
        if exists:
            subprocess.run(["git", "diff", "--check", "--find-renames", base, "HEAD"], check=True)
        else:
            raise SystemExit("Missing comparison commit: full checkout history is required")
    else:
        subprocess.run(["git", "show", "--check", "--find-renames", "--format=", "HEAD"], check=True)
print("PASS: parsed YAML; triggers, branch/deployment guard, immutable action refs, permissions, checkout, artifact, concurrency, root path and whitespace policy")
