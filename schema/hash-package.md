# Hash package format, version 1

A hash package names hashed script identifiers (`function_1a2b3c4d`, `#"hash_..."`) of the games
that compile names to hashes: Black Ops III, Black Ops 4 to Black Ops 7, Modern Warfare II and
III. Consumers hash plain names themselves with each game's hash families (the family ids of
Gruff's `gsc_hash`, `gruff hash --list`), so a list of names suffices; pairs are optional.

This specification is CC0-1.0, like the rest of gruff-data. **gruff-data ships no package**: name lists
recovered from a game's files are derived from the publisher's material, and lists copied from
other projects carry their licence. Packages stay with their users (see Gruff
`docs/hash-packages.md`, "Building your own"). The example below uses made-up names.

## Syntax

- UTF-8 text. A leading byte-order mark and CRLF line ends are accepted. One entry per line.
- **Header**: the `# key: value` lines before the first entry. Keys are case-insensitive:

  | key | meaning |
  |---|---|
  | `gsc-hash-package` | Format version, `1`. A reader refuses a newer version. |
  | `game` | Profile ids the package applies to (`t8, t9`, `jup`, `t11`), comma-separated; `*` or absent: any game. |
  | `family` | A hash family id (`t89.scr`, `t10.function`...); absent: every family of the game. |
  | `source` | Where the names come from. |
  | `licence` | Their licence, or `local only` when they may not be redistributed. |

  Other `# key: value` lines are metadata. A `#` line without a colon, or whose key holds a
  space, is a comment.
- **Entries**: a line is either a **name**, or a **pair** `hex<TAB>name`. The hex value may carry
  `0x` or a decompiler prefix (`hash_`, `function_`, `var_`...); a third tab-separated column is
  ignored. Names cannot hold a tab or start with `#`.
- **Sections**: a `# family: <id>` line after the header starts a new section whose entries
  belong to that family; `# family: *` returns to "every family".
- Blank lines are ignored.

## Meaning

- A name in a section with a family is hashed with that family; without one, with every family
  the game uses for script identifiers.
- A pair in a section with a family is kept as given, whether or not the name re-hashes to the
  value (a reader may count the ones that do not). A pair without a family is kept for each family
  of the game whose hash of the name equals the value, and dropped otherwise.
- Values of the 63- and 64-bit families are compared on at least their low 60 bits.
- The first name stored for a value wins.

## Example

```text
# gsc-hash-package: 1
# game: t8, t9
# source: identifiers of the example mod
# licence: CC0-1.0
example_mod_init
example_mod_spawn_wave
# family: t89.scr
0x1a2b3c4d	example_mod_on_player_spawned
```
