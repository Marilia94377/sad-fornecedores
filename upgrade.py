import streamlit as st
import pandas as pd
import plotly.express as px
import math

# Definir a cor de fundo do site para branco
st.markdown(
    """
    <style>
    .main {
        background-color: white;
        color: black;
    }
    h1 {
        font-size: 24px;  /* Diminuir o tamanho do título */
        color: #42434A;  /* Garantir que o título seja preto */
    }
    h2, h3, h4, h5, h6, p {
        color: black;  /* Garantir que todos os textos sejam pretos */
    }
    .gray-background {
        background-color: #f0f0f0;  /* Cinza claro */
        padding: 12px;  /* Espaçamento interno */
        border-radius: 20px;  /* Bordas arredondadas */
        border: 1px solid #d9d9d9;  /* Borda cinza */
    }
     div.stButton > button {
        color: white;  /* Cor do texto do botão */
        background-color: #4CAF50;  /* Cor de fundo do botão */
        border: none;
        padding: 10px 20px;
        text-align: center;
        font-size: 16px;
        margin: 4px 2px;
        border-radius: 8px;
        cursor: pointer;
    }
    .button-voltar {
        color: white;  /* Cor do texto do botão */
        background-color: #FF6347;  /* Cor do botão de voltar */
        border: none;
        padding: 10px 20px;
        text-align: center;
        font-size: 16px;
        margin: 4px 2px;
        border-radius: 8px;
        cursor: pointer;
    }
    .spacer {
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Função para a tela inicial
def tela_inicial():
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("/home/maria/sad-fornecedores/pmd.jpg", caption="Project Management Group", width=215)

    with col2:
        st.markdown("<div class='gray-background' ><h1>Sistema de Apoio à Decisão para a Seleção de Fornecedores Sustentáveis em Projetos</h1></div>", unsafe_allow_html=True)

    st.write("""
    Bem-vindo ao Sistema de Apoio à Decisão, criado para ajudar empresas na seleção de fornecedores sustentáveis, considerando critérios econômicos, sociais e ambientais.
    """)

    st.write("Este sistema foi desenvolvido no laboratório Project Management and Development - Research Group do Departamento de Engenharia de Produção da Universidade Federal de Pernambuco (UFPE).")
    
    st.write("""
    O crescente interesse por práticas empresariais sustentáveis tem impulsionado a necessidade de ferramentas que auxiliem na seleção de fornecedores, considerando critérios que vão além do custo e da qualidade. Este sistema foi desenvolvido para aplicar o modelo PROMETHEE II, permitindo uma análise multicritério e comparações estruturadas entre fornecedores.
    """)

    st.markdown("<div class='gray-background'><h5>Conheça quem está por trás da idealização desta solução inovadora: </h5></div>", unsafe_allow_html=True)

    # Adicionar espaçamento antes das imagens das desenvolvedoras
    st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

    dev1_col, dev2_col, dev3_col = st.columns(3)
    with dev1_col:
        st.image("/home/maria/sad-fornecedores/Luciana.jpg", width=200)
        st.markdown("<p style='color: black;'>Prof.ª Dr.ª Luciana Hazin Alencar - Orientadora</p>", unsafe_allow_html=True)
    with dev2_col:
        st.image("/home/maria/sad-fornecedores/marilia.jpg", width=200)
        st.markdown("<p style='color: black;'>Mestre Marília Martins - Desenvolvedora do Modelo Teórico</p>", unsafe_allow_html=True)
    with dev3_col:
        st.image("/home/maria/sad-fornecedores/maria.jpg", width=200)
        st.markdown("<p style='color: black;'>Maria Geyzianny - Desenvolvedora do Sistema</p>", unsafe_allow_html=True)

# Função para a tela do sistema com cálculo do PROMETHEE II
def tela_sistema():
    st.title("Aplicação do Modelo Proposto - PROMETHEE II")
    st.subheader("Configurações do Modelo de Decisão")

    st.write("""
    Selecione os critérios e fornecedores a serem usados na avaliação. Para cada fornecedor, atribua pesos, defina se os critérios devem ser maximizados ou minimizados, escolha a função de preferência e insira o desempenho em uma escala de 1 a 5.
    """)

    # Lista de fornecedores e critérios
    fornecedores_disponiveis = ['Fornecedor A', 'Fornecedor B', 'Fornecedor C', 'Fornecedor D', 'Fornecedor E', 'Fornecedor F']
    criterios_disponiveis = ['C1 - Preço/Custo do serviço', 'C2 - Qualidade', 'C3 - Entrega', 'C4 - Tecnologia', 
                             'C5 - Custos ambientais', 'C6 - Projeto verde', 'C7 - Gestão ambiental', 
                             'C8 - Partes interessadas (direito, atendimento)', 'C9 - Segurança e saúde no trabalho', 
                             'C10 - Respeito pela política dos funcionários', 'C11 - Gestão social', 
                             'C12 - Histórico de desempenho', 'C13 - Reputação']

    # Selecione fornecedores e critérios
    fornecedores_selecionados = st.multiselect("Selecione os fornecedores que serão avaliados", fornecedores_disponiveis, default=fornecedores_disponiveis[:4])
    criterios_selecionados = st.multiselect("Selecione os critérios que serão usados", criterios_disponiveis, default=criterios_disponiveis)

    # Atribuição de Pesos, Maximização/Minimização, Funções de Preferência e Desempenho
    pesos = {}
    max_min_criterios = {}
    funcoes_preferencia = {}
    parametros_preferencia = {}
    desempenho_fornecedores = {}

    for fornecedor in fornecedores_selecionados:
        st.write(f"### Configurações para {fornecedor}")

        desempenho_fornecedores[fornecedor] = {}
        pesos[fornecedor] = {}
        max_min_criterios[fornecedor] = {}
        funcoes_preferencia[fornecedor] = {}
        parametros_preferencia[fornecedor] = {}

        for criterio in criterios_selecionados:
            st.write(f"#### Critério: {criterio}")

            # Atribuição de peso para o critério e fornecedor
            pesos[fornecedor][criterio] = st.number_input(f"Peso para {criterio} de {fornecedor} (0 a 100)", min_value=0.0, max_value=100.0, value=50.0, key=f"peso_{fornecedor}_{criterio}")
            max_min_criterios[fornecedor][criterio] = st.selectbox(f"O critério {criterio} de {fornecedor} deve ser:", ['Maximizado', 'Minimizado'], key=f"max_min_{fornecedor}_{criterio}")

            # Função de preferência para o critério e fornecedor
            funcao = st.selectbox(f"Função de preferência para {criterio} de {fornecedor}", 
                                  ['Linear', 'U-Shape', 'V-Shape', 'Level', 'V-Shape I', 'Gaussian'], key=f"pref_{fornecedor}_{criterio}")
            funcoes_preferencia[fornecedor][criterio] = funcao

            # Parâmetros para a função de preferência, se aplicável
            if funcao in ['U-Shape', 'V-Shape', 'Level', 'V-Shape I']:
                parametros_preferencia[fornecedor][criterio] = {
                    'q': st.number_input(f"Limiar de indiferença (q) para {criterio} de {fornecedor}", min_value=0.0, max_value=100.0, value=10.0, key=f"q_{fornecedor}_{criterio}"),
                    'r': st.number_input(f"Limiar de preferência (r) para {criterio} de {fornecedor}", min_value=0.0, max_value=100.0, value=20.0, key=f"r_{fornecedor}_{criterio}")
                }
            elif funcao == 'Gaussian':
                parametros_preferencia[fornecedor][criterio] = {
                    's': st.number_input(f"Parâmetro s para função Gaussian para {criterio} de {fornecedor}", min_value=0.1, max_value=10.0, value=1.0, key=f"s_{fornecedor}_{criterio}")
                }

            # Desempenho do fornecedor no critério (Escala de 1 a 5)
            desempenho_fornecedores[fornecedor][criterio] = st.slider(f"Escala qualitativa do {fornecedor} no critério {criterio} (1 a 5)", 1, 5, 3, key=f"desempenho_{fornecedor}_{criterio}")

    # Transformar os dados de desempenho em um DataFrame
    df_desempenho = pd.DataFrame(desempenho_fornecedores).T
    st.write("### Matriz de Consequência:")
    st.dataframe(df_desempenho)

    # Normalização e cálculos
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

    df_normalizado = normalizar(df_desempenho, {criterio: max_min_criterios[fornecedores_selecionados[0]][criterio] for criterio in criterios_selecionados})
    st.write("### Matriz de Consequência Normalizada:")
    st.dataframe(df_normalizado)

    # Aplicar função de preferência
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

    # Cálculo dos fluxos
    def calcular_fluxos(df, pesos, funcoes_preferencia, parametros_preferencia):
        fluxos_positivos = {fornecedor: 0 for fornecedor in df.index}
        fluxos_negativos = {fornecedor: 0 for fornecedor in df.index}

        for fornecedor in df.index:
            for outro_fornecedor in df.index:
                if fornecedor != outro_fornecedor:
                    for criterio in df.columns:
                        diferenca = df.loc[fornecedor, criterio] - df.loc[outro_fornecedor, criterio]
                        preferencia = aplicar_funcao_preferencia(funcoes_preferencia[fornecedor][criterio], diferenca, parametros_preferencia[fornecedor].get(criterio, {}))
                        fluxos_positivos[fornecedor] += pesos[fornecedor][criterio] * preferencia
                        fluxos_negativos[outro_fornecedor] += pesos[fornecedor][criterio] * preferencia

        return fluxos_positivos, fluxos_negativos

    fluxos_positivos, fluxos_negativos = calcular_fluxos(df_normalizado, pesos, funcoes_preferencia, parametros_preferencia)
    fluxos_liquidos = {fornecedor: fluxos_positivos[fornecedor] - fluxos_negativos[fornecedor] for fornecedor in fornecedores_selecionados}

    df_fluxos = pd.DataFrame({
        'Fornecedor': fornecedores_selecionados,
        'Fluxo Positivo (ϕ+)': [fluxos_positivos[fornecedor] for fornecedor in fornecedores_selecionados],
        'Fluxo Negativo (ϕ-)': [fluxos_negativos[fornecedor] for fornecedor in fornecedores_selecionados],
        'Fluxo Líquido (ϕ)': [fluxos_liquidos[fornecedor] for fornecedor in fornecedores_selecionados]
    })

    st.write("### Resultados dos Fluxos (PROMETHEE II):")
    st.dataframe(df_fluxos)

    fig = px.bar(df_fluxos, x='Fornecedor', y='Fluxo Líquido (ϕ)', title="Fluxo Líquido dos Fornecedores")
    st.plotly_chart(fig)

    # Botão para voltar à tela inicial
    if st.button("Voltar", key="voltar"):
        st.session_state.tela_inicial = False
        

# Controle de fluxo entre as telas
if "tela_inicial" not in st.session_state or st.session_state.tela_inicial == False:
    tela_inicial()
    if st.button("Avançar para o Sistema"):
        st.session_state.tela_inicial = True
        
else:
    tela_sistema()
