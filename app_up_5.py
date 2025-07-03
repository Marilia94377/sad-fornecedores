# ===================================
# 📦 Importação de Bibliotecas
# ===================================
import streamlit as st
import pandas as pd
import plotly.express as px
import math
import numpy as np

#quando feito colocar no terminal: pip install streamlit pandas plotly
# streamlit run app_up_5.py

# ===================================
# 🎨 Estilo Visual
# ===================================
st.set_page_config(page_title="SAD PROMETHEE II", layout="wide")

st.markdown("""
    <style>
    .main {
        background-color: white;
        color: black;
    }
    h1 {
        font-size: 24px;
        color: #42434A;
    }
    h2, h3, h4, h5, h6, p {
        color: black;
    }
    .gray-background {
        background-color: #f0f0f0;
        padding: 12px;
        border-radius: 20px;
        border: 1px solid #d9d9d9;
    }
    div.stButton > button {
        color: white;
        background-color: #4CAF50;
        border: none;
        padding: 10px 20px;
        text-align: center;
        font-size: 16px;
        margin: 4px 2px;
        border-radius: 8px;
        cursor: pointer;
    }
    .button-voltar {
        color: white;
        background-color: #FF6347;
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
    .stDataFrame {
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ===================================
# 🧠 Descrição dos Critérios e Escalas Qualitativas
# ===================================
descricao_criterios = {
    'C1 - Preço': 'Valor monetário em reais. (↓)',
    'C2 - Qualidade': 'Avaliação subjetiva da qualidade com base em padrões de referência. (↑)',
    'C3 - Entrega': 'Prazo de entrega em dias. (↓)',
    'C4 - Tecnologia': 'Nível de inovação e adoção de tecnologias avançadas. (↑)',
    'C5 - Custos ambientais': 'Custos ambientais em reais, como multas ou tratamentos. (↓)',
    'C6 - Projeto verde': 'Grau de adoção de práticas sustentáveis no projeto. (↑)',
    'C7 - Gestão ambiental': 'Efetividade do sistema de gestão ambiental. (↑)',
    'C8 - Partes interessadas': 'Comprometimento com direitos e atendimento das partes interessadas. (↑)',
    'C9 - Segurança e saúde no trabalho': 'Taxa de acidentes ou incidentes ocupacionais. (↓)',
    'C10 - Respeito pela política dos funcionários': 'Cumprimento das políticas e direitos dos funcionários. (↑)',
    'C11 - Gestão social': 'Capacidade de implementar práticas de gestão social sustentável. (↑)',
    'C12 - Histórico de desempenho': 'Número de anos em operação. (↑)',
    'C13 - Reputação': 'Análise de mídia, avaliações e reconhecimentos. (↑)',
    'C14 - Logística': 'Distância em quilômetros. (↓)'
}

escala_qualitativa = {
    'C2 - Qualidade': """| Nota | Descrição |
|------|-----------|
| 1 | Produtos/serviços não atendem aos padrões de qualidade, resultando em retrabalho frequente e feedback negativo. |
| 2 | Produtos/serviços geralmente abaixo do padrão, com problemas ocasionais e feedback predominantemente negativo. |
| 3 | Produtos/serviços atendem ao padrão mínimo, com problemas ocasionais e feedback variado. |
| 4 | Produtos/serviços atendem ou excedem padrões de qualidade, com feedback positivo e poucas rejeições. |
| 5 | Produtos/serviços excepcionais, superando consistentemente os padrões, com feedback altamente positivo e mínimas rejeições. |""",

    'C4 - Tecnologia': """| Nota | Descrição |
|------|-----------|
| 1 | Práticas e tecnologias desatualizadas, sem inovação ou certificações. |
| 2 | Investimento limitado em tecnologia, com melhorias inconsistentes e poucas certificações. |
| 3 | Alguma inovação e tecnologias avançadas em áreas específicas, mas não abrangente. |
| 4 | Alinhado com as melhores práticas, com certificações, prêmios e parcerias relevantes. |
| 5 | Líder em inovação, com certificações ISO, prêmios e parcerias estratégicas. |""",

    'C6 - Projeto verde': """| Nota | Descrição |
|------|-----------|
| 1 | Sem práticas sustentáveis, ecoeficiência, certificações ou uso de energias renováveis. |
| 2 | Esforços limitados em sustentabilidade, poucas certificações, uso esporádico de energias renováveis. |
| 3 | Algumas práticas sustentáveis e certificações, uso moderado de energias renováveis. |
| 4 | Práticas ecoeficientes, certificações reconhecidas, uso consistente de energias renováveis e materiais sustentáveis. |
| 5 | Líder em sustentabilidade, práticas altamente ecoeficientes, certificações destacadas, uso significativo de energias renováveis e materiais sustentáveis. |""",

    'C7 - Gestão ambiental': """| Nota | Descrição |
|------|-----------|
| 1 | Sem sistema de gestão ambiental, não conformidade com regulamentações, nenhuma documentação ou programas de treinamento. |
| 2 | Esforços limitados em gestão ambiental, conformidade parcial, pouca documentação e poucos programas de treinamento. |
| 3 | Capacidade moderada em gestão ambiental, conformidade parcial, documentação adequada, programas de treinamento limitados. |
| 4 | Sistema de gestão ambiental eficaz, conformidade com regulamentações, documentação abrangente, programas de treinamento disponíveis. |
| 5 | Líder em gestão ambiental, total conformidade, excelente documentação, programas de treinamento exemplares. |""",

    'C8 - Partes interessadas': """| Nota | Descrição |
|------|-----------|
| 1 | Sem comprometimento com direitos das partes interessadas, não conformidade com normas, condições de trabalho e atendimento deficientes. |
| 2 | Comprometimento limitado, conformidade parcial com normas, condições de trabalho e atendimento inconsistentes. |
| 3 | Cumprimento parcial das normas, condições de trabalho e atendimento aceitáveis, feedback misto. |
| 4 | Comprometimento sólido, conformidade com normas, condições de trabalho e atendimento de alta qualidade, feedback positivo. |
| 5 | Comprometimento exemplar, alinhamento com melhores práticas, excelentes condições de trabalho e atendimento, feedback extremamente positivo. |""",

    'C10 - Respeito pela política dos funcionários': """| Nota | Descrição |
|------|-----------|
| 1 | Sem comprometimento com igualdade, diversidade e não discriminação; ausência de políticas e procedimentos. |
| 2 | Comprometimento mínimo, políticas limitadas e ineficazes, promoção de diversidade e inclusão é insuficiente. |
| 3 | Comprometimento parcial, políticas e procedimentos adequados, alguns esforços na promoção da diversidade e inclusão. |
| 4 | Comprometimento sólido, políticas alinhadas com melhores práticas, promoção ativa da diversidade e inclusão, políticas e procedimentos eficazes. |
| 5 | Comprometimento exemplar, políticas abrangentes, promoção fundamental da diversidade e inclusão, procedimentos robustos e igualdade de oportunidades clara. |""",

    'C11 - Gestão social': """| Nota | Descrição |
|------|-----------|
| 1 | Ausência de políticas de responsabilidade social corporativa (RSC), nenhum apoio à comunidade ou desenvolvimento sustentável. |
| 2 | Políticas de RSC limitadas, poucas ações concretas em apoio à comunidade e desenvolvimento sustentável, envolvimento mínimo com organizações sem fins lucrativos. |
| 3 | Algumas políticas de RSC e ações em apoio à comunidade, parcialmente desenvolvidas, envolvimento moderado com organizações sem fins lucrativos. |
| 4 | Políticas sólidas de RSC, envolvimento ativo em ações de apoio à comunidade e desenvolvimento sustentável, colaboração com organizações sem fins lucrativos. |
| 5 | Excelência em RSC, políticas abrangentes e eficazes, significativo apoio à comunidade, desenvolvimento sustentável e filantropia, colaboração destacada com organizações sem fins lucrativos. |""",

    'C13 - Reputação': """| Nota | Descrição |
|------|-----------|
| 1 | Reportagens negativas frequentes na mídia, avaliações online predominantemente negativas (1-2 estrelas), problemas recorrentes de conformidade. |
| 2 | Reportagens negativas ocasionais, avaliações abaixo da média (2-3 estrelas), questões esporádicas de conformidade. |
| 3 | Raramente em mídia, avaliações medianas (3 estrelas), conformidade com normas básicas sem grandes problemas. |
| 4 | Reportagens positivas frequentes, avaliações acima da média (4 estrelas), conformidade com todas as normas relevantes, boas práticas reconhecidas. |
| 5 | Destaque positivo constante na mídia, avaliações muito altas (4-5 estrelas), conformidade exemplar, líder em boas práticas. |"""
}


# ===================================
# 🚀 Cálculo PROMETHEE II
# ===================================
def calcular_promethee_sem_normalizar(df, criterios, objetivo, pesos, funcoes, parametros):
    alternativas = df.index.tolist()
    n = len(alternativas)
    peso_total = sum(pesos.values())

    # Inicializar matrizes
    matriz_d = {crit: np.zeros((n, n)) for crit in criterios}
    matriz_pref = {crit: np.zeros((n, n)) for crit in criterios}
    matriz_agregada = np.zeros((n, n))

    # Passo 1 e 2: calcular d(a,b) e aplicar F_j(a,b)
    for c_idx, crit in enumerate(criterios):
        for i, a in enumerate(alternativas):
            for j, b in enumerate(alternativas):
                if i == j:
                    continue

                # Diferença direta dos valores (sem normalizar)
                d = df.loc[a, crit] - df.loc[b, crit]

                # Inverter se critério for de minimização
                if objetivo[crit] == 'Minimizado':
                    d = -d

                matriz_d[crit][i][j] = d

                # Parâmetros q, p, s
                q = parametros[crit].get('q', 0)
                p = parametros[crit].get('p', 0)
                s = parametros[crit].get('s', 1)
                func = funcoes[crit]

                # Aplicar F_j conforme tipo
                if func == 'Usual':
                    pref = 1 if d > 0 else 0
                elif func == 'Quase-critério':
                    pref = 1 if d > q else 0
                elif func == 'Limiar de preferência':
                    if d <= 0:
                        pref = 0
                    elif d <= p:
                        pref = d / p
                    else:
                        pref = 1
                elif func == 'Pseudo-critério':
                    if d <= q:
                        pref = 0
                    elif d <= p:
                        pref = 0.5
                    else:
                        pref = 1
                elif func == 'Área de indiferença':
                    if d <= q:
                        pref = 0
                    elif d <= p:
                        pref = (d - q) / (p - q)
                    else:
                        pref = 1
                elif func == 'Gaussiana':
                    pref = 1 - math.exp(-(d ** 2) / (2 * s ** 2)) if d > 0 else 0
                else:
                    pref = 0

                matriz_pref[crit][i][j] = pref
                matriz_agregada[i][j] += pesos[crit] * pref

    # Passo 3: matriz de preferência agregada (dividir pelo peso total)
    matriz_agregada /= peso_total

    # Passo 4: cálculo dos fluxos
    fluxo_positivo = matriz_agregada.sum(axis=1) / (n - 1)
    fluxo_negativo = matriz_agregada.sum(axis=0) / (n - 1)
    fluxo_liquido = fluxo_positivo - fluxo_negativo

    # Ranking final
    resultado = pd.DataFrame({
        'Fornecedor': alternativas,
        'Fluxo Positivo (ϕ+)': fluxo_positivo,
        'Fluxo Negativo (ϕ-)': fluxo_negativo,
        'Fluxo Líquido (ϕ)': fluxo_liquido
    })
    resultado = resultado.sort_values('Fluxo Líquido (ϕ)', ascending=False)
    resultado['Ranking'] = range(1, len(resultado) + 1)

    return resultado, matriz_d, matriz_pref, matriz_agregada
    
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
# Tela do Sistema PROMETHEE II
# ===================================
def tela_sistema():
    st.title("Aplicação do Modelo - PROMETHEE II")
    
    # Explicação das funções de preferência
    with st.expander("ℹ️ Explicação das Funções de Preferência"):
        st.markdown("""
        **Tipos de Funções de Preferência:**
        
        1. **Usual (Tipo 1)**: Preferência estrita se diferença > 0. Não há parâmetros.
        2. **Quase-critério (Tipo 2)**: Preferência se diferença > q (limiar de indiferença)
        3. **Limiar de preferência (Tipo 3)**: Preferência linear entre 0 e p (limiar de preferência)
        4. **Pseudo-critério (Tipo 4)**: Zona de indiferença (q) e preferência linear até p
        5. **Área de indiferença (Tipo 5)**: Zona de indiferença (q) e zona de preferência fraca (0.5) até p
        6. **Gaussiana (Tipo 6)**: Preferência cresce suavemente conforme distribuição normal (parâmetro s)
        """)
    
    # Seleção de fornecedores e critérios
    fornecedores = ['Fornecedor A', 'Fornecedor B', 'Fornecedor C',
                    'Fornecedor D', 'Fornecedor E', 'Fornecedor F']
    criterios = list(descricao_criterios.keys())
    criterios_qualitativos = list(escala_qualitativa.keys())
    
    col1, col2 = st.columns(2)
    with col1:
        fornecedores_selecionados = st.multiselect(
            "Selecione os fornecedores:",
            fornecedores,
            default=fornecedores[:3]
        )
    
    with col2:
        criterios_selecionados = st.multiselect(
            "Selecione os critérios:",
            criterios,
            default=criterios[:3]
        )
    
    if len(fornecedores_selecionados) < 2:
        st.warning("Selecione pelo menos dois fornecedores para prosseguir.")
        st.stop()
    
    if not criterios_selecionados:
        st.warning("Selecione ao menos um critério para prosseguir.")
        st.stop()
    
    # Configuração dos critérios
    st.subheader("Configuração dos Critérios")
    
    pesos = {}
    objetivo = {}
    funcoes_preferencia = {}
    parametros_preferencia = {}
    desempenho = {forn: {} for forn in fornecedores_selecionados}
    
    for criterio in criterios_selecionados:
        with st.expander(f"Configuração do critério: {criterio}"):
            st.info(descricao_criterios[criterio])
            
            if criterio in escala_qualitativa:
                st.markdown("**Escala Qualitativa:**")
                st.markdown(escala_qualitativa[criterio])
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                pesos[criterio] = st.number_input(
                    f"Peso do critério {criterio}",
                    min_value=0.0,
                    value=1.0,
                    step=0.1,
                    key=f"peso_{criterio}"
                )
            
            with col2:
                objetivo[criterio] = st.radio(
                    f"O critério {criterio} deve ser:",
                    ['Maximizado', 'Minimizado'],
                    index=0 if '↓' not in descricao_criterios[criterio] else 1,
                    horizontal=True,
                    key=f"objetivo_{criterio}"
                )
            
            with col3:
                funcoes_preferencia[criterio] = st.selectbox(
                    f"Função de preferência para {criterio}",
                    ['Usual', 'Quase-critério', 'Limiar de preferência', 
                     'Pseudo-critério', 'Área de indiferença', 'Gaussiana'],
                    key=f"funcao_{criterio}"
                )
            
            # Parâmetros específicos para cada função
            parametros = {}
            func = funcoes_preferencia[criterio]
            
            if func in ['Quase-critério', 'Pseudo-critério', 'Área de indiferença']:
                parametros['q'] = st.number_input(
                    f"Limiar de indiferença (q) para {criterio}",
                    min_value=0.0,
                    value=0.1,
                    step=0.01,
                    key=f"q_{criterio}"
                )
            
            if func in ['Limiar de preferência', 'Pseudo-critério', 'Área de indiferença']:
                parametros['p'] = st.number_input(
                    f"Limiar de preferência (p) para {criterio}",
                    min_value=0.0,
                    value=0.5,
                    step=0.01,
                    key=f"p_{criterio}"
                )
            
            if func == 'Gaussiana':
                parametros['s'] = st.number_input(
                    f"Parâmetro s (desvio padrão) para {criterio}",
                    min_value=0.01,
                    value=0.5,
                    step=0.01,
                    key=f"s_{criterio}"
                )
            
            parametros_preferencia[criterio] = parametros
            
            # Entrada de desempenho dos fornecedores
            st.markdown("**Avaliação dos fornecedores:**")
            
            if criterio in criterios_qualitativos:
                for forn in fornecedores_selecionados:
                    desempenho[forn][criterio] = st.slider(
                        f"{forn} no critério {criterio} (1-5)",
                        1, 5, 3,
                        key=f"aval_{forn}_{criterio}"
                    )
            else:
                cols = st.columns(len(fornecedores_selecionados))
                for i, forn in enumerate(fornecedores_selecionados):
                    with cols[i]:
                        desempenho[forn][criterio] = st.number_input(
                            f"{forn}",
                            min_value=0.0,
                            step=0.1,
                            key=f"aval_{forn}_{criterio}"
                        )
    
    # Validação dos parâmetros
    for crit in criterios_selecionados:
        func = funcoes_preferencia[crit]
        params = parametros_preferencia[crit]
        
        if func in ['Pseudo-critério', 'Área de indiferença']:
            if params['p'] <= params['q']:
                st.error(f"Para o critério {crit}, o limiar de preferência (p) deve ser MAIOR que o limiar de indiferença (q)")
                st.stop()
        
        if func == 'Gaussiana' and params.get('s', 1) <= 0:
            st.error(f"Para o critério {crit}, o parâmetro s deve ser POSITIVO")
            st.stop()
    
    # Criar dataframe de desempenho
    df = pd.DataFrame(desempenho).T
    
    # Tabela resumo dos critérios
    st.subheader("Resumo dos Critérios Configurados")
    
    resumo_criterios = pd.DataFrame({
        'Critério': criterios_selecionados,
        'Objetivo': [objetivo[crit] for crit in criterios_selecionados],
        'Função Preferência': [funcoes_preferencia[crit] for crit in criterios_selecionados],
        'Peso': [pesos[crit] for crit in criterios_selecionados],
        'q (Indiferença)': [parametros_preferencia[crit].get('q', '-') for crit in criterios_selecionados],
        'p (Preferência)': [parametros_preferencia[crit].get('p', '-') for crit in criterios_selecionados],
        's (Gaussiana)': [parametros_preferencia[crit].get('s', '-') for crit in criterios_selecionados]
    })
    
    st.dataframe(resumo_criterios)
    
    # Exibir matriz de desempenho
    st.subheader("Matriz de Desempenho")
    st.dataframe(df.style.background_gradient(cmap='Blues'))
    
    # Botão para calcular
    if st.button("Calcular Ranking PROMETHEE II"):
        with st.spinner("Calculando ranking..."):
            resultado, matriz_d, matriz_pref, pref_agregada = calcular_promethee_sem_normalizar(
                df,
                criterios_selecionados,
                objetivo,
                pesos,
                funcoes_preferencia,
                parametros_preferencia
            )
        
        n = len(resultado)
        
        # Exibir resultados
        st.subheader("Resultados PROMETHEE II")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Ranking Final**")
            st.dataframe(
                resultado.style.format({
                    'Fluxo Positivo (ϕ+)': "{:.4f}",
                    'Fluxo Negativo (ϕ-)': "{:.4f}",
                    'Fluxo Líquido (ϕ)': "{:.4f}"
                }).background_gradient(subset=['Fluxo Líquido (ϕ)'], cmap='RdYlGn'
                )
            )
        
        with col2:
            st.markdown("**Relações de Preferência**")
            for i in range(len(resultado)):
                a = resultado.iloc[i]['Fornecedor']
                flux_a = resultado.iloc[i]['Fluxo Líquido (ϕ)']
                
                for j in range(i+1, len(resultado)):
                    b = resultado.iloc[j]['Fornecedor']
                    flux_b = resultado.iloc[j]['Fluxo Líquido (ϕ)']
                    
                    if abs(flux_a - flux_b) < 0.0001:  # Considera indiferença
                        st.write(f"🔹 {a} I {b} (Indiferentes)")
                    elif flux_a > flux_b:
                        st.write(f"✅ {a} P {b} (Preferência)")
                    else:
                        st.write(f"✅ {b} P {a} (Preferência)")
        
        # Gráfico de barras
        st.subheader("Visualização do Fluxo Líquido")
        fig = px.bar(
            resultado,
            x='Fornecedor',
            y='Fluxo Líquido (ϕ)',
            color='Fornecedor',
            title='Ranking PROMETHEE II - Fluxo Líquido',
            text='Fluxo Líquido (ϕ)',
            color_discrete_sequence=px.colors.qualitative.Plotly
        )
        fig.update_traces(texttemplate='%{text:.3f}', textposition='outside')
        fig.update_layout(
            yaxis_range=[-1, 1],
            yaxis_title='Fluxo Líquido (ϕ)',
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Matriz normalizada
        st.subheader("Matriz de Diferenças d(a,b) por Critério")
        for crit in criterios_selecionados:
            st.markdown(f"**Critério: {crit}**")
            df_dif = pd.DataFrame(matriz_d[crit],
                          index=resultado['Fornecedor'],
                          columns=resultado['Fornecedor'])
            st.dataframe(df_dif.style.format("{:.4f}").background_gradient(cmap='PuBu'))

        # Matriz de preferência agregada
        st.subheader("Matriz de Preferência Agregada")
        df_pref = pd.DataFrame(pref_agregada, 
                               index=resultado['Fornecedor'], 
                               columns=resultado['Fornecedor'])
        st.write("Matriz π(a, b) – Grau de preferência de a sobre b:")
        st.dataframe(df_pref.style.format("{:.4f}").background_gradient(cmap='Oranges'))

        # Matriz de Fluxo Líquido π(a,b) - π(b,a)
        st.subheader("Matriz de Fluxo Líquido Final (ϕ(a,b))")
        fluxo_liquido_matriz = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                fluxo_liquido_matriz[i][j] = pref_agregada[i][j] - pref_agregada[j][i]
        
        df_fluxo_liquido = pd.DataFrame(fluxo_liquido_matriz, 
                                        index=resultado['Fornecedor'], 
                                        columns=resultado['Fornecedor'])
        st.dataframe(df_fluxo_liquido.style.format("{:.4f}").background_gradient(cmap='RdBu', axis=None))

        st.subheader("Matriz de Diferenças Normalizadas d(a,b) por Critério")
       
        for crit in criterios_selecionados:
            st.markdown(f"**Critério: {crit}**")
            pref_crit = np.zeros((n, n))
            for i in range(n):
                for j in range(n):
                    d = df.loc[resultado['Fornecedor'].iloc[i], crit] - df.loc[resultado['Fornecedor'].iloc[j], crit]
                    if objetivo[crit] == 'Minimizado':
                        d = -d

                    q = parametros_preferencia[crit].get('q', 0)
                    p = parametros_preferencia[crit].get('p', 0)
                    s = parametros_preferencia[crit].get('s', 1)
                    func = funcoes_preferencia[crit]

                    if func == 'Usual':
                        pref = 1 if d > 0 else 0
                    elif func == 'Quase-critério':
                        pref = 1 if d > q else 0
                    elif func == 'Limiar de preferência':
                        if d <= 0:
                            pref = 0
                        elif d <= p:
                            pref = d / p
                        else:
                            pref = 1
                    elif func == 'Pseudo-critério':
                        if d <= q:
                            pref = 0
                        elif d <= p:
                            pref = 0.5
                        else:
                            pref = 1
                    elif func == 'Área de indiferença':
                        if d <= q:
                            pref = 0
                        elif d <= p:
                            pref = (d - q) / (p - q)
                        else:
                            pref = 1
                    elif func == 'Gaussiana':
                        pref = 1 - math.exp(-(d ** 2) / (2 * s ** 2)) if d > 0 else 0
                    else:
                        pref = 0

                    pref_crit[i][j] = pref

        # Cria e exibe o DataFrame dentro do loop para cada critério
        df_pi = pd.DataFrame(pref_crit,
                         index=resultado['Fornecedor'],
                         columns=resultado['Fornecedor'])
        st.dataframe(df_pi.style.format("{:.4f}").background_gradient(cmap='OrRd'))

# ===================================
# Roteamento entre telas
# ===================================
def main():
    menu = ["Tela Inicial", "Sistema PROMETHEE II"]
    escolha = st.sidebar.selectbox("Menu", menu)
    
    if escolha == "Tela Inicial":
        tela_inicial()
    elif escolha == "Sistema PROMETHEE II":
        tela_sistema()

if __name__ == "__main__":
    main()