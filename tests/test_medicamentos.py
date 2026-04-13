"""
Testes automatizados para o MedControl.
"""

import json
import os
import pytest

# Garante que os testes usam um arquivo temporário
TEST_DADOS = os.path.join(os.path.dirname(__file__), "..", "dados_teste.json")

import src.medicamentos as med_module

# Sobrescreve o caminho do arquivo de dados para o arquivo de teste
med_module.ARQUIVO_DADOS = TEST_DADOS


def setup_function():
    """Limpa dados antes de cada teste."""
    if os.path.exists(TEST_DADOS):
        os.remove(TEST_DADOS)


def teardown_function():
    """Remove arquivo de teste após cada teste."""
    if os.path.exists(TEST_DADOS):
        os.remove(TEST_DADOS)


# ─────────────────── Testes: Caminho Feliz ───────────────────


def test_adicionar_medicamento_correto():
    """Deve adicionar um medicamento com dados válidos."""
    med = med_module.adicionar_medicamento("Losartana", ["08:00", "20:00"], "1 comprimido")
    assert med["nome"] == "Losartana"
    assert med["dose"] == "1 comprimido"
    assert "08:00" in med["horarios"]
    assert med["id"] == 1


def test_listar_medicamentos_retorna_lista():
    """Deve retornar lista com os medicamentos cadastrados."""
    med_module.adicionar_medicamento("Metformina", ["07:00"], "500mg")
    meds = med_module.listar_medicamentos()
    assert len(meds) == 1
    assert meds[0]["nome"] == "Metformina"


def test_buscar_medicamento_parcial():
    """Deve encontrar medicamento por parte do nome, sem case-sensitive."""
    med_module.adicionar_medicamento("Atenolol", ["08:00"], "25mg")
    resultado = med_module.buscar_medicamento("ateno")
    assert len(resultado) == 1
    assert resultado[0]["nome"] == "Atenolol"


def test_remover_medicamento_existente():
    """Deve remover medicamento pelo ID e retornar True."""
    med = med_module.adicionar_medicamento("Omeprazol", ["07:30"], "20mg")
    removido = med_module.remover_medicamento(med["id"])
    assert removido is True
    assert len(med_module.listar_medicamentos()) == 0


def test_adicionar_multiplos_medicamentos():
    """Deve suportar múltiplos medicamentos com IDs incrementais."""
    med_module.adicionar_medicamento("Rivotril", ["22:00"], "0.5mg")
    med_module.adicionar_medicamento("Sinvastatina", ["21:00"], "20mg")
    meds = med_module.listar_medicamentos()
    assert len(meds) == 2
    assert meds[0]["id"] == 1
    assert meds[1]["id"] == 2


# ─────────────────── Testes: Entrada Inválida ───────────────────


def test_adicionar_nome_vazio_levanta_erro():
    """Deve levantar ValueError ao tentar cadastrar sem nome."""
    with pytest.raises(ValueError, match="Nome do medicamento não pode ser vazio"):
        med_module.adicionar_medicamento("", ["08:00"], "1 comprimido")


def test_adicionar_sem_horario_levanta_erro():
    """Deve levantar ValueError ao tentar cadastrar sem horário."""
    with pytest.raises(ValueError, match="Pelo menos um horário deve ser informado"):
        med_module.adicionar_medicamento("Vitamina C", [], "1 comprimido")


def test_adicionar_dose_vazia_levanta_erro():
    """Deve levantar ValueError ao tentar cadastrar sem dose."""
    with pytest.raises(ValueError, match="Dose não pode ser vazia"):
        med_module.adicionar_medicamento("Dipirona", ["12:00"], "")


# ─────────────────── Testes: Caso Limite ───────────────────


def test_remover_id_inexistente_retorna_false():
    """Deve retornar False ao tentar remover ID que não existe."""
    resultado = med_module.remover_medicamento(9999)
    assert resultado is False


def test_buscar_sem_resultados():
    """Deve retornar lista vazia ao buscar nome inexistente."""
    resultado = med_module.buscar_medicamento("xyzabc")
    assert resultado == []


def test_listar_sem_medicamentos():
    """Deve retornar lista vazia quando não há medicamentos cadastrados."""
    meds = med_module.listar_medicamentos()
    assert meds == []


def test_nome_com_espacos_em_branco_eh_normalizado():
    """Deve remover espaços em branco do início e fim do nome."""
    med = med_module.adicionar_medicamento("  Paracetamol  ", ["08:00"], "  500mg  ")
    assert med["nome"] == "Paracetamol"
    assert med["dose"] == "500mg"
