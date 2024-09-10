import pandas as pd

# Dados de fornecedores com critérios: Econômico, Ambiental e Social
data = {
    'Fornecedor': ['D1', 'D2', 'D3', 'D4', 'D5'],
    'Econômico': [6, 9, 8, 7, 1],
    'Ambiental': [7, 8, 2, 8, 10],
    'Social': [10, 9, 8, 5, 10]
}

# Pesos para os critérios
pesos = {
    'Econômico': 0.4,
    'Ambiental': 0.3,
    'Social': 0.3
}

# Criando o DataFrame
df = pd.DataFrame(data)
print(df)

# Função para calcular o fluxo líquido (simplificado)
def calcular_fluxo(df, pesos):
    fluxos_positivos = []
    fluxos_negativos = []
    
    # Iterar sobre cada fornecedor
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
    
    # Adicionando fluxos ao DataFrame
    df['Fluxo Positivo'] = fluxos_positivos
    df['Fluxo Negativo'] = fluxos_negativos
    df['Fluxo Líquido'] = df['Fluxo Positivo'] - df['Fluxo Negativo']
    
    return df

# Aplicar a função no DataFrame
df_resultado = calcular_fluxo(df, pesos)
print(df_resultado)

import streamlit as st

# Interface para ajustar os pesos
st.title("Seleção de Fornecedores Sustentáveis")
st.write("Ajuste os pesos para os critérios e veja a classificação dos fornecedores.")

# Entrada de pesos pelos usuários
pesos['Econômico'] = st.slider("Peso para Critério Econômico", 0.0, 1.0, 0.4)
pesos['Ambiental'] = st.slider("Peso para Critério Ambiental", 0.0, 1.0, 0.3)
pesos['Social'] = st.slider("Peso para Critério Social", 0.0, 1.0, 0.3)

# Calcular os fluxos com os pesos atualizados
df_resultado = calcular_fluxo(df, pesos)

# Exibir resultados
st.write("### Resultados:")
st.dataframe(df_resultado)

