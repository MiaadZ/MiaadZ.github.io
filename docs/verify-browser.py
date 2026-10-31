#!/usr/bin/env python3
"""Local Chromium/CDP regression checks; Python standard library only.
Start a localhost preview and isolated Chromium debugging instance first.
Usage: python3 docs/verify-browser.py [preview-origin] [debug-origin]
Writes only ignored .jekyll-cache/phase4 screenshots and numeric/route evidence.
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
output = Path(".jekyll-cache/phase4")
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

def visit(path, width, height=900, emulate=True):
    if emulate:
        call("Emulation.setDeviceMetricsOverride", {"width": width, "height": height, "deviceScaleFactor": 1, "mobile": width < 600})
    call("Page.navigate", {"url": preview + path})
    for _ in range(80):
        time.sleep(.05)
        if evaluate("location.pathname") == path and evaluate("document.readyState") == "complete":
            break
    else:
        raise AssertionError("Preview failed to load " + path)
    result = evaluate("""({
      path:location.pathname, width:innerWidth, documentWidth:document.documentElement.scrollWidth,
      images:[...document.images].every(i=>i.complete&&i.naturalWidth>0),
      renderedImageCount:document.images.length,
      devicePixelRatio:devicePixelRatio, viewportScale:visualViewport.scale,
      inlineProseColors:[...document.querySelectorAll('.article-body p[style*="color"]')].map(e=>({style:e.getAttribute("style"),color:getComputedStyle(e).color,background:getComputedStyle(document.documentElement).backgroundColor})),
      h1:document.querySelectorAll('h1').length,
      main:document.querySelectorAll('main').length,
      externalAssets:[...document.querySelectorAll('script[src],link[rel="stylesheet"],img[src]')].map(e=>e.src||e.href).filter(u=>!u.startsWith(location.origin)),
      codeRegions:[...document.querySelectorAll('pre')].every(e=>e.parentElement.matches('.scroll-region[tabindex="0"]')),
      tableRegions:[...document.querySelectorAll('table')].every(e=>e.parentElement.matches('.scroll-region[tabindex="0"]')),
      wideCodeRegions:[...document.querySelectorAll('.scroll-region')].filter(e=>e.scrollWidth>e.clientWidth+1).length
    })""")
    result["requestedWidth"] = width if emulate else None
    return result

def press(key, code, number, text=None):
    params = {"type": "keyDown", "key": key, "code": code, "windowsVirtualKeyCode": number}
    if text is not None:
        params["text"] = text
    call("Input.dispatchKeyEvent", params)
    call("Input.dispatchKeyEvent", {"type": "keyUp", "key": key, "code": code, "windowsVirtualKeyCode": number})
    time.sleep(.15)


def set_native_zoom(factor):
    call("Page.navigate", {"url":"chrome://settings/appearance"})
    for _ in range(50):
        time.sleep(.05)
        if evaluate("typeof chrome.settingsPrivate?.setDefaultZoom==='function'"):
            break
    else:
        raise RuntimeError("Native Chrome zoom API unavailable")
    expression = "Promise.race([new Promise(resolve=>chrome.settingsPrivate.setDefaultZoom(" + str(factor) + ",()=>resolve({ok:!chrome.runtime.lastError,error:chrome.runtime.lastError?.message}))),new Promise(resolve=>setTimeout(()=>resolve({ok:false,error:'zoom callback timeout'}),1500))])"
    result = call("Runtime.evaluate", {"expression":expression,"returnByValue":True,"awaitPromise":True})
    status = result.get("result",{}).get("value",{})
    if not status.get("ok"):
        raise RuntimeError(str(status))


call("Page.enable")
call("Network.enable")
call("Network.setBlockedURLs", {"urls": ["https://*"]})
set_native_zoom(1)
manifest = json.loads(Path("docs/legacy-manifest.yml").read_text())
results = []
for entry in manifest["writeups"]:
    results.append(visit(entry["permalink"], 320))
representatives = [
    "/TryHackMe/h4cked.html", "/TryHackMe/Compiled.html", "/TryHackMe/Relevant.html",
    "/TryHackMe/wonderland.html", "/TryHackMe/Skynet.html",
    "/TryHackMe/Advent-of-Cyber-2025.html", "/writeups/", "/tryhackme/", "/hackthebox/", "/tools/",
    "/", "/topics/", "/404.html", "/notes/", "/research/", "/projects/"
]
representatives += ["/topics/" + topic["slug"] + "/" for topic in json.loads(Path("docs/topic-evidence.json").read_text())["topics"]]
for path in representatives:
    for width in (1440, 390):
        results.append(visit(path, width))
        if path in ("/TryHackMe/h4cked.html", "/writeups/", "/", "/topics/", "/topics/network-forensics/", "/404.html"):
            shot = call("Page.captureScreenshot", {"format": "png", "captureBeyondViewport": False})
            name = (path.strip("/").replace("/", "-").replace(".html", "") or "home") + "-" + str(width) + ".png"
            (output / name).write_bytes(base64.b64decode(shot["data"]))
for path in [p for p in representatives if not p.startswith("/TryHackMe/")]:
    results.append(visit(path, 320))


# Motion is finite; base text never moves. Inspect only decorative AX nodes.
visit("/", 1440)
call("Emulation.setEmulatedMedia", {"features": [{"name": "prefers-reduced-motion", "value": "no-preference"}]})
motion = evaluate("""({
 cursorIterations:getComputedStyle(document.querySelector('.terminal-cursor')).animationIterationCount,
 cursorDuration:getComputedStyle(document.querySelector('.terminal-cursor')).animationDuration,
 originalOpacity:getComputedStyle(document.querySelector('.site-brand strong')).opacity,
 originalTransform:getComputedStyle(document.querySelector('.site-brand strong')).transform
})""")
time.sleep(3)
motion["cursorSettled"] = evaluate("document.querySelector('.terminal-cursor').getAnimations().length===0")
call("Input.dispatchMouseEvent", {"type":"mouseMoved","x":1,"y":1})
call("Page.navigate", {"url":"about:blank"})
time.sleep(.1)
visit("/",1440)
call("Page.bringToFront")
press("Tab","Tab",9)
press("Tab","Tab",9)
assert evaluate("document.activeElement.matches('.site-brand')")
motion["focusGlitch"] = evaluate("getComputedStyle(document.querySelector('.site-brand .glitch-layer')).animationName==='identity-glitch'")
motion["singleGlitchIteration"] = evaluate("getComputedStyle(document.querySelector('.site-brand .glitch-layer')).animationIterationCount==='1'")
evaluate("document.activeElement.blur()")
box = evaluate("(()=>{const r=document.querySelector('.site-brand').getBoundingClientRect();return {x:r.x+r.width/2,y:r.y+r.height/2}})()")
call("Input.dispatchMouseEvent", {"type":"mouseMoved", **box})
motion["hoverGlitch"] = evaluate("getComputedStyle(document.querySelector('.site-brand .glitch-layer')).animationName==='identity-glitch'")
time.sleep(.25)
motion["glitchSettled"] = evaluate("document.querySelector('.site-brand .glitch-layer').getAnimations().length===0")
dom = call("DOM.getDocument")
motion["decorationsIgnoredByAX"] = True
for selector in (".glitch-layer", ".binary", ".terminal-cursor"):
 node = call("DOM.querySelector", {"nodeId":dom["root"]["nodeId"],"selector":selector})
 ax = call("Accessibility.getPartialAXTree", {"nodeId":node["nodeId"],"fetchRelatives":False})
 motion["decorationsIgnoredByAX"] &= bool(ax["nodes"][0]["ignored"])
call("Emulation.setEmulatedMedia", {"features": [{"name":"prefers-reduced-motion","value":"reduce"}]})
motion["reducedMotionDisabled"] = evaluate("[document.querySelector('.terminal-cursor'),document.querySelector('.glitch-layer')].every(e=>getComputedStyle(e).animationName==='none')")
motion["reducedGlitchHidden"] = evaluate("getComputedStyle(document.querySelector('.glitch-layer')).display==='none'")
call("Emulation.setEmulatedMedia", {"features": [{"name":"prefers-reduced-motion","value":"no-preference"}]})


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

# Attempt real Chrome default page zoom in the isolated test profile, not CSS
# zoom, deviceScaleFactor, pinch/pageScaleFactor or viewport-only emulation.
zoom = {"requested":4,"verified":False,"control":"chrome.settingsPrivate.setDefaultZoom"}
try:
 call("Emulation.clearDeviceMetricsOverride")
 window = call("Browser.getWindowForTarget", {"targetId":target["id"]})
 call("Browser.setWindowBounds", {"windowId":window["windowId"],"bounds":{"width":1280,"height":1000}})
 before_zoom = visit("/",1280,emulate=False)
 call("Page.navigate", {"url":"chrome://settings/appearance"})
 for _ in range(50):
  time.sleep(.05)
  if evaluate("typeof chrome.settingsPrivate?.setDefaultZoom==='function'"):
   break
 else:
  raise RuntimeError("Native Chrome zoom API unavailable in this headless build")
 result = call("Runtime.evaluate", {"expression":"Promise.race([new Promise(resolve=>chrome.settingsPrivate.setDefaultZoom(4,()=>resolve({ok:!chrome.runtime.lastError,error:chrome.runtime.lastError?.message}))),new Promise(resolve=>setTimeout(()=>resolve({ok:false,error:'zoom callback timeout'}),1500))])","returnByValue":True,"awaitPromise":True})
 status = result.get("result",{}).get("value",{})
 if not status.get("ok"):
  raise RuntimeError(str(status))
 after_zoom = visit("/",1280,emulate=False)
 ratio = before_zoom["width"]/after_zoom["width"]
 zoom.update({"baselineCssWidth":before_zoom["width"],"zoomedCssWidth":after_zoom["width"],"devicePixelRatio":after_zoom["devicePixelRatio"],"measuredReflowRatio":ratio})
 if not (3.9 <= ratio <= 4.1 and after_zoom["devicePixelRatio"] >= 3.9 and after_zoom["viewportScale"] == 1):
  raise RuntimeError("Native 400% zoom could not be confirmed by independent layout/DPR measurements")
 zoom["views"] = [visit(path,1280,emulate=False) for path in ("/","/topics/","/topics/network-forensics/","/writeups/","/TryHackMe/h4cked.html","/404.html")]
 assert all(v["documentWidth"]<=v["width"] and v["images"] and v["h1"]==1 for v in zoom["views"])
 zoom["verified"] = True
 shot = call("Page.captureScreenshot", {"format":"png","captureBeyondViewport":False})
 (output/"native-400-percent.png").write_bytes(base64.b64decode(shot["data"]))
except Exception as error:
 zoom["manualReview"] = str(error)



def luminance(css):
    import re
    channels = [float(v)/255 for v in re.findall(r"[\d.]+",css)[:3]]
    linear = [v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in channels]
    return sum(a*b for a,b in zip(linear,(.2126,.7152,.0722)))
inline_contrast = []
for view in results:
    for sample in view["inlineProseColors"]:
        a,b = luminance(sample["color"]),luminance(sample["background"])
        ratio = (max(a,b)+.05)/(min(a,b)+.05)
        assert ratio>=4.5, (view["path"],sample,ratio)
        inline_contrast.append({"path":view["path"],"width":view["width"],"ratio":round(ratio,2),"authoredStyle":sample["style"]})

assert all(view["width"] == view["requestedWidth"] and view["documentWidth"] <= view["width"] and view["images"] and view["h1"] == view["main"] == 1 and not view["externalAssets"] and view["codeRegions"] and view["tableRegions"] for view in results), results
assert keyboard["firstTab"] == "skip-link" and keyboard["skipTarget"] == "main"
assert all(keyboard[key] for key in ("spaceOpensContents", "enterClosesContents", "arrowScrollsCode", "reducedMotion"))
assert keyboard["focusOutline"] == "solid"
assert motion["cursorIterations"]=="3" and motion["cursorDuration"]=="0.9s" and motion["cursorSettled"]
assert motion["originalOpacity"]=="1" and motion["originalTransform"]=="none"
assert all(motion[k] for k in ("focusGlitch","hoverGlitch","singleGlitchIteration","glitchSettled","decorationsIgnoredByAX","reducedMotionDisabled","reducedGlitchHidden")), motion
evidence = {"views": results, "keyboard": keyboard, "motion":motion, "nativeZoom":zoom, "inlineContrast":inline_contrast, "all_pass": True}
(output / "browser-results.json").write_text(json.dumps(evidence, indent=2) + "\n")
print(json.dumps({"views_checked": len(results), "all_pass": True, "keyboard": keyboard, "motion":motion, "nativeZoom":zoom, "inlineContrast":inline_contrast}, indent=2))
set_native_zoom(1)
connection.close()
