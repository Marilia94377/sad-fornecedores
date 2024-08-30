import streamlit as st
import pandas as pd

def main():
    st.sidebar.title("Seções")
    menu = ["Home", "Seleção de Serviço/Material", "Alternativas de Fornecedores"]
    choice = st.sidebar.selectbox("Escolha a seção", menu)

    if choice == "Home":
        st.title("Seleção de Fornecedores")
        st.write("O objetivo geral deste trabalho consiste em desenvolver um sistema de apoio a decisão (SAD) para a seleção de fornecedores dentro no âmbito da gestão de projetos considerando aspectos sustentáveis.")
    elif choice == "Seleção de Serviço/Material":
        st.title("Seleção de Serviço ou Material")
        st.write("Aqui você pode especificar o serviço ou material a ser adquirido.")
    
    elif choice == "Alternativas de Fornecedores":
        st.title("Alternativas de Fornecedores")
        st.write("Aqui você pode adicionar e gerenciar alternativas de fornecedores.")

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
    
        

if __name__ == "__main__":
    main()
