rm -rf .venv .mypy_cache __pycache__ *.egg-info dist build .pytest_cache .cache .tox .coverage
rm -rf uv.lock poetry.lock Pipfile.lock pip-wheel-metadata
rm -rf ~/.cache/uv ~/.local/share/uv

python -m venv .venv
source .venv/bin/activate

