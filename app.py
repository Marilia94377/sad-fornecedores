import streamlit as st
import pandas as pd
import numpy as np

def calcular_preferencia(avaliacoes, pesos):
    # Normalizar as avaliações se necessário (exemplo simples de normalização)
    maximos = np.max(avaliacoes, axis=0)
    minimos = np.min(avaliacoes, axis=0)
    
    avaliacoes_normalizadas = (avaliacoes - minimos) / (maximos - minimos)
    
    # Aplicar pesos
    avaliacoes_ponderadas = avaliacoes_normalizadas * pesos
    
    # Somar os valores ponderados para cada fornecedor
    pontuacao_final = np.sum(avaliacoes_ponderadas, axis=1)
    
    return pontuacao_final

def gerar_relatorio():
    st.title("Relatório de Resultados")

    if 'fornecedores' in st.session_state and 'criterios' in st.session_state:
        if st.session_state.fornecedores and st.session_state.criterios:
            # Mostrar tabela com as avaliações
            st.subheader("Tabela de Avaliações")
            avaliacoes = {fornecedor['Nome']: fornecedor['Avaliações'] for fornecedor in st.session_state.fornecedores}
            df_avaliacoes = pd.DataFrame(avaliacoes).T
            st.dataframe(df_avaliacoes)

            # Mostrar tabela com os pesos dos critérios
            st.subheader("Pesos dos Critérios")
            df_pesos = pd.DataFrame(st.session_state.criterios)
            st.dataframe(df_pesos[['Critério', 'Peso']])

            # Calcular pontuações novamente para mostrar no relatório
            pesos = [criterio['Peso'] for criterio in st.session_state.criterios]
            avaliacoes_np = df_avaliacoes.values
            pontuacoes = calcular_preferencia(avaliacoes_np, pesos)

            # Exibir pontuações e ranking final
            st.subheader("Pontuações e Ranking Final")
            resultados = sorted(zip(st.session_state.fornecedores, pontuacoes), key=lambda x: x[1], reverse=True)
            for rank, (fornecedor, pontuacao) in enumerate(resultados, start=1):
                st.write(f"{rank}. {fornecedor['Nome']} - Pontuação: {pontuacao:.2f}")

            # Exportar relatório para CSV
            if st.button("Exportar Relatório"):
                df_relatorio = df_avaliacoes.copy()
                df_relatorio['Pontuação'] = pontuacoes
                df_relatorio.to_csv('relatorio_selecao_fornecedores.csv')
                st.success("Relatório exportado com sucesso!")

        else:
            st.warning("Adicione fornecedores e critérios antes de gerar o relatório.")
    else:
        st.warning("Adicione fornecedores e critérios antes de gerar o relatório.")

def main():
    st.sidebar.title("Navegação")
    menu = ["Home", "Seleção de Serviço/Material", "Alternativas de Fornecedores", "Critérios de Avaliação", "Avaliação das Alternativas", "Análise de Sensibilidade", "Relatório de Resultados"]	
    choice = st.sidebar.selectbox("Escolha a seção", menu)

    if choice == "Relatório de Resultados":
        gerar_relatorio()

    if choice == "Home":
        st.title("Seleção de Fornecedores")
        st.write("Bem-vindo ao sistema de seleção de fornecedores.")
    
    elif choice == "Seleção de Serviço/Material":
        st.title("Seleção de Serviço ou Material")
        st.write("Aqui você pode especificar o serviço ou material a ser adquirido.")
    
    elif choice == "Alternativas de Fornecedores":
        st.title("Alternativas de Fornecedores")

        if 'fornecedores' not in st.session_state:
            st.session_state.fornecedores = []

        with st.form(key='fornecedor_form'):
            nome = st.text_input("Nome do Fornecedor")
            historico = st.text_area("Histórico do Fornecedor")
            localizacao = st.text_input("Localização")
            submit_button = st.form_submit_button(label="Adicionar Fornecedor")

            if submit_button:
                fornecedor = {"Nome": nome, "Histórico": historico, "Localização": localizacao}
                st.session_state.fornecedores.append(fornecedor)
                st.success("Fornecedor adicionado com sucesso!")

        if st.session_state.fornecedores:
            st.subheader("Lista de Fornecedores")
            df_fornecedores = pd.DataFrame(st.session_state.fornecedores)
            st.dataframe(df_fornecedores)

            for i, fornecedor in enumerate(st.session_state.fornecedores):
                if st.button(f"Remover {fornecedor['Nome']}", key=f"remove_{i}"):
                    st.session_state.fornecedores.pop(i)
                    st.experimental_rerun()

        else:
            st.write("Nenhum fornecedor adicionado ainda.")
    
    elif choice == "Critérios de Avaliação":
        st.title("Critérios de Avaliação")

        if 'criterios' not in st.session_state:
            st.session_state.criterios = []

        with st.form(key='criterio_form'):
            criterio = st.text_input("Nome do Critério")
            peso = st.slider("Peso do Critério (0 a 5)", 0, 5, 3)
            tipo = st.selectbox("Tipo de Critério", ["Qualitativo", "Quantitativo"])
            submit_button = st.form_submit_button(label="Adicionar Critério")

            if submit_button:
                novo_criterio = {"Critério": criterio, "Peso": peso, "Tipo": tipo}
                st.session_state.criterios.append(novo_criterio)
                st.success("Critério adicionado com sucesso!")

        if st.session_state.criterios:
            st.subheader("Lista de Critérios")
            df_criterios = pd.DataFrame(st.session_state.criterios)
            st.dataframe(df_criterios)
        else:
            st.write("Nenhum critério adicionado ainda.")
    
    elif choice == "Avaliação das Alternativas":
        st.title("Avaliação das Alternativas")

        if 'fornecedores' in st.session_state and 'criterios' in st.session_state:
            if st.session_state.fornecedores and st.session_state.criterios:
                avaliacoes = []
                pesos = [criterio['Peso'] for criterio in st.session_state.criterios]

                for fornecedor in st.session_state.fornecedores:
                    st.subheader(f"Avaliação para {fornecedor['Nome']}")
                    avaliacoes_fornecedor = []
                    for criterio in st.session_state.criterios:
                        if criterio["Tipo"] == "Quantitativo":
                            avaliacao = st.number_input(f"{criterio['Critério']} ({criterio['Tipo']})", min_value=0.0, key=f"{fornecedor['Nome']}_{criterio['Critério']}")
                        else:
                            avaliacao = st.slider(f"{criterio['Critério']} ({criterio['Tipo']})", 0, 5, key=f"{fornecedor['Nome']}_{criterio['Critério']}")
                        avaliacoes_fornecedor.append(avaliacao)
                    avaliacoes.append(avaliacoes_fornecedor)
                
                # Converter para numpy array para cálculos
                avaliacoes_np = np.array(avaliacoes)
                
                # Calcular pontuação final
                pontuacoes = calcular_preferencia(avaliacoes_np, pesos)

                # Exibir resultados
                for i, fornecedor in enumerate(st.session_state.fornecedores):
                    st.write(f"Pontuação final para {fornecedor['Nome']}: {pontuacoes[i]:.2f}")
                
                # Ordenar fornecedores com base na pontuação final
                resultados = sorted(zip(st.session_state.fornecedores, pontuacoes), key=lambda x: x[1], reverse=True)

                # Exibir o ranking final
                st.subheader("Ranking Final")
                for rank, (fornecedor, pontuacao) in enumerate(resultados, start=1):
                    st.write(f"{rank}. {fornecedor['Nome']} - Pontuação: {pontuacao:.2f}")
            else:
                st.warning("Adicione fornecedores e critérios antes de realizar a avaliação.")
        else:
            st.warning("Adicione fornecedores e critérios antes de realizar a avaliação.")

    elif choice == "Análise de Sensibilidade":
        st.title("Análise de Sensibilidade")
        
        if 'fornecedores' in st.session_state and 'criterios' in st.session_state:
            if st.session_state.fornecedores and st.session_state.criterios:
                # Interface para ajustar os pesos dos critérios
                st.subheader("Ajuste os Pesos dos Critérios")
                novos_pesos = []
                for criterio in st.session_state.criterios:
                    novo_peso = st.slider(f"{criterio['Critério']} (Peso Atual: {criterio['Peso']})", 0, 5, criterio['Peso'])
                    novos_pesos.append(novo_peso)
                
                if st.button("Recalcular Pontuações"):
                    # Recalcular pontuações com novos pesos
                    avaliacoes = []
                    for fornecedor in st.session_state.fornecedores:
                        avaliacoes_fornecedor = [fornecedor['Avaliações'][criterio['Critério']] for criterio in st.session_state.criterios]
                        avaliacoes.append(avaliacoes_fornecedor)
                    
                    avaliacoes_np = np.array(avaliacoes)
                    pontuacoes = calcular_preferencia(avaliacoes_np, novos_pesos)

                    # Exibir os resultados recalculados
                    for i, fornecedor in enumerate(st.session_state.fornecedores):
                        st.write(f"Nova pontuação para {fornecedor['Nome']}: {pontuacoes[i]:.2f}")
                    
                    # Ordenar fornecedores com base na nova pontuação final
                    resultados = sorted(zip(st.session_state.fornecedores, pontuacoes), key=lambda x: x[1], reverse=True)

                    # Exibir o novo ranking final
                    st.subheader("Novo Ranking Final")
                    for rank, (fornecedor, pontuacao) in enumerate(resultados, start=1):
                        st.write(f"{rank}. {fornecedor['Nome']} - Nova Pontuação: {pontuacao:.2f}")
            else:
                st.warning("Adicione fornecedores e critérios antes de realizar a análise de sensibilidade.")
        else:
            st.warning("Adicione fornecedores e critérios antes de realizar a análise de sensibilidade.")

if __name__ == "__main__":
    main()
