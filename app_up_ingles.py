# ===================================
# Library Imports
# ===================================
import streamlit as st
import pandas as pd
import plotly.express as px
import math
import numpy as np

# When setting up, run in terminal: pip install streamlit pandas plotly
# streamlit run app_up_ingles.py

# ===================================
# Visual Style
# ===================================
st.set_page_config(page_title="DSS PROMETHEE II", layout="wide")

st.markdown(
    """
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
# Criteria Descriptions and Qualitative Scales
# ===================================
criteria_description = {
    'C1 - Cost': 'Monetary cost of the proposal.(↓)',
    'C2 - Quality': 'Subjective quality assessment based on benchmark standards. (↑)',
    'C3 - Delivery': 'Delivery time in days. (↓)',
    'C4 - Technology': 'Level of innovation and adoption of advanced technologies. (↑)',
    'C5 - Environmental Costs': 'Annual monetary value or percentage of revenue invested in environmental management (e.g., waste treatment, emissions control, certifications). (↓)',
    'C6 - Green Design': 'Degree of integration of sustainable design practices in the supplier’s products, services, or processes, including choice of materials, production methods, packaging, and lifecycle considerations. (↑)',
    'C7 - Environmental Management': 'Effectiveness of the environmental management system. (↑)',
    'C8 - Stakeholders Management': 'Commitment to stakeholder rights and service. (↑)',
    'C9 - Occupational Health and Safety': (
        'TRIR calculated according to OSHA methodology (Total Recordable Incident Rate). '
        'Value provided by the supplier or verified via audit/documentation. (↓)\n\n'
        'TRIR = (Total number of recordable incidents × 200,000) / Total hours worked by all employees.'
    ),
    'C10 - Compliance with Labor Policies': 'Adherence to employee rights, labor laws, and ethical workplace standards, including diversity, inclusion, and non-discrimination measures. Evidence may include labor policy documents, compliance certificates (e.g., SA8000), diversity reports, and complaint-handling procedures. (↑)',
    'C11 - Social Management': 'Capacity to develop and implement structured social responsibility policies and programs, including community engagement, partnerships with NGOs, and measurable contributions to social well-being. Evidence may include CSR reports, certifications (ISO 26000, SA8000), project portfolios, and investment data. (↑)',
    'C12 - Performance History': 'Number of years of experience. (↑)',
    'C13 - Reputation': 'Media analysis, reviews, and recognitions. (↑)',
    'C14 - Logistics': 'Distance in kilometers. (↓)'
}

qualitative_scale = {
    'C2 - Quality': """| Scale Level | Description |
|------|-------------|
| 1 | Products/services do not meet quality standards, leading to frequent rework and negative feedback. |
| 2 | Products/services generally below standard, with occasional issues and mostly negative feedback. |
| 3 | Products/services meet the minimum standard, with occasional problems and mixed feedback. |
| 4 | Products/services meet or exceed quality standards, with positive feedback and few rejections. |
| 5 | Exceptional products/services, consistently exceeding standards, with highly positive feedback and minimal rejections. |
""",

    'C4 - Technology': """| Scale Level | Description |
|------|-------------|
| 1 | No current technology used; manual processes dominate. |
| 2 | Low technology adoption, with minimal process improvements. |
| 3 | Moderate use of known technologies; standard efficiency. |
| 4 | High adoption of technologies, promoting efficiency gains. |
| 5 | Use of cutting-edge technologies and continuous innovation. |
""",

    'C6 - Green Design': """| Scale Level | Description |
|------|-------------|
| 1 | The supplier does not apply any sustainable design principles. Products/services are developed without consideration for environmental impacts, recyclability, or resource efficiency. |
| 2 | Minimal and occasional sustainable actions in design. Examples: limited use of recyclable materials or occasional waste reduction initiatives. No systematic approach. |
| 3 | Some sustainable design initiatives are present, such as partial use of eco-friendly materials, basic packaging reduction, or energy efficiency in certain processes. However, these are not applied consistently across all projects. |
| 4 | Sustainable design principles are incorporated in several key aspects of the supplier’s operations: consistent use of recyclable or renewable materials, reduced energy consumption, optimized packaging, and partial application of lifecycle assessment. |
| 5 | The supplier’s design approach is fully sustainability-oriented, integrating eco-design principles at every stage: product conception, material selection, manufacturing, packaging, and end-of-life. Includes full lifecycle assessment, zero-waste strategies, renewable energy use, and alignment with international eco-certifications. |
""",

    'C7 - Environmental Management': """| Scale Level | Description |
|------|-------------|
| 1 | No structured environmental management system. |
| 2 | Informal and ineffective system. |
| 3 | Basic system implemented with limitations. |
| 4 | Well-structured system in compliance with standards. |
| 5 | Robust, certified system with continuous improvement. |
""",

    'C8 - Stakeholders Management': """| Scale Level | Description |
|------|-------------|
| 1 | Ignores stakeholder interests. |
| 2 | Reactively and minimally responsive. |
| 3 | Minimal stakeholder engagement. |
| 4 | Commitment to active engagement policies. |
| 5 | Transparent, active, and responsible stakeholder involvement. |
""",

    'C10 - Compliance with Labor Policies': """| Scale Level | Description |
|------|-------------|
| 1 | No formal labor policies; repeated violations in last 3 years. |
| 2 | Minimal/incomplete policies; limited diversity/inclusion; minor violations. |
| 3 | Basic policies covering essential rights; some diversity efforts; no serious violations. |
| 4 | Comprehensive policies aligned with law; active diversity programs; no violations. |
| 5 | Exemplary policies exceeding legal requirements; diversity and inclusion embedded in culture; recognized certifications or awards. |
""",

    'C11 - Social Management': """| Scale Level | Description |
|------|-------------|
| 1 | No CSR policies or social initiatives. |
| 2 | Limited or reactive initiatives with minimal documentation. |
| 3 | Some structured social programs, but inconsistent execution or limited scope. |
| 4 | Comprehensive CSR policies with consistent community engagement and documented results. |
| 5 | Strategic, certified, and impactful CSR programs integrated into corporate culture. |
""",

    'C13 - Reputation': """| Scale Level | Description |
|------|-------------|
| 1 | Very negative or unknown reputation. |
| 2 | Unfavorable or unstable market image. |
| 3 | Acceptable reputation, no major highlights. |
| 4 | Good reputation with consistent positive evaluations. |
| 5 | Excellent reputation, widely recognized in the industry. |
"""
}

# ===================================
# PROMETHEE II Calculation
# ===================================
def compute_promethee_without_normalizing(df, criteria, objective, weights, functions, parameters):
    alternatives = df.index.tolist()
    n = len(alternatives)
    total_weight = sum(weights.values())

    # Initialize matrices
    d_matrix = {crit: np.zeros((n, n)) for crit in criteria}
    pref_matrix = {crit: np.zeros((n, n)) for crit in criteria}
    aggregated_matrix = np.zeros((n, n))

    # Steps 1 & 2: compute d(a,b) and apply F_j(a,b)
    for c_idx, crit in enumerate(criteria):
        for i, a in enumerate(alternatives):
            for j, b in enumerate(alternatives):
                if i == j:
                    continue

                # Direct difference of values (no normalization)
                d = df.loc[a, crit] - df.loc[b, crit]

                # Invert if criterion is minimization
                if objective[crit] == 'Minimize':
                    d = -d

                d_matrix[crit][i][j] = d

                # Parameters q, p, s
                q = parameters[crit].get('q', 0)
                p = parameters[crit].get('p', 0)
                s = parameters[crit].get('s', 1)
                func = functions[crit]

                # Apply F_j according to type
                if func == 'Usual':
                    pref = 1 if d > 0 else 0
                elif func == 'U-Shape':
                    pref = 1 if d > q else 0
                elif func == 'V-Shape':
                    if d <= 0:
                        pref = 0
                    elif d <= p:
                        pref = d / p
                    else:
                        pref = 1
                elif func == 'Level':
                    if d <= q:
                        pref = 0
                    elif d <= p:
                        pref = 0.5
                    else:
                        pref = 1
                elif func == 'V-Shape with Indifference':
                    if d <= q:
                        pref = 0
                    elif d <= p:
                        pref = (d - q) / (p - q)
                    else:
                        pref = 1
                elif func == 'Gaussian':
                    pref = 1 - math.exp(-(d ** 2) / (2 * s ** 2)) if d > 0 else 0
                else:
                    pref = 0

                pref_matrix[crit][i][j] = pref
                aggregated_matrix[i][j] += weights[crit] * pref

    # Step 3: aggregated preference matrix (divide by total weight)
    aggregated_matrix /= total_weight

    # Step 4: flows
    positive_flow = aggregated_matrix.sum(axis=1) / (n - 1)
    negative_flow = aggregated_matrix.sum(axis=0) / (n - 1)
    net_flow = positive_flow - negative_flow

    # Final ranking
    result = pd.DataFrame({
        'Supplier': alternatives,
        'Positive Flow (ϕ+)': positive_flow,
        'Negative Flow (ϕ-)': negative_flow,
        'Net Flow (ϕ)': net_flow
    })
    result = result.sort_values('Net Flow (ϕ)', ascending=False)
    result['Ranking'] = range(1, len(result) + 1)

    return result, d_matrix, pref_matrix, aggregated_matrix

# ===================================
# Home Screen
# ===================================
def home_screen():
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("./pmd.jpg", caption="Project Management Group", width=215)

    with col2:
        st.markdown(
            "<div class='gray-background' ><h1>Decision Support System for the Selection of Sustainable Suppliers in Projects</h1></div>",
            unsafe_allow_html=True
        )

    st.write(
        "Welcome to the Decision Support System, designed to assist companies in selecting sustainable suppliers, "
        "considering economic, social, and environmental criteria."
    )

    st.write(
        "This system was developed at the Project Management and Development Research Group laboratory of the "
        "Department of Production Engineering at the Federal University of Pernambuco (UFPE)."
    )

    st.markdown(
        "<div class='gray-background'><h5>Meet the team behind the development of this solution:</h5></div>",
        unsafe_allow_html=True
    )

    st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

    dev1_col, dev2_col, dev3_col = st.columns(3)
    with dev1_col:
        st.image("./Luciana.jpg", width=200)
        st.markdown("<p style='color: black;'>Prof. Dr. Luciana Hazin Alencar</p>", unsafe_allow_html=True)
    with dev2_col:
        st.image("./marilia.jpg", width=200)
        st.markdown("<p style='color: black;'>MSc Marília Martins</p>", unsafe_allow_html=True)
    with dev3_col:
        st.image("./maria.jpg", width=200)
        st.markdown("<p style='color: black;'>Maria Geyzianny</p>", unsafe_allow_html=True)

# ===================================
# PROMETHEE II System Screen
# ===================================
def promethee_screen():
    st.title("Decision Support System for the Selection of Sustainable Suppliers - PROMETHEE II")
    
    # Explanation of preference functions
    with st.expander("ℹ️ Explanation of Preference Functions"):
        st.markdown("""
**Types of Preference Functions:**

1. **Usual (Type 1)**: Any performance difference, even minimal, is enough to indicate a preference.
2. **U-Shape (Type 2)**: Preference arises only after the performance difference exceeds a threshold **q**.
3. **V-Shape (Type 3)**: Small performance gaps lead to a gradually increasing preference up to threshold **p**.
4. **Level (Type 4)**: There is a range where the difference results in a partial preference (between **q** and **p**).
5. **V-Shape with Indifference (Type 5)**: Within the indifference zone (**q**), no preference; beyond it, preference grows up to **p**.
6. **Gaussian (Type 6)**: Preference follows a Gaussian curve based on parameter **s**.
""")
    
    # Supplier and criteria selection
    suppliers = [
        'Supplier A', 'Supplier B', 'Supplier C',
        'Supplier D', 'Supplier E', 'Supplier F'
    ]
    criteria = list(criteria_description.keys())
    qualitative_criteria = list(qualitative_scale.keys())
    
    col1, col2 = st.columns(2)
    with col1:
        selected_suppliers = st.multiselect(
            "Select the suppliers:",
            suppliers,
            default=suppliers[:3]
        )
    
    with col2:
        selected_criteria = st.multiselect(
            "Select the criteria:",
            criteria,
            default=criteria[:3]
        )
    
    if len(selected_suppliers) < 2:
        st.warning("Please select at least two suppliers to proceed.")
        st.stop()
    
    if not selected_criteria:
        st.warning("Please select at least one criterion to proceed.")
        st.stop()
    
    # Criteria configuration
    st.subheader("Criteria Settings")
    
    weights = {}
    objective = {}
    preference_functions = {}
    preference_parameters = {}
    performance = {sup: {} for sup in selected_suppliers}
    
    for criterion in selected_criteria:
        with st.expander(f"Settings for criterion: {criterion}"):
            st.info(criteria_description[criterion])
            
            if criterion in qualitative_criteria:
                st.markdown("**Qualitative Scale:**")
                st.markdown(qualitative_scale[criterion])
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                weights[criterion] = st.number_input(
                    f"Weight for {criterion}",
                    min_value=0.0,
                    value=1.0,
                    step=0.1,
                    key=f"weight_{criterion}"
                )
            
            with col2:
                objective[criterion] = st.radio(
                    f"Objective of the criterion {criterion}:",
                    ['Maximize', 'Minimize'],
                    index=0 if '↓' not in criteria_description[criterion] else 1,
                    horizontal=True,
                    key=f"objective_{criterion}"
                )
            
            with col3:
                preference_functions[criterion] = st.selectbox(
                    f"Preference function for {criterion}",
                    [
                        'Usual',
                        'U-Shape',
                        'V-Shape',
                        'Level',
                        'V-Shape with Indifference',
                        'Gaussian'
                    ],
                    key=f"function_{criterion}"
                )
            
            # Function-specific parameters
            params = {}
            func = preference_functions[criterion]
            
            if func in ['U-Shape', 'Level', 'V-Shape with Indifference']:
                params['q'] = st.number_input(
                    f"Indifference threshold (q) for {criterion}",
                    min_value=0.0,
                    value=0.1,
                    step=0.01,
                    key=f"q_{criterion}"
                )
            
            if func in ['V-Shape', 'Level', 'V-Shape with Indifference']:
                params['p'] = st.number_input(
                    f"Preference threshold (p) for {criterion}",
                    min_value=0.0,
                    value=0.5,
                    step=0.01,
                    key=f"p_{criterion}"
                )
            
            if func == 'Gaussian':
                params['s'] = st.number_input(
                    f"Parameter s (standard deviation) for {criterion}",
                    min_value=0.01,
                    value=0.5,
                    step=0.01,
                    key=f"s_{criterion}"
                )
            
            preference_parameters[criterion] = params
            
            # Suppliers' performance input
            st.markdown("**Supplier evaluation:**")
            
            if criterion in qualitative_criteria:
                for sup in selected_suppliers:
                    performance[sup][criterion] = st.slider(
                        f"{sup} on {criterion} (1-5)",
                        1, 5, 3,
                        key=f"eval_{sup}_{criterion}"
                    )
            else:
                cols = st.columns(len(selected_suppliers))
                for i, sup in enumerate(selected_suppliers):
                    with cols[i]:
                        performance[sup][criterion] = st.number_input(
                            f"{sup}",
                            min_value=0.0,
                            step=0.1,
                            key=f"eval_{sup}_{criterion}"
                        )
    
    # Parameter validation
    for crit in selected_criteria:
        func = preference_functions[crit]
        params = preference_parameters[crit]
        
        if func in ['Level', 'V-Shape with Indifference']:
            if params['p'] <= params['q']:
                st.error(f"For criterion {crit}, the preference threshold (p) must be GREATER than the indifference threshold (q).")
                st.stop()
        
        if func == 'Gaussian' and params.get('s', 1) <= 0:
            st.error(f"For criterion {crit}, parameter s must be POSITIVE.")
            st.stop()
    
    # Build performance dataframe
    df = pd.DataFrame(performance).T
    
    # Criteria summary table
    st.subheader("Configured Criteria Summary")
    
    criteria_summary = pd.DataFrame({
        'Criterion': selected_criteria,
        'Objective': [objective[crit] for crit in selected_criteria],
        'Preference Function': [preference_functions[crit] for crit in selected_criteria],
        'Weight': [weights[crit] for crit in selected_criteria],
        'q (Indifference)': [preference_parameters[crit].get('q', '-') for crit in selected_criteria],
        'p (Preference)': [preference_parameters[crit].get('p', '-') for crit in selected_criteria],
        's (Gaussian)': [preference_parameters[crit].get('s', '-') for crit in selected_criteria]
    })
    
    st.dataframe(criteria_summary)
    
    # Show performance matrix
    st.subheader("Performance Matrix")
    st.dataframe(df.style.background_gradient(cmap='Blues'))
    
    # Compute button
    if st.button("Run PROMETHEE II Ranking"):
        with st.spinner("Computing ranking..."):
            result, d_matrix, pref_matrix, aggregated_pref = compute_promethee_without_normalizing(
                df,
                selected_criteria,
                objective,
                weights,
                preference_functions,
                preference_parameters
            )
        
        n = len(result)
        
        # Show results
        st.subheader("PROMETHEE II Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Final Ranking**")
            st.dataframe(
                result.style.format({
                    'Positive Flow (ϕ+)': "{:.4f}",
                    'Negative Flow (ϕ-)': "{:.4f}",
                    'Net Flow (ϕ)': "{:.4f}"
                }).background_gradient(subset=['Net Flow (ϕ)'], cmap='RdYlGn')
            )
        
        with col2:
            st.markdown("**Preference Relations**")
            for i in range(len(result)):
                a = result.iloc[i]['Supplier']
                flux_a = result.iloc[i]['Net Flow (ϕ)']
                
                for j in range(i + 1, len(result)):
                    b = result.iloc[j]['Supplier']
                    flux_b = result.iloc[j]['Net Flow (ϕ)']
                    
                    if abs(flux_a - flux_b) < 0.0001:  # Indifference
                        st.write(f"🔹 {a} I {b} (Indifferent)")
                    elif flux_a > flux_b:
                        st.write(f"✅ {a} P {b} (Preference)")
                    else:
                        st.write(f"✅ {b} P {a} (Preference)")
        
        # Bar chart
        st.subheader("Net Flow Chart")
        fig = px.bar(
            result,
            x='Supplier',
            y='Net Flow (ϕ)',
            color='Supplier',
            title='PROMETHEE II Ranking - Net Flow',
            text='Net Flow (ϕ)',
            color_discrete_sequence=px.colors.qualitative.Plotly
        )
        fig.update_traces(texttemplate='%{text:.3f}', textposition='outside')
        fig.update_layout(
            yaxis_range=[-1, 1],
            yaxis_title='Net Flow (ϕ)',
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # d(a,b) matrices by criterion
        st.subheader("Difference Matrices d(a,b) by Criterion")
        for crit in selected_criteria:
            st.markdown(f"**Criterion: {crit}**")
            df_diff = pd.DataFrame(
                d_matrix[crit],
                index=result['Supplier'],
                columns=result['Supplier']
            )
            st.dataframe(df_diff.style.format("{:.4f}").background_gradient(cmap='PuBu'))

        # Aggregated preference matrix
        st.subheader("Aggregated Preference Matrix")
        df_pref = pd.DataFrame(
            aggregated_pref,
            index=result['Supplier'],
            columns=result['Supplier']
        )
        st.write("Matrix π(a, b) – Degree of preference of a over b:")
        st.dataframe(df_pref.style.format("{:.4f}").background_gradient(cmap='Oranges'))

        # Final net flow matrix π(a,b) - π(b,a)
        st.subheader("Final Net Flow Matrix (ϕ(a,b))")
        net_flow_matrix = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                net_flow_matrix[i][j] = aggregated_pref[i][j] - aggregated_pref[j][i]
        
        df_net_flow = pd.DataFrame(
            net_flow_matrix,
            index=result['Supplier'],
            columns=result['Supplier']
        )
        st.dataframe(df_net_flow.style.format("{:.4f}").background_gradient(cmap='RdBu', axis=None))

        # "Normalized" differences per criterion (as preference degrees per function)
        st.subheader("Normalized Difference Matrices d(a,b) by Criterion")
        for crit in selected_criteria:
            st.markdown(f"**Criterion: {crit}**")
            pref_crit = np.zeros((n, n))
            for i in range(n):
                for j in range(n):
                    d = df.loc[result['Supplier'].iloc[i], crit] - df.loc[result['Supplier'].iloc[j], crit]
                    if objective[crit] == 'Minimize':
                        d = -d

                    q = preference_parameters[crit].get('q', 0)
                    p = preference_parameters[crit].get('p', 0)
                    s = preference_parameters[crit].get('s', 1)
                    func = preference_functions[crit]

                    if func == 'Usual':
                        pref = 1 if d > 0 else 0
                    elif func == 'U-Shape':
                        pref = 1 if d > q else 0
                    elif func == 'V-Shape':
                        if d <= 0:
                            pref = 0
                        elif d <= p:
                            pref = d / p
                        else:
                            pref = 1
                    elif func == 'Level':
                        if d <= q:
                            pref = 0
                        elif d <= p:
                            pref = 0.5
                        else:
                            pref = 1
                    elif func == 'V-Shape with Indifference':
                        if d <= q:
                            pref = 0
                        elif d <= p:
                            pref = (d - q) / (p - q)
                        else:
                            pref = 1
                    elif func == 'Gaussian':
                        pref = 1 - math.exp(-(d ** 2) / (2 * s ** 2)) if d > 0 else 0
                    else:
                        pref = 0

                    pref_crit[i][j] = pref

            # NOTE: This mirrors your original structure: build and display after the loop.
            df_pi = pd.DataFrame(
                pref_crit,
                index=result['Supplier'],
                columns=result['Supplier']
            )
            st.dataframe(df_pi.style.format("{:.4f}").background_gradient(cmap='OrRd'))

# ===================================
# Routing
# ===================================
def main():
    menu = ["Home", "PROMETHEE II System"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Home":
        home_screen()
    elif choice == "PROMETHEE II System":
        promethee_screen()

if __name__ == "__main__":
    main()

