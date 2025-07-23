# ===================================
# Importação de Bibliotecas
# ===================================
import streamlit as st
import pandas as pd
import plotly.express as px
import math
import numpy as np

#quando feito colocar no terminal: pip install streamlit pandas plotly
#streamlit run app_up_TRADUÇÃO.py

# ===================================
# Estilo Visual
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
# Descrição dos Critérios e Escalas Qualitativas
# ===================================
descricao_criterios = {
    'C1 - Custo / Cost': 'Valor monetário em uma moeda específica / Monetary value in a specific currency. (↓)',
    'C2 - Qualidade / Quality': 'Avaliação subjetiva da qualidade com base em padrões de referência. (↑) / Subjective quality assessment based on benchmark standards. (↑)',
    'C3 - Entrega / Delivery': 'Prazo de entrega em dias. (↓) / Delivery time in days. (↓)',
    'C4 - Tecnologia / Technology': 'Nível de inovação e adoção de tecnologias avançadas. (↑) / Level of innovation and adoption of advanced technologies. (↑)',
    'C5 - Custos ambientais / Environmental Costs': 'Custos ambientais em reais, como multas ou tratamentos. (↓) / Environmental costs in BRL, such as fines or treatment. (↓)',
    'C6 - Projeto verde / Green Design': 'Grau de adoção de práticas sustentáveis no projeto. (↑) / Degree of adoption of sustainable practices in the project. (↑)',
    'C7 - Gestão ambiental / Environmental Management': 'Efetividade do sistema de gestão ambiental. (↑) / Effectiveness of the environmental management system. (↑)',
    'C8 - Partes interessadas / Stakeholders': 'Comprometimento com direitos e atendimento das partes interessadas. (↑) / Commitment to stakeholder rights and service. (↑)',
    'C9 - Segurança e saúde no trabalho / Occupational Health and Safety': 'Taxa de acidentes ou incidentes ocupacionais. (↓) / Rate of workplace accidents or incidents. (↓)',
    'C10 - Respeito pela política dos funcionários / Employee Policy Compliance': 'Cumprimento das políticas e direitos dos funcionários. (↑) / Compliance with employee policies and rights. (↑)',
    'C11 - Gestão social / Social Management': 'Capacidade de implementar práticas de gestão social sustentável. (↑) / Capacity to implement sustainable social management practices. (↑)',
    'C12 - Histórico de desempenho / Performance History': 'Número de anos em operação. (↑) / Number of years in operation. (↑)',
    'C13 - Reputação / Reputation': 'Análise de mídia, avaliações e reconhecimentos. (↑) / Media analysis, reviews, and recognitions. (↑)',
    'C14 - Logística / Logistics': 'Distância em quilômetros. (↓) / Distance in kilometers. (↓)'
}

escala_qualitativa = {
      'C2 - Qualidade / Quality': """| Nota | Descrição (PT / EN) |
|------|----------------------|
| 1 | Produtos/serviços não atendem aos padrões de qualidade, resultando em retrabalho frequente e feedback negativo. / Products/services do not meet quality standards, leading to frequent rework and negative feedback. |
| 2 | Produtos/serviços geralmente abaixo do padrão, com problemas ocasionais e feedback predominantemente negativo. / Products/services generally below standard, with occasional issues and mostly negative feedback. |
| 3 | Produtos/serviços atendem ao padrão mínimo, com problemas ocasionais e feedback variado. / Products/services meet the minimum standard, with occasional problems and mixed feedback. |
| 4 | Produtos/serviços atendem ou excedem padrões de qualidade, com feedback positivo e poucas rejeições. / Products/services meet or exceed quality standards, with positive feedback and few rejections. |
| 5 | Produtos/serviços excepcionais, superando consistentemente os padrões, com feedback altamente positivo e mínimas rejeições. / Exceptional products/services, consistently exceeding standards, with highly positive feedback and minimal rejections. |
""",

    'C4 - Tecnologia / Technology': """| Nota | Descrição (PT / EN) |
|------|----------------------|
| 1 | Nenhuma tecnologia atual utilizada; processos manuais predominam. / No current technology used; manual processes dominate. |
| 2 | Baixa adoção de tecnologia, com melhorias mínimas nos processos. / Low technology adoption, with minimal process improvements. |
| 3 | Uso moderado de tecnologias conhecidas; eficiência padrão. / Moderate use of known technologies; standard efficiency. |
| 4 | Alta adoção de tecnologias, promovendo ganho de eficiência. / High adoption of technologies, promoting efficiency gains. |
| 5 | Utilização de tecnologias de ponta e inovação contínua. / Use of cutting-edge technologies and continuous innovation. |
""",

    'C6 - Projeto verde / Green Design': """| Nota | Descrição (PT / EN) |
|------|----------------------|
| 1 | Nenhuma preocupação com sustentabilidade no projeto. / No concern with sustainability in the project. |
| 2 | Ações sustentáveis mínimas e pontuais. / Minimal and occasional sustainable actions. |
| 3 | Algumas iniciativas sustentáveis em práticas ou materiais. / Some sustainable initiatives in practices or materials. |
| 4 | Projeto incorpora várias práticas sustentáveis relevantes. / Project incorporates various relevant sustainable practices. |
| 5 | Projeto fortemente orientado à sustentabilidade em todas as etapas. / Project strongly oriented to sustainability in all stages. |
""",

    'C7 - Gestão ambiental / Environmental Management': """| Nota | Descrição (PT / EN) |
|------|----------------------|
| 1 | Sem sistema de gestão ambiental estruturado. / No structured environmental management system. |
| 2 | Sistema informal e pouco eficaz. / Informal and ineffective system. |
| 3 | Sistema básico implementado com limitações. / Basic system implemented with limitations. |
| 4 | Sistema bem estruturado e em conformidade com normas. / Well-structured system in compliance with standards. |
| 5 | Sistema robusto, certificado e com melhoria contínua. / Robust, certified system with continuous improvement. |
""",

    'C8 - Partes interessadas / Stakeholders': """| Nota | Descrição (PT / EN) |
|------|----------------------|
| 1 | Ignora interesses das partes envolvidas. / Ignores stakeholder interests. |
| 2 | Responde de forma reativa e limitada. / Reactively and minimally responsive. |
| 3 | Atendimento mínimo às partes interessadas. / Minimal stakeholder engagement. |
| 4 | Compromisso com políticas de engajamento ativo. / Commitment to active engagement policies. |
| 5 | Envolvimento transparente, ativo e responsável. / Transparent, active, and responsible stakeholder involvement. |
""",

    'C10 - Respeito pela política dos funcionários / Employee Policy Compliance': """| Nota | Descrição (PT / EN) |
|------|----------------------|
| 1 | Não respeita normas trabalhistas básicas. / Does not respect basic labor standards. |
| 2 | Apresenta falhas frequentes no cumprimento das normas. / Frequent failures in policy compliance. |
| 3 | Cumpre requisitos mínimos exigidos por lei. / Complies with minimum legal requirements. |
| 4 | Cumpre e monitora práticas e direitos dos funcionários. / Complies with and monitors employee rights and practices. |
| 5 | Promove ambiente justo, seguro e participativo. / Promotes a fair, safe, and participatory environment. |
""",

    'C11 - Gestão social / Social Management': """| Nota | Descrição (PT / EN) |
|------|----------------------|
| 1 | Nenhuma ação voltada ao bem-estar social. / No action focused on social well-being. |
| 2 | Práticas sociais reativas e pouco estruturadas. / Reactive and poorly structured social practices. |
| 3 | Algumas práticas sociais implementadas. / Some social practices implemented. |
| 4 | Políticas sociais definidas e em operação. / Defined and operational social policies. |
| 5 | Gestão social estratégica, com forte impacto positivo. / Strategic social management with strong positive impact. |
""",

    'C13 - Reputação / Reputation': """| Nota | Descrição (PT / EN) |
|------|----------------------|
| 1 | Reputação muito negativa ou desconhecida. / Very negative or unknown reputation. |
| 2 | Imagem desfavorável ou instável no mercado. / Unfavorable or unstable market image. |
| 3 | Reputação aceitável, sem grandes destaques. / Acceptable reputation, no major highlights. |
| 4 | Boa reputação com avaliações positivas consistentes. / Good reputation with consistent positive evaluations. |
| 5 | Reputação excelente, reconhecida amplamente no setor. / Excellent reputation, widely recognized in the industry. |
"""
}

# ===================================
# Cálculo PROMETHEE II
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
        st.markdown("<div class='gray-background' ><h1>Sistema de Apoio à Decisão para a Seleção de Fornecedores Sustentáveis em Projetos / Decision Support System for the Selection of Sustainable Suppliers in Projects</h1></div>", unsafe_allow_html=True)

    st.write("""
    Bem-vindo ao Sistema de Apoio à Decisão, criado para ajudar empresas na seleção de fornecedores sustentáveis, considerando critérios econômicos, sociais e ambientais. / 
    Welcome to the Decision Support System, designed to assist companies in selecting sustainable suppliers, considering economic, social, and environmental criteria.         
    """)

    st.write("Este sistema foi desenvolvido no laboratório Project Management and Development - Research Group do Departamento de Engenharia de Produção da Universidade Federal de Pernambuco (UFPE). / This system was developed at the Project Management and Development Research Group laboratory of the Department of Production Engineering at the Federal University of Pernambuco (UFPE).")

    st.markdown("<div class='gray-background'><h5>Conheça quem está por trás da idealização desta solução / Meet the team behind the development of this solution : </h5></div>", unsafe_allow_html=True)

    st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

    dev1_col, dev2_col, dev3_col = st.columns(3)
    with dev1_col:
        st.image("./Luciana.jpg", width=200)
        st.markdown("<p style='color: black;'>Prof.ª Dr.ª Luciana Hazin Alencar</p>", unsafe_allow_html=True)
    with dev2_col:
        st.image("./marilia.jpg", width=200)
        st.markdown("<p style='color: black;'>Mestre Marília Martins</p>", unsafe_allow_html=True)
    with dev3_col:
        st.image("./maria.jpg", width=200)
        st.markdown("<p style='color: black;'>Maria Geyzianny</p>", unsafe_allow_html=True)

# ===================================
# Tela do Sistema PROMETHEE II
# ===================================
def tela_sistema():
    st.title("Decision Support System for the Selection of Sustainable Suppliers - PROMETHEE II")
    
    # Explicação das funções de preferência
    with st.expander("ℹ️ Explicação das Funções de Preferência / Explanation of Preference Functions"):
        st.markdown("""
        **Tipos de Funções de Preferência / Types of Preference Functions:**
        
        1. **Usual (Tipo 1) / Usual Criterion**: Qualquer diferença de desempenho, por menor que seja, já é suficiente para indicar preferência por uma alternativa em relação à outra. / Any performance difference, even minimal, is enough to indicate a preference for one alternative over another.
        2. **Quase-critério (Tipo 2) / U-Shape Criterion**: A preferência por uma alternativa só ocorre quando a diferença de desempenho atinge um determinado limiar./ A preference for one alternative arises only after the performance difference exceeds a certain threshold.
        3. **Limiar de preferência (Tipo 3) / V-Shape Criterion**: Quando há uma pequena diferença de desempenho, já é possível começar a preferir uma alternativa em detrimento de outra, de forma gradual. / Even a small performance gap gradually leads to a preference for one alternative over another.
        4. **Pseudo-critério (Tipo 4) / Level Criterion**: Existe um intervalo em que a diferença de desempenho resulta em uma preferência parcial por uma das alternativas. / There is a range in which the performance difference results in a partial preference for one alternative.
        5. **Área de indiferença (Tipo 5) / V-Shape with Indifference Criterion**: Dentro de um intervalo de indiferença, não há preferência; após esse intervalo, a preferência cresce gradualmente conforme a diferença de desempenho aumenta. / Within the indifference zone, no preference exists; beyond that, preference gradually increases with performance difference.
        6. **Gaussiana (Tipo 6) / Gaussian Criterion**: A preferência por uma alternativa segue uma curva gaussiana, sendo mais intensa em torno de uma diferença ideal. / Preference follows a Gaussian curve, peaking around an ideal performance difference between alternatives.
        """)
    
    # Seleção de fornecedores e critérios
    fornecedores = ['Fornecedor A / Supplier A', 'Fornecedor B / Supplier B', 'Fornecedor C / Supplier C',
                    'Fornecedor D / Supplier D', 'Fornecedor E / Supplier E', 'Fornecedor F / Supplier F']
    criterios = list(descricao_criterios.keys())
    criterios_qualitativos = list(escala_qualitativa.keys())
    
    col1, col2 = st.columns(2)
    with col1:
        fornecedores_selecionados = st.multiselect(
            "Selecione os fornecedores / Select the suppliers:",
            fornecedores,
            default=fornecedores[:3]
        )
    
    with col2:
        criterios_selecionados = st.multiselect(
            "Selecione os critérios / Select the criteria:",
            criterios,
            default=criterios[:3]
        )
    
    if len(fornecedores_selecionados) < 2:
        st.warning("Selecione pelo menos dois fornecedores para prosseguir / Please select at least two suppliers to proceed.")
        st.stop()
    
    if not criterios_selecionados:
        st.warning("Selecione ao menos um critério para prosseguir / Please select at least one criterion to proceed.")
        st.stop()
    
    # Configuração dos critérios
    st.subheader("Configuração dos Critérios / / Criteria Settings")
    
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
    if st.button("Calcular Ranking PROMETHEE II / / Run PROMETHEE II Ranking"):
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
        st.subheader("Resultados PROMETHEE II / / PROMETHEE II Results")
        
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
        st.subheader("Visualização do Fluxo Líquido / Net Flow Chart")
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