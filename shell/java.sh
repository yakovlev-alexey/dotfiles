# JDK 17 for macOS: Homebrew openjdk@17 or system JVM under /Library/Java/JavaVirtualMachines.
# /usr/libexec/java_home on recent macOS can return a stub even when a JVM is installed.

if [ "$(uname -s)" != "Darwin" ] || [ -n "${JAVA_HOME:-}" ]; then
  return 0 2>/dev/null || exit 0
fi

_jdk_home_candidates=(
  "${HOMEBREW_PREFIX:-/opt/homebrew}/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home"
  "/Library/Java/JavaVirtualMachines/jdk-17.jdk/Contents/Home"
  "/Library/Java/JavaVirtualMachines/openjdk-17.jdk/Contents/Home"
)

for _jdk_home in "${_jdk_home_candidates[@]}"; do
  if [ -x "$_jdk_home/bin/java" ]; then
    export JAVA_HOME="$_jdk_home"
    case ":$PATH:" in
      *":$JAVA_HOME/bin:"*) ;;
      *) export PATH="$JAVA_HOME/bin:$PATH" ;;
    esac
    break
  fi
done

unset _jdk_home_candidates _jdk_home
