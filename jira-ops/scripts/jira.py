# -*- coding: utf-8 -*-
"""Jira (Atlassian Cloud) via REST API + token。憑證讀環境變數,不落 git/命令列。

env: JIRA_SITE / JIRA_EMAIL / JIRA_API_TOKEN
用法:
    py jira.py TICKET-1000 [KEY-2 ...]        # 抓 issue
    py jira.py --jql "project=PROJ AND status=Backlog" [--max 20]
"""
import os, sys, json, base64, urllib.request, urllib.parse, urllib.error

SITE = os.environ.get("JIRA_SITE", "https://your-org.atlassian.net").rstrip("/")
EMAIL = os.environ.get("JIRA_EMAIL", "")
TOKEN = os.environ.get("JIRA_API_TOKEN", "")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def api(path, params=None):
    url = SITE + path + ("?" + urllib.parse.urlencode(params) if params else "")
    auth = base64.b64encode(("%s:%s" % (EMAIL, TOKEN)).encode()).decode()
    req = urllib.request.Request(url, headers={
        "Authorization": "Basic " + auth, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        return {"_error": e.code, "_body": e.read().decode("utf-8", "replace")[:300]}


def adf_text(node, out):
    if not isinstance(node, dict):
        return
    t = node.get("type")
    if t == "text":
        out.append(node.get("text", ""))
    if t == "hardBreak":
        out.append("\n")
    for c in node.get("content", []) or []:
        adf_text(c, out)
    if t in ("paragraph", "heading", "listItem"):
        out.append("\n")


def show(key):
    d = api("/rest/api/3/issue/" + key, {
        "fields": "summary,status,assignee,reporter,issuetype,priority,"
                  "description,labels,created,updated,parent,duedate,"
                  "subtasks,comment,attachment"})
    if d.get("_error"):
        return "  [%s] HTTP %s — %s" % (key, d["_error"], d.get("_body", ""))
    f = d.get("fields", {})
    desc = []
    adf_text(f.get("description") or {}, desc)
    parent = f.get("parent")
    lines = [
        "═" * 72,
        "%s  |  %s  |  %s" % (
            key, (f.get("issuetype") or {}).get("name", "?"),
            (f.get("status") or {}).get("name", "?")),
        "標題: " + (f.get("summary") or ""),
        "指派: %s   通報: %s" % (
            (f.get("assignee") or {}).get("displayName", "未指派"),
            (f.get("reporter") or {}).get("displayName", "-")),
        "優先: %s   到期: %s   更新: %s" % (
            (f.get("priority") or {}).get("name", "-"),
            f.get("duedate") or "-", (f.get("updated") or "")[:19]),
    ]
    if parent:
        lines.append("上層: %s %s" % (parent.get("key"),
                     (parent.get("fields") or {}).get("summary", "")))
    if f.get("labels"):
        lines.append("標籤: " + ", ".join(f["labels"]))
    subs = f.get("subtasks") or []
    if subs:
        lines.append("子任務(%d):" % len(subs))
        for s in subs:
            lines.append("  · %s [%s] %s" % (
                s.get("key"), (s.get("fields") or {}).get("status", {}).get("name", "?"),
                (s.get("fields") or {}).get("summary", "")))
    atts = f.get("attachment") or []
    if atts:
        lines.append("附件(%d):" % len(atts))
        for a in atts:
            lines.append("  · %s  %s  %dKB  id=%s" % (
                a.get("filename"), a.get("mimeType", "?"),
                (a.get("size") or 0) // 1024, a.get("id")))
    lines += ["─" * 72, "".join(desc).strip() or "(無描述)"]
    cs = (f.get("comment") or {}).get("comments") or []
    if cs:
        lines.append("─── 留言(%d,最後 %d 則)───" % (len(cs), min(6, len(cs))))
        for c in cs[-6:]:
            body = []
            adf_text(c.get("body") or {}, body)
            who = (c.get("author") or {}).get("displayName", "?")
            when = (c.get("created") or "")[:10]
            lines.append("• [%s %s] %s" % (when, who,
                         " ".join("".join(body).split())[:400]))
    return "\n".join(lines)


def jql(q, mx):
    # /rest/api/3/search 已於 2025 汰換(HTTP 410)→ 用 /rest/api/3/search/jql(游標分頁)
    out, token, got = [], None, 0
    while got < mx:
        params = {"jql": q, "maxResults": min(100, mx - got),
                  "fields": "summary,status,assignee,updated,issuetype"}
        if token:
            params["nextPageToken"] = token
        d = api("/rest/api/3/search/jql", params)
        if d.get("_error"):
            return "JQL HTTP %s — %s" % (d["_error"], d.get("_body"))
        for it in d.get("issues", []):
            f = it["fields"]
            out.append("  %-13s [%-5s] %-46s %s  %s" % (
                it["key"], (f.get("status") or {}).get("name", "?")[:5],
                (f.get("summary", "") or "")[:46],
                (f.get("updated") or "")[:10],
                (f.get("assignee") or {}).get("displayName", "未指派")))
            got += 1
        token = d.get("nextPageToken")
        if not token or not d.get("issues"):
            break
    return "找到 %d 筆:\n%s" % (len(out), "\n".join(out)) if out else "(0 筆)"


def main():
    if not (EMAIL and TOKEN):
        print("缺 JIRA_EMAIL / JIRA_API_TOKEN 環境變數", file=sys.stderr)
        sys.exit(2)
    a = sys.argv[1:]
    if a and a[0] == "--jql":
        mx = 20
        if "--max" in a:
            mx = int(a[a.index("--max") + 1])
        print(jql(a[1], mx))
    else:
        for k in (a or ["TICKET-1000"]):
            if k.startswith("--"):
                continue
            print(show(k))


if __name__ == "__main__":
    main()
