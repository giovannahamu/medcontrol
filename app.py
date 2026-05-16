import streamlit as st
from src.viacep import buscar_endereco, formatar_endereco
from src.medicamentos import (
    adicionar_medicamento,
    listar_medicamentos,
    remover_medicamento,
    buscar_medicamento,
    verificar_horario_agora,
)

st.set_page_config(page_title="MedControl", page_icon="💊")
st.title("💊 MedControl - Controle de Medicamentos")

menu = st.sidebar.selectbox("Menu", [
    "Cadastrar Medicamento",
    "Listar Medicamentos",
    "Buscar Medicamento",
    "Alertas do Momento",
    "Consultar CEP de Farmácia",
])

if menu == "Cadastrar Medicamento":
    st.header("Cadastrar Medicamento")
    nome = st.text_input("Nome do medicamento")
    dose = st.text_input("Dose (ex: 1 comprimido)")
    horarios_str = st.text_input("Horários (ex: 08:00,20:00)")
    cep = st.text_input("CEP da farmácia (opcional)")

    if st.button("Cadastrar"):
        horarios = [h.strip() for h in horarios_str.split(",") if h.strip()]
        farmacia_cep = ""
        farmacia_endereco = ""
        if cep:
            dados = buscar_endereco(cep)
            if not dados.get("erro"):
                farmacia_cep = dados["cep"]
                farmacia_endereco = formatar_endereco(dados)
                st.success(f"📍 Endereço: {farmacia_endereco}")
            else:
                st.warning(dados["erro"])
        try:
            med = adicionar_medicamento(
                nome, horarios, dose, farmacia_cep, farmacia_endereco
            )
            st.success(f"✅ '{med['nome']}' cadastrado! (ID: {med['id']})")
        except ValueError as e:
            st.error(str(e))

elif menu == "Listar Medicamentos":
    st.header("Medicamentos Cadastrados")
    meds = listar_medicamentos()
    if not meds:
        st.info("Nenhum medicamento cadastrado.")
    for m in meds:
        with st.expander(f"💊 {m['nome']} (ID: {m['id']})"):
            st.write(f"**Dose:** {m['dose']}")
            st.write(f"**Horários:** {', '.join(m['horarios'])}")
            if m.get("farmacia_endereco"):
                st.write(f"**Farmácia:** {m['farmacia_endereco']}")
            st.write(f"**Cadastrado em:** {m['criado_em']}")

elif menu == "Buscar Medicamento":
    st.header("Buscar Medicamento")
    nome = st.text_input("Nome (ou parte do nome)")
    if st.button("Buscar"):
        resultados = buscar_medicamento(nome)
        if not resultados:
            st.warning("Nenhum medicamento encontrado.")
        for m in resultados:
            st.write(f"**{m['nome']}** — {m['dose']} | {', '.join(m['horarios'])}")

elif menu == "Alertas do Momento":
    st.header("⚠️ Alertas do Momento")
    meds = verificar_horario_agora()
    if not meds:
        st.success("Nenhum medicamento programado para agora.")
    for m in meds:
        st.warning(f"💊 {m['nome']} - {m['dose']}")

elif menu == "Consultar CEP de Farmácia":
    st.header("Consultar CEP de Farmácia")
    cep = st.text_input("Digite o CEP")
    if st.button("Consultar"):
        dados = buscar_endereco(cep)
        if dados.get("erro"):
            st.error(dados["erro"])
        else:
            st.success(f"📍 {formatar_endereco(dados)}")