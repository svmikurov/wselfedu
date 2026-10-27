#!/bin/sh
set -e

echo "🌐 Serving documentation on http://0.0.0.0:8000 (host: http://localhost:8010)"
exec python -m http.server --directory /docs/build/html 8000