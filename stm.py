import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="German Credit Data Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

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


@st.cache_data
def load_data():
    """Carrega o dataset German Credit Data."""
    df = pd.read_csv("german_credit_data_treated.csv")
    return df

@st.cache_data
def get_age_bins(df_age_in_years):
    """Cria faixas etárias para a coluna 'age_in_years'."""
    # Define os rótulos das faixas etárias de forma mais flexível
    bins = [18, 31, 41, 51, 61, df_age_in_years.max() + 1] # Ajusta o último bin para incluir o max
    labels = [f'{int(bins[i])}-{int(bins[i+1]-1)}' for i in range(len(bins)-2)] + [f'{int(bins[-2])}+']
    
    # Garante que pd.cut não gere erros se o df_age_in_years estiver vazio
    if not df_age_in_years.empty:
        age_bins = pd.cut(
            df_age_in_years,
            bins=bins,
            right=False,
            labels=labels,
            include_lowest=True
        )
        age_bins.name = 'age_bins'
        return age_bins
    return pd.Series([], dtype='object') # Retorna uma série vazia com dtype compatível


def plot_risk_distribution(df):
    """Gera um gráfico de pizza da distribuição de risco."""
    risk_counts = df['risk'].value_counts()
    fig = px.pie(
        values=risk_counts.values,
        names=risk_counts.index,
        title="Distribuição de Risco de Crédito",
        color_discrete_map={'Good Risk': '#2ecc71', 'Bad Risk': '#e74c3c'}
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(font=dict(size=14), showlegend=True, height=400)
    return fig

def plot_risk_by_age(df):
    """Gera um gráfico de barras empilhadas de risco por faixa etária."""
    age_bins = get_age_bins(df['age_in_years'])
    
    # Garante que age_bins não esteja vazio antes de criar o crosstab
    if age_bins.empty or df['risk'].empty:
        return px.bar(title="Dados insuficientes para Risco por Faixa Etária")

    # Cria um DataFrame temporário para o crosstab para evitar problemas com índices
    temp_df = pd.DataFrame({'age_bins': age_bins, 'risk': df['risk']})
    risk_by_age = pd.crosstab(temp_df['age_bins'], temp_df['risk'], normalize='index') * 100
    
    # Garante que todas as categorias de risco estejam presentes para evitar KeyError no melt
    all_risks = ['Good Risk', 'Bad Risk']
    for r in all_risks:
        if r not in risk_by_age.columns:
            risk_by_age[r] = 0.0
    risk_by_age = risk_by_age[all_risks] # Garante a ordem das colunas

    risk_by_age_long = risk_by_age.reset_index().melt(id_vars='age_bins', value_name='percentual', var_name='risk')

    fig = px.bar(
        risk_by_age_long,
        x='age_bins',
        y='percentual',
        color='risk',
        title="Distribuição de Risco por Faixa Etária (%)",
        labels={'age_bins': 'Faixa Etária', 'percentual': 'Percentual (%)'},
        color_discrete_map={'Good Risk': '#2ecc71', 'Bad Risk': '#e74c3c'}
    )
    fig.update_layout(barmode='stack', font=dict(size=14), height=400)
    return fig

def plot_age_distribution(df):
    """Gera um histograma da distribuição de idade."""
    fig = px.histogram(
        df, x='age_in_years', nbins=20, title="Distribuição de Idade dos Solicitantes",
        labels={'age_in_years': 'Idade', 'count': 'Quantidade'},
        color_discrete_sequence=['#3498db']
    )
    fig.update_layout(font=dict(size=14), height=400)
    return fig

def plot_personal_status(df):
    """Gera um gráfico de barras do status pessoal e sexo."""
    personal_status_counts = df['personal_status_sex'].value_counts()
    fig = px.bar(
        x=personal_status_counts.values, y=personal_status_counts.index, orientation='h',
        title="Status Pessoal e Sexo", labels={'x': 'Quantidade', 'y': 'Status'},
        color_discrete_sequence=['#9b59b6']
    )
    fig.update_layout(font=dict(size=14), height=400)
    return fig

def plot_credit_amount_distribution(df):
    """Gera um histograma da distribuição do valor do crédito."""
    fig = px.histogram(
        df, x='credit_amount', nbins=30, title="Distribuição do Valor do Crédito",
        labels={'credit_amount': 'Valor do Crédito (DM)', 'count': 'Quantidade'},
        color_discrete_sequence=['#f39c12']
    )
    fig.update_layout(font=dict(size=14), height=400)
    return fig

def plot_credit_vs_duration(df):
    """Gera um gráfico de dispersão de valor do crédito vs duração."""
    fig = px.scatter(
        df, x='credit_amount', y='duration_in_month', color='risk',
        title="Valor do Crédito vs Duração",
        labels={'credit_amount': 'Valor do Crédito (DM)', 'duration_in_month': 'Duração (meses)'},
        color_discrete_map={'Good Risk': '#2ecc71', 'Bad Risk': '#e74c3c'}
    )
    fig.update_layout(font=dict(size=14), height=400)
    return fig

def plot_purpose_distribution(df):
    """Gera um gráfico de barras da distribuição do propósito do crédito."""
    purpose_counts = df['purpose'].value_counts()
    fig = px.bar(
        x=purpose_counts.values, y=purpose_counts.index, orientation='h', title="Propósito do Crédito",
        labels={'x': 'Quantidade', 'y': 'Propósito'},
        color_discrete_sequence=['#1abc9c']
    )
    fig.update_layout(font=dict(size=14), height=500)
    return fig

def plot_housing_type_distribution(df):
    """Gera um gráfico de pizza da distribuição do tipo de habitação."""
    housing_counts = df['housing_type'].value_counts()
    fig = px.pie(
        values=housing_counts.values, names=housing_counts.index, title="Tipo de Habitação",
        color_discrete_sequence=['#ff6b6b', '#4ecdc4', '#45b7d1']
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(font=dict(size=14), height=400)
    return fig

def plot_risk_by_category(df, category_col, title_suffix, x_label):
    """Gera um gráfico de barras empilhadas de risco por categoria genérica."""
    if df[category_col].empty or df['risk'].empty:
        return px.bar(title=f"Dados insuficientes para Risco por {x_label}")

    risk_by_cat = pd.crosstab(df[category_col], df['risk'], normalize='index') * 100
    
    # Garante que todas as categorias de risco estejam presentes para evitar KeyError no melt
    all_risks = ['Good Risk', 'Bad Risk']
    for r in all_risks:
        if r not in risk_by_cat.columns:
            risk_by_cat[r] = 0.0
    risk_by_cat = risk_by_cat[all_risks] # Garante a ordem das colunas

    risk_by_cat_long = risk_by_cat.reset_index().melt(
        id_vars=category_col, value_name='percentual', var_name='risk'
    )

    fig = px.bar(
        risk_by_cat_long,
        x=category_col,
        y='percentual',
        color='risk',
        title=f"Distribuição de Risco por {title_suffix} (%)",
        labels={category_col: x_label, 'percentual': 'Percentual (%)'},
        color_discrete_map={'Good Risk': '#2ecc71', 'Bad Risk': '#e74c3c'}
    )
    fig.update_layout(barmode='stack', font=dict(size=12), height=400, xaxis_tickangle=-45)
    return fig

# --- 4. Carregamento e Filtragem de Dados ---
df = load_data()

st.markdown('<h1 class="main-header">German Credit Data Dashboard</h1>', unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
<h3>Sobre o Dataset</h3>
Este dashboard apresenta uma análise abrangente do dataset Statlog (German Credit Data) da UCI Machine Learning Repository.
O dataset contém informações sobre 1.000 solicitantes de crédito alemães, classificados como bom ou mau risco de crédito
com base em 20 atributos diferentes.
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("## Filtros")

# Garante que os valores únicos de 'risk' sejam obtidos do DataFrame original
# para que o multiselect sempre tenha todas as opções, mesmo que filtradas.
all_risks = df['risk'].unique().tolist()
risk_filter = st.sidebar.multiselect(
    "Selecione o tipo de risco:",
    options=all_risks,
    default=all_risks
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

# Aplicar filtros de forma robusta
filtered_df = df.copy() # Trabalha em uma cópia para não modificar o df original

if risk_filter:
    filtered_df = filtered_df[filtered_df['risk'].isin(risk_filter)]
else:
    filtered_df = pd.DataFrame() # Se nenhum risco for selecionado, o DF fica vazio

if not filtered_df.empty:
    filtered_df = filtered_df[
        (filtered_df['age_in_years'] >= age_range[0]) &
        (filtered_df['age_in_years'] <= age_range[1]) &
        (filtered_df['credit_amount'] >= credit_range[0]) &
        (filtered_df['credit_amount'] <= credit_range[1])
    ]

st.sidebar.markdown(f"**Registros exibidos:** {len(filtered_df)} de {len(df)}")

# --- 5. Seção Principal do Dashboard ---
if filtered_df.empty:
    st.warning("Por favor, selecione ao menos um tipo de risco ou ajuste os filtros para exibir dados.")
else:
    # Métricas principais
    st.markdown('<h2 class="sub-header">Métricas Principais</h2>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    total_applicants = len(filtered_df)
    good_risk_count = (filtered_df['risk'] == 'Good Risk').sum()
    good_risk_pct = (good_risk_count / total_applicants * 100) if total_applicants > 0 else 0.0
    avg_age = filtered_df['age_in_years'].mean()
    avg_credit = filtered_df['credit_amount'].mean()

    with col1:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{total_applicants:,}</div>
            <div class="metric-label">Total de Solicitantes</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{good_risk_pct:.1f}%</div>
            <div class="metric-label">Bom Risco de Crédito</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{avg_age:.1f}</div>
            <div class="metric-label">Idade Média</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
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
            st.plotly_chart(plot_risk_distribution(filtered_df), use_container_width=True)

        with col2:
            st.plotly_chart(plot_risk_by_age(filtered_df), use_container_width=True)

        # Insight principal de risco
        if 'Bad Risk' in filtered_df['risk'].unique():
            bad_risk_pct_val = (filtered_df['risk'] == 'Bad Risk').mean() * 100
            st.markdown(f"""
            <div class="insight-box">
            <h4>Insight Principal</h4>
            {bad_risk_pct_val:.1f}% dos solicitantes nos filtros atuais são classificados como mau risco.
            A análise por faixa etária tende a mostrar que clientes mais jovens têm maior proporção de mau risco.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="insight-box">
            <h4>Insight Principal</h4>
            Não há dados de 'Mau Risco' para análise com os filtros atuais.
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        st.markdown('<h2 class="sub-header">Análise Demográfica</h2>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            st.plotly_chart(plot_age_distribution(filtered_df), use_container_width=True)

        with col2:
            st.plotly_chart(plot_personal_status(filtered_df), use_container_width=True)

    with tab3:
        st.markdown('<h2 class="sub-header">Análise Financeira</h2>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            st.plotly_chart(plot_credit_amount_distribution(filtered_df), use_container_width=True)

        with col2:
            st.plotly_chart(plot_credit_vs_duration(filtered_df), use_container_width=True)

    with tab4:
        st.markdown('<h2 class="sub-header">Características Sociais</h2>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            st.plotly_chart(plot_purpose_distribution(filtered_df), use_container_width=True)

        with col2:
            st.plotly_chart(plot_housing_type_distribution(filtered_df), use_container_width=True)

    # Seção de análise avançada
    st.markdown('<h2 class="sub-header">Análise Avançada</h2>', unsafe_allow_html=True)

    st.markdown('<h3>Análise de Risco por Características</h3>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(plot_risk_by_category(filtered_df, 'purpose', 'Propósito', 'Propósito'), use_container_width=True)

    with col2:
        st.plotly_chart(plot_risk_by_category(filtered_df, 'employment_status', 'Status de Emprego', 'Status de Emprego'), use_container_width=True)

    # Rodapé
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #7f8c8d; font-size: 14px;">
        German Credit Data Dashboard | Desenvolvido com Streamlit e Plotly |
        Dados: UCI Machine Learning Repository
    </div>
    """, unsafe_allow_html=True)


