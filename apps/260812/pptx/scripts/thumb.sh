#!/usr/bin/env bash
# Thin wrapper so the thumbnail action can omit the optional output_prefix / cols.
# String passes omitted optionals as the literal two-char string '' or an
# unsubstituted {placeholder}; normalize both to "unset" before calling thumbnail.py.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"

clean() {
  v="${1:-}"
  # strip one surrounding quote pair
  if [ "${#v}" -ge 2 ]; then
    f="${v:0:1}"; l="${v: -1}"
    if { [ "$f" = "'" ] || [ "$f" = '"' ]; } && [ "$f" = "$l" ]; then v="${v:1:${#v}-2}"; fi
  fi
  case "$v" in "{"*"}") v="";; esac
  printf '%s' "$v"
}

input="$(clean "${1:-}")"
prefix="$(clean "${2:-}")"
cols="$(clean "${3:-}")"

args=("$input")
[ -n "$prefix" ] && args+=("$prefix")
[ -n "$cols" ] && args+=("--cols" "$cols")

exec python3 "$here/thumbnail.py" "${args[@]}"
