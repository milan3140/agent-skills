# -*- coding: utf-8 -*-
"""Jira REST v3 萬用小工具:身分/權限/版本/Sprint/留言/關聯/附件。
憑證讀環境變數(JIRA_SITE/JIRA_EMAIL/JIRA_API_TOKEN),不落檔。

py jira_api.py whoami                          # 自己的 accountId(開單填負責PM/reporter用)
py jira_api.py myperms PROJ                  # 專案權限(開單前驗)
py jira_api.py versions "Product A" [--ios|--android]  # 撈影響版本 id(動態查,別寫死)
py jira_api.py sprint TICKET-1000             # 從同看板任一單讀 active sprint id
py jira_api.py comment TICKET-1000 "留言文字"     # 純文字留言
py jira_api.py link Relates TICKET-1000 TICKET-1000   # 建關聯(議題分割/Relates/Blocks/Cloners)
py jira_api.py attach TICKET-1000 <檔案路徑> [顯示檔名]  # 上傳附件
py jira_api.py copyatt TICKET-6000 TICKET-1000 # 把 A 單附件全部搬到 B 單(轉單用)
"""
import os, sys, json, base64, uuid, mimetypes, urllib.request, urllib.parse, urllib.error

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
SITE = os.environ.get("JIRA_SITE", "https://your-org.atlassian.net").rstrip("/")
AUTH = "Basic " + base64.b64encode(
    ("%s:%s" % (os.environ.get("JIRA_EMAIL", ""), os.environ.get("JIRA_API_TOKEN", ""))).encode()).decode()


def api(method, path, payload=None, raw=None, ctype="application/json", params=None):
    url = SITE + path + ("?" + urllib.parse.urlencode(params) if params else "")
    headers = {"Authorization": AUTH, "Accept": "application/json"}
    data = None
    if payload is not None:
        data = json.dumps(payload).encode(); headers["Content-Type"] = ctype
    if raw is not None:
        data = raw; headers["Content-Type"] = ctype; headers["X-Atlassian-Token"] = "no-check"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            b = r.read()
            if not b:
                return {}
            try:
                return json.loads(b)
            except Exception:
                return b
    except urllib.error.HTTPError as e:
        print("HTTP", e.code, e.read().decode("utf-8", "replace")[:600], file=sys.stderr)
        sys.exit(1)


def upload(key, path, name=None):
    name = name or os.path.basename(path)
    mime = mimetypes.guess_type(name)[0] or "application/octet-stream"
    with open(path, "rb") as fh:
        blob = fh.read()
    b = uuid.uuid4().hex
    body = ((f"--{b}\r\nContent-Disposition: form-data; name=\"file\"; "
             f"filename=\"{name}\"\r\nContent-Type: {mime}\r\n\r\n").encode()
            + blob + f"\r\n--{b}--\r\n".encode())
    api("POST", f"/rest/api/3/issue/{key}/attachments", raw=body,
        ctype=f"multipart/form-data; boundary={b}")
    print("附件上傳:", key, name, len(blob) // 1024, "KB")


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__); return
    cmd = a[0]
    if cmd == "whoami":
        d = api("GET", "/rest/api/3/myself")
        print("displayName:", d.get("displayName"))
        print("accountId  :", d.get("accountId"))
    elif cmd == "myperms":
        proj = a[1] if len(a) > 1 else "PROJ"
        d = api("GET", "/rest/api/3/mypermissions",
                params={"projectKey": proj,
                        "permissions": "CREATE_ISSUES,EDIT_ISSUES,ADD_COMMENTS,CREATE_ATTACHMENTS,LINK_ISSUES,TRANSITION_ISSUES"})
        for k, v in d.get("permissions", {}).items():
            print(("✅" if v.get("havePermission") else "❌"), k)
    elif cmd == "versions":
        q = a[1]
        plat = "iOS" if "--ios" in a else ("Android" if "--android" in a else "")
        d = api("GET", "/rest/api/3/project/PROJ/version",
                params={"query": q, "maxResults": 30, "orderBy": "-sequence"})
        for v in d.get("values", []):
            if plat and plat not in v["name"]:
                continue
            print(v["id"], v["name"], "released" if v.get("released") else "unreleased")
        print("※ 版本號 semver 與 id 排序可能不同步,取最大要比版號字串")
    elif cmd == "sprint":
        d = api("GET", f"/rest/api/3/issue/{a[1]}", params={"fields": "customfield_10020"})
        for s in d["fields"].get("customfield_10020") or []:
            print(s["id"], s["state"], s["name"])
    elif cmd == "comment":
        body = {"body": {"type": "doc", "version": 1, "content": [
            {"type": "paragraph", "content": [{"type": "text", "text": a[2]}]}]}}
        r = api("POST", f"/rest/api/3/issue/{a[1]}/comment", body)
        print("留言已貼:", r.get("id"), "於", a[1])
    elif cmd == "link":
        api("POST", "/rest/api/3/issueLink", {"type": {"name": a[1]},
            "inwardIssue": {"key": a[2]}, "outwardIssue": {"key": a[3]}})
        print(f"{a[1]} 關聯建立: {a[2]} ↔ {a[3]}")
    elif cmd == "attach":
        upload(a[1], a[2], a[3] if len(a) > 3 else None)
    elif cmd == "copyatt":
        src, dst = a[1], a[2]
        d = api("GET", f"/rest/api/3/issue/{src}", params={"fields": "attachment"})
        for att in d["fields"].get("attachment") or []:
            blob = api("GET", f"/rest/api/3/attachment/content/{att['id']}")
            b = uuid.uuid4().hex
            body = ((f"--{b}\r\nContent-Disposition: form-data; name=\"file\"; "
                     f"filename=\"{att['filename']}\"\r\nContent-Type: {att['mimeType']}\r\n\r\n").encode()
                    + blob + f"\r\n--{b}--\r\n".encode())
            api("POST", f"/rest/api/3/issue/{dst}/attachments", raw=body,
                ctype=f"multipart/form-data; boundary={b}")
            print("搬運:", att["filename"], att["size"] // 1024, "KB →", dst)
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
