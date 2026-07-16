# Auto-switch Node version from .nvmrc on directory change (nvm chpwd hook).
# Source after nvm.sh is loaded.

if ! typeset -f nvm >/dev/null 2>&1; then
  return 0
fi

autoload -U add-zsh-hook

load-nvmrc() {
  local nvmrc_path nvmrc_node_version

  nvmrc_path="$(nvm_find_nvmrc)"

  if [[ -n "$nvmrc_path" ]]; then
    nvmrc_node_version="$(nvm version "$(cat "${nvmrc_path}")")"

    if [[ "$nvmrc_node_version" == "N/A" ]]; then
      nvm install
    elif [[ "$nvmrc_node_version" != "$(nvm version)" ]]; then
      nvm use
    fi
  elif [[ -n "$(PWD=$OLDPWD nvm_find_nvmrc)" ]] && [[ "$(nvm version)" != "$(nvm version default)" ]]; then
    echo "Reverting to nvm default version"
    nvm use default
  fi
}

add-zsh-hook chpwd load-nvmrc
load-nvmrc
