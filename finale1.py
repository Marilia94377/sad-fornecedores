import streamlit as st
import pandas as pd
import plotly.express as px
import math

# Etapa 1: Estruturação do Problema e Definição dos Critérios
st.title("Aplicação do Modelo Proposto - Seleção de Fornecedores")
st.subheader("Estruturação do Problema")

st.write("""
O processo de seleção de fornecedores de serviços de terraplanagem envolve critérios econômicos, ambientais, sociais e gerais. 
Por favor, selecione os critérios que você deseja considerar e os fornecedores que serão avaliados.
""")

# Lista de critérios disponíveis e seu tipo de mensuração (minimização ou maximização)
criterios = {
    'C1': ('Preço/Custo do serviço', 'minimização'),
    'C2': ('Qualidade', 'maximização'),
    'C3': ('Entrega', 'minimização'),
    'C4': ('Tecnologia', 'maximização'),
    'C5': ('Custos ambientais', 'minimização'),
    'C6': ('Projeto verde', 'maximização'),
    'C7': ('Gestão ambiental', 'maximização'),
    'C8': ('Partes interessadas (direito, atendimento)', 'maximização'),
    'C9': ('Segurança e saúde no trabalho', 'maximização'),
    'C10': ('Respeito pela política dos funcionários', 'maximização'),
    'C11': ('Gestão social', 'maximização'),
    'C12': ('Histórico de desempenho', 'maximização'),
    'C13': ('Reputação', 'maximização')
}

# Funções de preferência disponíveis
funcoes_preferencia = {
    'Linear': 'Linear',
    'U-Shape': 'U-Shape',
    'V-Shape': 'V-Shape',
    'Level': 'Level',
    'V-Shape I': 'V-Shape I',
    'Gaussian': 'Gaussian'
}

# Seleção de critérios pelo usuário
st.write("### Selecione os critérios que você deseja incluir na avaliação:")
criterios_selecionados = st.multiselect(
    "Critérios disponíveis", [f"{k} ({criterios[k][1]})" for k in criterios.keys()],
    default=[f"{k} ({criterios[k][1]})" for k in list(criterios.keys())]
)

# Conversão dos critérios selecionados para as chaves originais
criterios_selecionados = [item.split()[0] for item in criterios_selecionados]

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
funcoes_selecionadas = {}
parametros = {}

# Entrada de desempenho para cada fornecedor junto com a função de preferência para o critério
desempenho_fornecedores = {}
for fornecedor in fornecedores_selecionados:
    st.write(f"### Desempenho para {fornecedor}")
    desempenho_fornecedores[fornecedor] = {}
    for criterio in criterios_selecionados:
        # Entrada de desempenho do fornecedor
        desempenho_fornecedores[fornecedor][criterio] = st.number_input(
            f"Desempenho de {fornecedor} no critério {criterios[criterio][0]}",
            min_value=0, max_value=1000000 if criterio == 'C1' else 100,
            value=50
        )
        
        # Seleção da função de preferência ao lado da entrada de desempenho
        st.write(f"Função de preferência para {fornecedor} no critério {criterios[criterio][0]}")
        funcoes_selecionadas[criterio] = st.selectbox(
            f"Função de preferência para {criterios[criterio][0]}",
            list(funcoes_preferencia.values()),
            key=f"{fornecedor}_{criterio}"
        )
        
        # Inserir parâmetros q, r ou s dependendo da função de preferência
        if funcoes_selecionadas[criterio] in ['U-Shape', 'V-Shape', 'Level', 'V-Shape I']:
            parametros[criterio] = {
                'q': st.number_input(f"Limiar de indiferença (q) para o critério {criterios[criterio][0]} ({fornecedor})", min_value=0.0, max_value=100.0, value=10.0, key=f"q_{fornecedor}_{criterio}"),
                'r': st.number_input(f"Limiar de preferência (r) para o critério {criterios[criterio][0]} ({fornecedor})", min_value=0.0, max_value=100.0, value=20.0, key=f"r_{fornecedor}_{criterio}")
            }
        if funcoes_selecionadas[criterio] == 'Gaussian':
            parametros[criterio] = {
                's': st.number_input(f"Parâmetro Gaussiano (s) para o critério {criterios[criterio][0]} ({fornecedor})", min_value=0.1, max_value=10.0, value=1.0, key=f"s_{fornecedor}_{criterio}")
            }

# Exibir o desempenho inserido
st.write("### Desempenho dos Fornecedores:")
df_desempenho = pd.DataFrame(desempenho_fornecedores)
st.dataframe(df_desempenho)

# Função para calcular o diferencial de desempenho
def calcular_diferencial(df, fornecedor_1, fornecedor_2, criterio):
    return abs(df[fornecedor_1][criterio] - df[fornecedor_2][criterio])

# Função para aplicar a função de preferência
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
        return 1 - math.exp(-(diferenca ** 2) / (2 * (parametros['s'] ** 2)))

# Etapa 4: Cálculo dos Fluxos Positivos, Negativos e Líquidos (PROMETHEE II)
st.subheader("Cálculo dos Fluxos (PROMETHEE II)")

# Função para calcular os fluxos (com base nas funções de preferência)
def calcular_fluxos(df, pesos, funcoes_selecionadas, parametros):
    fluxos_positivos = {}
    fluxos_negativos = {}
    for fornecedor in df.columns:
        fluxo_positivo = 0
        fluxo_negativo = 0
        for outro_fornecedor in df.columns:
            if fornecedor != outro_fornecedor:
                for criterio in df.index:
                    diferenca = calcular_diferencial(df, fornecedor, outro_fornecedor, criterio)
                    pref_value = aplicar_funcao_preferencia(funcoes_selecionadas[criterio], diferenca, parametros.get(criterio, {}))
                    if df[fornecedor][criterio] > df[outro_fornecedor][criterio]:
                        fluxo_positivo += pesos[criterio] * pref_value
                    else:
                        fluxo_negativo += pesos[criterio] * pref_value
        fluxos_positivos[fornecedor] = fluxo_positivo
        fluxos_negativos[fornecedor] = fluxo_negativo
    return fluxos_positivos, fluxos_negativos

# Calcular os fluxos
fluxos_positivos, fluxos_negativos = calcular_fluxos(df_desempenho, pesos, funcoes_selecionadas, parametros)

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
