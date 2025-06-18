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
        st.image("./pmd.jpg", caption="Project Management Group", width=215)

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
        st.image("./Luciana.jpg", width=200)
        st.markdown("<p style='color: black;'>Prof.ª Dr.ª Luciana Hazin Alencar - Orientadora</p>", unsafe_allow_html=True)
    with dev2_col:
        st.image("./marilia.jpg", width=200)
        st.markdown("<p style='color: black;'>Mestre Marília Martins - Desenvolvedora do Modelo Teórico</p>", unsafe_allow_html=True)
    with dev3_col:
        st.image("./maria.jpg", width=200)
        st.markdown("<p style='color: black;'>Maria Geyzianny - Desenvolvedora do Sistema</p>", unsafe_allow_html=True)

# Função para a tela do sistema com cálculo do PROMETHEE II
def tela_sistema():
    st.title("Aplicação do Modelo - PROMETHEE II")
    # st.subheader("Configurações do Modelo de Decisão")

    st.write("""
    Selecione os critérios e fornecedores a serem usados na avaliação. Para cada fornecedor, atribua pesos, defina se os critérios devem ser maximizados ou minimizados, escolha a função de preferência e insira o desempenho em uma escala de 1 a 5.
    """)

# =============================
# DEFINIR DESCRIÇÕES DOS CRITÉRIOS E ESCALAS
# =============================
descricao_criterios = {
    'C1 - Preço': 'Valor monetário em reais. (↓ Minimizar)',
    'C2 - Qualidade': 'Avaliação da qualidade dos produtos ou serviços.',
    'C3 - Entrega': 'Prazo de entrega em dias. (↓ Minimizar)',
    'C4 - Tecnologia': 'Nível de inovação e uso de tecnologias.',
    'C5 - Custos ambientais': 'Custos relacionados ao impacto ambiental em milhões. (↓ Minimizar)',
    'C6 - Projeto verde': 'Grau de adoção de práticas sustentáveis.',
    'C7 - Gestão ambiental': 'Eficácia do sistema de gestão ambiental.',
    'C8 - Partes interessadas (direito, atendimento)': 'Comprometimento com direitos e atendimento.',
    'C9 - Segurança e saúde no trabalho': 'Taxa de acidentes. (↓ Minimizar)',
    'C10 - Respeito pela política dos funcionários': 'Cumprimento das políticas e direitos dos colaboradores.',
    'C11 - Gestão social': 'Capacidade de implementar práticas de gestão social.',
    'C12 - Histórico de desempenho': 'Número de anos em operação. (↑ Maximizar)',
    'C13 - Reputação': 'Análise de reputação (mídia, avaliações e prêmios).',
    'C14 - Logística e localização': 'Distância em quilômetros. (↓ Minimizar)'
}

# Definir quais são qualitativos e quais são quantitativos
criterios_qualitativos = ['C2 - Qualidade', 'C4 - Tecnologia', 'C6 - Projeto verde', 'C7 - Gestão ambiental',
                           'C8 - Partes interessadas (direito, atendimento)', 'C10 - Respeito pela política dos funcionários',
                           'C11 - Gestão social', 'C13 - Reputação']
criterios_quantitativos = ['C1 - Preço', 'C3 - Entrega', 'C5 - Custos ambientais', 'C9 - Segurança e saúde no trabalho',
                            'C12 - Histórico de desempenho', 'C14 - Logística e localização']

# =============================
# FUNÇÃO PARA TELA INICIAL
# =============================
def tela_inicial():
    st.title("Sistema de Apoio à Decisão - PROMETHEE II")
    st.subheader("Seleção de Fornecedores Sustentáveis")

    st.markdown("""
    Este sistema permite avaliar e selecionar fornecedores sustentáveis com base em critérios econômicos, ambientais e sociais, utilizando o método PROMETHEE II.
    
    **Desenvolvido por:**  
    - Prof.ª Dr.ª Luciana Hazin Alencar (Orientadora)  
    - Marília Martins (Modelo Teórico)  
    - Maria Geyzianny (Desenvolvimento do Sistema)  
    """)

# =============================
# FUNÇÃO PARA TELA DO SISTEMA
# =============================
def tela_sistema():
    st.header("Configuração do Modelo PROMETHEE II")

    fornecedores = st.multiselect(
        "Selecione os fornecedores para análise:",
        ['Fornecedor A', 'Fornecedor B', 'Fornecedor C', 'Fornecedor D'],
        default=['Fornecedor A', 'Fornecedor B']
    )

    criterios = st.multiselect(
        "Selecione os critérios:",
        list(descricao_criterios.keys()),
        default=list(descricao_criterios.keys())
    )

    st.subheader("Preenchimento dos Dados")

    dados = {}
    pesos = {}
    objetivo = {}

    for crit in criterios:
        st.markdown(f"### Critério: {crit}")
        st.info(descricao_criterios[crit])

        col1, col2 = st.columns(2)
        with col1:
            pesos[crit] = st.number_input(f"Peso do critério **{crit}**", min_value=0.0, value=1.0)

        with col2:
            objetivo[crit] = st.radio(f"O critério **{crit}** deve ser:",
                                      ['Maximizar', 'Minimizar'],
                                      horizontal=True)

        for forn in fornecedores:
            if forn not in dados:
                dados[forn] = {}
            if crit in criterios_qualitativos:
                tooltip = """
                1 = Muito Fraco | 2 = Fraco | 3 = Médio | 4 = Bom | 5 = Excelente
                """
                dados[forn][crit] = st.slider(
                    f"Desempenho de {forn} em {crit}",
                    1, 5, 3,
                    help=tooltip
                )
            else:
                dados[forn][crit] = st.number_input(
                    f"Valor quantitativo de {forn} em {crit}",
                    min_value=0.0, step=0.1
                )

    df = pd.DataFrame(dados).T
    st.subheader("Matriz de Desempenho")
    st.dataframe(df)

    # =============================
    # CÁLCULOS PROMETHEE
    # =============================

    # Normalização
    df_norm = pd.DataFrame()
    for crit in criterios:
        if objetivo[crit] == 'Maximizar':
            df_norm[crit] = (df[crit] - df[crit].min()) / (df[crit].max() - df[crit].min())
        else:
            df_norm[crit] = (df[crit].max() - df[crit]) / (df[crit].max() - df[crit].min())

    st.subheader("Matriz Normalizada")
    st.dataframe(df_norm)

    # Fluxos
    flux_positivo = {f: 0 for f in fornecedores}
    flux_negativo = {f: 0 for f in fornecedores}

    for a in fornecedores:
        for b in fornecedores:
            if a != b:
                soma = 0
                for crit in criterios:
                    pref = df_norm.loc[a, crit] - df_norm.loc[b, crit]
                    soma += pesos[crit] * max(pref, 0)
                flux_positivo[a] += soma
                flux_negativo[b] += soma

    flux_liquido = {f: flux_positivo[f] - flux_negativo[f] for f in fornecedores}

    resultado = pd.DataFrame({
        'Fornecedor': fornecedores,
        'Fluxo Positivo (ϕ+)': [flux_positivo[f] for f in fornecedores],
        'Fluxo Negativo (ϕ-)': [flux_negativo[f] for f in fornecedores],
        'Fluxo Líquido (ϕ)': [flux_liquido[f] for f in fornecedores]
    }).sort_values(by='Fluxo Líquido (ϕ)', ascending=False)

    st.subheader("Resultado PROMETHEE II")
    st.dataframe(resultado)

    fig = px.bar(resultado, x='Fornecedor', y='Fluxo Líquido (ϕ)', color='Fornecedor',
                 title="Ranking dos Fornecedores")
    st.plotly_chart(fig)


# =============================
# CONTROLE DE TELAS
# =============================
paginas = ["Tela Inicial", "Sistema PROMETHEE II"]
selecao = st.sidebar.selectbox("Navegar", paginas)

if selecao == "Tela Inicial":
    tela_inicial()
else:
    tela_sistema()