# Validate profiles/, builtins/, fields/, events/ and semantics/ against the JSON Schemas in schema/ and the repo rules
# listed in README.md ("Validation"). The schema check needs `jsonschema` (a venv: see README.md);
# --no-schema runs the repo rules only.
# Usage: python -I tools/validate.py [--no-schema]            (from the repo root)
import json
import os
import sys
import tomllib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REDERIVED_KINDS = {"corpus-measurement", "engine-measurement", "official-doc", "third-party-corpus"}
NEUTRAL_KINDS = {"project-report", "inference"}
GPL_NAME_SOURCES = {"gsc-tool", "iw5-handler-match"}  # gsc-tool's tables are GPL-3.0


def expected_license(srcs, sources):
    ids = [s.split("#")[0] for s in srcs]
    kinds = [sources[i]["kind"] for i in ids]
    if any(k in REDERIVED_KINDS for k in kinds):
        return "CC0-1.0"
    lic = [sources[i]["license"] for i in ids if sources[i]["kind"] not in NEUTRAL_KINDS]
    lic = [x for x in lic if x != "LicenseRef-Unknown"]
    if not lic:
        return "CC0-1.0"
    if "GPL-3.0-only" in lic:
        return "GPL-3.0-only"
    if "GPL-3.0-only OR MIT" in lic:
        return "GPL-3.0-only OR MIT"
    if all(x == "MIT-0" for x in lic):
        return "MIT-0"
    return "CC0-1.0"


# ---- the name hashes of the catalogues (same values as `gruff hash <family>`)
M32, M64 = 0xFFFFFFFF, (1 << 64) - 1


def _norm(name):
    return name.lower().replace("\\", "/").encode("latin1")


def _fnv64(data, basis, prime):
    h = basis
    for b in data:
        h = ((h ^ b) * prime) & M64
    return h


def _t7_canon(name):
    h = 0x4B9ACE2F
    for b in name.lower().encode("latin1"):
        h = ((h ^ b) * 0x01000193) & M32
    return (h * 0x01000193) & M32


def _t89_scr(name):
    h = 0x4B9ACE2F
    for b in _norm(name):
        x = (b + h) & M32
        x = (x ^ (x << 10)) & M32
        h = (x + (x >> 6)) & M32
    h = (h * 9) & M32
    return ((h ^ (h >> 11)) * 0x8001) & M32


def _t10_function(name):
    b = _norm(name)
    b = b[:1] + b"zt@f3yp(d[kkd=_@" + b[1:]
    return _fnv64(b, 0x1C2F2E3C8A257D07, 0x10000000233) & 0x0FFFFFFFFFFFFFFF


def _iw9_scr(name):
    return _fnv64(_norm(name), 0x79D6530B0BB9B5D1, 0x10000000233)


def _t8_fnv64(name):
    return _fnv64(_norm(name), 0xCBF29CE484222325, 0x100000001B3) & 0x7FFFFFFFFFFFFFFF


def _iw9_xhash(name):
    return _fnv64(_norm(name), 0xCBF29CE484222325, 0x100000001B3)


HASHES = {"t7.canon": _t7_canon, "t89.scr": _t89_scr, "t10.function": _t10_function,
          "iw9.scr": _iw9_scr, "t8.fnv64": _t8_fnv64, "iw9.xhash": _iw9_xhash}


def load_validator(name, use_schema):
    if not use_schema:
        return None
    with open(os.path.join(ROOT, "schema", name), encoding="utf-8") as fh:
        schema = json.load(fh)
    try:
        import jsonschema
    except ImportError:  # under -I the user site is off: add it explicitly, nothing else
        import site
        sys.path.append(site.getusersitepackages())
        try:
            import jsonschema
        except ImportError:
            sys.exit("validate.py: the `jsonschema` package is missing (README.md, Validation, "
                     "sets up a venv), or pass --no-schema to run the repo rules only")
    return jsonschema.Draft202012Validator(schema)


def schema_errors(validator, doc, where, errors, limit=20):
    if validator is None:
        return
    n = 0
    for e in validator.iter_errors(doc):
        n += 1
        if n <= limit:
            errors.append(f"{where}: schema: {'/'.join(map(str, e.path))}: {e.message[:300]}")
    if n > limit:
        errors.append(f"{where}: schema: {n - limit} more errors")


# A feature that can be "n/a" (does not apply) only when the dialect lacks this other feature.
APPLIES_IF = {"hash_equality": "hash_string_literal"}


def check_profiles(sources, use_schema, errors):
    validator = load_validator("profile.schema.json", use_schema)
    pdir = os.path.join(ROOT, "profiles")
    names = sorted(n for n in os.listdir(pdir) if n.endswith(".toml"))
    profiles = {}
    for name in names:
        with open(os.path.join(pdir, name), "rb") as fh:
            prof = tomllib.load(fh)
        profiles[prof.get("id")] = prof
        where = "profiles/" + name
        schema_errors(validator, prof, where, errors)
        if prof.get("id") + ".toml" != name:
            errors.append(f"{where}: id {prof.get('id')!r} does not match the file name")
        entries = [("keywords", prof.get("keywords", {}))]
        entries += [("features." + k, v) for k, v in prof.get("features", {}).items()]
        # community-mode values carry their own sources and follow the same licence rule
        entries += [("features." + k + ".community", v["community"])
                    for k, v in prof.get("features", {}).items() if "community" in v]
        file_lic = prof.get("license", "CC0-1.0")
        for label, e in entries:
            srcs = e.get("source", [])
            bad = [s for s in srcs if s.split("#")[0] not in sources]
            if bad:
                errors.append(f"{where}: {label}: unknown source {bad}")
                continue
            want = expected_license(srcs, sources)
            have = e.get("license", file_lic)
            if have != want:
                errors.append(f"{where}: {label}: licence {have!r}, rule gives {want!r}")
        # "n/a" (does not apply) only where the construct the feature is about cannot occur
        for f, e in prof.get("features", {}).items():
            pre = APPLIES_IF.get(f)
            if not pre:
                continue
            pe = prof["features"].get(pre, {})
            for label, x, pv in ((f, e, pe.get("value")),
                                 (f + ".community", e.get("community"),
                                  pe.get("community", pe).get("value"))):
                if x and x.get("value") == "n/a" and pv is not False:
                    errors.append(f"{where}: features.{label}: n/a while {pre} is {pv!r} "
                                  f"(n/a needs {pre} = false)")
        for u in prof.get("unresolved", []):
            for c in u.get("claims", []):
                if c["source"].split("#")[0] not in sources:
                    errors.append(f"{where}: unresolved {u['id']}: unknown source {c['source']!r}")
            for f in u.get("features", []):
                if prof["features"].get(f, {}).get("status") != "unresolved":
                    errors.append(f"{where}: unresolved {u['id']}: feature {f} lacks status = unresolved")
    return profiles


def entry_label(b):
    for k in ("name", "hash", "id", "index"):
        if k in b:
            return f"{b.get('kind')} {k}={b[k]}"
    return "?"


def check_entry(b, where, file_lic, hfun, family, seen, errors):
    label = entry_label(b)
    lic = b.get("license", file_lic)
    gpl_name = b.get("name_source") in GPL_NAME_SOURCES
    if gpl_name and lic != "GPL-3.0-only":
        errors.append(f"{where}: {label}: named from gsc-tool ({b['name_source']}) but licensed "
                      f"{lic!r}: must be GPL-3.0-only")
    if lic == "GPL-3.0-only" and not gpl_name:
        errors.append(f"{where}: {label}: GPL-3.0-only without a gsc-tool name source")
    if "name" in b and "name_source" not in b:
        errors.append(f"{where}: {label}: a name without name_source")
    if hfun and "name" in b and "hash" in b and hfun(b["name"]) != int(b["hash"], 16):
        errors.append(f"{where}: {label}: {b['name']!r} does not hash to {b['hash']} with {family}")
    ident = next((k for k in ("hash", "id", "index", "name") if k in b), None)
    # the same name in two tables (two mode sets) is a fact; the same slot written twice is not
    key = (b.get("vm"), b.get("kind"), ident, b.get(ident), b.get("table"), b.get("shadowed", False),
           b.get("handler_rva"), b.get("evidence"))
    if key in seen:
        errors.append(f"{where}: {label}: duplicate entry (same VM, kind, {ident}, handler and evidence)")
    seen.add(key)
    lo, hi = b.get("min_args"), b.get("max_args")
    loose = b.get("arity_unchecked") or b.get("arity_unknown")
    if (lo == -1 or hi == -1) and not loose:
        errors.append(f"{where}: {label}: -1 arity without arity_unknown or arity_unchecked")
    if lo is not None and hi is not None and lo >= 0 and hi >= 0 and lo > hi:
        errors.append(f"{where}: {label}: min_args {lo} > max_args {hi}")
    if ("corpus_arity" in b) != ("measured_args" in b):
        errors.append(f"{where}: {label}: corpus_arity and measured_args go together")
    if b.get("corpus_arity") == "unknown" and not b.get("arity_unknown"):
        errors.append(f"{where}: {label}: corpus_arity = unknown without arity_unknown")
    if "corpus_arity" in b and "corpus second measure" not in b.get("evidence", ""):
        errors.append(f"{where}: {label}: corpus_arity without its corpus evidence")
    # corpus_param_types is derived from corpus_arg_types: each type it names was counted
    counts, derived = b.get("corpus_arg_types", []), b.get("corpus_param_types", [])
    if len(derived) > len(counts):
        errors.append(f"{where}: {label}: corpus_param_types longer than corpus_arg_types")
    for i, (t, c) in enumerate(zip(derived, counts)):
        seen_t = set(c) | ({"int"} if "bool" in c else set())
        need = {"int", "float", "number"} if t == "number" else set(t.split("|"))
        if t != "?" and not need & seen_t:
            errors.append(f"{where}: {label}: corpus_param_types[{i}] {t!r} not in corpus_arg_types")


def check_builtins(profiles, use_schema, errors):
    validator = load_validator("builtins.schema.json", use_schema)
    bdir = os.path.join(ROOT, "builtins")
    names = sorted(n for n in os.listdir(bdir) if n.endswith(".toml"))
    total = 0
    for name in names:
        with open(os.path.join(bdir, name), "rb") as fh:
            cat = tomllib.load(fh)
        where = "builtins/" + name
        schema_errors(validator, cat, where, errors)
        game = cat.get("game", "")
        if game + ".toml" != name:
            errors.append(f"{where}: game {game!r} does not match the file name")
        family = cat.get("hash_family")
        if family is not None and family not in HASHES:
            errors.append(f"{where}: hash_family {family!r} has no checker here (add it to HASHES)")
        seen = set()
        read = set(cat.get("extraction", {}).get("modes", {}))
        for b in cat.get("builtin", []):
            total += 1
            check_entry(b, where, cat.get("license", "CC0-1.0"), HASHES.get(family), family, seen,
                        errors)
            # modes: a strict subset of the modes read (absent = all of them)
            m = set(b.get("modes", []))
            if m and not m < read:
                errors.append(f"{where}: {entry_label(b)}: modes {sorted(m)} not a strict subset "
                              f"of the modes read ({sorted(read)})")
            ma = b.get("mode_args", {})
            if not set(ma) <= (m or read) or any(lo > hi for lo, hi in ma.values()):
                errors.append(f"{where}: {entry_label(b)}: mode_args {ma} outside its modes or "
                              f"min > max")
        cm = set(cat.get("coverage", {}).get("complete_modes", []))
        if cm and (not cm <= read or cat["coverage"].get("complete", True)):
            errors.append(f"{where}: coverage.complete_modes {sorted(cm)} needs complete = false and "
                          f"modes read ({sorted(read)})")
        inames = [i["name"] for i in cat.get("intrinsic", [])]
        dup = sorted({n for n in inames if inames.count(n) > 1})
        if dup:
            errors.append(f"{where}: intrinsic listed twice: {dup}")
        for i in cat.get("intrinsic", []):
            if ("min_args" in i) != ("max_args" in i):
                errors.append(f"{where}: intrinsic {i['name']}: min_args and max_args go together")
            elif "min_args" in i and i["min_args"] > i["max_args"]:
                errors.append(f"{where}: intrinsic {i['name']}: min_args > max_args")
        # the tools read the catalogue's intrinsics only: a profile list must not hold more
        ob = profiles.get(game, {}).get("features", {}).get("opcode_builtins", {}).get("value")
        if isinstance(ob, list) and set(ob) - set(inames):
            errors.append(f"{where}: profiles/{game}.toml opcode_builtins missing from the "
                          f"catalogue's [[intrinsic]] list: {sorted(set(ob) - set(inames))}")
    return len(names), total


def check_fields(sources, use_schema, errors):
    fdir = os.path.join(ROOT, "fields")
    if not os.path.isdir(fdir):
        return 0
    validator = load_validator("fields.schema.json", use_schema)
    n = 0
    for name in sorted(x for x in os.listdir(fdir) if x.endswith(".toml")):
        n += 1
        with open(os.path.join(fdir, name), "rb") as fh:
            cat = tomllib.load(fh)
        where = "fields/" + name
        schema_errors(validator, cat, where, errors)
        if cat.get("game", "") + ".toml" != name:
            errors.append(f"{where}: game {cat.get('game')!r} does not match the file name")
        bad = [s for s in cat.get("sources", []) if s.split("#")[0] not in sources]
        if bad:
            errors.append(f"{where}: unknown source {bad}")
        family = cat.get("hash_family")
        hfun = HASHES.get(family)
        seen = set()
        for f in cat.get("field", []):
            k = (f.get("kind"), f.get("hash"), f.get("offset"))
            if k in seen:
                errors.append(f"{where}: duplicate field {k}")
            seen.add(k)
            if hfun and "name" in f and "hash" in f and hfun(f["name"]) != int(f["hash"], 16):
                errors.append(f"{where}: field {f['name']!r} does not hash to {f['hash']} with {family}")
    return n


def check_events(use_schema, errors):
    """events/<game>.toml: schema, file name, names re-hashed, no identity listed twice, the
    coverage counts consistent with the entries."""
    edir = os.path.join(ROOT, "events")
    if not os.path.isdir(edir):
        return 0, 0
    validator = load_validator("events.schema.json", use_schema)
    n = total = 0
    for name in sorted(x for x in os.listdir(edir) if x.endswith(".toml")):
        n += 1
        with open(os.path.join(edir, name), "rb") as fh:
            cat = tomllib.load(fh)
        where = "events/" + name
        schema_errors(validator, cat, where, errors)
        meta = cat.get("meta", {})
        if meta.get("game", "") + ".toml" != name:
            errors.append(f"{where}: game {meta.get('game')!r} does not match the file name")
        family = meta.get("hash_family")
        if family is not None and family not in HASHES:
            errors.append(f"{where}: hash_family {family!r} has no checker here (add it to HASHES)")
        seen = set()
        named = 0
        events = cat.get("event", [])
        for e in events:
            total += 1
            fam = e.get("hash_family", family)
            hfun = HASHES.get(fam)
            if "name" in e:
                named += 1
                if "name_source" not in e:
                    errors.append(f"{where}: event {e['name']!r}: a name without name_source")
            if hfun and "name" in e and "hash" in e and hfun(e["name"]) != int(e["hash"], 16):
                errors.append(f"{where}: event {e['name']!r} does not hash to {e['hash']} with {fam}")
            if "hash" in e and "name" not in e and fam is None:
                errors.append(f"{where}: unnamed event {e['hash']} without a hash_family")
            ident = e.get("hash") or e.get("name", "").lower()
            if ident in seen:
                errors.append(f"{where}: event {ident} listed twice")
            seen.add(ident)
            if e.get("sites", 0) < 1 and e.get("confidence") == "measured":
                errors.append(f"{where}: event {ident}: measured with no site")
        cov = cat.get("coverage", {})
        if cov.get("named") is not None and cov["named"] != named:
            errors.append(f"{where}: coverage.named {cov['named']} but {named} named entries")
        w = cov.get("corpus_waittill_events")
        parts = [cov.get(k) for k in ("explained_by_engine", "explained_by_scripts", "unexplained")]
        if w is not None and None not in parts and sum(parts) != w:
            errors.append(f"{where}: coverage: engine + scripts + unexplained != "
                          f"corpus_waittill_events")
        if cov.get("complete") and (cov.get("sites_unresolved") or named != len(events)):
            errors.append(f"{where}: coverage.complete with unresolved sites or unnamed events")
    return n, total


def check_semantics(sources, use_schema, errors):
    """semantics/<game>.toml: schema, file name, ids unique, an answer for every passing
    behaviour, every claim's source known, a profile for the game."""
    sdir = os.path.join(ROOT, "semantics")
    if not os.path.isdir(sdir):
        return 0, 0
    validator = load_validator("semantics.schema.json", use_schema)
    n = total = 0
    for name in sorted(x for x in os.listdir(sdir) if x.endswith(".toml")):
        n += 1
        with open(os.path.join(sdir, name), "rb") as fh:
            doc = tomllib.load(fh)
        where = "semantics/" + name
        schema_errors(validator, doc, where, errors)
        game = doc.get("meta", {}).get("game", "")
        if game + ".toml" != name:
            errors.append(f"{where}: game {game!r} does not match the file name")
        if not os.path.exists(os.path.join(ROOT, "profiles", name)):
            errors.append(f"{where}: no profiles/{name}")
        seen = set()
        for b in doc.get("behaviour", []):
            total += 1
            bid = b.get("id")
            if bid in seen:
                errors.append(f"{where}: behaviour {bid} listed twice")
            seen.add(bid)
            if b.get("result") == "pass" and not b.get("answer"):
                errors.append(f"{where}: behaviour {bid}: pass without an answer")
            if b.get("result") == "unsupported" and not b.get("reason"):
                errors.append(f"{where}: behaviour {bid}: unsupported without a reason")
            if b.get("result") == "pass" and "trace" not in b and "compile_error" not in b:
                errors.append(f"{where}: behaviour {bid}: pass with neither trace nor compile_error")
            for c in b.get("claims", []):
                if c["source"].split("#")[0] not in sources:
                    errors.append(f"{where}: behaviour {bid}: unknown source {c['source']!r}")
    return n, total


def check_semantic_refs(profiles, errors):
    """A profile source vm-<game>-emulation#<id> names a passing behaviour of
    semantics/<game>.toml, and a measured-in-engine value cites at least one such source."""
    beh = {}
    sdir = os.path.join(ROOT, "semantics")
    names = os.listdir(sdir) if os.path.isdir(sdir) else []
    for name in sorted(x for x in names if x.endswith(".toml")):
        with open(os.path.join(sdir, name), "rb") as fh:
            doc = tomllib.load(fh)
        beh[name[:-5]] = {b.get("id"): b.get("result") for b in doc.get("behaviour", [])}
    for pid, prof in profiles.items():
        where = f"profiles/{pid}.toml"
        entries = [(k, v) for k, v in prof.get("features", {}).items()]
        entries += [(k + ".community", v["community"])
                    for k, v in prof.get("features", {}).items() if "community" in v]
        for label, e in entries:
            vm = [s for s in e.get("source", [])
                  if s.split("#")[0].startswith("vm-") and s.split("#")[0].endswith("-emulation")]
            if e.get("confidence") == "measured-in-engine" and not vm:
                errors.append(f"{where}: features.{label}: measured-in-engine without a vm-*-emulation source")
            for s in vm:
                src, _, bid = s.partition("#")
                game = src[len("vm-"):-len("-emulation")]
                if not bid:
                    continue
                if bid not in beh.get(game, {}):
                    errors.append(f"{where}: features.{label}: {s}: no behaviour {bid} in semantics/{game}.toml")
                elif beh[game][bid] != "pass":
                    errors.append(f"{where}: features.{label}: {s}: behaviour {bid} is not a pass")


def main():
    use_schema = "--no-schema" not in sys.argv[1:]
    with open(os.path.join(ROOT, "sources.toml"), "rb") as fh:
        sources = tomllib.load(fh)["sources"]
    errors = []
    profiles = check_profiles(sources, use_schema, errors)
    ncat, nentries = check_builtins(profiles, use_schema, errors)
    nfields = check_fields(sources, use_schema, errors)
    nev, nevents = check_events(use_schema, errors)
    nsem, nbeh = check_semantics(sources, use_schema, errors)
    check_semantic_refs(profiles, errors)
    for e in errors:
        print(e)
    print(f"{len(profiles)} profiles, {ncat} builtin catalogues ({nentries} entries), "
          f"{nfields} field catalogues, {nev} event catalogues ({nevents} events), "
          f"{nsem} semantics files ({nbeh} behaviours), "
          f"{len(errors)} errors"
          + ("" if use_schema else " (schema not checked)"))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
