import streamlit as st
import pandas as pd
import plotly.express as px

# Etapa 1: Estruturação do Problema e Definição dos Critérios
st.title("Aplicação do Modelo Proposto - Seleção de Fornecedores")
st.subheader("Estruturação do Problema")

st.write("""
O processo de seleção de fornecedores de serviços de terraplanagem envolve critérios econômicos, ambientais, sociais e gerais. 
Por favor, selecione os critérios que você deseja considerar e os fornecedores que serão avaliados.
""")

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

st.write("### Selecione os critérios que você deseja incluir na avaliação:")
criterios_selecionados = st.multiselect(
    "Critérios disponíveis", list(criterios.values()), default=list(criterios.values())
)

# Etapa 2: Seleção de Fornecedores
st.write("### Selecione os fornecedores que você deseja avaliar:")
fornecedores_disponiveis = ['Fornecedor A', 'Fornecedor B', 'Fornecedor C', 'Fornecedor D']
fornecedores_selecionados = st.multiselect(
    "Fornecedores disponíveis", fornecedores_disponiveis, default=fornecedores_disponiveis
)

# Etapa 3: Atribuição de Pesos aos Critérios (ajustando para refletir os valores reais)
st.subheader("Atribuição de Pesos aos Critérios")
st.write("""
Atribua os pesos de importância relativa para cada critério selecionado com base nos valores da Tabela 27. O peso padrão é 10.
""")

pesos = {}
for criterio in criterios_selecionados:
    # Ajuste da faixa de 0 a 25 para refletir os valores reais
    pesos[criterio] = st.slider(f"Peso para o critério {criterio}", 0.0, 25.0, 10.0)

# Etapa 4: Entrada de Desempenho dos Fornecedores
st.subheader("Desempenho dos Fornecedores em cada Critério")
st.write("""
Insira o desempenho de cada fornecedor em relação aos critérios selecionados. 
Os valores podem variar de acordo com o critério e a escala apropriada para cada um (por exemplo, preço em reais, qualidade de 1 a 5, etc.).
""")

# Criar dicionário para armazenar as entradas de desempenho
desempenho_fornecedores = {}
for fornecedor in fornecedores_selecionados:
    st.write(f"### Desempenho para {fornecedor}")
    desempenho_fornecedores[fornecedor] = {}
    for criterio in criterios_selecionados:
        desempenho_fornecedores[fornecedor][criterio] = st.number_input(
            f"Desempenho de {fornecedor} no critério {criterio}",
            min_value=0, max_value=1000000 if criterio == 'Preço/Custo do serviço' else 100,
            value=50
        )

st.write("### Desempenho dos Fornecedores:")
df_desempenho = pd.DataFrame(desempenho_fornecedores)
st.dataframe(df_desempenho)

# Etapa 5: Cálculo dos Fluxos Positivos, Negativos e Líquidos (PROMETHEE II)
st.subheader("Cálculo dos Fluxos (PROMETHEE II)")

# Função para calcular os fluxos (simplificação do PROMETHEE II)
def calcular_fluxos(df, pesos):
    fluxos_positivos = {}
    fluxos_negativos = {}
    for fornecedor in df.columns:
        fluxo_positivo = 0
        fluxo_negativo = 0
        for outro_fornecedor in df.columns:
            if fornecedor != outro_fornecedor:
                for criterio in df.index:
                    if df[fornecedor][criterio] > df[outro_fornecedor][criterio]:
                        fluxo_positivo += pesos[criterio]
                    else:
                        fluxo_negativo += pesos[criterio]
        fluxos_positivos[fornecedor] = fluxo_positivo
        fluxos_negativos[fornecedor] = fluxo_negativo
    return fluxos_positivos, fluxos_negativos

# Calcular os fluxos
fluxos_positivos, fluxos_negativos = calcular_fluxos(df_desempenho, pesos)

# Calcular os fluxos líquidos
fluxos_liquidos = {fornecedor: fluxos_positivos[fornecedor] - fluxos_negativos[fornecedor] for fornecedor in fornecedores_selecionados}

# Exibir os fluxos calculados
df_fluxos = pd.DataFrame({
    'Fornecedor': fornecedores_selecionados,
    'Fluxo Positivo (ϕ+)': [fluxos_positivos[fornecedor] for fornecedor in fornecedores_selecionados],
    'Fluxo Negativo (ϕ-)': [fluxos_negativos[fornecedor] for fornecedor in fornecedores_selecionados],
    'Fluxo Líquido (ϕ)': [fluxos_liquidos[fornecedor] for fornecedor in fornecedores_selecionados]
})
st.write("### Resultados dos Fluxos:")
st.dataframe(df_fluxos)

# Gráfico interativo dos fluxos líquidos
fig = px.bar(df_fluxos, x='Fornecedor', y='Fluxo Líquido (ϕ)', title="Fluxo Líquido dos Fornecedores")
st.plotly_chart(fig)
