#!/bin/bash
# Run all linting checks locally (same as GitHub Actions)

echo "=== Running Black (code formatting) ==="
poetry run black --check .
if [ $? -eq 0 ]; then
    echo "✅ Black formatting passed"
else
    echo "❌ Black formatting failed. Run 'poetry run black .' to fix"
    exit 1
fi

echo ""
echo "=== Running isort (import sorting) ==="
poetry run isort --check-only .
if [ $? -eq 0 ]; then
    echo "✅ isort passed"
else
    echo "❌ isort failed. Run 'poetry run isort .' to fix"
    exit 1
fi

echo ""
echo "=== Running Flake8 (linting) ==="
poetry run flake8 mac_utils/ --max-line-length=100 --extend-ignore=E203,W503
if [ $? -eq 0 ]; then
    echo "✅ Flake8 passed"
else
    echo "❌ Flake8 failed. See errors above"
    exit 1
fi

echo ""
echo "=== Running mypy (type checking) ==="
poetry run mypy mac_utils/ --ignore-missing-imports
if [ $? -eq 0 ]; then
    echo "✅ mypy passed"
else
    echo "❌ mypy failed. See errors above"
    exit 1
fi

echo ""
echo "✅ All linting checks passed!"
