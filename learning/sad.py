import streamlit as st
import pandas as pd
import numpy as np

# Função para normalizar a matriz de decisão
def normalize_matrix(matrix, criteria_types):
    min_criteria_array = matrix.min(axis=0)
    max_criteria_array = matrix.max(axis=0)
    
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if criteria_types[j] == 'Minimização':
                matrix[i][j] = (max_criteria_array[j] - matrix[i][j]) / (max_criteria_array[j] - min_criteria_array[j])
            else:
                matrix[i][j] = (matrix[i][j] - min_criteria_array[j]) / (max_criteria_array[j] - min_criteria_array[j])
    
    return matrix

# Função para calcular a matriz de preferências
def calculate_preference_matrix(matrix, weights):
    num_alternatives = len(matrix)
    preference_matrix = np.zeros((num_alternatives, num_alternatives))
    
    for i in range(num_alternatives):
        for j in range(num_alternatives):
            if i != j:
                preference_sum = 0
                for k in range(len(matrix[i])):
                    preference_sum += weights[k] * (matrix[i][k] - matrix[j][k])
                preference_matrix[i, j] = preference_sum
    
    return preference_matrix

# Função para calcular os fluxos de entrada, saída e líquido
def calculate_flows(preference_matrix):
    positive_flow = np.mean(preference_matrix, axis=1)
    negative_flow = np.mean(preference_matrix, axis=0)
    net_flow = positive_flow - negative_flow
    
    return positive_flow, negative_flow, net_flow

# Função para carregar os dados
def load_data(uploaded_file):
    return pd.read_csv(uploaded_file)

st.title("Sistema de Apoio à Decisão (SAD) - Seleção de Fornecedores")

# Upload dos arquivos de dados
st.header("Carregamento dos Dados")
uploaded_decision_file = st.file_uploader("Escolha um arquivo CSV para a Matriz de Decisão", type="csv")
uploaded_weights_file = st.file_uploader("Escolha um arquivo CSV para os Pesos dos Critérios", type="csv")

if uploaded_decision_file is not None and uploaded_weights_file is not None:
    # Carregar dados
    decision_matrix = load_data(uploaded_decision_file)
    weights = load_data(uploaded_weights_file).values[0]
    
    st.write("Matriz de Decisão Carregada:")
    st.write(decision_matrix)
    
    st.write("Pesos dos Critérios Carregados:")
    st.write(weights)
    
    # Seleção dos tipos de critério (Maximização/Minimização)
    criteria = decision_matrix.columns[1:]
    criteria_types = []
    for criterion in criteria:
        criteria_types.append(st.selectbox(f"Tipo de Otimização para {criterion}", ['Maximização', 'Minimização']))
    
    # Normalização dos dados
    st.header("Normalização dos Dados")
    alternatives = decision_matrix.iloc[:, 0]
    matrix = decision_matrix.iloc[:, 1:].values
    normalized_matrix = normalize_matrix(matrix.copy(), criteria_types)
    
    normalized_df = pd.DataFrame(normalized_matrix, columns=criteria)
    normalized_df.insert(0, 'Alternativa', alternatives)
    st.write("Matriz Normalizada:")
    st.write(normalized_df)
    
    # Calcular a matriz de preferências
    st.header("Matriz de Preferências")
    preference_matrix = calculate_preference_matrix(normalized_matrix, weights)
    
    st.write("Matriz de Preferências:")
    st.write(preference_matrix)
    
    # Calcular os fluxos de entrada, saída e líquido
    st.header("Fluxos de Entrada, Saída e Líquido")
    positive_flow, negative_flow, net_flow = calculate_flows(preference_matrix)
    
    st.write("Fluxo de Saída (φ+):")
    st.write(positive_flow)
    
    st.write("Fluxo de Entrada (φ-):")
    st.write(negative_flow)
    
    st.write("Fluxo Líquido (φ):")
    st.write(net_flow)
    
    # Ranking final
    st.header("Ranking Final")
    ranking = pd.DataFrame({'Fornecedor': alternatives, 'Fluxo Líquido': net_flow})
    ranking = ranking.sort_values(by='Fluxo Líquido', ascending=False)
    
    st.write("Ranking:")
    st.write(ranking)
    