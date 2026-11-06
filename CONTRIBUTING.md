# Contributing to gruff-data

Thank you for helping. Most useful contributions are small: one measured fact, with the
command that measured it.

## Developer Certificate of Origin

Every commit must be signed off under the [Developer Certificate of Origin 1.1](https://developercertificate.org/):

```sh
git commit -s -m "t6: measure foreach lowering on the T6 corpus"
```

The `Signed-off-by:` line certifies that you wrote the change, or have the right to submit it
under the licence of the file it touches. There is no CLA.

By contributing, you agree that your contribution is dedicated under **CC0-1.0**. The only
exception is an entry that carries another `license` label under the rule in `README.md`.

## No proprietary files, ever

Do not commit, attach to an issue, or paste into a pull request:

- game scripts (`.gsc`, `.csc`, `.gsh`), whether shipped, from mod tools, decompiled or dumped;
- text, tables or syntax files from official documentation or mod tools;
- binaries, fastfiles, zone dumps, assets, or any file extracted from a game;
- function descriptions or comments copied from any of the above.

Facts you re-derive are welcome: a feature is present or absent, a keyword exists, a usage
count, a function name, an arity. Record how you obtained them:

- add or reuse a source in `sources.toml` (`kind`, `license`, and `usage = "facts-only"` for
  proprietary material);
- prefer a measurement with `tools/featcount.py` on your own local install, and commit the
  resulting counts under `evidence/`;
- put the count or the reasoning in the entry's `note`.

Bug reports need a fixture. Write a minimal fixture yourself instead of copying game code.

## Changing a profile

1. Edit `profiles/<id>.toml`. Every feature stays present. Write `"unknown"` rather than delete,
   and `"n/a"` (enum features) when the feature cannot apply to the game.
2. Set `confidence` honestly. A value that a community compiler accepts but the retail compiler
   may not is `assumed`.
3. If your evidence contradicts an existing claim, do not overwrite it. Set
   `status = "unresolved"` and add an `[[unresolved]]` block with both claims and the measurement
   that would settle it.
4. Run `python -I tools/validate.py` (README.md, Validation: a venv with `jsonschema`). It checks the
   schemas, the source ids, the licence labels and the catalogue rules.

## Adding a feature

Add it to `schema/profile.schema.json` with a description and a value type. Then add an entry for
it to every profile, since every feature is required. Name it after the construct, not the game,
and keep the name of the matching `gsc.ungram` gate in step (`gruff/grammar/`).

## Takedown

If you hold rights in something you believe was committed here by mistake, open an issue or
contact the maintainers. It will be removed from the tree and from history.
