# cdp.py — minimal, self-diagnosing Chrome DevTools helper.
#
# Usage:
#   python tools/cdp.py --js "expr" [--dark] [--url URL]   # evaluate, print JSON
#   python tools/cdp.py --dump [--url URL]                 # print rendered DOM (no WebSocket)
#
# Design notes:
#   - Kills only Chrome processes using OUR profile dir (cdp-profile), never
#     the user's own browser.
#   - Probes with a trivial eval before running the real expression.
#   - Async expressions are installed fire-and-forget and polled, so we do
#     not depend on awaitPromise behaviour.
import argparse
import json
import subprocess
import sys
import time
import urllib.request

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PROFILE = r"C:\Temp\cdp-profile"
DEFAULT_URL = "file:///D:/web%20hoc%20tieng%20viet/index.html"


def log(*a):
    print(*a, file=sys.stderr)


def kill_stale():
    ps = (
        "Get-CimInstance Win32_Process -Filter \"Name='chrome.exe'\" | "
        "Where-Object { $_.CommandLine -like '*cdp-profile*' } | "
        "ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }"
    )
    subprocess.run(["powershell", "-NoProfile", "-Command", ps],
                   capture_output=True)


def get_targets(port):
    for _ in range(40):
        try:
            with urllib.request.urlopen(
                    f"http://127.0.0.1:{port}/json/list", timeout=2) as r:
                tabs = json.loads(r.read())
            pages = [t for t in tabs if t.get("type") == "page"]
            if pages:
                return pages
        except Exception:
            pass
        time.sleep(0.5)
    return []


def rpc(ws, expr_or_method, params, want_id, timeout=20, is_eval=False):
    method = "Runtime.evaluate" if is_eval else expr_or_method
    if is_eval:
        params = dict(params, expression=expr_or_method)
    ws.send(json.dumps({"id": want_id, "method": method, "params": params}))
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            ws.settimeout(min(5.0, max(0.5, deadline - time.time())))
            raw = ws.recv()
        except Exception:
            continue
        if not isinstance(raw, str):
            continue
        msg = json.loads(raw)
        if msg.get("id") == want_id:
            if "error" in msg:
                raise RuntimeError(json.dumps(msg["error"]))
            return msg.get("result", {})
    raise TimeoutError(f"no response for {method} (id {want_id})")


class Session:
    def __init__(self, ws_url):
        import websocket
        self.ws = websocket.create_connection(ws_url, timeout=15)
        self.n = 100

    def _id(self):
        self.n += 1
        return self.n

    def eval(self, expr, timeout=20):
        res = rpc(self.ws, expr, {"returnByValue": True}, self._id(),
                  timeout=timeout, is_eval=True)
        return res.get("result", {}).get("value")

    def eval_async(self, expr, timeout=60):
        install = (
            "window.__R=undefined;window.__D=0;"
            "Promise.resolve().then(()=>(" + expr + "))"
            ".then(v=>{window.__R=v;window.__D=1},"
            "e=>{window.__R='ERR:'+(e&&e.message||e);window.__D=2});'ok'"
        )
        ack = self.eval(install)
        if ack != "ok":
            raise RuntimeError("failed to install async expression: " + str(ack))
        deadline = time.time() + timeout
        while time.time() < deadline:
            s = self.eval("window.__D ? JSON.stringify({d:window.__D,r:window.__R}) : '0'",
                          timeout=10)
            if s and s != "0":
                out = json.loads(s)
                if out["d"] == 1:
                    return out["r"]
                raise RuntimeError(str(out["r"]))
            time.sleep(0.5)
        raise TimeoutError("async expression did not finish")


def choose(pages, url):
    for p in pages:
        if "index.html" in p.get("url", ""):
            return p
    return pages[0]


def run_dump(url):
    out = subprocess.run(
        [CHROME, "--headless=new", f"--user-data-dir={PROFILE}-dump",
         "--no-first-run", "--disable-gpu", "--dump-dom", url],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        timeout=60)
    sys.stdout.write(out.stdout)
    if out.returncode != 0:
        log("chrome exit", out.returncode, out.stderr[-500:])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--js")
    ap.add_argument("--dark", action="store_true")
    ap.add_argument("--dump", action="store_true")
    ap.add_argument("--url", default=DEFAULT_URL)
    ap.add_argument("--port", type=int, default=9333)
    args = ap.parse_args()

    if args.dump:
        run_dump(args.url)
        return

    kill_stale()
    proc = subprocess.Popen(
        [CHROME, "--headless=new", f"--remote-debugging-port={args.port}",
         "--remote-allow-origins=*", f"--user-data-dir={PROFILE}",
         "--no-first-run", "--disable-gpu", "--window-size=1440,900", args.url],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        pages = get_targets(args.port)
        if not pages:
            raise SystemExit("no CDP page targets found")
        log("targets:", [(p.get("url", "")[:60]) for p in pages])
        last_err = None
        for target in pages:
            try:
                s = Session(target["webSocketDebuggerUrl"])
            except Exception as e:
                last_err = f"connect failed: {e}"
                continue
            try:
                try:
                    rpc(s.ws, "Runtime.enable", {}, s._id(), timeout=10)
                except Exception as e:
                    log("Runtime.enable:", e)
                probe = s.eval("1+1", timeout=10)
                if probe != 2:
                    last_err = f"probe returned {probe!r} on {target.get('url')}"
                    continue
                log("probe ok on", target.get("url", "")[:70])
                if args.dark:
                    s.eval("document.documentElement.setAttribute('data-theme','dark')")
                if args.js:
                    print(json.dumps(s.eval_async(args.js), ensure_ascii=False,
                                     indent=1))
                break
            except Exception as e:
                last_err = f"{type(e).__name__}: {e}"
                log("target failed:", last_err)
                continue
        else:
            raise SystemExit("all targets failed: " + str(last_err))
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:
            proc.kill()


if __name__ == "__main__":
    main()
