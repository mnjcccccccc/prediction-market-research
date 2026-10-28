"""Portable JSON + Markdown + HTML reports, including escaped external strings."""

from html import escape
import json
from pathlib import Path
from urllib.parse import urlparse

from .models import parse_time
from .audit import atomic_text, write_json


def _pct(value):
    return "N/A" if value is None else f"{value:.1%}"


def _md(value):
    return escape(str(value)).replace("|", "\\|").replace("\n", " ")


def sparkline(points: list[dict]) -> str:
    pts = [p for p in points if p["probability"] is not None]
    if len(pts) < 2:
        return '<p class="muted">Collect at least two valid snapshots to display history.</p>'
    lo, hi = parse_time(pts[0]["observed_at"]), parse_time(pts[-1]["observed_at"])
    width = max((hi - lo).total_seconds(), 1)
    coords = " ".join(
        f"{40 + (parse_time(p['observed_at']) - lo).total_seconds() / width * 660:.2f},"
        f"{125 - p['probability'] * 100:.2f}"
        for p in pts
    )
    return f'''<svg viewBox="0 0 740 158" role="img" aria-label="Observed YES probability over time">
      <line x1="40" y1="25" x2="700" y2="25" class="grid"/>
      <line x1="40" y1="75" x2="700" y2="75" class="grid"/>
      <line x1="40" y1="125" x2="700" y2="125" class="grid"/>
      <text x="2" y="29">100%</text><text x="8" y="79">50%</text><text x="14" y="129">0%</text>
      <polyline points="{coords}" fill="none" stroke="#225f50" stroke-width="2.5"/>
      <text x="40" y="150">{lo.strftime("%m-%d %H:%M")} UTC</text>
      <text x="580" y="150">{hi.strftime("%m-%d %H:%M")} UTC</text></svg>'''


def _safe_link(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme == "https" and parsed.hostname in {"polymarket.com", "kalshi.com"}:
        return f'<a href="{escape(url, quote=True)}" target="_blank" rel="noopener noreferrer">Open market ↗</a>'
    return '<span class="muted">Synthetic event · no external market</span>'


def write_reports(out: Path, entries: list[dict], meta: dict) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    report = {"schema_version": "2.0", "meta": meta, "markets": entries}
    write_json(out / "report.json", report)
    counts = {
        action: sum(x["agent"]["decision"]["action"] == action for x in entries)
        for action in ("investigate", "monitor", "abstain")
    }
    md = [
        "# Prediction Market Research",
        "",
        f"Data mode: **{meta['data_mode']}**",
        f"As of: {meta['as_of']} (UTC timestamps)",
        "",
        "Research priority only. Prices are market-implied, not independent forecasts.",
        "",
        "| Venue | Market | YES | Score | Decision |",
        "|---|---|---:|---:|---|",
    ]
    cards = []
    for entry in entries:
        a, agent = entry["analysis"], entry["agent"]
        m, d = a["market"], agent["decision"]
        md.append(
            f"| {m['source']} | {_md(m['title'])} | {_pct(m['probability'])} | "
            f"{a['score']} | {d['action']} |"
        )
        p = _pct(m["probability"])
        v = "N/A" if m["volume_24h"] is None else f"{m['volume_24h']:,.0f} {m['volume_unit']}"
        changes = []
        for hours in (1, 24):
            e = a["evidence"][f"e_change_{hours}h"]
            changes.append(
                f"{hours}h: unavailable"
                if e["value"] is None
                else f"{hours}h: {e['value'] * 100:+.2f} pp ({e['elapsed_hours']:.2f}h actual)"
            )
        native = entry.get("native_history")
        chart_points = entry["history"]
        chart_label = "Local snapshots · " + m["probability_basis"]
        if native and a["evidence"].get("e_native_history", {}).get("available"):
            chart_points = [
                {"observed_at": p["event_time"], "probability": p["probability"]}
                for p in native["points"]
                if parse_time(p["event_time"]) <= parse_time(m["observed_at"])
            ]
            chart_label = "Exchange-native history · " + native["basis"]
        if any(
            a["evidence"][f"e_change_{h}h"].get("origin") == "exchange_native_history"
            for h in (1, 24)
        ):
            changes.append("exchange-native basis; see evidence")
        signals = "".join(f"<li>{escape(s['description'])}</li>" for s in a["signals"])
        risks = "".join(f"<li>{escape(r)}</li>" for r in d["risks"])
        next_steps = "".join(f"<li>{escape(r)}</li>" for r in d["next_steps"])
        evidence = escape(json.dumps(a["evidence"], ensure_ascii=False, indent=2))
        decision = escape(json.dumps(d, ensure_ascii=False, indent=2))
        cards.append(f'''<article class="market" data-source="{m["source"]}" data-action="{d["action"]}">
          <div class="market-top"><div><span class="venue">{m["source"].upper()}</span>
          <h2>{escape(m["title"])}</h2><span class="muted id">{escape(m["market_id"])}</span></div>
          <span class="badge {d["action"]}">{d["action"].upper()}</span></div>
          <div class="numbers"><div><small>YES IMPLIED</small><strong>{p}</strong></div>
          <div><small>RESEARCH PRIORITY</small><strong>{a["score"]:.1f}<em>/100</em></strong></div>
          <div><small>ROLLING 24H VOLUME</small><strong class="volume">{escape(v)}</strong></div></div>
          <p class="changes">{escape(" · ".join(changes))}</p>
          <p>{escape(d["summary"])}</p>
          <details><summary>Evidence, risk review &amp; observed history</summary>
          <p class="muted">{escape(chart_label)}</p>{sparkline(chart_points)}
          <div class="detail-grid"><div><h3>Signals</h3><ul>{signals or "<li>No threshold crossed.</li>"}</ul>
          <h3>Next research steps</h3><ol>{next_steps}</ol></div><div><h3>Risk review</h3><ul>{risks}</ul></div></div>
          <p class="muted">Observed: {escape(m["observed_at"])}<br>
          Price basis: {escape(m["probability_basis"])} · Agent: {escape(agent["mode"])}
          · {agent["latency_ms"]} ms</p>
          <h3>Structured decision</h3><pre>{decision}</pre>
          <h3>Evidence IDs</h3><pre>{evidence}</pre>{_safe_link(m["url"])}</details></article>''')
    md.extend(
        [
            "",
            "## Data coverage",
            "",
            "```json",
            json.dumps(meta["coverage"], ensure_ascii=False, indent=2),
            "```",
            "",
            "## Limitations",
            "",
            "- Bounded REST sampling, not complete exchange coverage or a real-time stream.",
            "- Unavailable time-matched history is reported as null, never fabricated.",
            "- Rolling-volume ratios do not measure interval volume.",
            "- No automatic cross-venue matching, executable arbitrage, or profitability claim.",
            "- Model evidence IDs are validated; semantic factuality still needs human review.",
        ]
    )
    for entry in entries:
        md.extend(
            [
                "",
                f"## {_md(entry['analysis']['market']['title'])}",
                "",
                entry["agent"]["decision"]["summary"],
                "",
                "```json",
                json.dumps(entry["agent"]["decision"], ensure_ascii=False, indent=2),
                "```",
            ]
        )
    atomic_text(out / "report.md", "\n".join(md) + "\n")
    label = {
        "synthetic": "SYNTHETIC DEMO · NOT LIVE DATA",
        "captured_api_replay": "CAPTURED API REPLAY · ORIGINAL TIMESTAMP",
        "stored_api_snapshots": "STORED API SNAPSHOTS",
    }.get(meta["data_mode"], "LIVE API CAPTURE · AS OF TIMESTAMP")
    coverage = escape(json.dumps(meta, ensure_ascii=False, indent=2))
    html = """<!doctype html><html lang="en"><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Prediction Market Research | ARTi Challenge</title><style>
    :root{--ink:#202b29;--green:#225f50;--muted:#67736f;--line:#dce3df;--paper:#f5f7f3}
    *{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.6 system-ui,sans-serif}
    main{max-width:1120px;margin:auto;padding:42px 32px}header{border-top:4px solid var(--green);padding-top:24px}
    .eyebrow,.venue,small{font-size:11px;letter-spacing:.12em;font-weight:700;color:var(--green)}
    h1{font-size:clamp(32px,5vw,58px);line-height:1.12;letter-spacing:-.045em;margin:18px 0}
    h1 span{color:var(--green)}.intro{max-width:710px;color:var(--muted);font-size:16px}
    .meta{display:flex;gap:18px;align-items:center;flex-wrap:wrap;margin:22px 0}
    .mode{background:#e4ecdf;padding:5px 12px;font-size:11px;font-weight:750;letter-spacing:.06em;border-radius:3px}
    .metrics{display:grid;grid-template-columns:repeat(4,1fr);border:1px solid var(--line);background:#fff;margin:28px 0}
    .metric{padding:18px 22px;border-right:1px solid var(--line)}.metric:last-child{border:0}
    .metric strong{display:block;font-size:32px;line-height:1.3}.metric span{color:var(--muted);font-size:12px}
    .toolbar{display:flex;gap:12px;margin:24px 0 12px}input,select{font:inherit;padding:10px 12px;border:1px solid #c7d2cb;border-radius:4px;background:#fff;color:var(--ink)}
    input{flex:1;min-width:130px}.market{border:1px solid var(--line);background:white;margin:14px 0;padding:25px;border-radius:6px}
    .market-top{display:flex;justify-content:space-between;align-items:flex-start;gap:20px}h2{font-size:19px;line-height:1.4;letter-spacing:-.015em;margin:5px 0}.id{font-size:11px;word-break:break-all}
    .badge{font-size:10px;font-weight:800;letter-spacing:.09em;padding:4px 9px;border-radius:3px;white-space:nowrap}
    .investigate{background:#f7e8ca;color:#805817}.monitor{background:#e2eee8;color:#225f50}.abstain{background:#eceeec;color:#68706d}
    .numbers{display:grid;grid-template-columns:1fr 1fr 1.4fr;margin-top:18px;gap:20px}.numbers small{display:block;color:var(--muted);font-size:10px}
    .numbers strong{font-size:29px;font-weight:650;letter-spacing:-.035em}.numbers .volume{font-size:23px}em{font-size:13px;font-style:normal;color:var(--muted);margin-left:4px}
    .changes{font-size:12px;color:var(--green);font-family:ui-monospace,monospace}.muted{color:var(--muted)}
    details{border-top:1px solid var(--line);margin-top:18px;padding-top:12px}summary{cursor:pointer;color:var(--green);font-size:13px;font-weight:600}
    .detail-grid{display:grid;grid-template-columns:1fr 1fr;gap:28px}h3{font-size:13px}li{margin:6px 0;font-size:13px}
    pre{background:#f2f5f1;padding:16px;overflow:auto;font-size:11px;white-space:pre-wrap;overflow-wrap:anywhere;border-radius:4px}
    svg{max-width:740px;width:100%;margin-top:16px}svg text{font-size:10px;fill:#67736f}.grid{stroke:#dce3df;stroke-dasharray:3 3}
    a{color:var(--green)}footer{padding:28px 0;color:var(--muted);font-size:12px}.empty{display:none;color:var(--muted);padding:30px;text-align:center}
    @media(max-width:650px){main{padding:24px 14px}.metrics{grid-template-columns:1fr 1fr}.metric{border-bottom:1px solid var(--line)}.market{padding:18px}.toolbar{flex-wrap:wrap}.toolbar input{flex-basis:100%}.market-top{gap:8px}.numbers{grid-template-columns:1fr 1fr}.numbers>div:last-child{grid-column:span 2}.detail-grid{grid-template-columns:1fr}.meta{gap:8px}h2{font-size:17px}}
    </style></head><body><main><header>
    <div class="eyebrow">ARTi ENGINEERING CHALLENGE / RESEARCH PIPELINE</div>
    <h1>Prediction markets.<br><span>Evidence before judgment.</span></h1>
    <p class="intro">Public market data, time-matched probability changes and a risk-reviewed research queue.
    Every decision traces back to explicit evidence. Open a market card to inspect its history.</p>
    <div class="meta"><span class="mode">__MODE__</span><span class="muted">As of __ASOF__</span></div></header>
    <section class="metrics" aria-label="Research queue statistics">
    <div class="metric"><strong>__TOTAL__</strong><span>reported markets</span></div>
    <div class="metric"><strong>__INVESTIGATE__</strong><span>investigate</span></div>
    <div class="metric"><strong>__MONITOR__</strong><span>monitor</span></div>
    <div class="metric"><strong>__ABSTAIN__</strong><span>abstain / excluded</span></div></section>
    <div class="toolbar"><input id="search" aria-label="Search market title" placeholder="Search market title or ID…">
    <select id="source" aria-label="Filter venue"><option value="">All venues</option><option>polymarket</option><option>kalshi</option></select>
    <select id="action" aria-label="Filter decision"><option value="">All decisions</option><option>investigate</option><option>monitor</option><option>abstain</option></select></div>
    <p class="muted" style="font-size:12px">Sorted by eligibility, then research priority. Volume retains each venue’s native unit.</p>
    <section id="markets">__CARDS__</section><p class="empty" id="empty">No markets match these filters.</p>
    <details><summary>Collection coverage &amp; run metadata</summary><pre>__COVERAGE__</pre></details>
    <footer>Research prototype · REST polling, not streaming · No external scripts or tracking.<br>
    A signal indicates research attention, not causal explanation, fair value, or executable trading profit.<br>
    Missing history stays unknown. Source metadata time is not a quote timestamp.</footer></main>
    <script>
    const fields=['search','source','action'].map(x=>document.getElementById(x));
    function filter(){const [q,s,a]=fields.map(x=>x.value.toLowerCase());let n=0;
      document.querySelectorAll('.market').forEach(el=>{const ok=(!q||el.querySelector('.market-top').textContent.toLowerCase().includes(q))&&(!s||el.dataset.source===s)&&(!a||el.dataset.action===a);el.hidden=!ok;if(ok)n++;});
      document.getElementById('empty').style.display=n?'none':'block';}
    fields.forEach(el=>el.addEventListener('input',filter));
    </script></body></html>"""
    replacements = {
        "__MODE__": label,
        "__ASOF__": escape(meta["as_of"]),
        "__TOTAL__": str(len(entries)),
        "__INVESTIGATE__": str(counts["investigate"]),
        "__MONITOR__": str(counts["monitor"]),
        "__ABSTAIN__": str(counts["abstain"]),
        "__CARDS__": "\n".join(cards),
        "__COVERAGE__": coverage,
    }
    # Replace placeholders once; untrusted content cannot introduce new substitutions.
    import re

    html = re.sub(
        "|".join(re.escape(k) for k in replacements),
        lambda match: replacements[match.group()],
        html,
    )
    atomic_text(out / "report.html", html)
    return {"markets": len(entries), **counts}
