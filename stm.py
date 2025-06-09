import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

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

# Filtro de risco
risk_filter = st.sidebar.multiselect(
    "Selecione o tipo de risco:",
    options=df['risk'].unique(),
    default=df['risk'].unique()
)

# Filtro de idade
age_range = st.sidebar.slider(
    "Faixa etária:",
    min_value=int(df['age_in_years'].min()),
    max_value=int(df['age_in_years'].max()),
    value=(int(df['age_in_years'].min()), int(df['age_in_years'].max()))
)

# Filtro de valor do crédito
credit_range = st.sidebar.slider(
    "Valor do crédito (DM):",
    min_value=int(df['credit_amount'].min()),
    max_value=int(df['credit_amount'].max()),
    value=(int(df['credit_amount'].min()), int(df['credit_amount'].max()))
)

# Aplicar filtros
filtered_df = df[
    (df['risk'].isin(risk_filter)) &
    (df['age_in_years'] >= age_range[0]) &
    (df['age_in_years'] <= age_range[1]) &
    (df['credit_amount'] >= credit_range[0]) &
    (df['credit_amount'] <= credit_range[1])
]

st.sidebar.markdown(f"**Registros exibidos:** {len(filtered_df)} de {len(df)}")

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
    good_risk_pct = (filtered_df['risk'] == 'Good Risk').mean() * 100
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
        # Distribuição de risco
        risk_counts = filtered_df['risk'].value_counts()
        fig_risk = px.pie(
            values=risk_counts.values,
            names=risk_counts.index,
            title="Distribuição de Risco de Crédito",
            color_discrete_sequence=['#2ecc71', '#e74c3c']
        )
        fig_risk.update_traces(textposition='inside', textinfo='percent+label')
        fig_risk.update_layout(
            font=dict(size=14),
            showlegend=True,
            height=400
        )
        st.plotly_chart(fig_risk, use_container_width=True)
    
    with col2:
        # Risco por faixa etária
        age_bins = pd.cut(filtered_df['age_in_years'], bins=5, labels=['18-30', '31-40', '41-50', '51-60', '61+'])
        risk_by_age = pd.crosstab(age_bins, filtered_df['risk'], normalize='index') * 100
        
        fig_age_risk = px.bar(
            x=risk_by_age.index,
            y=[risk_by_age['Good Risk'], risk_by_age['Bad Risk']],
            title="Distribuição de Risco por Faixa Etária (%)",
            labels={'x': 'Faixa Etária', 'y': 'Percentual'},
            color_discrete_sequence=['#2ecc71', '#e74c3c']
        )
        fig_age_risk.update_layout(
            barmode='stack',
            font=dict(size=14),
            height=400
        )
        st.plotly_chart(fig_age_risk, use_container_width=True)
    
    # Insight sobre risco
    bad_risk_pct = (filtered_df['risk'] == 'Bad Risk').mean() * 100
    st.markdown(f"""
    <div class="insight-box">
    <h4>💡 Insight Principal</h4>
    {bad_risk_pct:.1f}% dos solicitantes são classificados como mau risco de crédito. 
    A análise por faixa etária mostra que clientes mais jovens (18-30 anos) tendem a ter maior proporção de mau risco.
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.markdown('<h2 class="sub-header">Análise Demográfica</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribuição de idade
        fig_age = px.histogram(
            filtered_df,
            x='age_in_years',
            nbins=20,
            title="Distribuição de Idade dos Solicitantes",
            labels={'age_in_years': 'Idade', 'count': 'Quantidade'},
            color_discrete_sequence=['#3498db']
        )
        fig_age.update_layout(
            font=dict(size=14),
            height=400
        )
        st.plotly_chart(fig_age, use_container_width=True)
    
    with col2:
        # Status pessoal e sexo
        personal_status_counts = filtered_df['personal_status_sex'].value_counts()
        fig_personal = px.bar(
            x=personal_status_counts.values,
            y=personal_status_counts.index,
            orientation='h',
            title="Status Pessoal e Sexo",
            labels={'x': 'Quantidade', 'y': 'Status'},
            color_discrete_sequence=['#9b59b6']
        )
        fig_personal.update_layout(
            font=dict(size=14),
            height=400
        )
        st.plotly_chart(fig_personal, use_container_width=True)
    
    # Estatísticas demográficas
    st.markdown(f"""
    <div class="insight-box">
    <h4>Estatísticas Demográficas</h4>
    • Idade média: {filtered_df['age_in_years'].mean():.1f} anos<br>
    • Idade mínima: {filtered_df['age_in_years'].min()} anos<br>
    • Idade máxima: {filtered_df['age_in_years'].max()} anos<br>
    • Desvio padrão da idade: {filtered_df['age_in_years'].std():.1f} anos
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.markdown('<h2 class="sub-header">Análise Financeira</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribuição do valor do crédito
        fig_credit = px.histogram(
            filtered_df,
            x='credit_amount',
            nbins=30,
            title="Distribuição do Valor do Crédito",
            labels={'credit_amount': 'Valor do Crédito (DM)', 'count': 'Quantidade'},
            color_discrete_sequence=['#f39c12']
        )
        fig_credit.update_layout(
            font=dict(size=14),
            height=400
        )
        st.plotly_chart(fig_credit, use_container_width=True)
    
    with col2:
        # Relação entre valor do crédito e duração
        fig_scatter = px.scatter(
            filtered_df,
            x='credit_amount',
            y='duration_in_month',
            color='risk',
            title="Valor do Crédito vs Duração",
            labels={'credit_amount': 'Valor do Crédito (DM)', 'duration_in_month': 'Duração (meses)'},
            color_discrete_sequence=['#2ecc71', '#e74c3c']
        )
        fig_scatter.update_layout(
            font=dict(size=14),
            height=400
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Status das contas
    col1, col2 = st.columns(2)
    
    with col1:
        # Status da conta corrente
        checking_counts = filtered_df['checking_account_status'].value_counts()
        fig_checking = px.pie(
            values=checking_counts.values,
            names=checking_counts.index,
            title="Status da Conta Corrente",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_checking.update_traces(textposition='inside', textinfo='percent+label')
        fig_checking.update_layout(
            font=dict(size=12),
            height=400
        )
        st.plotly_chart(fig_checking, use_container_width=True)
    
    with col2:
        # Status da conta poupança
        saving_counts = filtered_df['saving_account_status'].value_counts()
        fig_saving = px.pie(
            values=saving_counts.values,
            names=saving_counts.index,
            title="Status da Conta Poupança",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_saving.update_traces(textposition='inside', textinfo='percent+label')
        fig_saving.update_layout(
            font=dict(size=12),
            height=400
        )
        st.plotly_chart(fig_saving, use_container_width=True)

with tab4:
    st.markdown('<h2 class="sub-header">Características Sociais</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Propósito do crédito
        purpose_counts = filtered_df['purpose'].value_counts()
        fig_purpose = px.bar(
            x=purpose_counts.values,
            y=purpose_counts.index,
            orientation='h',
            title="Propósito do Crédito",
            labels={'x': 'Quantidade', 'y': 'Propósito'},
            color_discrete_sequence=['#1abc9c']
        )
        fig_purpose.update_layout(
            font=dict(size=14),
            height=500
        )
        st.plotly_chart(fig_purpose, use_container_width=True)
    
    with col2:
        # Tipo de habitação
        housing_counts = filtered_df['housing_type'].value_counts()
        fig_housing = px.pie(
            values=housing_counts.values,
            names=housing_counts.index,
            title="Tipo de Habitação",
            color_discrete_sequence=['#ff6b6b', '#4ecdc4', '#45b7d1']
        )
        fig_housing.update_traces(textposition='inside', textinfo='percent+label')
        fig_housing.update_layout(
            font=dict(size=14),
            height=400
        )
        st.plotly_chart(fig_housing, use_container_width=True)
        
        # Status de emprego
        employment_counts = filtered_df['employment_status'].value_counts()
        fig_employment = px.bar(
            x=employment_counts.index,
            y=employment_counts.values,
            title="Status de Emprego",
            labels={'x': 'Status de Emprego', 'y': 'Quantidade'},
            color_discrete_sequence=['#ff9ff3']
        )
        fig_employment.update_layout(
            font=dict(size=14),
            height=400,
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig_employment, use_container_width=True)

# Seção de análise avançada
st.markdown('<h2 class="sub-header">Análise Avançada</h2>', unsafe_allow_html=True)

# Matriz de correlação para variáveis numéricas
numeric_cols = ['age_in_years', 'credit_amount', 'duration_in_month', 'installment_rate', 'residence_since', 'number_existing_credits', 'number_people_maintenance']
correlation_matrix = filtered_df[numeric_cols].corr()

fig_corr = px.imshow(
    correlation_matrix,
    text_auto=True,
    aspect="auto",
    title="Matriz de Correlação - Variáveis Numéricas",
    color_continuous_scale='RdBu'
)
fig_corr.update_layout(
    font=dict(size=14),
    height=500
)
st.plotly_chart(fig_corr, use_container_width=True)

# Análise de risco por diferentes características
st.markdown('<h3>Análise de Risco por Características</h3>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Risco por propósito
    risk_by_purpose = pd.crosstab(filtered_df['purpose'], filtered_df['risk'], normalize='index') * 100
    fig_risk_purpose = px.bar(
        x=risk_by_purpose.index,
        y=[risk_by_purpose['Good Risk'], risk_by_purpose['Bad Risk']],
        title="Distribuição de Risco por Propósito (%)",
        labels={'x': 'Propósito', 'y': 'Percentual'},
        color_discrete_sequence=['#2ecc71', '#e74c3c']
    )
    fig_risk_purpose.update_layout(
        barmode='stack',
        font=dict(size=12),
        height=400,
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig_risk_purpose, use_container_width=True)

with col2:
    # Risco por status de emprego
    risk_by_employment = pd.crosstab(filtered_df['employment_status'], filtered_df['risk'], normalize='index') * 100
    fig_risk_employment = px.bar(
        x=risk_by_employment.index,
        y=[risk_by_employment['Good Risk'], risk_by_employment['Bad Risk']],
        title="Distribuição de Risco por Status de Emprego (%)",
        labels={'x': 'Status de Emprego', 'y': 'Percentual'},
        color_discrete_sequence=['#2ecc71', '#e74c3c']
    )
    fig_risk_employment.update_layout(
        barmode='stack',
        font=dict(size=12),
        height=400,
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig_risk_employment, use_container_width=True)

# Resumo final
st.markdown(f"""
<div class="info-box">
<h3>Resumo Executivo</h3>
<p>Este dashboard analisou {len(df)} solicitantes de crédito alemães. Os principais insights incluem:</p>
<ul>
<li><strong>Taxa de Risco:</strong> {(df['risk'] == 'Bad Risk').mean()*100:.1f}% dos solicitantes são classificados como mau risco</li>
<li><strong>Demografia:</strong> Idade média de {df['age_in_years'].mean():.1f} anos, com maior concentração entre 25-45 anos</li>
<li><strong>Financeiro:</strong> Valor médio de crédito de {df['credit_amount'].mean():,.0f} DM</li>
<li><strong>Propósito Principal:</strong> {df['purpose'].value_counts().index[0]} é o propósito mais comum</li>
</ul>
</div>
""", unsafe_allow_html=True)

# Rodapé
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; font-size: 14px;">
    German Credit Data Dashboard | Desenvolvido com Streamlit e Plotly | 
    Dados: UCI Machine Learning Repository
</div>
""", unsafe_allow_html=True)