"""
Testes do MedControl — Etapa 3
Usa mock para não depender do Supabase real durante o CI.
"""

from unittest.mock import MagicMock, patch

import pytest


# --------------------------------------------------------------------------- #
#  Helpers de mock                                                              #
# --------------------------------------------------------------------------- #


def _make_response(data):
    """Cria um objeto de resposta fake no estilo supabase-py."""
    resp = MagicMock()
    resp.data = data
    return resp


def _mock_client(data_retornado):
    """Retorna um client Supabase mockado que devolve data_retornado."""
    client = MagicMock()
    table = client.table.return_value
    resp = _make_response(data_retornado)
    table.insert.return_value.execute.return_value = resp
    table.select.return_value.order.return_value.execute.return_value = resp
    table.select.return_value.ilike.return_value.execute.return_value = resp
    table.delete.return_value.eq.return_value.execute.return_value = resp
    return client


# --------------------------------------------------------------------------- #
#  Testes de cadastro                                                           #
# --------------------------------------------------------------------------- #


class TestCadastrarMedicamento:
    def test_cadastra_e_retorna_registro(self):
        from src.medicamentos import cadastrar_medicamento

        registro = {
            "id": 1,
            "nome": "Losartana",
            "dose": "1 comprimido",
            "horarios": ["08:00", "20:00"],
        }
        client = _mock_client([registro])

        with patch("src.medicamentos.get_client", return_value=client):
            resultado = cadastrar_medicamento(
                "Losartana", "1 comprimido", ["08:00", "20:00"]
            )

        assert resultado["nome"] == "Losartana"
        assert resultado["id"] == 1

    def test_strip_nos_campos(self):
        from src.medicamentos import cadastrar_medicamento

        registro = {
            "id": 2,
            "nome": "Metformina",
            "dose": "500mg",
            "horarios": ["12:00"],
        }
        client = _mock_client([registro])

        with patch("src.medicamentos.get_client", return_value=client):
            cadastrar_medicamento("  Metformina  ", "  500mg  ", ["12:00"])

        call_args = client.table.return_value.insert.call_args[0][0]
        assert call_args["nome"] == "Metformina"
        assert call_args["dose"] == "500mg"


# --------------------------------------------------------------------------- #
#  Testes de listagem                                                           #
# --------------------------------------------------------------------------- #


class TestListarMedicamentos:
    def test_retorna_lista_vazia(self):
        from src.medicamentos import listar_medicamentos

        client = _mock_client([])

        with patch("src.medicamentos.get_client", return_value=client):
            resultado = listar_medicamentos()

        assert resultado == []

    def test_retorna_todos_medicamentos(self):
        from src.medicamentos import listar_medicamentos

        dados = [
            {"id": 1, "nome": "Atenolol", "dose": "25mg", "horarios": ["08:00"]},
            {"id": 2, "nome": "Omeprazol", "dose": "20mg", "horarios": ["07:00"]},
        ]
        client = _mock_client(dados)

        with patch("src.medicamentos.get_client", return_value=client):
            resultado = listar_medicamentos()

        assert len(resultado) == 2
        assert resultado[0]["nome"] == "Atenolol"


# --------------------------------------------------------------------------- #
#  Testes de remoção                                                            #
# --------------------------------------------------------------------------- #


class TestRemoverMedicamento:
    def test_remove_existente_retorna_true(self):
        from src.medicamentos import remover_medicamento

        client = _mock_client([{"id": 1}])

        with patch("src.medicamentos.get_client", return_value=client):
            resultado = remover_medicamento(1)

        assert resultado is True

    def test_nao_encontrado_retorna_false(self):
        from src.medicamentos import remover_medicamento

        client = _mock_client([])

        with patch("src.medicamentos.get_client", return_value=client):
            resultado = remover_medicamento(999)

        assert resultado is False


# --------------------------------------------------------------------------- #
#  Testes de busca                                                              #
# --------------------------------------------------------------------------- #


class TestBuscarMedicamento:
    def test_busca_retorna_resultados(self):
        from src.medicamentos import buscar_medicamento

        dados = [{"id": 1, "nome": "Losartana", "dose": "50mg", "horarios": ["08:00"]}]
        client = _mock_client(dados)

        with patch("src.medicamentos.get_client", return_value=client):
            resultado = buscar_medicamento("losar")

        assert len(resultado) == 1
        assert "Losartana" in resultado[0]["nome"]

    def test_busca_sem_resultado(self):
        from src.medicamentos import buscar_medicamento

        client = _mock_client([])

        with patch("src.medicamentos.get_client", return_value=client):
            resultado = buscar_medicamento("xpto")

        assert resultado == []


# --------------------------------------------------------------------------- #
#  Testes de alertas                                                            #
# --------------------------------------------------------------------------- #


class TestAlertasMomento:
    def test_alerta_quando_horario_coincide(self):
        from datetime import datetime

        from src.medicamentos import alertas_momento

        dados = [
            {"id": 1, "nome": "Dipirona", "dose": "1 comprimido", "horarios": ["10:00"]}
        ]
        client = _mock_client(dados)

        horario_fake = datetime(2024, 1, 1, 10, 5)
        with patch("src.medicamentos.get_client", return_value=client):
            with patch("src.medicamentos.datetime") as mock_dt:
                mock_dt.now.return_value = horario_fake
                resultado = alertas_momento()

        assert len(resultado) == 1
        assert resultado[0]["nome"] == "Dipirona"

    def test_sem_alerta_fora_da_janela(self):
        from datetime import datetime

        from src.medicamentos import alertas_momento

        dados = [
            {"id": 1, "nome": "Dipirona", "dose": "1 comprimido", "horarios": ["10:00"]}
        ]
        client = _mock_client(dados)

        horario_fake = datetime(2024, 1, 1, 15, 0)
        with patch("src.medicamentos.get_client", return_value=client):
            with patch("src.medicamentos.datetime") as mock_dt:
                mock_dt.now.return_value = horario_fake
                resultado = alertas_momento()

        assert resultado == []

    def test_horario_invalido_ignorado(self):
        from datetime import datetime

        from src.medicamentos import alertas_momento

        dados = [{"id": 2, "nome": "Paracetamol", "dose": "500mg", "horarios": ["invalido"]}]
        client = _mock_client(dados)

        horario_fake = datetime(2024, 1, 1, 10, 0)
        with patch("src.medicamentos.get_client", return_value=client):
            with patch("src.medicamentos.datetime") as mock_dt:
                mock_dt.now.return_value = horario_fake
                resultado = alertas_momento()

        assert resultado == []


# --------------------------------------------------------------------------- #
#  Teste de configuração do cliente                                             #
# --------------------------------------------------------------------------- #


class TestGetClient:
    def test_erro_sem_variaveis_de_ambiente(self):
        import importlib
        import os

        import src.medicamentos as mod

        with patch.dict(os.environ, {"SUPABASE_URL": "", "SUPABASE_KEY": ""}):
            importlib.reload(mod)
            with pytest.raises(EnvironmentError):
                mod.get_client()