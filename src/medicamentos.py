"""
MedControl - Controlador de Medicamentos para Idosos
Versão: 1.0.0
"""

import json
import os
from datetime import datetime

ARQUIVO_DADOS = os.path.join(os.path.dirname(__file__), "..", "dados.json")


def carregar_dados() -> dict:
    """Carrega os dados do arquivo JSON."""
    if not os.path.exists(ARQUIVO_DADOS):
        return {"medicamentos": []}
    with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_dados(dados: dict) -> None:
    """Salva os dados no arquivo JSON."""
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def adicionar_medicamento(nome: str, horarios: list, dose: str) -> dict:
    """Adiciona um novo medicamento ao controle."""
    if not nome or not nome.strip():
        raise ValueError("Nome do medicamento não pode ser vazio.")
    if not horarios:
        raise ValueError("Pelo menos um horário deve ser informado.")
    if not dose or not dose.strip():
        raise ValueError("Dose não pode ser vazia.")

    dados = carregar_dados()
    medicamento = {
        "id": len(dados["medicamentos"]) + 1,
        "nome": nome.strip(),
        "horarios": horarios,
        "dose": dose.strip(),
        "criado_em": datetime.now().strftime("%d/%m/%Y %H:%M"),
    }
    dados["medicamentos"].append(medicamento)
    salvar_dados(dados)
    return medicamento


def listar_medicamentos() -> list:
    """Retorna a lista de medicamentos cadastrados."""
    dados = carregar_dados()
    return dados["medicamentos"]


def remover_medicamento(medicamento_id: int) -> bool:
    """Remove um medicamento pelo ID. Retorna True se removido, False se não encontrado."""
    dados = carregar_dados()
    antes = len(dados["medicamentos"])
    dados["medicamentos"] = [
        m for m in dados["medicamentos"] if m["id"] != medicamento_id
    ]
    if len(dados["medicamentos"]) == antes:
        return False
    salvar_dados(dados)
    return True


def buscar_medicamento(nome: str) -> list:
    """Busca medicamentos pelo nome (parcial, sem case-sensitive)."""
    dados = carregar_dados()
    nome_lower = nome.lower()
    return [m for m in dados["medicamentos"] if nome_lower in m["nome"].lower()]


def verificar_horario_agora() -> list:
    """Retorna medicamentos cujo horário coincide com a hora atual."""
    agora = datetime.now().strftime("%H:%M")
    dados = carregar_dados()
    return [m for m in dados["medicamentos"] if agora in m["horarios"]]


# ─────────────────────────── Interface CLI ───────────────────────────


def exibir_menu():
    print("\n" + "=" * 45)
    print("   💊 MedControl - Controle de Medicamentos")
    print("=" * 45)
    print("  1. Cadastrar medicamento")
    print("  2. Listar medicamentos")
    print("  3. Remover medicamento")
    print("  4. Buscar medicamento")
    print("  5. Ver alertas do momento")
    print("  0. Sair")
    print("=" * 45)


def fluxo_cadastrar():
    print("\n[ CADASTRAR MEDICAMENTO ]")
    nome = input("Nome do medicamento: ").strip()
    dose = input("Dose (ex: 1 comprimido, 5ml): ").strip()
    horarios_str = input("Horários (ex: 08:00,14:00,20:00): ").strip()
    horarios = [h.strip() for h in horarios_str.split(",") if h.strip()]

    try:
        med = adicionar_medicamento(nome, horarios, dose)
        print(f"\n✅ Medicamento '{med['nome']}' cadastrado com sucesso! (ID: {med['id']})")
    except ValueError as e:
        print(f"\n❌ Erro: {e}")


def fluxo_listar():
    print("\n[ MEDICAMENTOS CADASTRADOS ]")
    meds = listar_medicamentos()
    if not meds:
        print("Nenhum medicamento cadastrado.")
        return
    for m in meds:
        print(f"\n  ID: {m['id']}")
        print(f"  Nome: {m['nome']}")
        print(f"  Dose: {m['dose']}")
        print(f"  Horários: {', '.join(m['horarios'])}")
        print(f"  Cadastrado em: {m['criado_em']}")
        print("  " + "-" * 30)


def fluxo_remover():
    print("\n[ REMOVER MEDICAMENTO ]")
    try:
        med_id = int(input("Digite o ID do medicamento: "))
        if remover_medicamento(med_id):
            print("✅ Medicamento removido com sucesso.")
        else:
            print("❌ Medicamento não encontrado.")
    except ValueError:
        print("❌ ID inválido.")


def fluxo_buscar():
    print("\n[ BUSCAR MEDICAMENTO ]")
    nome = input("Digite o nome (ou parte do nome): ").strip()
    resultados = buscar_medicamento(nome)
    if not resultados:
        print("Nenhum medicamento encontrado.")
    else:
        for m in resultados:
            print(f"\n  ID: {m['id']} | Nome: {m['nome']} | Dose: {m['dose']} | Horários: {', '.join(m['horarios'])}")


def fluxo_alertas():
    print("\n[ ALERTAS DO MOMENTO ]")
    agora = datetime.now().strftime("%H:%M")
    print(f"Hora atual: {agora}")
    meds = verificar_horario_agora()
    if not meds:
        print("Nenhum medicamento programado para agora.")
    else:
        print("\n⚠️  Hora de tomar:")
        for m in meds:
            print(f"  💊 {m['nome']} - {m['dose']}")


def main():
    print("\nBem-vindo ao MedControl!")
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            fluxo_cadastrar()
        elif opcao == "2":
            fluxo_listar()
        elif opcao == "3":
            fluxo_remover()
        elif opcao == "4":
            fluxo_buscar()
        elif opcao == "5":
            fluxo_alertas()
        elif opcao == "0":
            print("\nAté logo! Cuide-se. 💙")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
