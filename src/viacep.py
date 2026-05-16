"""
Integração com a API pública ViaCEP.
Busca informações de endereço a partir de um CEP brasileiro.
"""

import re

import requests

API_URL = "https://viacep.com.br/ws/{cep}/json/"


def formatar_cep(cep: str) -> str:
    """Remove caracteres não numéricos do CEP."""
    return re.sub(r"\D", "", cep)


def buscar_endereco(cep: str) -> dict:
    """
    Consulta a API ViaCEP e retorna os dados do endereço.
    """
    cep_limpo = formatar_cep(cep)

    if len(cep_limpo) != 8:
        return {"erro": "CEP inválido. Informe 8 dígitos numéricos."}

    try:
        url = API_URL.format(cep=cep_limpo)
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        dados = response.json()

        if "erro" in dados:
            return {"erro": "CEP não encontrado."}

        return {
            "cep": dados.get("cep", ""),
            "logradouro": dados.get("logradouro", ""),
            "bairro": dados.get("bairro", ""),
            "cidade": dados.get("localidade", ""),
            "estado": dados.get("uf", ""),
            "erro": None,
        }

    except requests.exceptions.Timeout:
        return {"erro": "Tempo de conexão esgotado. Tente novamente."}
    except requests.exceptions.ConnectionError:
        return {"erro": "Sem conexão com a internet."}
    except Exception as e:
        return {"erro": f"Erro inesperado: {e}"}


def formatar_endereco(dados: dict) -> str:
    """Formata os dados do endereço em uma string legível."""
    if dados.get("erro"):
        return f"❌ {dados['erro']}"
    partes = []
    if dados.get("logradouro"):
        partes.append(dados["logradouro"])
    if dados.get("bairro"):
        partes.append(dados["bairro"])
    if dados.get("cidade") and dados.get("estado"):
        partes.append(f"{dados['cidade']}/{dados['estado']}")
    return ", ".join(partes)
