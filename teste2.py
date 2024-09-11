import streamlit as st
import pandas as pd
import plotly.express as px
import math

# Etapa 1: Estruturação do Problema e Definição dos Critérios e Fornecedores
st.title("Aplicação do Modelo Proposto - PROMETHEE II")
st.subheader("Configurações do Modelo de Decisão")

st.write("""
Selecione os critérios e fornecedores a serem usados na avaliação, atribua pesos, defina se os critérios devem ser maximizados ou minimizados e selecione a função de preferência para cada critério.
""")

# Lista de fornecedores disponíveis
fornecedores_disponiveis = ['Fornecedor A', 'Fornecedor B', 'Fornecedor C', 'Fornecedor D', 'Fornecedor E', 'Fornecedor F']

# Lista de critérios disponíveis
criterios_disponiveis = ['C1 - Preço/Custo do serviço', 'C2 - Qualidade', 'C3 - Entrega', 'C4 - Tecnologia', 
                         'C5 - Custos ambientais', 'C6 - Projeto verde', 'C7 - Gestão ambiental', 
                         'C8 - Partes interessadas (direito, atendimento)', 'C9 - Segurança e saúde no trabalho', 
                         'C10 - Respeito pela política dos funcionários', 'C11 - Gestão social', 
                         'C12 - Histórico de desempenho', 'C13 - Reputação']

# Selecione fornecedores
fornecedores_selecionados = st.multiselect("Selecione os fornecedores que serão avaliados", fornecedores_disponiveis, default=fornecedores_disponiveis[:4])

# Selecione critérios
criterios_selecionados = st.multiselect("Selecione os critérios que serão usados", criterios_disponiveis, default=criterios_disponiveis)

# Etapa 2: Atribuição de Pesos, Maximização/Minimização e Funções de Preferência
st.subheader("Atribuição de Pesos, Maximização/Minimização e Funções de Preferência")

pesos = {}
max_min_criterios = {}
funcoes_preferencia = {}
parametros_preferencia = {}

for criterio in criterios_selecionados:
    st.write(f"### Critério: {criterio}")
    
    # Pesos
    pesos[criterio] = st.number_input(f"Peso para {criterio} (0 a 100)", min_value=0.0, max_value=100.0, value=50.0)
    
    # Maximização ou Minimização
    max_min_criterios[criterio] = st.selectbox(f"O critério {criterio} deve ser:", 
                                               ['Maximizado', 'Minimizado'], key=f"max_min_{criterio}")
    
    # Função de preferência
    funcao = st.selectbox(f"Função de preferência para {criterio}", 
                          ['Linear', 'U-Shape', 'V-Shape', 'Level', 'V-Shape I', 'Gaussian'], key=f"pref_{criterio}")
    funcoes_preferencia[criterio] = funcao
    
    # Parâmetros para as funções, se aplicável
    if funcao in ['U-Shape', 'V-Shape', 'Level', 'V-Shape I']:
        parametros_preferencia[criterio] = {
            'q': st.number_input(f"Limiar de indiferença (q) para {criterio}", min_value=0.0, max_value=100.0, value=10.0),
            'r': st.number_input(f"Limiar de preferência (r) para {criterio}", min_value=0.0, max_value=100.0, value=20.0)
        }
    elif funcao == 'Gaussian':
        parametros_preferencia[criterio] = {
            's': st.number_input(f"Parâmetro s para função Gaussian para {criterio}", min_value=0.1, max_value=10.0, value=1.0)
        }

# Etapa 3: Inserção de Desempenho para cada Fornecedor e Critério (Escala de 1 a 5)
st.subheader("Desempenho dos Fornecedores em cada Critério (Escala de 1 a 5)")

desempenho_fornecedores = {}
for fornecedor in fornecedores_selecionados:
    st.write(f"### Desempenho para {fornecedor}")
    desempenho_fornecedores[fornecedor] = {}
    for criterio in criterios_selecionados:
        desempenho_fornecedores[fornecedor][criterio] = st.slider(
            f"Desempenho de {fornecedor} no critério {criterio} (1 a 5)", 1, 5, 3
        )

# Transformar os dados de desempenho em um DataFrame
df_desempenho = pd.DataFrame(desempenho_fornecedores).T
st.write("### Desempenho dos Fornecedores:")
st.dataframe(df_desempenho)

# Etapa 4: Normalização
st.subheader("Normalização dos Valores")

def normalizar(df, max_min_criterios):
    df_normalizado = pd.DataFrame()
    for criterio in df.columns:
        max_valor = df[criterio].max()
        min_valor = df[criterio].min()
        if max_min_criterios[criterio] == 'Maximizado':
            df_normalizado[criterio] = (df[criterio] - min_valor) / (max_valor - min_valor)
        else:
            df_normalizado[criterio] = (max_valor - df[criterio]) / (max_valor - min_valor)
    return df_normalizado

df_normalizado = normalizar(df_desempenho, max_min_criterios)
st.write("### Matriz de Consequência Normalizada:")
st.dataframe(df_normalizado)

# Função para aplicar função de preferência
def aplicar_funcao_preferencia(funcao, diferenca, parametros):
    if funcao == 'Linear':
        return 1 if diferenca > 0 else 0
    elif funcao == 'U-Shape':
        return 1 if diferenca > parametros['q'] else 0
    elif funcao == 'V-Shape':
        return min(diferenca / parametros['r'], 1)
    elif funcao == 'Level':
        if diferenca <= parametros['q']:
            return 0
        elif parametros['q'] < diferenca <= parametros['r']:
            return 0.5
        else:
            return 1
    elif funcao == 'V-Shape I':
        if diferenca <= parametros['q']:
            return 0
        elif parametros['q'] < diferenca <= parametros['r']:
            return (diferenca - parametros['q']) / (parametros['r'] - parametros['q'])
        else:
            return 1
    elif funcao == 'Gaussian':
        return 1 - math.exp(-(diferenca ** 2) / (2 * parametros['s'] ** 2))

# Etapa 5: Cálculo dos Fluxos Positivos, Negativos e Líquidos
st.subheader("Cálculo dos Fluxos (PROMETHEE II)")

def calcular_fluxos(df, pesos, funcoes_preferencia, parametros_preferencia):
    fluxos_positivos = {fornecedor: 0 for fornecedor in df.index}
    fluxos_negativos = {fornecedor: 0 for fornecedor in df.index}
    
    for fornecedor in df.index:
        for outro_fornecedor in df.index:
            if fornecedor != outro_fornecedor:
                for criterio in df.columns:
                    diferenca = df.loc[fornecedor, criterio] - df.loc[outro_fornecedor, criterio]
                    preferencia = aplicar_funcao_preferencia(funcoes_preferencia[criterio], diferenca, parametros_preferencia.get(criterio, {}))
                    fluxos_positivos[fornecedor] += pesos[criterio] * preferencia
                    fluxos_negativos[outro_fornecedor] += pesos[criterio] * preferencia
    
    return fluxos_positivos, fluxos_negativos

fluxos_positivos, fluxos_negativos = calcular_fluxos(df_normalizado, pesos, funcoes_preferencia, parametros_preferencia)

# Calcular os fluxos líquidos
fluxos_liquidos = {fornecedor: fluxos_positivos[fornecedor] - fluxos_negativos[fornecedor] for fornecedor in fornecedores_selecionados}

# Exibir os resultados
df_fluxos = pd.DataFrame({
    'Fornecedor': fornecedores_selecionados,
    'Fluxo Positivo (ϕ+)': [fluxos_positivos[fornecedor] for fornecedor in fornecedores_selecionados],
    'Fluxo Negativo (ϕ-)': [fluxos_negativos[fornecedor] for fornecedor in fornecedores_selecionados],
    'Fluxo Líquido (ϕ)': [fluxos_liquidos[fornecedor] for fornecedor in fornecedores_selecionados]
})

st.write("### Resultados dos Fluxos (PROMETHEE II):")
st.dataframe(df_fluxos)

# Gráfico interativo dos fluxos líquidos
fig = px.bar(df_fluxos, x='Fornecedor', y='Fluxo Líquido (ϕ)', title="Fluxo Líquido dos Fornecedores")
st.plotly_chart(fig)
