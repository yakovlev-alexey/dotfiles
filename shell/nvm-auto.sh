# Auto-switch Node version from .nvmrc on cd (bash).
# Source after nvm.sh is loaded.

if ! type nvm >/dev/null 2>&1; then
  return 0 2>/dev/null || true
fi

cdnvm() {
  command cd "$@" || return $?

  local nvm_path nvm_version locally_resolved_nvm_version default_version

  nvm_path="$(nvm_find_up .nvmrc | command tr -d '\n')"

  # No .nvmrc in this directory tree — fall back to default.
  if [[ ! $nvm_path = *[^[:space:]]* ]]; then
    default_version="$(nvm version default)"

    if [[ "$default_version" == "N/A" ]]; then
      nvm alias default node
      default_version="$(nvm version default)"
    fi

    if [[ "$(nvm current)" == "$default_version" ]]; then
      return
    fi

    nvm use default
    return
  fi

  nvm_version="$(<"$nvm_path"/.nvmrc)"
  locally_resolved_nvm_version="$(nvm ls --no-colors "$nvm_version" | command sed "s/^[[:space:]]*//" | command cut -d' ' -f2)"

  if [[ "$locally_resolved_nvm_version" == "N/A" ]]; then
    nvm install "$nvm_version"
  elif [[ "$(nvm current)" != "$locally_resolved_nvm_version" ]]; then
    nvm use "$nvm_version"
  fi
}

alias cd='cdnvm'
cdnvm "$PWD" || true
