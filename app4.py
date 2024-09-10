import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Etapa 1: Estruturação do Problema e Definição dos Critérios
st.title("Aplicação do Modelo Proposto - Seleção de Fornecedores")
st.subheader("Estruturação do Problema")
st.write("""
O processo de seleção de fornecedores de serviços de terraplanagem envolve critérios econômicos, ambientais, sociais e gerais. 
Os critérios a serem considerados para esta seleção são definidos conforme o exemplo fornecido.
""")

# Exibindo a lista de critérios
criterios = {
    'C1': 'Preço/Custo do serviço',
    'C2': 'Qualidade',
    'C3': 'Entrega',
    'C4': 'Tecnologia',
    'C5': 'Custos ambientais',
    'C6': 'Projeto verde',
    'C7': 'Gestão ambiental',
    'C8': 'Partes interessadas (direito, atendimento)',
    'C9': 'Segurança e saúde no trabalho',
    'C10': 'Respeito pela política dos funcionários',
    'C11': 'Gestão social',
    'C12': 'Histórico de desempenho',
    'C13': 'Reputação'
}
st.write("### Critérios para seleção:")
for k, v in criterios.items():
    st.write(f"{k}: {v}")

# Etapa 2: Determinação dos Critérios Qualificadores e Atribuição de Pesos
st.subheader("Atribuição de Pesos aos Critérios")
st.write("""
A Tabela 27 da dissertação fornece os pesos atribuídos aos critérios, com base na importância relativa definida pelo decisor.
Esses pesos serão utilizados nos cálculos subsequentes.
""")

# Definindo os pesos dos critérios (conforme Tabela 27)
pesos = {
    'C1': 20.90, 'C2': 20.90, 'C3': 10.45, 'C4': 6.97, 'C5': 6.97, 'C6': 5.23, 
    'C7': 4.19, 'C8': 6.97, 'C9': 6.97, 'C10': 6.97, 'C11': 0, 'C12': 10.45, 'C13': 6.97
}

# Exibindo os pesos
st.write("### Pesos dos Critérios:")
df_pesos = pd.DataFrame(list(pesos.items()), columns=["Critério", "Peso"])
st.dataframe(df_pesos)

# Etapa 3: Geração da Matriz de Consequências (Tabela 25)
st.subheader("Matriz de Consequências")
st.write("""
A Matriz de Consequências avalia o desempenho de cada fornecedor (A, B, C, D) em relação aos critérios estabelecidos.
Os dados abaixo são baseados nos exemplos fornecidos na dissertação (Tabela 25).
""")

# Dados da Matriz de Consequências (Tabela 25)
data_consequencias = {
    'Alternativa': ['A', 'B', 'C', 'D'],
    'C1': [1501200.32, 1345622.58, 1450565.12, 1897264.56],
    'C2': [5, 2, 3, 5],
    'C3': [90, 120, 90, 85],
    'C4': [4, 1, 2, 4],
    'C5': [0, 1, 0, 0],
    'C6': [3, 1, 2, 2],
    'C7': [2, 3, 2, 4],
    'C8': [4, 3, 1, 1],
    'C9': [0, 2, 0, 1],
    'C10': [0, 0, 0, 0],
    'C11': [0, 0, 0, 0],
    'C12': [20, 12, 7, 25],
    'C13': [5, 3, 3, 5]
}

# Criando DataFrame
df_consequencias = pd.DataFrame(data_consequencias)
st.write("### Matriz de Consequências:")
st.dataframe(df_consequencias)

# Etapa 4: Cálculo das Funções de Preferência (Tabela 26)
st.subheader("Funções de Preferência dos Critérios")
st.write("""
As funções de preferência definem como a diferença entre as alternativas será avaliada para cada critério.
A Tabela 26 abaixo descreve as funções utilizadas para cada critério.
""")

# Funções de preferência (Tabela 26)
funcoes_preferencia = {
    'Critério': ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C12', 'C13'],
    'Função': ['Área de indiferença (Tipo 5)', 'Critério usual (Tipo 1)', 'Área de indiferença (Tipo 5)', 
               'Critério usual (Tipo 1)', 'Critério usual (Tipo 1)', 'Critério usual (Tipo 1)',
               'Critério usual (Tipo 1)', 'Critério usual (Tipo 1)', 'Critério usual (Tipo 1)',
               'Critério usual (Tipo 1)', 'Critério usual (Tipo 1)'],
    'q': [90000, '-', 15, '-', '-', '-', '-', '-', '-', '-', '-'],
    'p': [100000, '-', 25, '-', '-', '-', '-', '-', '-', '-', '-']
}

df_funcoes_preferencia = pd.DataFrame(funcoes_preferencia)
st.write("### Funções de Preferência:")
st.dataframe(df_funcoes_preferencia)

# Etapa 5: Ordenação e Atribuição dos Pesos (Tabela 27 já implementada acima)

# Etapa 6: Cálculo dos Fluxos (PROMETHEE II)
st.subheader("Cálculo dos Fluxos (PROMETHEE II)")
st.write("""
Usando o método PROMETHEE II, calculamos os fluxos positivos, negativos e líquidos para cada fornecedor.
""")

# Dados calculados dos fluxos (Tabela 28)
fluxos = {
    'Fornecedor': ['Fornecedor 1', 'Fornecedor 4', 'Fornecedor 3', 'Fornecedor 2'],
    'Fluxo Positivo (ϕ+)': [0.5622, 0.5215, 0.2207, 0.2439],
    'Fluxo Negativo (ϕ-)': [0.1219, 0.2555, 0.5157, 0.6551],
    'Fluxo Líquido (ϕ)': [0.4402, 0.2660, -0.2950, -0.4112]
}

# Criar DataFrame
df_fluxos = pd.DataFrame(fluxos)

# Exibir tabela de fluxos
st.write("### Fluxos Positivos, Negativos e Líquidos:")
st.dataframe(df_fluxos)

# Gráfico interativo dos fluxos líquidos
fig = px.bar(df_fluxos, x='Fornecedor', y='Fluxo Líquido (ϕ)', title="Fluxo Líquido dos Fornecedores")
st.plotly_chart(fig)

