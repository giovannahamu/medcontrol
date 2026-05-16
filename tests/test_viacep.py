"""
Testes de integração para o módulo viacep.
Valida a comunicação com a API ViaCEP mockando as respostas HTTP.
"""

from unittest.mock import MagicMock, patch

from src.viacep import buscar_endereco, formatar_cep, formatar_endereco

# ─────────────────── Testes: formatar_cep ───────────────────


def test_formatar_cep_remove_hifen():
    """Deve remover hífen do CEP formatado."""
    assert formatar_cep("01310-100") == "01310100"


def test_formatar_cep_remove_espacos():
    """Deve remover espaços do CEP."""
    assert formatar_cep("01310 100") == "01310100"


def test_formatar_cep_apenas_numeros():
    """Deve manter CEP já numérico sem alteração."""
    assert formatar_cep("01310100") == "01310100"


# ─────────────────── Testes: buscar_endereco ───────────────────


def test_buscar_endereco_cep_invalido_menos_de_8_digitos():
    """Deve retornar erro para CEP com menos de 8 dígitos."""
    resultado = buscar_endereco("1234")
    assert resultado["erro"] is not None
    assert "inválido" in resultado["erro"].lower()


def test_buscar_endereco_sucesso():
    """
    Teste de integração: valida que buscar_endereco processa
    corretamente uma resposta bem-sucedida da API ViaCEP.
    """
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json.return_value = {
        "cep": "01310-100",
        "logradouro": "Avenida Paulista",
        "bairro": "Bela Vista",
        "localidade": "São Paulo",
        "uf": "SP",
    }

    with patch("src.viacep.requests.get", return_value=mock_response):
        resultado = buscar_endereco("01310-100")

    assert resultado["erro"] is None
    assert resultado["logradouro"] == "Avenida Paulista"
    assert resultado["bairro"] == "Bela Vista"
    assert resultado["cidade"] == "São Paulo"
    assert resultado["estado"] == "SP"


def test_buscar_endereco_cep_nao_encontrado():
    """
    Teste de integração: valida que CEP inexistente retorna erro
    quando a API responde com o campo 'erro' no JSON.
    """
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json.return_value = {"erro": True}

    with patch("src.viacep.requests.get", return_value=mock_response):
        resultado = buscar_endereco("99999999")

    assert resultado["erro"] is not None
    assert "não encontrado" in resultado["erro"].lower()


def test_buscar_endereco_timeout():
    """
    Teste de integração: valida que a aplicação não quebra
    quando a API está inacessível por timeout.
    """
    import requests as req

    with patch("src.viacep.requests.get", side_effect=req.exceptions.Timeout):
        resultado = buscar_endereco("01310100")

    assert resultado["erro"] is not None
    assert "esgotado" in resultado["erro"].lower()


def test_buscar_endereco_sem_conexao():
    """
    Teste de integração: valida que a aplicação lida com
    ausência de conexão de forma segura.
    """
    import requests as req

    with patch(
        "src.viacep.requests.get", side_effect=req.exceptions.ConnectionError
    ):
        resultado = buscar_endereco("01310100")

    assert resultado["erro"] is not None
    assert "conexão" in resultado["erro"].lower()


# ─────────────────── Testes: formatar_endereco ───────────────────


def test_formatar_endereco_completo():
    """Deve formatar corretamente um endereço completo."""
    dados = {
        "logradouro": "Avenida Paulista",
        "bairro": "Bela Vista",
        "cidade": "São Paulo",
        "estado": "SP",
        "erro": None,
    }
    resultado = formatar_endereco(dados)
    assert "Avenida Paulista" in resultado
    assert "São Paulo" in resultado


def test_formatar_endereco_com_erro():
    """Deve retornar mensagem de erro formatada."""
    dados = {"erro": "CEP não encontrado."}
    resultado = formatar_endereco(dados)
    assert "❌" in resultado
    assert "não encontrado" in resultado.lower()
