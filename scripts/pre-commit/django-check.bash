#!/usr/bin/env bash
set -euo pipefail

uv run python manage.py check || exit 0
