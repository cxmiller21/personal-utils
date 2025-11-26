#!/bin/bash
# Auto-fix linting issues

echo "=== Auto-fixing with Black ==="
poetry run black .

echo ""
echo "=== Auto-fixing with isort ==="
poetry run isort .

echo ""
echo "✅ Auto-fixes complete!"
echo ""
echo "⚠️  Note: Some issues may require manual fixes (unused imports, f-strings, etc.)"
echo "Run './lint.sh' to check for remaining issues"
