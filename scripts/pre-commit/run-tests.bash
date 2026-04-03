#!/usr/bin/env bash
set -euo pipefail

uv run coverage run manage.py test --failfast
