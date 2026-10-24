"""Render a model report without changing its claims or evidence."""


def render_report(report: dict, status: dict) -> str:
    lines = [
        "# " + report["title"],
        "",
        f"Mode: {status['mode']}; provider: {status.get('provider', 'legacy')}; model: {status.get('model', 'unknown')}",
        "",
        "> Model-generated report. Provenance checks do not establish semantic support.",
        "",
        report.get("summary", ""),
        "",
        "## Claims and evidence",
        "",
    ]
    for i, claim in enumerate(report.get("claims", []), 1):
        lines.extend([f"### {i}. {claim['statement']}", ""])
        for evidence in claim.get("evidence", []):
            quote = " ".join(evidence["quote"].split())
            lines.extend([f"[{evidence['paper_id']} p.{evidence['page']}] {quote}", ""])
    for key in ["limitations", "next_experiments"]:
        lines.extend(["## " + key.replace("_", " ").title(), ""])
        lines.extend(f"- {value}" for value in report.get(key, []))
        lines.append("")
    return "\n".join(lines)
