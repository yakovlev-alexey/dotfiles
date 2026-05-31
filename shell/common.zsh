export EDITOR="${EDITOR:-nvim}"
export VISUAL="${VISUAL:-$EDITOR}"
export LANG="${LANG:-en_US.UTF-8}"
export LC_ALL="${LC_ALL:-en_US.UTF-8}"

case ":$PATH:" in
  *":$HOME/.local/bin:"*) ;;
  *) export PATH="$HOME/.local/bin:$PATH" ;;
esac

setopt hist_ignore_all_dups append_history hist_ignore_space share_history
HISTFILE="${HISTFILE:-$HOME/.zsh_history}"
HISTSIZE="${HISTSIZE:-50000}"
SAVEHIST="${SAVEHIST:-50000}"

bindkey -e
bindkey '^[[H' beginning-of-line
bindkey '^[[F' end-of-line
bindkey '^[[1;3D' backward-word
bindkey '^[[1;3C' forward-word

export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"
if ! command -v nvm >/dev/null 2>&1 && [[ -s "$NVM_DIR/nvm.sh" ]]; then
  source "$NVM_DIR/nvm.sh"
fi
[[ -s "$NVM_DIR/bash_completion" ]] && source "$NVM_DIR/bash_completion"
