# Dialect matrix

Every GSC dialect feature of every game, generated from the profiles by `docs/gen_matrix.py`. Do not edit by hand.

**Legend.** ✓ present, ✗ absent, ? unknown, ?! sources disagree (see the profile's `[[unresolved]]` block), ∅ empty list, – does not apply (`n/a`). A bare mark is **verified on a corpus**: measured by this project on the game's shipped or decompiled scripts (`evidence/corpus/`). ᵉ = **measured in the engine**: this project's scripts run in the game's own VM, emulated offline (`semantics/<game>.toml`), ᵈ = **documented** by a cited tool or document, ᵃ = **assumed** (carried from a sibling game or a community superset). Lists of more than three items show their length.

**Caveats.** On decompiled corpora (every game from iw5 on, except codol and the t7 mod tools) a count shows what the bytecode encodes in the decompiler's spelling. Constructs the decompilers rebuild from a bytecode shape (foreach, default parameters, tuples, path-qualified calls, the `function` keyword, pointer spelling, #namespace and #using_animtree placement) are never marked verified from decompiled output alone. A verified ✗ means 0 uses on the corpus: absence of use, not proof that the compiler rejects it, unless the profile note cites a compiler probe.

## Profiles

| id | game | year | grade | verified | documented | assumed |
|---|---|---:|---|---:|---:|---:|
| `iw1` | Call of Duty | 2003 | verified-on-corpus | 43 | 2 | 32 |
| `iw1-uo` | Call of Duty: United Offensive | 2004 | core | 0 | 2 | 75 |
| `iw2` | Call of Duty 2 | 2005 | verified-on-corpus | 43 | 2 | 32 |
| `iw3` | Call of Duty 4: Modern Warfare | 2007 | verified-on-corpus | 16 | 27 | 26 |
| `t4` | Call of Duty: World at War | 2008 | verified-on-corpus | 16 | 27 | 26 |
| `iw4` | Call of Duty: Modern Warfare 2 | 2009 | verified-on-corpus | 22 | 25 | 30 |
| `t5` | Call of Duty: Black Ops | 2010 | verified-on-corpus | 17 | 26 | 26 |
| `iw5` | Call of Duty: Modern Warfare 3 | 2011 | documented | 12 | 29 | 36 |
| `codol` | Call of Duty Online | 2015 | verified-on-corpus | 10 | 0 | 67 |
| `t6` | Call of Duty: Black Ops II | 2012 | documented | 18 | 26 | 27 |
| `iw6` | Call of Duty: Ghosts | 2013 | documented | 9 | 32 | 36 |
| `s1` | Call of Duty: Advanced Warfare | 2014 | documented | 10 | 31 | 36 |
| `t7` | Call of Duty: Black Ops III | 2015 | verified-on-corpus | 51 | 16 | 4 |
| `iw7` | Call of Duty: Infinite Warfare | 2016 | documented | 9 | 32 | 36 |
| `h1` | Call of Duty: Modern Warfare Remastered | 2016 | documented | 10 | 31 | 36 |
| `s2` | Call of Duty: WWII | 2017 | documented | 10 | 31 | 36 |
| `t8` | Call of Duty: Black Ops 4 | 2018 | documented | 18 | 7 | 42 |
| `iw8` | Call of Duty: Modern Warfare (2019) | 2019 | documented | 11 | 32 | 34 |
| `t9` | Call of Duty: Black Ops Cold War | 2020 | documented | 19 | 6 | 42 |
| `s4` | Call of Duty: Vanguard | 2021 | documented | 0 | 40 | 37 |
| `iw9` | Call of Duty: Modern Warfare II (2022) | 2022 | documented | 0 | 42 | 35 |
| `jup` | Call of Duty: Modern Warfare III (2023) | 2023 | documented | 18 | 18 | 41 |
| `t10` | Call of Duty: Black Ops 6 | 2024 | documented | 0 | 24 | 53 |
| `t11` | Call of Duty: Black Ops 7 | 2025 | documented | 23 | 13 | 41 |

## Files

| feature | `iw1` | `iw1-uo` | `iw2` | `iw3` | `t4` | `iw4` | `t5` | `iw5` | `codol` | `t6` | `iw6` | `s1` | `t7` | `iw7` | `h1` | `s2` | `t8` | `iw8` | `t9` | `s4` | `iw9` | `jup` | `t10` | `t11` |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `file_kinds` | gsc | gscᵃ | gsc | gsc | gsc csc | gsc | gsc csc | gsc | gsc | gsc csc | gsc | gsc | gsc csc gsh | gsc | gsc | gsc | gsc csc | gsc | gsc csc | gscᵃ | gscᵃ | gsc | gscᵃ | gsc |

## Lexing

| feature | `iw1` | `iw1-uo` | `iw2` | `iw3` | `t4` | `iw4` | `t5` | `iw5` | `codol` | `t6` | `iw6` | `s1` | `t7` | `iw7` | `h1` | `s2` | `t8` | `iw8` | `t9` | `s4` | `iw9` | `jup` | `t10` | `t11` |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `case_insensitive_identifiers` | ✓ᵃ | ✓ᵃ | ✓ᵃ | ✓ᵈ | ✓ᵈ | ✓ᵈ | ✓ᵈ | ✓ᵈ | ✓ᵃ | ✓ᵈ | ✓ᵈ | ✓ᵈ | ✓ᵈ | ✓ᵈ | ✓ᵈ | ✓ᵈ | ✓ᵈ | ✓ᵈ | ✓ᵈ | ✓ᵈ | ✓ᵈ | ✓ᵈ | ✓ᵈ | ✓ᵈ |
| `dev_blocks` | ✓ | ✓ᵃ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ᵈ | ✓ᵈ | ✓ | ✓ᵈ | ✓ᵈ | ✓ᵈ | ✓ | ✓ᵈ | ✓ | ✓ᵈ | ✓ᵈ | ✓ | ✓ᵈ | ✓ |
| `doc_comment_style` | none | ///ᵃ | none | /// | /// | /// | /// | ///ᵃ | ///ᵃ | /@ᵃ | ///ᵃ | ///ᵃ | /@ | ///ᵃ | ///ᵃ | ///ᵃ | /@ᵃ | ///ᵃ | /@ᵃ | ///ᵃ | ///ᵃ | /@ᵃ | /@ᵃ | /@ᵃ |
| `istring_literal` | ✓ | ✓ᵃ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ᵃ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ᵃ | ✓ | ✓ᵃ | ✓ᵈ | ✓ᵈ | ✓ | ✓ᵈ | ✓ |
| `hash_string_literal` | ✗ | ✗ᵃ | ✗ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✓ | ✗ᵃ | ✗ᵃ | ✓ | ✗ᵃ | ✗ᵃ | ✓ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✓ | ✗ᵃ | ✓ | ✗ᵃ | ✓ᵈ | ✓ | ✓ᵈ | ✓ |
| `extra_string_prefixes` | ∅ᵃ | ∅ᵃ | ∅ᵃ | ∅ᵃ | ∅ᵃ | ∅ᵃ | ∅ᵃ | ∅ᵃ | ∅ᵃ | ∅ᵃ | ∅ᵃ | ∅ᵃ | ∅ | ∅ᵃ | ∅ᵃ | ∅ᵃ | ∅ᵃ | ∅ᵃ | ∅ᵃ | ∅ᵃ | ∅ᵃ | @ % t | @ᵃ | @ % o |
| `anim_reference` | ✓ | ✓ᵃ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ᵃ | ✓ | ✓ᵃ | ✓ᵈ | ✓ᵈ | ✓ | ✓ᵈ | ✓ |
| `anim_reference_qualified` | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✓ | ✗ᵃ | ✗ᵃ | ✓ᵈ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✓ᵃ | ✗ᵃ | ✓ᵃ | ✗ᵃ | ✗ᵃ | ✓ᵈ | ✓ᵈ | ✓ᵈ |
| `animtree_expression` | ✓ | ✓ᵃ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ᵃ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ᵃ | ✓ | ✓ᵃ | ✓ᵈ | ✓ᵈ | ✓ | ✓ᵈ | ✓ |
| `dollar_identifiers` | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✓ᵈ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ |
| `hashed_identifier_spellings` | ∅ᵈ | ∅ᵈ | ∅ᵈ | ∅ᵈ | ∅ᵈ | ∅ᵈ | ∅ᵈ | id-token | ∅ | ∅ᵈ | id-token | id-token | hex-prefixedᵈ | id-token | id-token | id-token | hex-prefixed script-path-hash | id-token | hex-prefixed script-path-hash | id-tokenᵈ | id-tokenᵈ | hex-prefixed script-path-hash | hex-prefixed script-path-hashᵈ | hex-prefixed script-path-hash |

## Bytecode

| feature | `iw1` | `iw1-uo` | `iw2` | `iw3` | `t4` | `iw4` | `t5` | `iw5` | `codol` | `t6` | `iw6` | `s1` | `t7` | `iw7` | `h1` | `s2` | `t8` | `iw8` | `t9` | `s4` | `iw9` | `jup` | `t10` | `t11` |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `identifier_encoding` | textᵈ | textᵈ | textᵈ | textᵈ | textᵈ | textᵈ | textᵈ | tokenᵈ | tokenᵃ | textᵈ | tokenᵈ | tokenᵈ | fnv32ᵈ | tokenᵈ | tokenᵈ | tokenᵈ | scr32ᵈ | canonᵈ | scr32ᵈ | ? | ? | fnv64ᵃ | fnv64sᵈ | fnv64sᵈ |

## Imports

| feature | `iw1` | `iw1-uo` | `iw2` | `iw3` | `t4` | `iw4` | `t5` | `iw5` | `codol` | `t6` | `iw6` | `s1` | `t7` | `iw7` | `h1` | `s2` | `t8` | `iw8` | `t9` | `s4` | `iw9` | `jup` | `t10` | `t11` |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `import_directive` | none | noneᵃ | #include | #include | #include | #include | #include | #include | #include | #include | #includeᵈ | #includeᵈ | #using | #includeᵈ | #includeᵈ | #includeᵈ | #using | #includeᵈ | #using | #includeᵈ | #includeᵈ | #using | #usingᵃ | #using |
| `name_resolution` | mergeᵃ | mergeᵃ | mergeᵃ | mergeᵈ | mergeᵈ | mergeᵈ | mergeᵈ | mergeᵈ | mergeᵃ | mergeᵈ | mergeᵈ | mergeᵈ | nsᵈ | mergeᵈ | mergeᵈ | mergeᵈ | nsᵃ | mergeᵈ | nsᵃ | mergeᵈ | mergeᵈ | nsᵈ | nsᵃ | nsᵃ |
| `namespace_directive` | ✗ | ✗ᵃ | ✗ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✗ᵃ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✓ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✓ᵃ | ✗ᵈ | ✓ᵃ | ✗ᵈ | ✗ᵈ | ✓ᵈ | ✓ᵃ | ✓ᵃ |
| `path_qualified_calls` | ✓ | ✓ᵃ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ᵈ | ✓ᵈ | ✓ᵈ | ✗ | ✓ᵈ | ✓ᵈ | ✓ᵈ | ✗ᵃ | ✓ᵈ | ✗ᵃ | ✓ᵈ | ✓ᵈ | ✓ | ✗ᵃ | ✗ᵃ |
| `namespace_qualified_calls` | ✗ | ✗ᵃ | ✗ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✗ᵃ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✓ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✓ | ✗ᵈ | ✓ | ✗ᵈ | ✗ᵈ | ✓ᵈ | ✓ᵃ | ✓ |
| `builtin_namespace_qualifier` | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✓ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ? | ✗ᵃ | ? | ✗ᵃ | ✗ᵃ | ? | ? | ? |
| `header_directive` | none | noneᵃ | none | noneᵈ | noneᵈ | noneᵈ | noneᵈ | noneᵃ | noneᵃ | ?! | noneᵃ | noneᵃ | #insert | noneᵃ | noneᵃ | noneᵃ | #insertᵃ | noneᵃ | #insertᵃ | noneᵃ | noneᵃ | #insertᵃ | #insertᵃ | #insertᵃ |
| `precache_directive` | ✗ | ✗ᵃ | ✗ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✗ᵃ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✓ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ? | ✗ᵈ | ? | ✗ᵈ | ✗ᵈ | ? | ? | ? |
| `using_animtree_directive` | ✓ | ✓ᵃ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ᵈ | ✓ | ✓ᵈ | ✓ᵈ | ✓ᵈ | ✓ | ✓ᵈ | ✓ᵈ | ✓ᵈ | ✓ᵃ | ✓ᵈ | ✓ᵃ | ✓ᵈ | ✓ᵈ | ✓ᵈ | ✓ᵈ | ✓ᵈ |
| `imports_before_declarations` | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? | ✓ᵈ | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? |

## Preprocessor

| feature | `iw1` | `iw1-uo` | `iw2` | `iw3` | `t4` | `iw4` | `t5` | `iw5` | `codol` | `t6` | `iw6` | `s1` | `t7` | `iw7` | `h1` | `s2` | `t8` | `iw8` | `t9` | `s4` | `iw9` | `jup` | `t10` | `t11` |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `preprocessor_define` | ✗ | ✗ᵃ | ✗ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✗ᵃ | ✗ᵃ | ?! | ✗ᵃ | ✗ᵃ | ✓ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ? | ✗ᵃ | ? | ✗ᵃ | ✗ᵃ | ? | ? | ? |
| `preprocessor_function_macros` | ✗ | ✗ᵃ | ✗ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✗ᵃ | ✗ᵃ | ?! | ✗ᵃ | ✗ᵃ | ✓ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ? | ✗ᵃ | ? | ✗ᵃ | ✗ᵃ | ? | ? | ? |
| `preprocessor_conditionals` | ✗ | ✗ᵃ | ✗ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✗ᵃ | ✗ᵃ | ?! | ✗ᵃ | ✗ᵃ | ✓ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ? | ✗ᵃ | ? | ✗ᵃ | ✗ᵃ | ? | ? | ? |
| `preprocessor_ifdef_undef` | ✗ | ✗ᵃ | ✗ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✗ᵃ | ✗ᵃ | ?! | ✗ᵃ | ✗ᵃ | ✗ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ? | ✗ᵃ | ? | ✗ᵃ | ✗ᵃ | ? | ? | ? |
| `predefined_macros` | ∅ᵃ | ∅ᵃ | ∅ᵃ | ∅ᵃ | ∅ᵃ | ∅ᵃ | ∅ᵃ | ∅ᵃ | ∅ᵃ | ?! | ∅ᵃ | ∅ᵃ | __FILE__ __LINE__ FASTFILEᵈ | ∅ᵃ | ∅ᵃ | ∅ᵃ | ∅ᵃ | ∅ᵃ | ∅ᵃ | ∅ᵃ | ∅ᵃ | ∅ᵃ | ∅ᵃ | ∅ᵃ |
| `file_scope_macro_calls` | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✓ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ? | ✗ᵃ | ? | ✗ᵃ | ✗ᵃ | ? | ? | ? |

## Declarations

| feature | `iw1` | `iw1-uo` | `iw2` | `iw3` | `t4` | `iw4` | `t5` | `iw5` | `codol` | `t6` | `iw6` | `s1` | `t7` | `iw7` | `h1` | `s2` | `t8` | `iw8` | `t9` | `s4` | `iw9` | `jup` | `t10` | `t11` |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `function_keyword` | ✗ | ✗ᵃ | ✗ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✗ᵃ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✓ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✓ᵃ | ✗ᵈ | ✓ᵃ | ✗ᵈ | ✗ᵈ | ✓ᵈ | ✓ᵃ | ✓ᵃ |
| `autoexec_modifier` | ✗ | ✗ᵃ | ✗ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✗ᵃ | ✓ | ✗ᵈ | ✗ᵈ | ✓ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✓ | ✗ᵈ | ✓ | ✗ᵈ | ✗ᵈ | ✓ | ✓ᵈ | ✓ |
| `private_modifier` | ✗ | ✗ᵃ | ✗ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✗ᵃ | ✓ | ✗ᵈ | ✗ᵈ | ✓ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✓ | ✗ᵈ | ✓ | ✗ᵈ | ✗ᵈ | ✓ | ✓ᵈ | ✓ |
| `event_handler_modifier` | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✓ | ✗ᵃ | ✓ | ✗ᵃ | ✗ᵃ | ✗ᵈ | ✓ᵈ | ✓ |
| `codecall_modifier` | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✓ | ✗ᵃ | ✗ᵃ | ✗ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ |
| `classes` | ✗ | ✗ᵃ | ✗ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✗ᵃ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✓ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✓ | ✗ᵈ | ✓ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✗ᵈ |
| `file_scope_constants` | ✗ | ✗ᵃ | ✗ | ✗ᵈ | ✗ᵈ | ✓ | ✗ᵈ | ✓ᵈ | ✓ᵃ | ✗ᵈ | ✓ᵈ | ✓ᵈ | ✗ | ✓ᵈ | ✓ᵈ | ✓ᵈ | ✗ᵃ | ✓ᵈ | ✗ᵃ | ✓ᵈ | ✓ᵈ | ✗ᵃ | ✗ᵃ | ✗ᵃ |
| `const_locals` | ✗ | ✗ᵃ | ✗ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✗ᵃ | ✓ᵈ | ✗ᵈ | ✗ᵈ | ✓ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✓ᵃ | ✗ᵈ | ✓ᵃ | ✗ᵈ | ✗ᵈ | ✓ᵃ | ✓ᵃ | ✓ᵃ |
| `default_parameters` | ✗ | ✗ᵃ | ✗ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵈ | ✗ᵃ | ✓ᵈ | ✗ᵈ | ✗ᵈ | ✓ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✓ᵃ | ✗ᵈ | ✓ᵃ | ✗ᵈ | ✗ᵈ | ✓ᵃ | ✓ᵃ | ✓ᵃ |
| `reference_parameters` | ✗ | ✗ᵃ | ✗ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵈ | ✗ᵃ | ✗ᵃ | ✓ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✓ | ✗ᵃ | ✓ | ✗ᵃ | ✗ᵃ | ✗ᵈ | ✗ᵈ | ✗ᵈ |
| `pointer_parameters` | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵈ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵈ | ✗ᵃ | ✓ | ✗ᵃ | ✗ᵃ | ✗ᵈ | ✗ᵈ | ✗ᵈ |
| `varargs` | ✗ | ✗ᵃ | ✗ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✓ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✓ | ✗ᵃ | ✓ | ✗ᵃ | ✗ᵃ | ✗ᵈ | ✓ᵈ | ✓ |

## Statements

| feature | `iw1` | `iw1-uo` | `iw2` | `iw3` | `t4` | `iw4` | `t5` | `iw5` | `codol` | `t6` | `iw6` | `s1` | `t7` | `iw7` | `h1` | `s2` | `t8` | `iw8` | `t9` | `s4` | `iw9` | `jup` | `t10` | `t11` |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `foreach` | ✗ | ✗ᵃ | ✗ | ✗ᵈ | ✗ᵈ | ✓ | ✗ᵈ | ✓ᵈ | ✓ | ✓ | ✓ᵈ | ✓ᵈ | ✓ | ✓ᵈ | ✓ᵈ | ✓ᵈ | ✓ᵈ | ✓ᵈ | ✓ᵈ | ✓ᵈ | ✓ᵈ | ✓ᵈ | ✓ᵈ | ✓ᵈ |
| `foreach_key_value` | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✓ | ✗ᵃ | ✓ᵃ | ✓ᵃ | ✓ | ✓ᵃ | ✓ᵃ | ✓ | ✓ᵃ | ✓ᵃ | ✓ᵃ | ✓ᵃ | ✓ᵃ | ✓ᵃ | ✓ᵃ | ✓ᵈ | ✓ᵃ | ✓ᵈ | ✓ᵈ |
| `do_while` | ✗ | ✗ᵃ | ✗ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✓ᵃ | ✓ᵃ | ✓ | ✓ᵃ | ✓ᵃ | ✓ | ✓ᵃ | ✓ᵃ | ✓ᵃ | ✓ | ✓ᵃ | ✓ | ✓ᵃ | ✓ᵃ | ✓ᵃ | ✓ᵃ | ✓ |
| `childthread` | ✗ | ✗ᵃ | ✗ | ✗ᵉ | ✗ᵉ | ✓ | ✗ᵉ | ✓ | ✓ᵃ | ✗ᵃ | ✓ | ✓ | ✗ᵉ | ✓ | ✓ | ✓ | ✓ᵉ | ✓ | ✓ᵉ | ✓ᵈ | ✓ᵈ | ✓ | ✗ᵃ | ✓ |
| `call_pointer_sync` | ✗ | ✗ᵃ | ✗ | ✗ᵈ | ✗ᵈ | ✓ | ✗ᵈ | ✓ᵈ | ✓ᵃ | ✗ᵈ | ✓ᵈ | ✓ᵈ | ✗ | ✓ᵈ | ✓ᵈ | ✓ᵈ | ✗ᵃ | ✓ᵈ | ✗ᵃ | ✓ᵈ | ✓ᵈ | ✗ᵃ | ✗ᵃ | ✗ᵃ |
| `builtin_call` | ✗ | ✗ᵃ | ✗ | ✗ | ✗ | ✗ | ✗ | ? | ? | ✗ | ? | ? | ✗ | ? | ? | ? | ✗ | ? | ✗ | ? | ? | ✓ | ? | ✓ |
| `thisthread` | ✗ | ✗ᵃ | ✗ | ✗ᵈ | ✗ᵈ | ✓ | ✗ᵈ | ✓ᵈ | ✓ᵃ | ✗ᵈ | ✓ᵈ | ✓ᵈ | ✗ | ✓ᵈ | ✓ᵈ | ✓ᵈ | ✗ᵃ | ✓ᵈ | ✗ᵃ | ✓ᵈ | ✓ᵈ | ✓ᵃ | ✓ᵃ | ✓ᵃ |
| `threadendon_call` | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✓ᵈ | ✓ᵈ | ✓ᵈ | ✗ᵃ | ✗ᵃ | ✓ᵈ | ✓ᵈ | ✓ᵈ |
| `waittillframeend` | ✗ | ✓ᵃ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ᵉ | ✓ | ✓ᵉ | ✓ᵈ | ✓ᵈ | ✓ᵃ | ✓ᵃ | ✓ᵃ |
| `waitframe` | ✗ | ✗ᵃ | ✗ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵈ | ✗ᵃ | ✗ᵃ | ✗ᵈ | ✓ | ✗ | ✗ᵈ | ✓ | ✓ | ✓ᵉ | ✓ | ✓ᵉ | ✓ᵈ | ✓ᵈ | ✓ᵈ | ✓ᵈ | ✓ᵈ |
| `waitrealtime` | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵈ | ✗ᵃ | ✓ | ✗ᵈ | ✗ᵈ | ✓ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ? | ✗ᵈ | ? | ✗ᵈ | ✗ᵈ | ? | ? | ? |
| `tuple_assignment` | ✗ | ✗ᵃ | ✗ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✓ᵈ | ✓ᵃ | ✗ᵈ | ✓ᵈ | ✓ᵈ | ✗ᵈ | ✓ᵈ | ✓ᵈ | ✓ᵈ | ✗ᵃ | ✓ᵈ | ✗ᵃ | ✓ᵈ | ✓ᵈ | ? | ? | ? |
| `profiler_keywords` | ∅ | ∅ᵃ | prof_begin prof_end | prof_begin prof_end | prof_begin prof_end | prof_begin prof_end | prof_begin prof_end | prof_begin prof_endᵈ | prof_begin prof_endᵃ | prof_begin prof_endᵈ | prof_begin prof_endᵈ | prof_begin prof_endᵈ | profilestart profilestopᵈ | prof_begin prof_endᵈ | prof_begin prof_endᵈ | prof_begin prof_endᵈ | profilestart profilestopᵃ | prof_begin prof_endᵈ | profilestart profilestopᵃ | prof_begin prof_endᵈ | prof_begin prof_endᵈ | ∅ᵃ | profilestart profilestopᵃ | profilestart profilestopᵃ |
| `assert_keywords` | assertmsgᵃ | assert assertmsgᵃ | assertmsgᵃ | assertmsgᵈ | assertmsgᵈ | assertmsgᵈ | assert assertmsgᵈ | assert assertex assertmsgᵈ | assert assertex assertmsgᵃ | ∅ᵈ | assert assertex assertmsgᵈ | assert assertex assertmsgᵈ | assert assertmsgᵈ | assert assertex assertmsgᵈ | assert assertex assertmsgᵈ | assert assertex assertmsgᵈ | ∅ᵃ | assert assertex assertmsgᵈ | ∅ᵃ | assert assertex assertmsgᵈ | assert assertex assertmsgᵈ | ∅ᵃ | ∅ᵃ | ∅ᵃ |
| `breakpoint_keyword` | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✓ᵈ | ✓ᵃ | ✗ᵃ | ✓ᵈ | ✓ᵈ | ✗ᵈ | ✓ᵈ | ✓ᵈ | ✓ᵈ | ✗ᵃ | ✓ᵈ | ✗ᵃ | ✓ᵈ | ✓ᵈ | ✗ᵃ | ✗ᵃ | ✗ᵃ |
| `goto_labels` | ✗ | ✗ᵃ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ |
| `waittill_return_value` | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵉ | ✗ᵉ | ✗ᵃ | ✗ᵉ | ✗ᵃ | ✗ᵃ | ✗ᵉ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✓ᵉ | ✗ᵃ | ✓ᵉ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✓ᵃ | ✓ᵈ |

## Expressions

| feature | `iw1` | `iw1-uo` | `iw2` | `iw3` | `t4` | `iw4` | `t5` | `iw5` | `codol` | `t6` | `iw6` | `s1` | `t7` | `iw7` | `h1` | `s2` | `t8` | `iw8` | `t9` | `s4` | `iw9` | `jup` | `t10` | `t11` |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `function_pointer_style` | ::f | ::fᵃ | ::f | ::f | ::f | ::f | ::f | ::fᵈ | ::f | ::fᵈ | ::fᵈ | ::fᵈ | &f | ::fᵈ | ::fᵈ | ::fᵈ | &fᵃ | ::fᵈ | &fᵃ | ::fᵈ | ::fᵈ | &fᵈ | &fᵃ | &fᵃ |
| `pointer_call` | ✓ | ✓ᵃ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ᵃ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ᵈ | ✓ᵈ | ✓ | ✓ᵃ | ✓ |
| `strict_equality` | ✗ | ✗ᵃ | ✗ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵈ | ✗ᵃ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✓ | ✗ᵈ | ✗ᵈ | ✗ᵈ | ✓ | ✗ᵈ | ✓ | ✗ᵈ | ✗ᵈ | ✓ᵃ | ✓ᵃ | ✓ |
| `null_coalescing` | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵈ | ✗ᵃ | ✗ᵈ | ✗ᵃ | ✗ᵃ | ✗ᵈ | ✓ᵈ | ✓ |
| `optional_chaining` | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ |
| `is_expression` | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ |
| `casts` | ✓ | ✓ᵃ | ✗ | ✗ | ✗ | ✗ | ✗ | ? | ? | ? | ? | ? | ✗ | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? |
| `array_literal` | ✗ | ✗ᵃ | ✗ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✓ | ✓ᵃ | ✗ᵈ | ✓ | ✓ | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ᵈ | ✓ᵈ | ✓ | ? | ✓ |
| `struct_literal` | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✓ | ✗ᵃ | ✓ | ✗ᵃ | ✗ᵃ | ✓ | ? | ✓ |
| `isdefined_form` | ? | ? | ? | kwᵈ | kwᵈ | kwᵈ | kwᵈ | fnᵈ | fnᵃ | kwᵈ | fnᵈ | fnᵈ | kwᵈ | fnᵈ | fnᵈ | fnᵈ | kwᵈ | kwᵈ | kwᵈ | kwᵈ | kwᵈ | kwᵈ | kwᵈ | kwᵈ |
| `istrue_operator` | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✗ᵃ | ✓ | ✗ᵃ | ✓ᵈ | ✓ᵈ | ✓ | ✓ᵈ | ✓ |
| `opcode_builtins` | ∅ᵃ | ∅ᵃ | ∅ᵃ | ∅ᵃ | ∅ᵃ | ∅ᵃ | ∅ᵃ | ∅ᵈ | ∅ᵃ | 18ᵈ | ∅ᵈ | ∅ᵈ | 18ᵈ | ∅ᵈ | ∅ᵈ | ∅ᵈ | ? | ∅ᵈ | ? | ∅ᵈ | ∅ᵈ | ∅ᵃ | ∅ᵃ | ∅ᵃ |
| `bare_call_resolution` | builtinᵃ | builtinᵃ | builtinᵃ | fileᵉ | fileᵉ | builtinᵈ | fileᵉ | builtinᵈ | builtinᵃ | strictᵉ | builtinᵈ | builtinᵈ | nsᵉ | builtinᵈ | builtinᵈ | builtinᵈ | nsᵉ | builtinᵈ | nsᵉ | builtinᵈ | builtinᵈ | builtinᵃ | nsᵃ | nsᵃ |
| `global_objects` | 4ᵃ | 4ᵃ | 4ᵃ | 4ᵈ | 4ᵈ | 4ᵈ | 4ᵈ | 4ᵈ | 4ᵃ | 4ᵈ | 4ᵈ | 4ᵈ | 6ᵈ | 4ᵈ | 4ᵈ | 4ᵈ | 4ᵃ | 4ᵈ | 4ᵃ | 4ᵈ | 4ᵈ | 4ᵃ | 5ᵃ | 4ᵃ |

## Semantics

| feature | `iw1` | `iw1-uo` | `iw2` | `iw3` | `t4` | `iw4` | `t5` | `iw5` | `codol` | `t6` | `iw6` | `s1` | `t7` | `iw7` | `h1` | `s2` | `t8` | `iw8` | `t9` | `s4` | `iw9` | `jup` | `t10` | `t11` |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `array_argument_passing` | copyᵃ | copyᵃ | copyᵃ | copyᵉ | copyᵉ | copyᵈ | copyᵉ | copyᵃ | copyᵃ | copyᵉ | copyᵃ | copyᵃ | copy/&ᵉ | copyᵃ | copyᵃ | copyᵃ | copy/&ᵉ | copyᵃ | copy/&ᵉ | copyᵃ | copyᵃ | ? | ? | ? |
| `waittill_multiple_events` | ? | ? | ? | ✗ᵉ | ✗ᵉ | ? | ✗ᵉ | ? | ? | ✗ᵉ | ? | ? | ✗ᵉ | ? | ? | ? | ✓ᵉ | ? | ✓ᵉ | ? | ? | ? | ✓ᵃ | ✓ᵃ |
| `endon_multiple_events` | ? | ? | ? | ✗ᵉ | ✗ᵉ | ? | ✗ᵉ | ? | ? | ✗ᵃ | ? | ? | ✗ | ? | ? | ? | ✓ᵉ | ? | ✓ᵉ | ? | ? | ? | ✓ᵃ | ✓ᵃ |
| `notify_wakes_waiters` | ? | ? | ? | deferᵉ | deferᵉ | ? | deferᵉ | ? | ? | deferᵉ | ? | ? | deferᵉ | ? | ? | ? | deferᵉ | ? | inlineᵉ | ? | ? | ? | inlineᵃ | inlineᵃ |
| `hash_equality` | –ᵃ | –ᵃ | –ᵃ | –ᵉ | –ᵉ | –ᵃ | valueᵉ | ? | ? | errorᵉ | ? | ? | errorᵉ | ? | ? | ? | valueᵉ | ? | valueᵉ | ? | ? | ? | valueᵃ | valueᵃ |

## Keywords

| id | words | confidence |
|---|---:|---|
| `iw1` | 21 | assumed |
| `iw1-uo` | 22 | assumed |
| `iw2` | 24 | assumed |
| `iw3` | 24 | documented |
| `t4` | 24 | documented |
| `iw4` | 29 | documented |
| `t5` | 25 | documented |
| `iw5` | 37 | documented |
| `codol` | 37 | assumed |
| `t6` | 53 | documented |
| `iw6` | 37 | documented |
| `s1` | 38 | documented |
| `t7` | 46 | documented |
| `iw7` | 37 | documented |
| `h1` | 38 | documented |
| `s2` | 38 | documented |
| `t8` | 34 | assumed |
| `iw8` | 40 | documented |
| `t9` | 34 | assumed |
| `s4` | 40 | documented |
| `iw9` | 40 | documented |
| `jup` | 29 | assumed |
| `t10` | 31 | assumed |
| `t11` | 30 | assumed |
