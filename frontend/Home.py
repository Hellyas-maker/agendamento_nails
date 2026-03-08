import streamlit as st

st.set_page_config(
    page_title="Aline Nails Studio",
    page_icon="💅",
    layout="wide"
)

# CSS PERSONALIZADO
st.markdown("""
<style>

.main {
    background-color: #fff5f7;
}

h1 {
    text-align: center;
    color: #e75480;
}

h2 {
    text-align: center;
}

.stButton>button {
    background-color: #e75480;
    color: white;
    border-radius: 10px;
    height: 50px;
    width: 200px;
    font-size: 18px;
}

</style>
""", unsafe_allow_html=True)

# LOGO
col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.image("assets/logo.png", width=450)


st.markdown("### Beleza, cuidado e autoestima em cada detalhe",)

st.write("")

# COLUNAS PARA LAYOUT
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("💅 Manicure")
    st.write("Cuidado completo para suas unhas.")

with col2:
    st.subheader("✨ Pedicure")
    st.write("Pés lindos e bem cuidados.")

with col3:
    st.subheader("💎 Alongamento")
    st.write("Unhas em gel e fibra.")

st.write("")
st.write("")

# SEÇÃO DE AGENDAMENTO

ag = st.markdown("### 📅 Agende seu horário online")

st.page_link("pages/1_Agendamentos.py", label="💅 Agendar Horário",)
    

st.write("")
st.write("")

# RODAPÉ
st.markdown("---")
st.markdown(
"""
<center>
📍 Atendimento com hora marcada  
💖 Obrigado por escolher Aline Nails
</center>
""",
unsafe_allow_html=True
)