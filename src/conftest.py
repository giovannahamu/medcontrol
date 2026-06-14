"""
Configuração do pytest — garante que a raiz do projeto
esteja no sys.path para que os imports src.* funcionem.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))