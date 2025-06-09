import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="German Credit Data Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para melhorar a estética
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size: 2rem;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
    }
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    .insight-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .info-box {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f8f9fa;
        border-radius: 10px 10px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
        border: 2px solid #e9ecef;
        color: #4f4f4f;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-color: #667eea;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
</style>
""", unsafe_allow_html=True)

# Função para carregar dados
@st.cache_data
def load_data():
    df = pd.read_csv("german_credit_data_treated.csv")
    return df

# Carregar dados
df = load_data()

# Título principal
st.markdown('<h1 class="main-header">German Credit Data Dashboard</h1>', unsafe_allow_html=True)

# Informações sobre o dataset
st.markdown("""
<div class="info-box">
<h3>Sobre o Dataset</h3>
Este dashboard apresenta uma análise abrangente do dataset Statlog (German Credit Data) da UCI Machine Learning Repository.
O dataset contém informações sobre 1.000 solicitantes de crédito alemães, classificados como bom ou mau risco de crédito
com base em 20 atributos diferentes.
</div>
""", unsafe_allow_html=True)

# Sidebar com filtros
st.sidebar.markdown("## Filtros")

risk_filter = st.sidebar.multiselect(
    "Selecione o tipo de risco:",
    options=df['risk'].unique(),
    default=df['risk'].unique()
)

age_range = st.sidebar.slider(
    "Faixa etária:",
    min_value=int(df['age_in_years'].min()),
    max_value=int(df['age_in_years'].max()),
    value=(int(df['age_in_years'].min()), int(df['age_in_years'].max()))
)

credit_range = st.sidebar.slider(
    "Valor do crédito (DM):",
    min_value=int(df['credit_amount'].min()),
    max_value=int(df['credit_amount'].max()),
    value=(int(df['credit_amount'].min()), int(df['credit_amount'].max()))
)

# Aplicar filtros
if not risk_filter:
    filtered_df = pd.DataFrame()
else:
    filtered_df = df[
        (df['risk'].isin(risk_filter)) &
        (df['age_in_years'] >= age_range[0]) &
        (df['age_in_years'] <= age_range[1]) &
        (df['credit_amount'] >= credit_range[0]) &
        (df['credit_amount'] <= credit_range[1])
    ]

st.sidebar.markdown(f"**Registros exibidos:** {len(filtered_df)} de {len(df)}")

# --- Seção principal ---
if filtered_df.empty:
    st.warning("Por favor, selecione ao menos um tipo de risco ou ajuste os filtros para exibir dados.")
else:
    # Métricas principais
    st.markdown('<h2 class="sub-header">Métricas Principais</h2>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{len(filtered_df):,}</div>
            <div class="metric-label">Total de Solicitantes</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        good_risk_pct = (filtered_df['risk'] == 'Good Risk').sum() / len(filtered_df) * 100 if 'Good Risk' in filtered_df['risk'].unique() else 0.0
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{good_risk_pct:.1f}%</div>
            <div class="metric-label">Bom Risco de Crédito</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        avg_age = filtered_df['age_in_years'].mean()
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{avg_age:.1f}</div>
            <div class="metric-label">Idade Média</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        avg_credit = filtered_df['credit_amount'].mean()
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{avg_credit:,.0f} DM</div>
            <div class="metric-label">Crédito Médio</div>
        </div>
        """, unsafe_allow_html=True)

    # Abas para organizar o conteúdo
    tab1, tab2, tab3, tab4 = st.tabs(["Análise de Risco", "Demografia", "Análise Financeira", "Características Sociais"])

    with tab1:
        st.markdown('<h2 class="sub-header">Análise de Risco de Crédito</h2>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            risk_counts = filtered_df['risk'].value_counts()
            fig_risk = px.pie(
                values=risk_counts.values,
                names=risk_counts.index,
                title="Distribuição de Risco de Crédito",
                color_discrete_map={'Good Risk': '#2ecc71', 'Bad Risk': '#e74c3c'}
            )
            fig_risk.update_traces(textposition='inside', textinfo='percent+label')
            fig_risk.update_layout(font=dict(size=14), showlegend=True, height=400)
            st.plotly_chart(fig_risk, use_container_width=True)

        with col2:
            # --- CORREÇÃO FINAL APLICADA AQUI ---
            # 1. Usamos 'labels' para que pd.cut já crie textos legíveis em vez de 'Intervals'
            age_bins = pd.cut(
                filtered_df['age_in_years'], 
                bins=5, 
                right=False, 
                labels=['18-30', '31-40', '41-50', '51-60', '61+']
            )
            
            # 2. Damos um nome à nossa série de faixas etárias para evitar o erro no .melt()
            age_bins.name = 'age_bins'
            
            risk_by_age = pd.crosstab(age_bins, filtered_df['risk'], normalize='index') * 100
            risk_by_age_long = risk_by_age.reset_index().melt(id_vars='age_bins', value_name='percentual', var_name='risk')

            fig_age_risk = px.bar(
                risk_by_age_long,
                x='age_bins',
                y='percentual',
                color='risk',
                title="Distribuição de Risco por Faixa Etária (%)",
                labels={'age_bins': 'Faixa Etária', 'percentual': 'Percentual (%)'},
                color_discrete_map={'Good Risk': '#2ecc71', 'Bad Risk': '#e74c3c'}
            )
            fig_age_risk.update_layout(barmode='stack', font=dict(size=14), height=400)
            st.plotly_chart(fig_age_risk, use_container_width=True)

        if 'Bad Risk' in filtered_df['risk'].unique():
            bad_risk_pct_val = (filtered_df['risk'] == 'Bad Risk').mean() * 100
            st.markdown(f"""
            <div class="insight-box">
            <h4>Insight Principal</h4>
            {bad_risk_pct_val:.1f}% dos solicitantes nos filtros atuais são classificados como mau risco.
            A análise por faixa etária tende a mostrar que clientes mais jovens têm maior proporção de mau risco.
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        st.markdown('<h2 class="sub-header">Análise Demográfica</h2>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            fig_age = px.histogram(
                filtered_df, x='age_in_years', nbins=20, title="Distribuição de Idade dos Solicitantes",
                labels={'age_in_years': 'Idade', 'count': 'Quantidade'}, color_discrete_sequence=['#3498db']
            )
            fig_age.update_layout(font=dict(size=14), height=400)
            st.plotly_chart(fig_age, use_container_width=True)

        with col2:
            personal_status_counts = filtered_df['personal_status_sex'].value_counts()
            fig_personal = px.bar(
                x=personal_status_counts.values, y=personal_status_counts.index, orientation='h',
                title="Status Pessoal e Sexo", labels={'x': 'Quantidade', 'y': 'Status'},
                color_discrete_sequence=['#9b59b6']
            )
            fig_personal.update_layout(font=dict(size=14), height=400)
            st.plotly_chart(fig_personal, use_container_width=True)

    with tab3:
        st.markdown('<h2 class="sub-header">Análise Financeira</h2>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            fig_credit = px.histogram(
                filtered_df, x='credit_amount', nbins=30, title="Distribuição do Valor do Crédito",
                labels={'credit_amount': 'Valor do Crédito (DM)', 'count': 'Quantidade'},
                color_discrete_sequence=['#f39c12']
            )
            fig_credit.update_layout(font=dict(size=14), height=400)
            st.plotly_chart(fig_credit, use_container_width=True)

        with col2:
            fig_scatter = px.scatter(
                filtered_df, x='credit_amount', y='duration_in_month', color='risk',
                title="Valor do Crédito vs Duração",
                labels={'credit_amount': 'Valor do Crédito (DM)', 'duration_in_month': 'Duração (meses)'},
                color_discrete_map={'Good Risk': '#2ecc71', 'Bad Risk': '#e74c3c'}
            )
            fig_scatter.update_layout(font=dict(size=14), height=400)
            st.plotly_chart(fig_scatter, use_container_width=True)

    with tab4:
        st.markdown('<h2 class="sub-header">Características Sociais</h2>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            purpose_counts = filtered_df['purpose'].value_counts()
            fig_purpose = px.bar(
                x=purpose_counts.values, y=purpose_counts.index, orientation='h', title="Propósito do Crédito",
                labels={'x': 'Quantidade', 'y': 'Propósito'}, color_discrete_sequence=['#1abc9c']
            )
            fig_purpose.update_layout(font=dict(size=14), height=500)
            st.plotly_chart(fig_purpose, use_container_width=True)

        with col2:
            housing_counts = filtered_df['housing_type'].value_counts()
            fig_housing = px.pie(
                values=housing_counts.values, names=housing_counts.index, title="Tipo de Habitação",
                color_discrete_sequence=['#ff6b6b', '#4ecdc4', '#45b7d1']
            )
            fig_housing.update_traces(textposition='inside', textinfo='percent+label')
            fig_housing.update_layout(font=dict(size=14), height=400)
            st.plotly_chart(fig_housing, use_container_width=True)

    # Seção de análise avançada
    st.markdown('<h2 class="sub-header">Análise Avançada</h2>', unsafe_allow_html=True)

    st.markdown('<h3>Análise de Risco por Características</h3>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        risk_by_purpose = pd.crosstab(filtered_df['purpose'], filtered_df['risk'], normalize='index') * 100
        risk_by_purpose_long = risk_by_purpose.reset_index().melt(id_vars='purpose', value_name='percentual', var_name='risk')

        fig_risk_purpose = px.bar(
            risk_by_purpose_long,
            x='purpose',
            y='percentual',
            color='risk',
            title="Distribuição de Risco por Propósito (%)",
            labels={'purpose': 'Propósito', 'percentual': 'Percentual (%)'},
            color_discrete_map={'Good Risk': '#2ecc71', 'Bad Risk': '#e74c3c'}
        )
        fig_risk_purpose.update_layout(barmode='stack', font=dict(size=12), height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig_risk_purpose, use_container_width=True)

    with col2:
        risk_by_employment = pd.crosstab(filtered_df['employment_status'], filtered_df['risk'], normalize='index') * 100
        risk_by_employment_long = risk_by_employment.reset_index().melt(id_vars='employment_status', value_name='percentual', var_name='risk')

        fig_risk_employment = px.bar(
            risk_by_employment_long,
            x='employment_status',
            y='percentual',
            color='risk',
            title="Distribuição de Risco por Status de Emprego (%)",
            labels={'employment_status': 'Status de Emprego', 'percentual': 'Percentual (%)'},
            color_discrete_map={'Good Risk': '#2ecc71', 'Bad Risk': '#e74c3c'}
        )
        fig_risk_employment.update_layout(barmode='stack', font=dict(size=12), height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig_risk_employment, use_container_width=True)

    # Rodapé
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #7f8c8d; font-size: 14px;">
        German Credit Data Dashboard | Desenvolvido com Streamlit e Plotly |
        Dados: UCI Machine Learning Repository
    </div>
    """, unsafe_allow_html=True)