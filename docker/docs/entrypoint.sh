#!/bin/sh
set -e

echo "📚 Building documentation..."
sphinx-build /docs/source /docs/build/html

echo "✅ Documentation successfully built!"
echo "🌐 Starting HTTP server on http://localhost:8010"

exec python -m http.server --directory /docs/build/html 8000