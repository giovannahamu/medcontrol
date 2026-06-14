"""
MedControl — Interface Web com Streamlit
Etapa 3: dados persistidos no Supabase
"""

import streamlit as st
from src.medicamentos import (
    cadastrar_medicamento,
    listar_medicamentos,
    remover_medicamento,
    buscar_medicamento,
    alertas_momento,
)

st.set_page_config(page_title="MedControl", page_icon="💊", layout="centered")

st.title("💊 MedControl")
st.caption("Controle de Medicamentos para Idosos — dados salvos na nuvem")

aba = st.tabs(["🏠 Início", "➕ Cadastrar", "🔍 Buscar", "🗑️ Remover"])

# --- ABA INÍCIO ---
with aba[0]:
    st.subheader("Medicamentos Cadastrados")
    alertas = alertas_momento()
    if alertas:
        st.warning(f"⚠️ {len(alertas)} medicamento(s) para tomar AGORA!")
        for m in alertas:
            st.error(f"💊 **{m['nome']}** — {m['dose']}")
        st.divider()

    meds = listar_medicamentos()
    if not meds:
        st.info("Nenhum medicamento cadastrado ainda.")
    else:
        for m in meds:
            st.markdown(
                f"**[{m['id']}] {m['nome']}** — {m['dose']}  \n"
                f"🕐 Horários: {', '.join(m['horarios'])}"
            )
            st.divider()

# --- ABA CADASTRAR ---
with aba[1]:
    st.subheader("Cadastrar Novo Medicamento")
    with st.form("form_cadastrar"):
        nome = st.text_input("Nome do medicamento")
        dose = st.text_input("Dose (ex: 1 comprimido)")
        horarios_raw = st.text_input("Horários separados por vírgula (ex: 08:00,20:00)")
        submitted = st.form_submit_button("Cadastrar")

    if submitted:
        if nome and dose and horarios_raw:
            horarios = [h.strip() for h in horarios_raw.split(",")]
            med = cadastrar_medicamento(nome, dose, horarios)
            st.success(f"✅ **{med['nome']}** cadastrado com ID {med['id']}!")
        else:
            st.error("Preencha todos os campos.")

# --- ABA BUSCAR ---
with aba[2]:
    st.subheader("Buscar Medicamento")
    termo = st.text_input("Digite o nome (ou parte do nome)")
    if termo:
        resultados = buscar_medicamento(termo)
        if resultados:
            for m in resultados:
                st.markdown(
                    f"**[{m['id']}] {m['nome']}** — {m['dose']}  \n"
                    f"🕐 {', '.join(m['horarios'])}"
                )
        else:
            st.warning("Nenhum resultado encontrado.")

# --- ABA REMOVER ---
with aba[3]:
    st.subheader("Remover Medicamento")
    med_id = st.number_input("ID do medicamento", min_value=1, step=1)
    if st.button("Remover"):
        if remover_medicamento(int(med_id)):
            st.success(f"✅ Medicamento ID {int(med_id)} removido.")
        else:
            st.error(f"❌ ID {int(med_id)} não encontrado.")