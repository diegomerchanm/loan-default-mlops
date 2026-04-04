# tests/test_app.py
import pytest

def test_imports():
    """Vérifie que les dépendances principales sont installées."""
    import sklearn
    import pandas
    import numpy
    import mlflow
    import streamlit

def test_version_python():
    """Vérifie que la version Python est compatible."""
    import sys
    assert sys.version_info >= (3, 11), "Python 3.11+ requis"