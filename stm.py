import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="German Credit Data Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)



# --- Nova Paleta de Cores ---
PRIMARY_COLOR = "#2C3E50"  # Azul escuro
SECONDARY_COLOR = "#3498DB"  # Azul médio
ACCENT_COLOR = "#E74C3C"  # Vermelho
SUCCESS_COLOR = "#27AE60"  # Verde
WARNING_COLOR = "#F39C12"  # Laranja
NEUTRAL_COLOR = "#95A5A6"  # Cinza
BACKGROUND_COLOR = "#ECF0F1"  # Cinza claro
CARD_GRADIENT_1 = "linear-gradient(135deg, #3498DB 0%, #2C3E50 100%)"
CARD_GRADIENT_2 = "linear-gradient(135deg, #27AE60 0%, #16A085 100%)"
CARD_GRADIENT_3 = "linear-gradient(135deg, #E74C3C 0%, #C0392B 100%)"
CARD_GRADIENT_4 = "linear-gradient(135deg, #F39C12 0%, #D35400 100%)"

# --- Estilos CSS com Nova Paleta ---
st.markdown(f"""
<style>
    /* Fontes e estrutura */
    body {{
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-color: {BACKGROUND_COLOR};
    }}
    
    /* Cabeçalhos */
    .main-header {{
        font-size: 2.8rem;
        color: {PRIMARY_COLOR};
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: 700;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid {SECONDARY_COLOR};
    }}
    
    .sub-header {{
        font-size: 1.8rem;
        color: {PRIMARY_COLOR};
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        font-weight: 600;
    }}
    
    /* Cards de métricas */
    .metric-container {{
        background: {CARD_GRADIENT_1};
        padding: 1.2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }}
    
    .metric-container:hover {{
        transform: translateY(-5px);
    }}
    
    .metric-value {{
        font-size: 2.2rem;
        font-weight: bold;
        margin-bottom: 0.3rem;
    }}
    
    .metric-label {{
        font-size: 1rem;
        opacity: 0.9;
        letter-spacing: 0.5px;
    }}
    
    /* Boxes de informação */
    .info-box {{
        background: {CARD_GRADIENT_2};
        padding: 1.2rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }}
    
    .insight-box {{
        background: linear-gradient(135deg, #9B59B6 0%, #8E44AD 100%);
        padding: 1.2rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }}
    
    /* Abas */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        height: 45px;
        padding: 0 20px;
        background-color: #FFFFFF;
        border-radius: 8px 8px 0 0;
        border: 1px solid #DFE6E9;
        color: {PRIMARY_COLOR};
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    
    .stTabs [aria-selected="true"] {{
        background-color: {SECONDARY_COLOR};
        color: white;
        border-color: {SECONDARY_COLOR};
    }}
    
    /* Sidebar */
    .sidebar .sidebar-content {{
        background: #FFFFFF;
        border-right: 1px solid #DFE6E9;
    }}
    
    /* Filtros */
    .stSlider>div>div>div>div {{
        background-color: {SECONDARY_COLOR} !important;
    }}
    
    .st-bb {{
        background-color: {BACKGROUND_COLOR};
    }}
    
    .st-at {{
        background-color: {SECONDARY_COLOR};
    }}
    
    /* Rodapé */
    .footer {{
        text-align: center;
        color: {NEUTRAL_COLOR};
        font-size: 0.9rem;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #DFE6E9;
    }}
</style>
""", unsafe_allow_html=True)

# --- Tema ---
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

def toggle_theme():
    st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'

st.sidebar.button("Alternar Tema", on_click=toggle_theme)
theme = st.session_state.theme

# --- Estilo personalizado ---
if theme == 'dark':
    st.markdown(
        """
        <style>
        body {
            background-color: #0e1117;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

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
            # Conta os tipos de risco
    risk_counts = df['risk'].value_counts()
    num_riscos = risk_counts.size

    if num_riscos > 1:
        # Quando tem mais de um risco, mostra proporção
        risk_dist = risk_counts.reset_index()
        risk_dist.columns = ['Risco', 'Contagem']
        risk_dist['Proporcao'] = (risk_dist['Contagem'] / risk_dist['Contagem'].sum()) * 100

        fig = px.bar(
            risk_dist,
            x=["Distribuição de Risco"] * num_riscos,
            y='Proporcao',
            color='Risco',
            text='Proporcao',
            labels={'Proporcao': 'Proporção (%)'},
            title='Distribuição Percentual de Risco de Crédito',
        )

        fig.update_layout(
            barmode='stack',
            yaxis=dict(range=[0, 100]),
            xaxis_title='',
            yaxis_title='Proporção (%)',
            showlegend=True
        )

        fig.update_traces(
            texttemplate='%{text:.1f}%',
            textposition='inside'
        )

    else:
        # Quando só tem um risco, mostra a contagem absoluta
        risco = risk_counts.index[0]
        contagem = risk_counts.iloc[0]

        df_count = {'Risco': [risco], 'Contagem': [contagem]}
        fig = px.bar(
            df_count,
            x='Risco',
            y='Contagem',
            text='Contagem',
            labels={'Contagem': 'Quantidade'},
            title='Quantidade de Solicitantes por Tipo de Risco',
        )

        fig.update_traces(
            texttemplate='%{text}',
            textposition='outside'
        )
        fig.update_layout(
            yaxis=dict(range=[0, contagem * 1.2]),
            showlegend=False
        )
    return fig


def plot_risk_by_age(df):
    """Gera um gráfico de barras empilhadas de risco por faixa etária."""
    age_bins = get_age_bins(df['age_in_years'])
    if age_bins.empty or df['risk'].empty:
        return px.bar(title="Dados insuficientes para Risco por Faixa Etária")

    temp_df = pd.DataFrame({'age_bins': age_bins, 'risk': df['risk']})

    single_risk_class = temp_df['risk'].nunique() == 1
    normalize = 'index' if not single_risk_class else False

    risk_by_age = pd.crosstab(temp_df['age_bins'], temp_df['risk'], normalize=normalize)
    
    # Adiciona colunas ausentes com 0s
    all_risks = ['Good Risk', 'Bad Risk']
    for r in all_risks:
        if r not in risk_by_age.columns:
            risk_by_age[r] = 0.0

    risk_by_age = risk_by_age[all_risks]
    risk_by_age_long = risk_by_age.reset_index().melt(id_vars='age_bins', value_name='valor', var_name='risk')

    y_label = 'Percentual (%)' if not single_risk_class else 'Contagem'

    fig = px.bar(
        risk_by_age_long,
        x='age_bins',
        y='valor',
        color='risk',
        title="Distribuição de Risco por Faixa Etária" + (" (%)" if not single_risk_class else " (Contagem)"),
        labels={'age_bins': 'Faixa Etária', 'valor': y_label},
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

def plot_risk_by_category(df, column, title, xaxis_label):
    """Gera gráfico de barras empilhadas para qualquer coluna categórica."""
    if df.empty or df['risk'].empty or column not in df.columns:
        return px.bar(title=f"Dados insuficientes para {title}")

    single_risk_class = df['risk'].nunique() == 1
    normalize = 'index' if not single_risk_class else False

    risk_by_category = pd.crosstab(df[column], df['risk'], normalize=normalize)

    all_risks = ['Good Risk', 'Bad Risk']
    for r in all_risks:
        if r not in risk_by_category.columns:
            risk_by_category[r] = 0.0

    risk_by_category = risk_by_category[all_risks]
    risk_by_category_long = risk_by_category.reset_index().melt(id_vars=column, value_name='valor', var_name='risk')

    y_label = 'Percentual (%)' if not single_risk_class else 'Contagem'

    fig = px.bar(
        risk_by_category_long,
        x=column,
        y='valor',
        color='risk',
        title=title + (" (%)" if not single_risk_class else " (Contagem)"),
        labels={column: xaxis_label, 'valor': y_label},
        color_discrete_map={'Good Risk': '#2ecc71', 'Bad Risk': '#e74c3c'}
    )
    fig.update_layout(barmode='stack', font=dict(size=14), height=400)
    return fig


# --- 4. Carregamento e Filtragem de Dados ---
df = load_data()

st.markdown('<h1 class="main-header">Customer Profile Analysis Dashboard</h1>', unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
<h3>💳 Sobre o Dataset</h3>
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
        <div class="metric-container" style="linear-gradient(135deg, #3498DB 0%, #2C3E50 100%)">
            <div class="metric-value">1.000</div>
            <div class="metric-label">Total de Solicitantes</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        if not filtered_df.empty:
            risk_counts = filtered_df['risk'].value_counts()
        
        if 'Bad Risk' in risk_counts and 'Good Risk' in risk_counts:
            # Ambos riscos presentes - mostra % bom risco
            good_pct = (risk_counts['Good Risk'] / total_applicants * 100)
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-value">{good_pct:.1f}%</div>
                <div class="metric-label">Bom Risco</div>
            </div>
            """, unsafe_allow_html=True)
        elif 'Bad Risk' in risk_counts:
            # Apenas mau risco - mostra contagem absoluta
            st.markdown(f"""
            <div class="metric-container" style="background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);">
                <div class="metric-value">{risk_counts['Bad Risk']}</div>
                <div class="metric-label">Mau Risco (total)</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Apenas bom risco - mostra contagem absoluta
            st.markdown(f"""
            <div class="metric-container" style="background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);">
                <div class="metric-value">{risk_counts['Good Risk']}</div>
                <div class="metric-label">Bom Risco (total)</div>
            </div>
            """, unsafe_allow_html=True)

    with col3:
        avg_age = filtered_df['age_in_years'].mean()
        st.markdown(f"""
        <div class="metric-container" style="linear-gradient(135deg, #F39C12 0%, #D35400 100%)">
            <div class="metric-value">{avg_age:.1f}</div>
            <div class="metric-label">Idade Média</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        avg_credit = filtered_df['credit_amount'].mean()
        st.markdown(f"""
        <div class="metric-container" style="background: linear-gradient(135deg, #9B59B6 0%, #8E44AD 100%);">
            <div class="metric-value">{avg_credit:,.0f}</div>
            <div class="metric-label">Crédito Médio (DM)</div>
        </div>
        """, unsafe_allow_html=True)

    # Abas para organizar o conteúdo
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Análise de Risco", "👥 Demografia", "💰 Análise Financeira", "📊 Características Sociais"])

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
            Para aqueles caracterizados com bom risco, observa-se que a maioria desses são clientes que possuem mais temporalidade em seus empregos, além de realizar operações de crédito em sua maioria para carros, móveis e equipamento de rádio ou tv.
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
    #st.markdown('<h2 class="sub-header">Análise Avançada</h2>', unsafe_allow_html=True)

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


