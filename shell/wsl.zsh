export PNPM_HOME="${PNPM_HOME:-$HOME/.local/share/pnpm}"
case ":$PATH:" in
  *":$PNPM_HOME:"*) ;;
  *) export PATH="$PNPM_HOME:$PATH" ;;
esac

if command -v wslview >/dev/null 2>&1; then
  alias open='wslview'
fi

if command -v clip.exe >/dev/null 2>&1; then
  alias pbcopy='clip.exe'
fi

if command -v powershell.exe >/dev/null 2>&1; then
  alias pbpaste='powershell.exe -NoProfile -Command Get-Clipboard'
fi

if ! command -v bat >/dev/null 2>&1 && command -v batcat >/dev/null 2>&1; then
  alias bat='batcat'
fi

if ! command -v fd >/dev/null 2>&1 && command -v fdfind >/dev/null 2>&1; then
  alias fd='fdfind'
fi

cursor() {
  if command -v cursor.exe >/dev/null 2>&1; then
    cursor.exe "$@"
  elif command -v cursor >/dev/null 2>&1; then
    command cursor "$@"
  else
    echo "cursor is not installed" >&2
    return 1
  fi
}
