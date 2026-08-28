# -*- coding: utf-8 -*-
"""開單範本(實跑過的完整流程,複製後改內容即用)。涵蓋:
- ADF 色塊描述(【標題】段落=Jira 彩色 panel)
- Bug 單(含五評估欄位)與故事三張套裝(主單+iOS+Android+議題分割)
- 建單後補關聯與附件

用法:複製本檔改 build_desc()/fields 後執行。**先跑 dry-run 印 payload 確認,再拿掉 --apply 檢查**。
欄位 id 一律對照 ../reference/field_registry.md;Sprint/版本當場動態查(jira_api.py sprint/versions)。
"""
import os, sys, json, base64, urllib.request, urllib.error

sys.stdout.reconfigure(encoding="utf-8")
SITE = os.environ["JIRA_SITE"].rstrip("/")
AUTH = "Basic " + base64.b64encode(
    f"{os.environ['JIRA_EMAIL']}:{os.environ['JIRA_API_TOKEN']}".encode()).decode()

ME = "<跑 jira_api.py whoami 取得你的 accountId>"   # 負責PM + reporter


def api(method, path, payload=None):
    req = urllib.request.Request(SITE + path,
        data=json.dumps(payload).encode() if payload else None,
        headers={"Authorization": AUTH, "Accept": "application/json",
                 "Content-Type": "application/json"}, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            b = r.read().decode("utf-8", "replace")
            return json.loads(b) if b.strip() else {}
    except urllib.error.HTTPError as e:
        print("HTTP", e.code, e.read().decode("utf-8", "replace")[:600], file=sys.stderr)
        raise


# ── ADF 積木(色塊 panel/段落/清單) ──────────────────────────────
def p(t, strong=False):
    n = {"type": "text", "text": t}
    if strong:
        n["marks"] = [{"type": "strong"}]
    return n

def para(*ns):
    return {"type": "paragraph", "content": list(ns)}

def bullets(items):
    return {"type": "bulletList", "content": [
        {"type": "listItem", "content": [para(p(i))]} for i in items]}

def panel(ptype, title, blocks):
    """ptype: info(藍=背景/連結) note(紫=目的) warning(橘=需求/問題/研判) success(綠=驗收)"""
    return {"type": "panel", "attrs": {"panelType": ptype},
            "content": [para(p(title, True))] + blocks}


def build_desc():
    return {"type": "doc", "version": 1, "content": [
        panel("info", "背景", [
            para(p("<發生什麼、為什麼要做;結尾一行:來源:<可點連結或明確出處>——硬規範,每張單必有>")),
        ]),
        panel("warning", "需求", [
            bullets(["<可施作條目1>", "<條目2>"]),
            para(p("範圍:✅ 包含 <…>;❌ 不包含 <…>(防打回最高CP值欄,務必寫)")),
        ]),
        panel("success", "驗收標準", [
            bullets(["<白話場景:誰在什麼情況下做什麼,會看到什麼>", "<邊界情境>", "<原有行為不變>"]),
        ]),
    ]}


def create_bug():
    fields = {
        "project": {"key": "PROJ"},
        "issuetype": {"id": "10015"},                      # 漏洞
        "parent": {"key": "TICKET-1000"},                    # 作者 Epic,見 field_registry
        "summary": "【BUG】【iOS-Product A】<問題簡述>",
        "description": build_desc(),
        "assignee": {"accountId": "<RD accountId>"},
        "reporter": {"accountId": ME},
        "components": [{"id": "10062"}, {"id": "12559"}],  # iOS_RD + VIP2看板
        "customfield_10059": [{"accountId": ME}],          # 負責PM(陣列!)
        "customfield_10020": 15429,                        # Sprint——動態查!
        "customfield_10169": {"id": "10375"},              # Bug來源:使用者回報
        "versions": [{"id": "<動態查最大版>"}],
        "duedate": "YYYY-MM-DD",                           # 必填,沒給先問
        # 五評估欄位(bug 才要,id 見 field_registry)
        "customfield_10069": {"id": "10135"}, "customfield_10070": {"id": "10138"},
        "customfield_10071": {"id": "10143"}, "customfield_10072": {"id": "10147"},
        "customfield_10073": {"id": "10148"},
    }
    key = api("POST", "/rest/api/3/issue", {"fields": fields})["key"]
    print("建單:", SITE + "/browse/" + key)
    return key


def create_story_pack():
    """三張套裝:主單(雙平台)+iOS+Android;平台單描述=主單完整複製。"""
    def one(summary, assignee, comps):
        fields = {
            "project": {"key": "PROJ"}, "issuetype": {"id": "10010"},
            "parent": {"key": "TICKET-1000"}, "summary": summary,
            "description": build_desc(),
            "assignee": {"accountId": assignee}, "reporter": {"accountId": ME},
            "components": [{"id": c} for c in comps],
            "customfield_10059": [{"accountId": ME}], "customfield_10020": 15429,
            "duedate": "YYYY-MM-DD",
        }
        return api("POST", "/rest/api/3/issue", {"fields": fields})["key"]

    main = one("【雙平台-Product A】<功能名>", ME, ["10062", "10061", "12559"])
    ios = one("【iOS-Product A】<功能名>", "<iOS RD>", ["10062", "12559"])
    andr = one("【Android-Product A】<功能名>", "<Android RD>", ["10061", "12559"])
    for part in (ios, andr):                               # 議題分割:inward=主單
        api("POST", "/rest/api/3/issueLink", {"type": {"name": "議題分割"},
            "inwardIssue": {"key": main}, "outwardIssue": {"key": part}})
    print("三張套裝:", main, ios, andr)
    # 附件與 Relates 用 jira_api.py attach / link / copyatt


if __name__ == "__main__":
    print("這是範本:複製後改內容再跑。先印 payload 自檢,確認才送出。")
