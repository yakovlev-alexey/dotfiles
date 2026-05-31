if [[ -x /opt/homebrew/bin/brew ]]; then
  eval "$(/opt/homebrew/bin/brew shellenv)"
fi

export HOMEBREW_PREFIX="${HOMEBREW_PREFIX:-/opt/homebrew}"
fpath+=("$HOMEBREW_PREFIX/share/zsh/site-functions")

if [[ -d "$HOME/.oh-my-zsh" ]]; then
  export ZSH="${ZSH:-$HOME/.oh-my-zsh}"
  plugins=(git zsh-interactive-cd zsh-autosuggestions colorize brew)
  source "$ZSH/oh-my-zsh.sh"
fi

if [[ -s "$HOMEBREW_PREFIX/opt/nvm/nvm.sh" ]]; then
  export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"
  source "$HOMEBREW_PREFIX/opt/nvm/nvm.sh"
fi

if [[ -s "$HOMEBREW_PREFIX/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh" ]]; then
  source "$HOMEBREW_PREFIX/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh"
fi

export PNPM_HOME="$HOME/Library/pnpm"
case ":$PATH:" in
  *":$PNPM_HOME:"*) ;;
  *) export PATH="$PNPM_HOME:$PATH" ;;
esac

[[ -d "$HOME/.opencode/bin" ]] && export PATH="$HOME/.opencode/bin:$PATH"

cursor() {
  open -a "/Applications/Cursor.app" "$@"
}
