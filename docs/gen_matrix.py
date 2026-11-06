"""Write docs/dialect-matrix.md from the profiles and schema/profile.schema.json.

Usage: python -I docs/gen_matrix.py            (from the repo root)
"""
import json
import os
import tomllib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORDER = ["iw1", "iw1-uo", "iw2", "iw3", "t4", "iw4", "t5", "iw5", "codol", "t6", "iw6", "s1", "t7",
         "iw7", "h1", "s2", "t8", "iw8", "t9", "s4", "iw9", "jup", "t10", "t11"]
MARK = {"measured-in-engine": "ᵉ", "verified-on-corpus": "", "documented": "ᵈ", "assumed": "ᵃ"}
SHORT = {"triple-slash": "///", "at-block": "/@", "include": "#include", "using": "#using",
         "insert": "#insert", "inline": "#inline", "colon": "::f", "ampersand": "&f",
         "merge": "merge", "namespace": "ns", "builtin-first": "builtin", "namespace-first": "ns",
         "file-first": "file", "builtin-strict": "strict",
         "copy-unless-ref-param": "copy/&", "plain-text": "text", "token-table": "token",
         "canonical-table": "canon", "fnv1a32-t7": "fnv32", "scr32-t89": "scr32",
         "fnv64": "fnv64", "fnv64-secure": "fnv64s", "keyword": "kw", "builtin": "fn",
         "none": "none", "copy": "copy", "reference": "ref", "deferred": "defer",
         "inline": "inline", "script-error": "error", "by-value": "value"}
LEGEND = [
    "Every GSC dialect feature of every game, generated from the profiles by `docs/gen_matrix.py`. "
    "Do not edit by hand.",
    "",
    "**Legend.** ✓ present, ✗ absent, ? unknown, ?! sources disagree (see the profile's "
    "`[[unresolved]]` block), ∅ empty list, – does not apply (`n/a`). A bare mark is **verified on a corpus**: measured by "
    "this project on the game's shipped or decompiled scripts (`evidence/corpus/`). "
    "ᵉ = **measured in the engine**: this project's scripts run in the game's own VM, emulated "
    "offline (`semantics/<game>.toml`), "
    "ᵈ = **documented** by a cited tool or document, ᵃ = **assumed** (carried from a sibling game "
    "or a community superset). Lists of more than three items show their length.",
    "",
    "**Caveats.** On decompiled corpora (every game from iw5 on, except codol and the t7 mod "
    "tools) a count shows what the bytecode encodes in the decompiler's spelling. Constructs the "
    "decompilers rebuild from a bytecode shape (foreach, default parameters, tuples, "
    "path-qualified calls, the `function` keyword, pointer spelling, #namespace and "
    "#using_animtree placement) are never marked verified from decompiled output alone. A "
    "verified ✗ means 0 uses on the corpus: absence of use, not proof that the compiler rejects "
    "it, unless the profile note cites a compiler probe.",
]


def cell(e):
    if e is None:
        return ""
    v = e.get("value")
    m = MARK[e["confidence"]]
    if e.get("status") == "unresolved":
        return "?!"
    if v == "unknown":
        return "?"
    if v == "n/a":
        return "–" + m
    if v is True:
        return "✓" + m
    if v is False:
        return "✗" + m
    if isinstance(v, list):
        if not v:
            return "∅" + m
        if len(v) > 3:
            return f"{len(v)}" + m
        return " ".join(SHORT.get(x, x) for x in v) + m
    return SHORT.get(v, v) + m


def main():
    with open(os.path.join(ROOT, "schema", "profile.schema.json"), encoding="utf-8") as fh:
        schema = json.load(fh)
    fprops = schema["properties"]["features"]["properties"]
    profs = {}
    for n in os.listdir(os.path.join(ROOT, "profiles")):
        if n.endswith(".toml"):
            with open(os.path.join(ROOT, "profiles", n), "rb") as fh:
                p = tomllib.load(fh)
            profs[p["id"]] = p
    ids = [i for i in ORDER if i in profs] + sorted(i for i in profs if i not in ORDER)
    out = ["# Dialect matrix", ""] + LEGEND + ["", "## Profiles", "",
           "| id | game | year | grade | verified | documented | assumed |",
           "|---|---|---:|---|---:|---:|---:|"]
    for i in ids:
        p = profs[i]
        c = {k: 0 for k in MARK}
        for e in p["features"].values():
            c[e["confidence"]] += 1
        out.append(f"| `{i}` | {p['name']} | {p['release_year']} | {p['grade']} | "
                   f"{c['verified-on-corpus']} | {c['documented']} | {c['assumed']} |")
    head = "| feature | " + " | ".join(f"`{i}`" for i in ids) + " |"
    groups = {}
    for f, d in fprops.items():
        groups.setdefault(d.get("x-group", "other"), []).append(f)
    for g, feats in groups.items():
        out += ["", f"## {g.capitalize()}", "", head, "|---|" + "---|" * len(ids)]
        for f in feats:
            row = [cell(profs[i]["features"].get(f)) for i in ids]
            out.append(f"| `{f}` | " + " | ".join(row) + " |")
    out += ["", "## Keywords", "", "| id | words | confidence |", "|---|---:|---|"]
    for i in ids:
        k = profs[i]["keywords"]
        out.append(f"| `{i}` | {len(k['words'])} | {k['confidence']} |")
    out.append("")
    with open(os.path.join(ROOT, "docs", "dialect-matrix.md"), "w", encoding="utf-8",
              newline="\n") as fh:
        fh.write("\n".join(out))


if __name__ == "__main__":
    main()
