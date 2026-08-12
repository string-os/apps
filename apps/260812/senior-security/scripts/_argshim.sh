#!/usr/bin/env bash
# Run a bundled generator, normalizing String's arg-passing artifacts so the
# generator scripts stay byte-identical.
#   - An omitted optional field arrives as the literal token '' or {placeholder}: drop it.
#   - A raw-flag field (e.g. extra_args) arrives as ONE token holding several
#     space-separated flags: word-split it into real argv (guide §6 / memory rule #3).
# Usage: _argshim.sh <script.py> <fixed args...> -- <raw-flag string>
# Simplrer form used here: _argshim.sh <script.py> [token...]; each token is dropped
# if empty/placeholder, else word-split (unquoted) into the final command.
script="$1"; shift
final=()
for tok in "$@"; do
  case "$tok" in
    "''"|"") continue ;;
    "{"*"}") continue ;;
  esac
  # strip one surrounding quote-pair if present
  case "$tok" in
    \'*\') tok="${tok#\'}"; tok="${tok%\'}" ;;
    \"*\") tok="${tok#\"}"; tok="${tok%\"}" ;;
  esac
  [ -z "$tok" ] && continue
  # word-split this token into argv (intended for flag bundles like extra_args)
  # shellcheck disable=SC2206
  parts=($tok)
  final+=("${parts[@]}")
done
exec python3 "$script" "${final[@]}"
