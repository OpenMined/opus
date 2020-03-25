import os

docs_path = lambda *args: os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'docs', *args))
