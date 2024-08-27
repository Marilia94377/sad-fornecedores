import streamlit as st
import pandas as pd

def main():
    st.title('Teste de Upload de CSV')
    st.write("Se você está vendo isso, Streamlit está funcionando corretamente.")

    # uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")

    # if uploaded_file is not None:
    #     df = pd.read_csv(uploaded_file)
    #     st.write("Arquivo CSV carregado com sucesso.")
    #     st.dataframe(df)
    # else:
    #     st.write("Por favor, carregue um arquivo CSV.")

    df = pd.DataFrame(
        [
            {"command": "st.selectbox", "rating": 4, "is_widget": True},
            {"command": "st.balloons", "rating": 5, "is_widget": False},
            {"command": "st.time_input", "rating": 3, "is_widget": True},
        ]
    )

    st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()
