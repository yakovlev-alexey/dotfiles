mcd() {
  mkdir -p -- "$@" && cd -- "${@:$#}"
}

path-prepend() {
  [[ -d "$1" ]] || return 0
  case ":$PATH:" in
    *":$1:"*) ;;
    *) export PATH="$1:$PATH" ;;
  esac
}
