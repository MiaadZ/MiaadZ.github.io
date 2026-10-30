#!/usr/bin/env python3
"""Local Chromium/CDP regression checks; Python standard library only.
Start a localhost preview and isolated Chromium debugging instance first.
Usage: python3 docs/verify-browser.py [preview-origin] [debug-origin]
Writes only ignored .jekyll-cache/phase3 screenshots and numeric/route evidence.
"""
import base64
import json
import os
from pathlib import Path
import socket
import struct
import sys
import time
import urllib.request
from urllib.parse import urlsplit

preview = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8873"
debug = sys.argv[2] if len(sys.argv) > 2 else "http://127.0.0.1:9333"
assert all(urlsplit(url).hostname in ("127.0.0.1", "localhost") for url in (preview, debug))
output = Path(".jekyll-cache/phase3")
output.mkdir(parents=True, exist_ok=True)
target = json.load(urllib.request.urlopen(debug + "/json"))[0]
url = urlsplit(target["webSocketDebuggerUrl"])
connection = socket.create_connection((url.hostname, url.port), timeout=15)
connection.sendall(("GET " + url.path + " HTTP/1.1\r\nHost: " + url.netloc + "\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: " + base64.b64encode(os.urandom(16)).decode() + "\r\nSec-WebSocket-Version: 13\r\n\r\n").encode())
header = b""
while b"\r\n\r\n" not in header:
    header += connection.recv(4096)
assert b"101" in header.split(b"\r\n")[0], header[:100]

def exact(length):
    data = b""
    while len(data) < length:
        block = connection.recv(length - len(data))
        if not block:
            raise RuntimeError("Browser disconnected")
        data += block
    return data

sequence = 0
def call(method, params=None):
    global sequence
    sequence += 1
    request_id = sequence
    data = json.dumps({"id": request_id, "method": method, "params": params or {}}).encode()
    mask = os.urandom(4)
    length = len(data)
    frame = bytes([0x81, 0x80 | length]) if length < 126 else bytes([0x81, 0xfe]) + struct.pack(">H", length) if length < 65536 else bytes([0x81, 0xff]) + struct.pack(">Q", length)
    connection.sendall(frame + mask + bytes(value ^ mask[i % 4] for i, value in enumerate(data)))
    while True:
        header = exact(2)
        length = header[1] & 127
        if length == 126:
            length = struct.unpack(">H", exact(2))[0]
        elif length == 127:
            length = struct.unpack(">Q", exact(8))[0]
        response = json.loads(exact(length))
        if response.get("id") == request_id:
            assert "error" not in response, response
            return response.get("result", {})

def evaluate(expression):
    result = call("Runtime.evaluate", {"expression": expression, "returnByValue": True})
    assert "exceptionDetails" not in result, result
    return result["result"].get("value")

def visit(path, width, height=900):
    call("Emulation.setDeviceMetricsOverride", {"width": width, "height": height, "deviceScaleFactor": 1, "mobile": width < 600})
    call("Page.navigate", {"url": preview + path})
    for _ in range(80):
        time.sleep(.05)
        if evaluate("location.pathname") == path and evaluate("document.readyState") == "complete":
            break
    else:
        raise AssertionError("Preview failed to load " + path)
    return evaluate("""({
      path:location.pathname, width:innerWidth, documentWidth:document.documentElement.scrollWidth,
      images:[...document.images].every(i=>i.complete&&i.naturalWidth>0),
      renderedImageCount:document.images.length,
      h1:document.querySelectorAll('h1').length,
      main:document.querySelectorAll('main').length,
      externalAssets:[...document.querySelectorAll('script[src],link[rel="stylesheet"],img[src]')].map(e=>e.src||e.href).filter(u=>!u.startsWith(location.origin)),
      codeRegions:[...document.querySelectorAll('pre')].every(e=>e.parentElement.matches('.scroll-region[tabindex="0"]')),
      tableRegions:[...document.querySelectorAll('table')].every(e=>e.parentElement.matches('.scroll-region[tabindex="0"]')),
      wideCodeRegions:[...document.querySelectorAll('.scroll-region')].filter(e=>e.scrollWidth>e.clientWidth+1).length
    })""")

def press(key, code, number, text=None):
    params = {"type": "keyDown", "key": key, "code": code, "windowsVirtualKeyCode": number}
    if text is not None:
        params["text"] = text
    call("Input.dispatchKeyEvent", params)
    call("Input.dispatchKeyEvent", {"type": "keyUp", "key": key, "code": code, "windowsVirtualKeyCode": number})
    time.sleep(.15)

call("Page.enable")
call("Network.enable")
call("Network.setBlockedURLs", {"urls": ["https://*"]})
manifest = json.loads(Path("docs/legacy-manifest.yml").read_text())
results = []
for entry in manifest["writeups"]:
    results.append(visit(entry["permalink"], 320))
representatives = [
    "/TryHackMe/h4cked.html", "/TryHackMe/Compiled.html", "/TryHackMe/Relevant.html",
    "/TryHackMe/wonderland.html", "/TryHackMe/Skynet.html",
    "/TryHackMe/Advent-of-Cyber-2025.html", "/writeups/", "/tryhackme/", "/hackthebox/", "/tools/"
]
for path in representatives:
    for width in (1440, 390):
        results.append(visit(path, width))
        if path in ("/TryHackMe/h4cked.html", "/writeups/"):
            shot = call("Page.captureScreenshot", {"format": "png", "captureBeyondViewport": False})
            name = ("h4cked" if "h4cked" in path else "writeups") + "-" + str(width) + ".png"
            (output / name).write_bytes(base64.b64decode(shot["data"]))
for path in ("/writeups/", "/tryhackme/", "/hackthebox/", "/tools/"):
    results.append(visit(path, 320))

call("Page.navigate", {"url": "about:blank"})
time.sleep(.1)
visit("/TryHackMe/h4cked.html", 320)
call("Page.bringToFront")
press("Tab", "Tab", 9)
keyboard = {"firstTab": evaluate("document.activeElement.className")}
press("Enter", "Enter", 13, "\r")
keyboard["skipTarget"] = evaluate("document.activeElement.id")
evaluate("document.querySelector('.toc').open=false; document.querySelector('.toc summary').focus()")
press(" ", "Space", 32)
keyboard["spaceOpensContents"] = evaluate("document.querySelector('.toc').open")
keyboard["focusOutline"] = evaluate("getComputedStyle(document.activeElement).outlineStyle")
press("Enter", "Enter", 13, "\r")
keyboard["enterClosesContents"] = not evaluate("document.querySelector('.toc').open")
evaluate("window.region=[...document.querySelectorAll('.scroll-region')].find(e=>e.scrollWidth>e.clientWidth+1); region.focus(); region.scrollLeft=0")
press("ArrowRight", "ArrowRight", 39)
keyboard["arrowScrollsCode"] = evaluate("region.scrollLeft>0")
call("Emulation.setEmulatedMedia", {"features": [{"name": "prefers-reduced-motion", "value": "reduce"}]})
keyboard["reducedMotion"] = evaluate("matchMedia('(prefers-reduced-motion: reduce)').matches")
assert all(view["documentWidth"] <= view["width"] and view["images"] and view["h1"] == view["main"] == 1 and not view["externalAssets"] and view["codeRegions"] and view["tableRegions"] for view in results), results
assert keyboard["firstTab"] == "skip-link" and keyboard["skipTarget"] == "main"
assert all(keyboard[key] for key in ("spaceOpensContents", "enterClosesContents", "arrowScrollsCode", "reducedMotion"))
assert keyboard["focusOutline"] == "solid"
evidence = {"views": results, "keyboard": keyboard, "all_pass": True}
(output / "browser-results.json").write_text(json.dumps(evidence, indent=2) + "\n")
print(json.dumps({"views_checked": len(results), "all_pass": True, "keyboard": keyboard}, indent=2))
connection.close()
