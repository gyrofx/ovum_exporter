install:
    pip install -e .

test:
    pytest -v

format:
    black src tests
