#!/usr/bin/env bash
# Normalize String's trailing optional-bundle arg so bundled scripts stay byte-identical.
# Usage: _optshim.sh <cmd...> -- <bundle-token>
# Args before -- pass verbatim. The bundle after -- is dropped when empty/placeholder,
# else word-split into argv (one String field carrying "--a 1 --b 2" becomes real flags).
cmd=()
while [ "$#" -gt 0 ] && [ "$1" != "--" ]; do cmd+=("$1"); shift; done
shift 2>/dev/null
b="${1:-}"
case "$b" in "''"|""|"{"*"}") b="" ;; esac
case "$b" in \'*\') b="${b#\'}"; b="${b%\'}" ;; esac
extra=()
[ -n "$b" ] && extra=($b)
exec "${cmd[@]}" "${extra[@]}"
