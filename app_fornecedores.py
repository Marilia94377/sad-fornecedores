import streamlit as st
import pandas as pd
import plotly.express as px
import math

# ===================================
# Estilo Visual
# ===================================
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

# ===================================
# Tela Inicial
# ===================================

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

# ===================================
# 🔧 Função das Preferências
# ===================================
def aplicar_funcao_preferencia(funcao, diferenca, parametros):
    if funcao == 'Linear':
        return max(0, min(1, diferenca))
    elif funcao == 'U-Shape':
        q = parametros.get('q', 0)
        return 1 if diferenca > q else 0
    elif funcao == 'V-Shape':
        r = parametros.get('r', 1e-6)
        return min(diferenca / r, 1) if diferenca > 0 else 0
    elif funcao == 'Level':
        q = parametros.get('q', 0)
        r = parametros.get('r', 1e-6)
        if diferenca <= q:
            return 0
        elif q < diferenca <= r:
            return 0.5
        else:
            return 1
    elif funcao == 'V-Shape with Indifference':
        q = parametros.get('q', 0)
        r = parametros.get('r', 1e-6)
        if diferenca <= q:
            return 0
        else:
            return min((diferenca - q) / (r - q), 1)
    elif funcao == 'Gaussian':
        s = parametros.get('s', 1)
        return 1 - math.exp(- (diferenca ** 2) / (2 * (s ** 2)))
    else:
        return 0
    
# ===================================
# 🔧 Tela do Sistema
# ===================================
def tela_sistema():
    st.title("Aplicação do Modelo - PROMETHEE II")

    st.write("""
    Selecione os critérios e os fornecedores que serão avaliados.  
    Para cada **critério**, atribua um **peso**, defina se deve ser **maximizado ou minimizado**, escolha a **função de preferência** e insira o **desempenho de cada fornecedor**.  
    🔸 **A escala de 1 a 5 é utilizada apenas para os critérios qualitativos.**  
    🔸 Para os critérios quantitativos, insira o **valor numérico correspondente**.
    """)

    fornecedores = ['Fornecedor A', 'Fornecedor B', 'Fornecedor C',
                    'Fornecedor D', 'Fornecedor E', 'Fornecedor F']
    criterios = [
        'C1 - Preço', 'C2 - Qualidade', 'C3 - Entrega', 'C4 - Tecnologia',
        'C5 - Custos ambientais', 'C6 - Projeto verde', 'C7 - Gestão ambiental',
        'C8 - Partes interessadas', 'C9 - Segurança e saúde no trabalho',
        'C10 - Respeito pela política dos funcionários', 'C11 - Gestão social',
        'C12 - Histórico de desempenho', 'C13 - Reputação', 'C14 - Logística'
    ]

    criterios_qualitativos = ['C2 - Qualidade', 'C4 - Tecnologia', 'C6 - Projeto verde',
                               'C7 - Gestão ambiental', 'C8 - Partes interessadas',
                               'C10 - Respeito pela política dos funcionários',
                               'C11 - Gestão social', 'C13 - Reputação']

    criterios_quantitativos = ['C1 - Preço', 'C3 - Entrega', 'C5 - Custos ambientais',
                                'C9 - Segurança e saúde no trabalho',
                                'C12 - Histórico de desempenho', 'C14 - Logística']

    fornecedores_selecionados = st.multiselect(
        "Selecione os fornecedores:",
        fornecedores,
        default=fornecedores
    )

    criterios_selecionados = st.multiselect(
        "Selecione os critérios:",
        criterios,
        default=criterios
    )

    # ==============================
    # 📥 Entrada dos Dados
    # ==============================
    pesos = {}
    objetivo = {}
    funcoes_preferencia = {}
    parametros_preferencia = {}
    desempenho = {}

    for criterio in criterios_selecionados:
        st.markdown(f"### Critério: {criterio}")

        col1, col2, col3 = st.columns(3)

        with col1:
            pesos[criterio] = st.number_input(
                f"Peso do critério {criterio}",
                min_value=0.0,
                value=1.0
            )

        with col2:
            objetivo[criterio] = st.radio(
                f"O critério {criterio} deve ser:",
                ['Maximizado', 'Minimizado'],
                horizontal=True
            )

        with col3:
            func = st.selectbox(
                f"Função de preferência para {criterio}",
                ['Linear', 'U-Shape', 'V-Shape', 'Level', 'V-Shape with Indifference', 'Gaussian']
            )
            funcoes_preferencia[criterio] = func

        parametros = {}
        if func in ['U-Shape', 'V-Shape', 'Level', 'V-Shape with Indifference']:
            parametros['q'] = st.number_input(
                f"Limiar de indiferença (q) para {criterio}",
                min_value=0.0,
                value=0.1
            )
            parametros['r'] = st.number_input(
                f"Limiar de preferência (r) para {criterio}",
                min_value=0.0,
                value=0.5
            )
        elif func == 'Gaussian':
            parametros['s'] = st.number_input(
                f"Parâmetro s para função Gaussian para {criterio}",
                min_value=0.1,
                value=0.5
            )
        parametros_preferencia[criterio] = parametros

        for forn in fornecedores_selecionados:
            if forn not in desempenho:
                desempenho[forn] = {}
            if criterio in criterios_qualitativos:
                desempenho[forn][criterio] = st.slider(
                    f"Desempenho de {forn} no critério {criterio}",
                    1, 5, 3
                )
            else:
                desempenho[forn][criterio] = st.number_input(
                    f"Valor quantitativo de {forn} no critério {criterio}",
                    min_value=0.0,
                    step=0.1
                )

    df = pd.DataFrame(desempenho).T
    st.subheader("Matriz de Desempenho")
    st.dataframe(df)

    # ==============================
    # 🔢 Cálculo PROMETHEE II
    # ==============================
    df_norm = pd.DataFrame()

    for crit in criterios_selecionados:
        max_valor = df[crit].max()
        min_valor = df[crit].min()
        if max_valor == min_valor:
            df_norm[crit] = 0
        elif objetivo[crit] == 'Maximizado':
            df_norm[crit] = (df[crit] - min_valor) / (max_valor - min_valor)
        else:
            df_norm[crit] = (max_valor - df[crit]) / (max_valor - min_valor)

    st.subheader("Matriz Normalizada")
    st.dataframe(df_norm)

    # ==============================
    # ⚙️ Cálculo dos Fluxos
    # ==============================
    flux_positivo = {f: 0 for f in fornecedores_selecionados}
    flux_negativo = {f: 0 for f in fornecedores_selecionados}

    for a in fornecedores_selecionados:
        for b in fornecedores_selecionados:
            if a != b:
                soma = 0
                for crit in criterios_selecionados:
                    diferenca = df_norm.loc[a, crit] - df_norm.loc[b, crit]
                    pref = aplicar_funcao_preferencia(
                        funcoes_preferencia[crit],
                        diferenca,
                        parametros_preferencia[crit]
                    )
                    soma += pesos[crit] * pref
                flux_positivo[a] += soma
                flux_negativo[b] += soma

    flux_liquido = {f: flux_positivo[f] - flux_negativo[f] for f in fornecedores_selecionados}

    resultado = pd.DataFrame({
        'Fornecedor': fornecedores_selecionados,
        'Fluxo Positivo (ϕ+)': [flux_positivo[f] for f in fornecedores_selecionados],
        'Fluxo Negativo (ϕ-)': [flux_negativo[f] for f in fornecedores_selecionados],
        'Fluxo Líquido (ϕ)': [flux_liquido[f] for f in fornecedores_selecionados]
    }).sort_values(by='Fluxo Líquido (ϕ)', ascending=False)

    st.subheader("Resultado PROMETHEE II")
    st.dataframe(resultado)

    fig = px.bar(resultado, x='Fornecedor', y='Fluxo Líquido (ϕ)',
                 title="Ranking dos Fornecedores", color='Fornecedor')
    st.plotly_chart(fig)

# ===================================
# 🚦 Controle de Telas
# ===================================
if "tela_inicial" not in st.session_state or st.session_state.tela_inicial == False:
    tela_inicial()
    if st.button("Avançar para o Sistema"):
        st.session_state.tela_inicial = True
else:
    tela_sistema()