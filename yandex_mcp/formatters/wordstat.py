"""Markdown formatters for Yandex Wordstat API responses."""

from typing import Any, Dict, List, Union


def _format_single_top_requests(data: Dict[str, Any]) -> str:
    lines = [f"# Wordstat: {data.get('requestPhrase', 'N/A')}\n"]
    lines.append(f"**Total count**: {data.get('totalCount', 0):,}\n")

    top = data.get("topRequests", [])
    if top:
        lines.append("## Top Requests")
        for item in top:
            lines.append(f"- **{item.get('phrase', 'N/A')}**: {item.get('count', 0):,}")

    assoc = data.get("associations", [])
    if assoc:
        lines.append("\n## Associations")
        for item in assoc:
            lines.append(f"- **{item.get('phrase', 'N/A')}**: {item.get('count', 0):,}")

    return "\n".join(lines)


def format_wordstat_top_requests_markdown(data: Union[Dict[str, Any], List[Dict[str, Any]]]) -> str:
    if isinstance(data, list):
        parts = []
        for item in data:
            if item.get("error"):
                parts.append(f"**Error for phrase**: {item['error']}")
            else:
                parts.append(_format_single_top_requests(item))
        return "\n\n---\n\n".join(parts)
    return _format_single_top_requests(data)


def format_wordstat_dynamics_markdown(data: Dict[str, Any]) -> str:
    lines = ["# Wordstat Query Dynamics\n"]
    dynamics = data.get("dynamics", [])
    if not dynamics:
        return "No dynamics data found."
    lines.append("| Date | Count | Share |")
    lines.append("| --- | ---: | ---: |")
    for item in dynamics:
        lines.append(f"| {item.get('date', 'N/A')} | {item.get('count', 0):,} | {item.get('share', 0):.4f} |")
    return "\n".join(lines)


def format_wordstat_regions_markdown(data: Dict[str, Any]) -> str:
    lines = ["# Wordstat Regional Distribution\n"]
    regions = data.get("regions", [])
    if not regions:
        return "No regional data found."
    lines.append("| Region ID | Count | Share | Affinity Index |")
    lines.append("| --- | ---: | ---: | ---: |")
    for item in regions:
        lines.append(f"| {item.get('regionId', 'N/A')} | {item.get('count', 0):,} | {item.get('share', 0):.4f} | {item.get('affinityIndex', 0):.2f} |")
    return "\n".join(lines)
