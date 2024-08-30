import streamlit as st
import pandas as pd
import numpy as np

st.title("Sistema de Apoio à Decisão (SAD) - Seleção de Fornecedores")

# Passo 1: Inserção de dados
st.header("Inserção de Dados")

# Upload do arquivo de dados
uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Dados carregados:")
    st.write(df)
    
    # Definição dos pesos e critérios
    st.header("Definição dos Pesos e Critérios")
    criteria = df.columns[1:]  # Excluindo a coluna de alternativas
    weights = {}
    optimization = {}

    for criterion in criteria:
        weights[criterion] = st.slider(f"Peso para {criterion}", 0.0, 1.0, 0.1)
        optimization[criterion] = st.selectbox(f"Otimização para {criterion}", ['Maximização', 'Minimização'])

    # Normalização dos dados
    st.header("Normalização dos Dados")
    normalized_df = df.copy()
    for criterion in criteria:
        if optimization[criterion] == 'Maximização':
            normalized_df[criterion] = (df[criterion] - df[criterion].min()) / (df[criterion].max() - df[criterion].min())
        else:
            normalized_df[criterion] = (df[criterion].max() - df[criterion]) / (df[criterion].max() - df[criterion].min())
    
    st.write("Dados normalizados:")
    st.write(normalized_df)
    
    # Matriz de preferências
    st.header("Matriz de Preferências")
    num_alternatives = len(df)
    preference_matrix = np.zeros((num_alternatives, num_alternatives))
    
    for i in range(num_alternatives):
        for j in range(num_alternatives):
            if i != j:
                preference_sum = 0
                for criterion in criteria:
                    preference_sum += weights[criterion] * (normalized_df.loc[i, criterion] - normalized_df.loc[j, criterion])
                preference_matrix[i, j] = preference_sum

    st.write("Matriz de Preferências:")
    st.write(preference_matrix)
    
    # Fluxos de entrada e saída
    st.header("Fluxos de Entrada e Saída")
    positive_flow = np.mean(preference_matrix, axis=1)
    negative_flow = np.mean(preference_matrix, axis=0)
    
    st.write("Fluxo de Saída (φ+):")
    st.write(positive_flow)
    
    st.write("Fluxo de Entrada (φ-):")
    st.write(negative_flow)
    
    # Fluxo líquido
    st.header("Fluxo Líquido")
    net_flow = positive_flow - negative_flow
    
    st.write("Fluxo Líquido (φ):")
    st.write(net_flow)
    
    # Ranking final
    st.header("Ranking Final")
    ranking = pd.DataFrame({'Fornecedor': df.iloc[:, 0], 'Fluxo Líquido': net_flow})
    ranking = ranking.sort_values(by='Fluxo Líquido', ascending=False)
    
    st.write("Ranking:")
    st.write(ranking)
