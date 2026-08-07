#!/usr/bin/env bash

set -euo pipefail

crawler_script_dir="$({ CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd; })"
crawler_source_dir="${crawler_script_dir}/tools/feishu-doc-crawler/src"

supports_crawl4ai() {
  local candidate="$1"
  test -x "$candidate" && "$candidate" -c 'import crawl4ai' >/dev/null 2>&1
}

resolve_python() {
  local candidate=""

  if test -n "${CRAWLER_FEISHU_PYTHON:-}"; then
    candidate="${CRAWLER_FEISHU_PYTHON}"
    if supports_crawl4ai "$candidate"; then
      printf '%s\n' "$candidate"
      return 0
    fi
    printf 'CRAWLER_FEISHU_PYTHON 不可执行或未安装 crawl4ai: %s\n' "$candidate" >&2
    return 1
  fi

  candidate="$(command -v python 2>/dev/null || true)"
  if test -n "$candidate" && supports_crawl4ai "$candidate"; then
    printf '%s\n' "$candidate"
    return 0
  fi

  if command -v pyenv >/dev/null 2>&1; then
    candidate="$(pyenv prefix 3.11.7 2>/dev/null || true)/bin/python"
    if supports_crawl4ai "$candidate"; then
      printf '%s\n' "$candidate"
      return 0
    fi
  fi

  printf '%s\n' '未找到安装了 crawl4ai 的 Python。请先在目标环境安装 crawl4ai==0.9.2。' >&2
  return 1
}

crawler_python="$(resolve_python)"
export PYTHONPATH="${crawler_source_dir}${PYTHONPATH:+:${PYTHONPATH}}"

exec "$crawler_python" -m feishu_doc_crawler "$@"
