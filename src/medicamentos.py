"""
MedControl — Controlador de Medicamentos para Idosos
Etapa 3: Integração com Supabase (PostgreSQL na nuvem)
"""

import os
from datetime import datetime

# Supabase
from supabase import create_client, Client

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")


def get_client() -> Client:
    """Retorna o cliente Supabase configurado."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise EnvironmentError(
            "Variáveis SUPABASE_URL e SUPABASE_KEY não configuradas."
        )
    return create_client(SUPABASE_URL, SUPABASE_KEY)


# --------------------------------------------------------------------------- #
#  CRUD                                                                         #
# --------------------------------------------------------------------------- #

def cadastrar_medicamento(nome: str, dose: str, horarios: list[str]) -> dict:
    """Insere um medicamento no banco e retorna o registro criado."""
    client = get_client()
    payload = {
        "nome": nome.strip(),
        "dose": dose.strip(),
        "horarios": horarios,
    }
    response = client.table("medicamentos").insert(payload).execute()
    return response.data[0]


def listar_medicamentos() -> list[dict]:
    """Retorna todos os medicamentos cadastrados."""
    client = get_client()
    response = client.table("medicamentos").select("*").order("id").execute()
    return response.data


def remover_medicamento(med_id: int) -> bool:
    """Remove um medicamento pelo ID. Retorna True se removeu, False se não existia."""
    client = get_client()
    response = (
        client.table("medicamentos").delete().eq("id", med_id).execute()
    )
    return len(response.data) > 0


def buscar_medicamento(nome_parcial: str) -> list[dict]:
    """Busca medicamentos cujo nome contenha a string fornecida (case-insensitive)."""
    client = get_client()
    response = (
        client.table("medicamentos")
        .select("*")
        .ilike("nome", f"%{nome_parcial}%")
        .execute()
    )
    return response.data


def alertas_momento() -> list[dict]:
    """
    Retorna os medicamentos que devem ser tomados na hora atual
    (janela de ±10 minutos).
    """
    agora = datetime.now().strftime("%H:%M")
    todos = listar_medicamentos()

    def dentro_da_janela(horario: str) -> bool:
        try:
            h, m = map(int, horario.split(":"))
            ha, ma = map(int, agora.split(":"))
            diff = abs((h * 60 + m) - (ha * 60 + ma))
            return diff <= 10
        except ValueError:
            return False

    return [
        med for med in todos
        if any(dentro_da_janela(h) for h in med.get("horarios", []))
    ]


# --------------------------------------------------------------------------- #
#  CLI (interface de linha de comando — mantida para compatibilidade)           #
# --------------------------------------------------------------------------- #

def menu():
    print("\n==========================================")
    print("   💊 MedControl - Controle de Medicamentos")
    print("==========================================")
    print("  1. Cadastrar medicamento")
    print("  2. Listar medicamentos")
    print("  3. Remover medicamento")
    print("  4. Buscar medicamento")
    print("  5. Ver alertas do momento")
    print("  0. Sair")
    print("==========================================")


def cli():  # pragma: no cover
    while True:
        menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            nome = input("Nome do medicamento: ")
            dose = input("Dose (ex: 1 comprimido): ")
            horarios_raw = input("Horários separados por vírgula (ex: 08:00,20:00): ")
            horarios = [h.strip() for h in horarios_raw.split(",")]
            med = cadastrar_medicamento(nome, dose, horarios)
            print(f"✅ Medicamento cadastrado com ID {med['id']}.")

        elif opcao == "2":
            meds = listar_medicamentos()
            if not meds:
                print("Nenhum medicamento cadastrado.")
            for m in meds:
                print(f"[{m['id']}] {m['nome']} — {m['dose']} — {', '.join(m['horarios'])}")

        elif opcao == "3":
            med_id = int(input("ID do medicamento a remover: "))
            if remover_medicamento(med_id):
                print("✅ Medicamento removido.")
            else:
                print("❌ ID não encontrado.")

        elif opcao == "4":
            termo = input("Nome (ou parte do nome): ")
            resultados = buscar_medicamento(termo)
            if not resultados:
                print("Nenhum resultado encontrado.")
            for m in resultados:
                print(f"[{m['id']}] {m['nome']} — {m['dose']} — {', '.join(m['horarios'])}")

        elif opcao == "5":
            alertas = alertas_momento()
            if not alertas:
                print("Nenhum medicamento para tomar agora.")
            else:
                print("⚠️  Tome agora:")
                for m in alertas:
                    print(f"  💊 {m['nome']} — {m['dose']}")

        elif opcao == "0":
            print("Até logo!")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":  # pragma: no cover
    cli()