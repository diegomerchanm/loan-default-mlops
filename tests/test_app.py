# tests/test_app.py
from pathlib import Path
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

def test_structure_projet():
    """Vérifie que la structure du projet est correcte."""
    from pathlib import Path
    assert Path("Dockerfile").exists(), "Dockerfile manquant"
    assert Path("requirements.txt").exists(), "requirements.txt manquant"
    assert Path("app").exists(), "Dossier app/ manquant"
    assert Path("model").exists(), "Dossier model/ manquant"

def test_dockerfile_contenu():
    """Vérifie que le Dockerfile est correctement configuré."""
    contenu = Path("Dockerfile").read_text()
    assert "python:3.11-slim" in contenu, "Image de base incorrecte"
    assert "8501" in contenu, "Port Streamlit manquant"
    assert "app.py" in contenu, "Point d'entrée manquant"