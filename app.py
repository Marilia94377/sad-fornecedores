import streamlit as st
import pandas as pd

def main():
    st.sidebar.title("Navegação")
    menu = ["Home", "Seleção de Serviço/Material", "Alternativas de Fornecedores", "Critérios de Avaliação"]
    choice = st.sidebar.selectbox("Escolha a seção", menu)

    if choice == "Home":
        st.title("Seleção de Fornecedores")
        st.write("Bem-vindo ao sistema de seleção de fornecedores.")
    
    elif choice == "Seleção de Serviço/Material":
        st.title("Seleção de Serviço ou Material")
        st.write("Aqui você pode especificar o serviço ou material a ser adquirido.")
    
    elif choice == "Alternativas de Fornecedores":
        st.title("Alternativas de Fornecedores")

        # Inicializar lista de fornecedores
        if 'fornecedores' not in st.session_state:
            st.session_state.fornecedores = []

        # Formulário para adicionar fornecedores
        with st.form(key='fornecedor_form'):
            nome = st.text_input("Nome do Fornecedor")
            historico = st.text_area("Histórico do Fornecedor")
            localizacao = st.text_input("Localização")
            submit_button = st.form_submit_button(label="Adicionar Fornecedor")

            if submit_button:
                fornecedor = {"Nome": nome, "Histórico": historico, "Localização": localizacao}
                st.session_state.fornecedores.append(fornecedor)
                st.success("Fornecedor adicionado com sucesso!")

        # Exibir a lista de fornecedores
        if st.session_state.fornecedores:
            st.subheader("Lista de Fornecedores")
            df_fornecedores = pd.DataFrame(st.session_state.fornecedores)
            st.dataframe(df_fornecedores)

            # Opções para editar e remover
            for i, fornecedor in enumerate(st.session_state.fornecedores):
                if st.button(f"Remover {fornecedor['Nome']}", key=f"remove_{i}"):
                    st.session_state.fornecedores.pop(i)
                    st.experimental_rerun()

        else:
            st.write("Nenhum fornecedor adicionado ainda.")
    
    elif choice == "Critérios de Avaliação":
        st.title("Critérios de Avaliação")

        # Inicializar lista de critérios
        if 'criterios' not in st.session_state:
            st.session_state.criterios = []

        # Formulário para adicionar critérios
        with st.form(key='criterio_form'):
            criterio = st.text_input("Nome do Critério")
            peso = st.slider("Peso do Critério (0 a 5)", 0, 5, 3)
            tipo = st.selectbox("Tipo de Critério", ["Qualitativo", "Quantitativo"])
            submit_button = st.form_submit_button(label="Adicionar Critério")

            if submit_button:
                novo_criterio = {"Critério": criterio, "Peso": peso, "Tipo": tipo}
                st.session_state.criterios.append(novo_criterio)
                st.success("Critério adicionado com sucesso!")

        # Exibir a lista de critérios
        if st.session_state.criterios:
            st.subheader("Lista de Critérios")
            df_criterios = pd.DataFrame(st.session_state.criterios)
            st.dataframe(df_criterios)
        else:
            st.write("Nenhum critério adicionado ainda.")

if __name__ == "__main__":
    main()
