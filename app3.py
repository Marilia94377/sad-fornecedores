import streamlit as st
import pandas as pd
import plotly.express as px

# Dados dos fornecedores
data = {
    'Fornecedor': ['D1', 'D2', 'D3', 'D4', 'D5'],
    'Econômico': [6, 9, 8, 7, 1],
    'Ambiental': [7, 8, 2, 8, 10],
    'Social': [10, 9, 8, 5, 10]
}

# Criar o DataFrame
df = pd.DataFrame(data)

# Interface do Usuário para Seleção de Critérios e Fornecedores
st.title("Sistema de Seleção de Fornecedores Sustentáveis")

st.write("Selecione os critérios que você deseja considerar na avaliação:")
criterios_selecionados = st.multiselect(
    "Critérios disponíveis",
    options=["Econômico", "Ambiental", "Social"],
    default=["Econômico", "Ambiental", "Social"]
)

st.write("Selecione os fornecedores que você deseja avaliar:")
fornecedores_selecionados = st.multiselect(
    "Fornecedores disponíveis",
    options=df['Fornecedor'].tolist(),
    default=df['Fornecedor'].tolist()
)

# Ajuste de pesos para os critérios selecionados
pesos = {}
for criterio in criterios_selecionados:
    pesos[criterio] = st.slider(f"Peso para o critério {criterio}", 0.0, 1.0, 0.3)

# Filtrar o DataFrame com base nas seleções do usuário
df_filtrado = df[df['Fornecedor'].isin(fornecedores_selecionados)][['Fornecedor'] + criterios_selecionados]

# Função para calcular o fluxo líquido (simplificado)
def calcular_fluxo(df, pesos):
    fluxos_positivos = []
    fluxos_negativos = []
    
    for index, row in df.iterrows():
        fluxo_positivo = 0
        fluxo_negativo = 0
        
        # Comparar com outros fornecedores
        for i, other_row in df.iterrows():
            if index != i:
                for crit in pesos.keys():
                    if row[crit] > other_row[crit]:
                        fluxo_positivo += pesos[crit]
                    else:
                        fluxo_negativo += pesos[crit]
        
        fluxos_positivos.append(fluxo_positivo)
        fluxos_negativos.append(fluxo_negativo)
    
    # Adicionar fluxos ao DataFrame
    df['Fluxo Positivo'] = fluxos_positivos
    df['Fluxo Negativo'] = fluxos_negativos
    df['Fluxo Líquido'] = df['Fluxo Positivo'] - df['Fluxo Negativo']
    
    return df

# Calcular fluxos para o DataFrame filtrado
df_resultado = calcular_fluxo(df_filtrado, pesos)

# Exibir os resultados
st.write("### Resultados:")
st.dataframe(df_resultado)

# Gráfico interativo dos fluxos líquidos
fig = px.bar(df_resultado, x='Fornecedor', y='Fluxo Líquido', title="Fluxo Líquido dos Fornecedores")
st.plotly_chart(fig)

with st.form("Formulário de Seleção"):
    criterios_selecionados = st.multiselect("Critérios disponíveis", ["Econômico", "Ambiental", "Social"], default=["Econômico"])
    fornecedores_selecionados = st.multiselect("Fornecedores disponíveis", df['Fornecedor'].tolist(), default=df['Fornecedor'].tolist())
    pesos = {}
    for criterio in criterios_selecionados:
        pesos[criterio] = st.slider(f"Peso para o critério {criterio}", 0.0, 1.0, 0.3)

    # Botão para submeter
    submit_button = st.form_submit_button("Gerar Resultados")

if submit_button:
    # Calcular os fluxos e gerar os resultados
    df_filtrado = df[df['Fornecedor'].isin(fornecedores_selecionados)][['Fornecedor'] + criterios_selecionados]
    df_resultado = calcular_fluxo(df_filtrado, pesos)
    
    # Exibir os resultados
    st.write("### Resultados:")
    st.dataframe(df_resultado)

    # Gráfico interativo
    fig = px.bar(df_resultado, x='Fornecedor', y='Fluxo Líquido', title="Fluxo Líquido dos Fornecedores")
    st.plotly_chart(fig)
