"""Count GSC dialect-feature occurrences in a local script corpus.

Read-only. Sources: directories (walked) and/or .pk3/.iwd/.zip archives (read in memory).
Prints only aggregate counts (files containing / total occurrences) per feature probe.
Probes are regexes, not a parser: treat small counts as leads and check them by hand.
scr_hash_ident also matches directives, so it is not used as evidence.
Usage: python -I featcount.py <label> <path> [<path> ...]

Parser mode (phase 2): exact counts from the gruff parser instead of regexes.
  python -I featcount.py --parser <gruff.exe> <profile.toml> <label> <path> [<path> ...]
It builds a probe profile from <profile.toml> (same keywords, every boolean feature off, every
enum and list feature set to a value no construct matches, imports_before_declarations on), runs
`gruff parse --profile <probe>` and prints, per feature, the files and constructs the dialect check
reported: each report is one use of the feature. D004 counts goto/labels, D003 imports after a
declaration. It then removes each keyword of the profile in turn and re-parses with the real
feature values: a keyword whose removal lowers the syntax-error count is used as a plain name in
the corpus (kwname rows). Only counts are printed; no file content is stored.
"""
import os
import re
import sys
import zipfile

EXTS = (".gsc", ".csc", ".gsh")
BS = chr(92)


def iter_sources(paths):
    for p in paths:
        if os.path.isdir(p):
            for root, _, files in os.walk(p):
                for f in files:
                    if f.lower().endswith(EXTS):
                        fp = os.path.join(root, f)
                        with open(fp, "rb") as fh:
                            yield fp, fh.read()
        elif p.lower().endswith((".pk3", ".iwd", ".zip")):
            with zipfile.ZipFile(p) as z:
                for n in z.namelist():
                    if n.lower().endswith(EXTS):
                        yield p + "!" + n, z.read(n)


def strip(text):
    """Remove // and /* */ comments; blank string contents (keep prefix + quotes)."""
    out = []
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if text.startswith("//", i):
            j = text.find("\n", i)
            i = n if j < 0 else j
            continue
        if text.startswith("/*", i):
            j = text.find("*/", i + 2)
            i = n if j < 0 else j + 2
            out.append(" ")
            continue
        if c == '"':
            j = i + 1
            while j < n and text[j] != '"' and text[j] != "\n":
                if text[j] == BS:
                    j += 1
                j += 1
            out.append('""')
            i = j + 1
            continue
        out.append(c)
        i += 1
    return "".join(out)


ID = r"[A-Za-z_][A-Za-z0-9_]*"
PROBES = {
    # directives (line-anchored)
    "dir_include": r"(?m)^\s*#include\b",
    "dir_using": r"(?m)^\s*#using\s",
    "dir_using_animtree": r"(?m)^\s*#using_animtree\b",
    "dir_namespace": r"(?m)^\s*#namespace\b",
    "dir_insert": r"(?m)^\s*#insert\b",
    "dir_define": r"(?m)^\s*#define\b",
    "dir_if_family": r"(?m)^\s*#(if|ifdef|ifndef|elif|else|endif)\b",
    "dir_precache": r"(?m)^\s*#precache\b",
    "dir_ifdef_undef": r"(?m)^\s*#(ifdef|ifndef|undef)\b",
    "define_function_like": r"(?m)^\s*#define\s+" + ID + r"\(",
    "col0_macro_call": r"(?m)^[A-Z][A-Z0-9_]+\s*\(",
    "waitframe_definition": r"(?m)^waitframe\s*\(",
    "expr_animtree": r"#animtree\b",
    # literals
    "hash_string": r'(?<![A-Za-z0-9_"])#""',
    "istring": r'(?<![A-Za-z0-9_])&""',
    "at_string": r'(?<![A-Za-z0-9_])@""',
    "anim_ref": r"(?<![A-Za-z0-9_)\]\s])\s*%" + ID,
    "anim_ref_after_op": r"[=(,:?]\s*%" + ID,
    # pointers
    "ptr_colon": r"[=(,\[]\s*::\s*" + ID,
    "ptr_path": r"[=(,]\s*" + ID + r"(" + re.escape(BS) + ID + r")+::" + ID + r"\s*[;,)]",
    "ptr_amp": r"[=(,]\s*&\s*" + ID + r"(::" + ID + r")?\s*[;,)]",
    "path_call": ID + r"(" + re.escape(BS) + ID + r")+::" + ID + r"\s*\(",
    "ptr_call": r"\[\[",
    # keywords / statements
    "kw_function": r"(?m)^\s*function\b",
    "kw_class": r"(?m)^\s*class\s+" + ID,
    "kw_foreach": r"\bforeach\s*\(",
    "kw_do": r"\bdo\s*(\{|$)",
    "kw_childthread": r"\bchildthread\b",
    "kw_call_ptr": r"\bcall\s*\[\[",
    "kw_thisthread": r"\bthisthread\b",
    "kw_autoexec": r"\bautoexec\b",
    "kw_private": r"\bprivate\b",
    "kw_const": r"\bconst\s+" + ID + r"\s*=",
    "kw_vararg": r"\bvararg\b",
    "param_ellipsis": r"\.\.\.\s*\)",
    "kw_new": r"\bnew\s+" + ID + r"\s*\(",
    "op_arrow": r"->",
    "op_strict_eq": r"===|!==",
    "op_coalesce": r"\?\?",
    "op_safe_nav": r"\?\.",
    "kw_event_handler": r"\bevent_handler\b",
    "kw_waitframe": r"\bwaitframe\b",
    "kw_waitrealtime": r"\bwaitrealtime\b",
    "kw_waittillmatch": r"\bwaittillmatch\b",
    "kw_waittillframeend": r"\bwaittillframeend\b",
    "kw_prof_begin": r"\bprof_begin\b",
    "kw_profilestart": r"\bprofilestart\b",
    "kw_breakpoint": r"\bbreakpoint\b",
    "kw_istrue": r"\bistrue\s*\(",
    "kw_is_expr": r"\bis\s+(not\s+)?(undefined|defined|true|false|function)\b",
    "world_obj": r"\bworld\s*\.",
    "classes_obj": r"\bclasses\s*\.",
    "dev_block": r"/#",
    "tuple_assign": r"(?m)^\s*\[\s*" + ID + r"\s*(,\s*" + ID + r"\s*)+\]\s*=",
    "array_literal": r"=\s*\[\s*(?!\[)[^\]\s]",
    "world_kw": r"\bworld\b",
    "classes_kw": r"\bclasses\b",
    "sys_qualifier": r"\bsys::",
    "ns_call": r"(?<![A-Za-z0-9_" + re.escape(BS) + r"])" + ID + r"::" + ID + r"\s*\(",
    "scr_hash_ident": r"(?<![A-Za-z0-9_\"])#" + ID + r"\b(?!\s*\()",
    "dollar_token": r"\$" + ID,
    # string prefixes (bodies are blanked, so the probe sees prefix + "")
    "str_prefix_pct": r'(?<![A-Za-z0-9_"])%""',
    "str_prefix_t": r'(?<![A-Za-z0-9_"])t""',
    "str_prefix_o": r'(?<![A-Za-z0-9_"])o""',
    "str_prefix_s": r'(?<![A-Za-z0-9_"])s""',
    "str_prefix_r": r'(?<![A-Za-z0-9_"])r""',
    # C-style casts: (int)x, (float)x, (string)x, (bool)x
    "cast": r"\(\s*(int|float|string|bool)\s*\)\s*[A-Za-z0-9_(\-.]",
    # acts' builtin pointer call modifier: builtin [[ p ]]( ... )
    "kw_builtin_call": r"\bbuiltin\s*\[\[",
    "kw_builtin": r"\bbuiltin\b",
    # decompiler control flow: goto LOC; jumpiffalse( c ) LOC; and labels on their own line
    "goto_stmt": r"\bgoto\s+" + ID + r"\s*;",
    "jumpif_stmt": r"\bjumpif(false|true)\s*\(",
    "label_stmt": r"(?m)^\s*(?!(case|default)\b)" + ID + r"\s*:(?!:)\s*$",
    # class members and modifiers
    "kw_constructor": r"\bconstructor\s*\(",
    "kw_destructor": r"\bdestructor\s*\(",
    "kw_codecall": r"\bcodecall\b",
    # `class` used as a name: not a declaration, not a script-path component
    "class_as_name": r"(?<![A-Za-z0-9_/" + re.escape(BS) + r"])class\b(?!\s+" + ID + r"\s*[{:])(?!\s*::)(?!\s*[" + re.escape(BS) + r"/;])",
    "class_path_component": r"[" + re.escape(BS) + r"/]class\b",
    "file_scope_const": r"(?m)^[A-Z][A-Z0-9_]+\s*=\s*[^=;]+;",
    # function headers only: name(...) at column 0 (IW style) or after `function`, followed by `{`
    "default_param": r"(?m)^(function\s+(private\s+|autoexec\s+)*)?(?!(if|for|while|switch|foreach|return|wait)\b)" + ID + r"\s*\([^)\n]*\b" + ID + r"\s*=(?!=)[^)\n]*\)\s*\n?\s*\{",
    "ref_param": r"(?m)^(function\s+(private\s+|autoexec\s+)*)?(?!(if|for|while|switch|foreach|return|wait)\b)" + ID + r"\s*\(([^)\n]*,)?\s*&(?!&)\s*" + ID + r"[^)\n]*\)\s*\n?\s*\{",
    "func_header": r"(?m)^(function\s+(private\s+|autoexec\s+)*)?(?!(if|for|while|switch|foreach|return|wait)\b)" + ID + r"\s*\([^)\n]*\)\s*\n?\s*\{",
    # phase 2: probes for the remaining features
    "dir_inline": r"(?m)^\s*#inline\b",
    "kw_assert": r"\bassert\s*\(",
    "kw_assertmsg": r"\bassertmsg\s*\(",
    "kw_assertex": r"\bassertex\s*\(",
    "kw_prof_end": r"\bprof_end\b",
    "kw_profilestop": r"\bprofilestop\b",
    "kw_threadendon": r"\bthreadendon\b",
    "kw_isdefined": r"\bisdefined\s*\(",
    "star_param": r"(?m)^(function\s+(private\s+|autoexec\s+)*)?" + ID + r"\s*\(([^)\n]*,)?\s*\*\s*" + ID + r"[^)\n]*\)\s*\n?\s*\{",
    "op_ternary": r"\?(?![?.])",
    "struct_literal": r"[=(,]\s*\{\s*" + ID + r"\s*:(?!:)",
    # decompiler spellings of unresolved hashes (hashed_identifier_spellings)
    "hash_hexprefixed": r"\b(function|var|namespace|event|class|field)_[0-9a-f]{6,16}\b",
    "hash_idtoken": r"\b_(id|func|meth)_[0-9A-Fa-f]{4,}\b",
    "hash_scriptpath": r"\bscript_[0-9a-f]{6,16}\b",
}
RAW_PROBES = {
    "doc_at": r"/@",
    "doc_tripleslash": r"///\s*ScriptDocBegin",
}


def main():
    label, paths = sys.argv[1], sys.argv[2:]
    cre = {k: re.compile(v) for k, v in PROBES.items()}
    rre = {k: re.compile(v) for k, v in RAW_PROBES.items()}
    files = {k: 0 for k in list(PROBES) + list(RAW_PROBES)}
    occ = dict(files)
    kinds = {}
    nfiles = 0
    for name, data in iter_sources(paths):
        nfiles += 1
        ext = os.path.splitext(name)[1].lower()
        kinds[ext] = kinds.get(ext, 0) + 1
        raw = data.decode("latin-1")
        s = strip(raw)
        for k, r in rre.items():
            c = len(r.findall(raw))
            if c:
                files[k] += 1
                occ[k] += c
        for k, r in cre.items():
            c = len(r.findall(s))
            if c:
                files[k] += 1
                occ[k] += c
    print(f"# corpus={label} files={nfiles} kinds={kinds}")
    print("# probe\tfiles_with_match\toccurrences (regex probes; comments and string bodies stripped first)")
    for k in files:
        print(f"{k}\t{files[k]}\t{occ[k]}")


# Keywords of the gruff parser (gsc_syntax SyntaxKind::KEYWORDS, directives excluded): only
# these change lexing, so only these are tested as names.
PARSER_KEYWORDS = [
    "if", "else", "while", "for", "foreach", "in", "do", "switch", "case", "default", "break",
    "continue", "return", "wait", "waitrealtime", "waitframe", "waittillframeend", "thread",
    "childthread", "call", "threadendon", "builtin", "function", "autoexec", "private", "codecall",
    "event_handler", "class", "var", "const", "constructor", "destructor", "new", "true", "false",
    "undefined", "thisthread", "breakpoint", "prof_begin", "prof_end", "profilestart",
    "profilestop", "is", "not", "self", "level", "game", "anim", "world", "classes", "isdefined",
    "istrue", "notify", "endon", "waittill", "waittillmatch", "assert", "assertex", "assertmsg",
    "size", "vararg",
]
ENUM_FEATURES = {"doc_comment_style", "identifier_encoding", "import_directive", "name_resolution",
                 "header_directive", "function_pointer_style", "isdefined_form",
                 "bare_call_resolution", "array_argument_passing", "notify_wakes_waiters",
                 "hash_equality"}
LIST_FEATURES = {"file_kinds", "extra_string_prefixes", "hashed_identifier_spellings",
                 "predefined_macros", "profiler_keywords", "assert_keywords", "opcode_builtins",
                 "global_objects"}
DIAG = re.compile(r"^(.*?):(\d+):(\d+): ([DE]\d{3,4}) (.*)$")
FEATURE = re.compile(r"\(feature `([a-z_]+)`\)")
SUMMARY = re.compile(r"(\d+) with syntax errors .*?, (\d+) syntax errors")


def looks_decompiled_text(data):
    """gsc_syntax::looks_decompiled: a decompiler header in the first 16 KiB."""
    head = data[:16384]
    return b"// Checksum 0x" in head or b"github.com/xensik/gsc-tool" in head or b"// Params " in head


def looks_decompiled(path):
    with open(path, "rb") as fh:
        return looks_decompiled_text(fh.read(16384))


def toml_value(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, str):
        return '"' + v.replace(BS, BS + BS).replace('"', BS + '"') + '"'
    if isinstance(v, list):
        return "[" + ", ".join(toml_value(x) for x in v) + "]"
    raise TypeError(v)


def write_profile(path, pid, words, features):
    lines = ["schema_version = 1", "id = " + toml_value(pid), "[keywords]",
             "words = " + toml_value(words), "[features]"]
    for k, v in features.items():
        lines.append(k + " = { value = " + toml_value(v) + " }")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def run_gsc(exe, profile, paths, quiet):
    import subprocess
    cmd = [exe, "parse", *paths, "--profile", profile, "--max-per-file", "1000000000"]
    if quiet:
        cmd.append("-q")
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.stdout


def syntax_errors(text):
    m = SUMMARY.search(text)
    return int(m.group(2)) if m else -1


def parser_main(argv):
    import tempfile
    import tomllib
    exe, prof_path, label, paths = argv[0], argv[1], argv[2], argv[3:]
    with open(prof_path, "rb") as fh:
        prof = tomllib.load(fh)
    words = prof["keywords"]["words"]
    probe = {}
    for k, e in prof["features"].items():
        v = e.get("value")
        if k == "case_insensitive_identifiers":
            probe[k] = v if isinstance(v, bool) else True
        elif k == "imports_before_declarations":
            probe[k] = True
        elif k in LIST_FEATURES:
            probe[k] = []
        elif k in ENUM_FEATURES:
            probe[k] = "probe-no-match"
        else:
            probe[k] = False
    tmp = tempfile.mkdtemp(prefix="featcount-")
    probe_path = os.path.join(tmp, "probe.toml")
    write_profile(probe_path, "probe", words, probe)
    out = run_gsc(exe, probe_path, paths, quiet=False)
    files, occ = {}, {}
    for line in out.splitlines():
        m = DIAG.match(line)
        if not m or m.group(4).startswith("E"):
            continue
        path, code, msg = m.group(1), m.group(4), m.group(5)
        f = FEATURE.search(msg)
        if f:
            key = "parser:" + f.group(1) + ":" + msg.split(" is not available")[0]
        elif code == "D004":
            key = "parser:goto_labels:goto or label"
        elif code == "D003":
            key = "parser:imports_before_declarations:import after a declaration"
        elif code == "D002":
            key = "parser:function_keyword:declaration without function"
        else:
            key = "parser:" + code + ":" + msg
        occ[key] = occ.get(key, 0) + 1
        files.setdefault(key, []).append(path)
    plain_cache = {}

    def plain(path):
        if path not in plain_cache:
            plain_cache[path] = not looks_decompiled(path)
        return plain_cache[path]

    nplain = ndec = 0
    for _, data in iter_sources(paths):
        if looks_decompiled_text(data):
            ndec += 1
        else:
            nplain += 1
    print(f"# corpus={label} parser={os.path.basename(exe)} profile={os.path.basename(prof_path)} "
          f"probe_syntax_errors={syntax_errors(out)} plain_files={nplain} decompiled_files={ndec}")
    print("# probe\tfiles_with_match\toccurrences\tplain_files\tplain_occurrences "
          "(gruff parse with every feature off: each dialect report is one use; plain = files "
          "without a decompiler header, the parser's own test)")
    for k in sorted(occ):
        ps = [p for p in files[k] if plain(p)]
        print(f"{k}\t{len(set(files[k]))}\t{occ[k]}\t{len(set(ps))}\t{len(ps)}")
    # keyword-as-name test, on the real feature values with one keyword removed at a time
    real = {k: e["value"] for k, e in prof["features"].items()
            if e.get("status") != "unresolved" and "value" in e}
    base_path = os.path.join(tmp, "base.toml")
    write_profile(base_path, "base", words, real)
    base = syntax_errors(run_gsc(exe, base_path, paths, quiet=True))
    print(f"# keyword test: {base} syntax errors with the profile's keywords; "
          "kwname rows: keyword, errors with it, errors without it (fewer = used as a plain name)")
    for w in words:
        if w.lower() not in PARSER_KEYWORDS:
            continue
        pth = os.path.join(tmp, "kw.toml")
        write_profile(pth, "kw", [x for x in words if x != w], real)
        n = syntax_errors(run_gsc(exe, pth, paths, quiet=True))
        print(f"kwname:{w}\t{base}\t{n}")
    # The parser accepts name-like keywords (self, level, size...) where a name stands, so the
    # error test cannot see them: count plain-name uses directly. kwvar: assigned as a variable
    # (`w = x`, not a field); kwfunc: declared as a function or a parameter.
    print("# kwvar/kwfunc rows: keyword, files, occurrences (regex on stripped text)")
    texts = [strip(d.decode("latin-1")) for _, d in iter_sources(paths)]
    for w in words:
        e = re.escape(w)
        rv = re.compile(r"(?<![.\w$#&%:" + re.escape(BS) + r"/])" + e + r"\s*=(?!=)")
        rf = re.compile(r"(?m)^(function\s+(private\s+|autoexec\s+)*)?" + e + r"\s*\([^)\n]*\)\s*\n?\s*\{"
                        + r"|^(function\s+)?" + ID + r"\s*\(([^)\n]*,)?\s*&?" + e + r"\s*[,)=][^)\n]*\)?\s*\n?\s*\{")
        for tag, r in (("kwvar", rv), ("kwfunc", rf)):
            nf = no = 0
            for t in texts:
                c = len(r.findall(t))
                if c:
                    nf += 1
                    no += c
            print(f"{tag}:{w}\t{nf}\t{no}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--parser":
        parser_main(sys.argv[2:])
    else:
        main()
