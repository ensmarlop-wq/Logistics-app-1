import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
from datetime import datetime, timedelta, time

# ═══════════════════════════════════════════════════════════
# CONFIGURACIÓN VISUAL PREMIUM
# ═══════════════════════════════════════════════════════════
st.set_page_config(
    page_title="SmartDock Pro Enterprise", 
    page_icon="🚛", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS PERSONALIZADO PREMIUM
st.markdown("""
    <style>
    /* Importar fuente moderna */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Variables de color corporativo */
    :root {
        --primary-blue: #1e3a8a;
        --secondary-blue: #3b82f6;
        --accent-teal: #06b6d4;
        --steel-gray: #475569;
        --light-gray: #f1f5f9;
        --success-green: #10b981;
        --warning-yellow: #f59e0b;
        --danger-red: #ef4444;
    }
    
    /* Estilos globales */
    .stApp {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    /* Header principal */
    h1 {
        color: var(--primary-blue);
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        padding: 20px 0;
        border-bottom: 3px solid var(--accent-teal);
    }
    
    h2, h3 {
        color: var(--steel-gray);
        font-weight: 600;
    }
    
    /* Tarjetas de métricas premium */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-blue);
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem;
        font-weight: 500;
        color: var(--steel-gray);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stMetric {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07), 0 2px 4px rgba(0, 0, 0, 0.05);
        border-left: 4px solid var(--secondary-blue);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .stMetric:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 12px rgba(0, 0, 0, 0.1), 0 4px 6px rgba(0, 0, 0, 0.06);
    }
    
    /* Botones premium */
    .stButton > button {
        background: linear-gradient(135deg, var(--secondary-blue) 0%, var(--primary-blue) 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Sidebar premium */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--primary-blue) 0%, #1e293b 100%);
        color: white;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] label {
        color: white !important;
    }
    
    /* Tabs premium */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: white;
        padding: 10px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: var(--light-gray);
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        color: var(--steel-gray);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--secondary-blue) 0%, var(--accent-teal) 100%);
        color: white;
    }
    
    /* DataFrames premium */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
    }
    
    /* Contenedores con estilo */
    .block-container {
        padding: 2rem;
    }
    
    /* Info boxes */
    .stAlert {
        border-radius: 8px;
        border-left: 4px solid var(--accent-teal);
    }
    
    /* Selectbox y inputs */
    .stSelectbox, .stNumberInput, .stTextInput {
        border-radius: 6px;
    }
    
    /* Expander premium */
    .streamlit-expanderHeader {
        background-color: var(--light-gray);
        border-radius: 8px;
        font-weight: 600;
    }
    
    </style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# INICIALIZACIÓN DE DATOS
# ═══════════════════════════════════════════════════════════
if 'df_input' not in st.session_state:
    st.session_state.df_input = pd.DataFrame(columns=[
        "ID_Camion", "Producto", "Tipo_Producto", "Prioridad", 
        "Hora_Llegada_Est", "Duracion_Min"
    ])

if 'config_muelles' not in st.session_state:
    st.session_state.config_muelles = {
        1: "Seco", 2: "Seco", 3: "Frío"
    }

# ═══════════════════════════════════════════════════════════
# CLASE OPTIMIZADOR AVANZADO
# ═══════════════════════════════════════════════════════════
class DockOptimizerPro:
    """
    Optimizador de muelles con:
    - Prioridades ponderadas (Alta > Media > Baja)
    - Restricciones de tipo de muelle
    - Cálculo de costos de demurrage
    """
    
    PRIORIDAD_PESOS = {"Alta": 3, "Media": 2, "Baja": 1}
    COSTO_DEMURRAGE_POR_HORA = 150  # USD por hora de espera
    
    def __init__(self, num_docks, dock_config, start_hour=8):
        self.num_docks = num_docks
        self.dock_config = dock_config  # {dock_id: "Seco" o "Frío"}
        self.base_date = datetime.now().date()
        self.start_time = datetime.combine(self.base_date, time(start_hour, 0))
        self.docks = {i+1: self.start_time for i in range(num_docks)}
    
    def _puede_asignar_muelle(self, tipo_producto, dock_id):
        """Valida si el producto puede ir en el muelle"""
        tipo_muelle = self.dock_config.get(dock_id, "Seco")
        
        if tipo_producto == "Refrigerado":
            return tipo_muelle == "Frío"
        else:  # Secos/Electrónicos/etc
            return tipo_muelle == "Seco"
    
    def _calcular_prioridad_score(self, row, arrival_time):
        """
        Calcula score de prioridad combinando:
        - Peso de prioridad
        - Tiempo de llegada (para romper empates)
        """
        peso = self.PRIORIDAD_PESOS.get(row['Prioridad'], 1)
        # Convertimos tiempo a minutos desde inicio para ordenar
        tiempo_minutos = (arrival_time - self.start_time).total_seconds() / 60
        
        # Score: Prioridad alta tiene más peso, pero el tiempo de llegada desempata
        return (peso * 10000) - tiempo_minutos
    
    def agendar_camiones(self, df_camiones):
        schedule_log = []
        costos_totales = 0
        
        if df_camiones.empty:
            return pd.DataFrame(), 0
        
        # Agregar columna de score para ordenamiento
        df_camiones = df_camiones.copy()
        df_camiones['_score'] = df_camiones.apply(
            lambda row: self._calcular_prioridad_score(row, row['Hora_Llegada_Est']), 
            axis=1
        )
        
        # Ordenar por score (prioridad + llegada)
        df_sorted = df_camiones.sort_values(by='_score', ascending=False)
        
        for _, row in df_sorted.iterrows():
            arrival_time = row['Hora_Llegada_Est']
            duration_min = row['Duracion_Min']
            tipo_producto = row['Tipo_Producto']
            
            # Buscar muelle compatible que se libere primero
            muelles_compatibles = [
                dock_id for dock_id in self.docks.keys()
                if self._puede_asignar_muelle(tipo_producto, dock_id)
            ]
            
            if not muelles_compatibles:
                # No hay muelles compatibles - marcar como error
                schedule_log.append({
                    "Camión": row['ID_Camion'],
                    "Producto": row['Producto'],
                    "Tipo_Producto": tipo_producto,
                    "Prioridad": row['Prioridad'],
                    "Muelle_Asignado": "❌ SIN MUELLE",
                    "Llegada_Teorica": arrival_time,
                    "Inicio_Real": None,
                    "Fin_Real": None,
                    "Duracion_Min": int(duration_min),
                    "Espera_Min": 0,
                    "Costo_Demurrage_USD": 0,
                    "Estado": "Error: Muelle incompatible"
                })
                continue
            
            # Elegir el que se libera primero
            best_dock = min(muelles_compatibles, key=lambda d: self.docks[d])
            free_time = self.docks[best_dock]
            
            # Calcular inicio real
            actual_start = max(arrival_time, free_time, self.start_time)
            actual_end = actual_start + timedelta(minutes=int(duration_min))
            
            # Calcular espera
            wait_time = max(0, (actual_start - arrival_time).total_seconds() / 60)
            
            # Calcular costo de demurrage
            costo_demurrage = (wait_time / 60) * self.COSTO_DEMURRAGE_POR_HORA
            costos_totales += costo_demurrage
            
            # Determinar estado
            if wait_time == 0:
                estado = "✅ A Tiempo"
            elif wait_time < 30:
                estado = "⚠️ Retraso Leve"
            else:
                estado = "🔴 Crítico"
            
            schedule_log.append({
                "Camión": row['ID_Camion'],
                "Producto": row['Producto'],
                "Tipo_Producto": tipo_producto,
                "Prioridad": row['Prioridad'],
                "Muelle_Asignado": f"Muelle {best_dock} ({self.dock_config[best_dock]})",
                "Llegada_Teorica": arrival_time,
                "Inicio_Real": actual_start,
                "Fin_Real": actual_end,
                "Duracion_Min": int(duration_min),
                "Espera_Min": int(wait_time),
                "Costo_Demurrage_USD": round(costo_demurrage, 2),
                "Estado": estado
            })
            
            self.docks[best_dock] = actual_end
        
        return pd.DataFrame(schedule_log), costos_totales

# ═══════════════════════════════════════════════════════════
# INTERFAZ PRINCIPAL
# ═══════════════════════════════════════════════════════════

# Header con estilo
st.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <h1 style='margin: 0; font-size: 3rem;'>
            🚛 SmartDock Pro <span style='color: #06b6d4;'>Enterprise</span>
        </h1>
        <p style='color: #64748b; font-size: 1.1rem; margin-top: 10px;'>
            Sistema Inteligente de Gestión de Patios Logísticos
        </p>
    </div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# SIDEBAR - CONFIGURACIÓN
# ═══════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### ⚙️ Configuración del Sistema")
    
    # Configuración de recursos
    st.markdown("#### 📦 Recursos Disponibles")
    num_muelles = st.slider("Cantidad de Muelles", 1, 10, 3, help="Número total de muelles operativos")
    hora_inicio = st.number_input("Hora Inicio Turno (24hrs)", 0, 23, 8, 
                                   help="Hora a la que abre el patio de maniobras")
    
    # Configuración de tipos de muelle
    st.markdown("#### 🔧 Configuración de Muelles")
    st.session_state.config_muelles = {}
    for i in range(1, num_muelles + 1):
        tipo_muelle = st.selectbox(
            f"Muelle {i}", 
            ["Seco", "Frío"],
            key=f"muelle_{i}",
            index=0 if i <= 2 else 1
        )
        st.session_state.config_muelles[i] = tipo_muelle
    
    st.markdown("---")
    st.markdown("### 🎲 Simulador de Escenarios")
    
    # Generador de escenarios
    if st.button("🔄 Generar Escenario Aleatorio", use_container_width=True):
        st.session_state.df_input = st.session_state.df_input.iloc[0:0]
        
        base_time = datetime.combine(datetime.now().date(), time(hora_inicio, 0))
        
        # Productos con tipos
        productos_config = [
            ("Electrónicos", "Seco"),
            ("Papel", "Seco"),
            ("Textil", "Seco"),
            ("Alimentos Refrigerados", "Refrigerado"),
            ("Farmacéuticos", "Refrigerado"),
            ("Automotriz", "Seco"),
            ("Químicos", "Seco")
        ]
        
        nuevos_datos = []
        for i in range(10):  # 10 camiones
            mins_random = random.randint(0, 360)  # Primeras 6 horas
            llegada_random = base_time + timedelta(minutes=mins_random)
            duracion_random = random.choice([30, 45, 60, 90, 120])
            prioridad = random.choice(["Alta", "Alta", "Media", "Media", "Baja"])  # Más Altas
            producto, tipo = random.choice(productos_config)
            
            nuevos_datos.append({
                "ID_Camion": f"TRK-{random.randint(1000, 9999)}",
                "Producto": producto,
                "Tipo_Producto": tipo,
                "Prioridad": prioridad,
                "Hora_Llegada_Est": llegada_random,
                "Duracion_Min": duracion_random
            })
        
        st.session_state.df_input = pd.DataFrame(nuevos_datos)
        st.success("✅ Escenario generado exitosamente")
        st.rerun()
    
    st.markdown("---")
    if st.button("🗑️ Limpiar Todo", use_container_width=True):
        st.session_state.df_input = st.session_state.df_input.iloc[0:0]
        st.rerun()
    
    # Info del sistema
    st.markdown("---")
    st.markdown("""
        <div style='background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; margin-top: 20px;'>
            <p style='margin: 0; font-size: 0.85rem; color: #cbd5e1;'>
                <strong>💡 Tip:</strong> Los camiones de alta prioridad se procesan primero.
                Los productos refrigerados requieren muelles tipo "Frío".
            </p>
        </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# PESTAÑAS DE NAVEGACIÓN
# ═══════════════════════════════════════════════════════════
tab_dashboard, tab_gestor, tab_analytics = st.tabs([
    "📊 Dashboard Operativo", 
    "📝 Gestor de Camiones", 
    "📈 Analytics"
])

# ═══════════════════════════════════════════════════════════
# TAB 1: DASHBOARD OPERATIVO
# ═══════════════════════════════════════════════════════════
with tab_dashboard:
    if st.session_state.df_input.empty:
        st.info("👈 Presiona 'Generar Escenario Aleatorio' para comenzar la simulación")
    else:
        # Ejecutar optimización
        optimizer = DockOptimizerPro(
            num_docks=num_muelles, 
            dock_config=st.session_state.config_muelles,
            start_hour=hora_inicio
        )
        resultado_df, costo_total = optimizer.agendar_camiones(st.session_state.df_input)
        
        # KPIs en tarjetas premium
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Cargas", 
                len(resultado_df),
                delta=f"{len(resultado_df[resultado_df['Estado'].str.contains('✅')])} a tiempo"
            )
        
        with col2:
            espera_avg = resultado_df['Espera_Min'].mean()
            st.metric(
                "Espera Promedio", 
                f"{espera_avg:.1f} min",
                delta="Óptimo" if espera_avg < 20 else "Alto",
                delta_color="normal" if espera_avg < 20 else "inverse"
            )
        
        with col3:
            st.metric(
                "Costo Demurrage", 
                f"${costo_total:,.2f} USD",
                delta=f"${(costo_total/len(resultado_df)):.2f} por carga" if len(resultado_df) > 0 else "$0"
            )
        
        with col4:
            if not resultado_df.empty and resultado_df['Fin_Real'].notna().any():
                fin_turno = resultado_df[resultado_df['Fin_Real'].notna()]['Fin_Real'].max().strftime("%H:%M")
                st.metric("Fin de Operaciones", fin_turno)
            else:
                st.metric("Fin de Operaciones", "N/A")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Gráfico Gantt Premium
        resultado_valido = resultado_df[resultado_df['Inicio_Real'].notna()].copy()
        
        if not resultado_valido.empty:
            # Mapeo de colores por estado
            color_map = {
                "✅ A Tiempo": "#10b981",
                "⚠️ Retraso Leve": "#f59e0b", 
                "🔴 Crítico": "#ef4444"
            }
            
            fig = px.timeline(
                resultado_valido,
                x_start="Inicio_Real",
                x_end="Fin_Real",
                y="Muelle_Asignado",
                color="Estado",
                color_discrete_map=color_map,
                text="Camión",
                hover_data={
                    "Producto": True,
                    "Tipo_Producto": True,
                    "Prioridad": True,
                    "Llegada_Teorica": "|%H:%M",
                    "Duracion_Min": True,
                    "Espera_Min": True,
                    "Costo_Demurrage_USD": ":.2f",
                    "Inicio_Real": False,
                    "Fin_Real": False,
                    "Muelle_Asignado": False,
                    "Estado": False
                },
                title="<b>Diagrama de Ocupación de Muelles (Timeline Operativo)</b>"
            )
            
            fig.update_layout(
                height=500,
                xaxis_title="<b>Horario del Turno</b>",
                yaxis_title=None,
                font=dict(family="Inter, sans-serif", size=12),
                plot_bgcolor='rgba(248,250,252,0.5)',
                paper_bgcolor='white',
                title_font_size=18,
                title_font_color='#1e3a8a',
                hovermode='closest',
                showlegend=True,
                legend=dict(
                    title="Estado de Carga",
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            fig.update_yaxes(categoryorder="category ascending")
            fig.update_traces(textposition='inside', textfont_size=10)
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Tabla de resultados con estilo
        st.markdown("### 📋 Detalle de Asignaciones")
        
        display_df = resultado_df.copy()
        if not display_df.empty:
            display_df['Llegada_Teorica'] = display_df['Llegada_Teorica'].dt.strftime('%H:%M')
            display_df['Inicio_Real'] = display_df['Inicio_Real'].apply(
                lambda x: x.strftime('%H:%M') if pd.notna(x) else 'N/A'
            )
            display_df['Fin_Real'] = display_df['Fin_Real'].apply(
                lambda x: x.strftime('%H:%M') if pd.notna(x) else 'N/A'
            )
            
            st.dataframe(
                display_df[[
                    "Camión", "Producto", "Tipo_Producto", "Prioridad", 
                    "Muelle_Asignado", "Llegada_Teorica", "Inicio_Real", 
                    "Fin_Real", "Espera_Min", "Costo_Demurrage_USD", "Estado"
                ]],
                use_container_width=True,
                hide_index=True
            )

# ═══════════════════════════════════════════════════════════
# TAB 2: GESTOR MANUAL
# ═══════════════════════════════════════════════════════════
with tab_gestor:
    col_add, col_edit = st.columns([1, 1])
    
    with col_add:
        st.markdown("### ➕ Agregar Camión")
        with st.form("add_truck_form", clear_on_submit=True):
            new_id = st.text_input("ID Camión", placeholder="TRK-XXXX")
            new_prod = st.text_input("Producto", placeholder="Ej. Papel")
            
            col_tipo, col_prior = st.columns(2)
            new_tipo = col_tipo.selectbox("Tipo", ["Seco", "Refrigerado"])
            new_prioridad = col_prior.selectbox("Prioridad", ["Alta", "Media", "Baja"])
            
            col_time, col_dur = st.columns(2)
            new_time = col_time.time_input("Hora Llegada", value=time(hora_inicio, 0))
            new_dur = col_dur.number_input("Duración (min)", min_value=15, value=60, step=15)
            
            if st.form_submit_button("➕ Agregar Camión", use_container_width=True):
                if new_id and new_prod:
                    full_arrival = datetime.combine(datetime.now().date(), new_time)
                    new_row = pd.DataFrame([{
                        "ID_Camion": new_id,
                        "Producto": new_prod,
                        "Tipo_Producto": new_tipo,
                        "Prioridad": new_prioridad,
                        "Hora_Llegada_Est": full_arrival,
                        "Duracion_Min": new_dur
                    }])
                    st.session_state.df_input = pd.concat([st.session_state.df_input, new_row], ignore_index=True)
                    st.success(f"✅ {new_id} agregado correctamente")
                    st.rerun()
                else:
                    st.error("Por favor completa ID y Producto")
    
    with col_edit:
        st.markdown("### ✏️ Editar / Eliminar")
        if not st.session_state.df_input.empty:
            lista_ids = st.session_state.df_input['ID_Camion'].tolist()
            camion_sel = st.selectbox("Seleccionar Camión:", lista_ids)
            
            datos_act = st.session_state.df_input[st.session_state.df_input['ID_Camion'] == camion_sel].iloc[0]
            
            with st.expander(f"🔧 Modificar {camion_sel}", expanded=True):
                edit_prod = st.text_input("Producto", value=datos_act['Producto'], key="edit_prod")
                
                col_t, col_p = st.columns(2)
                edit_tipo = col_t.selectbox("Tipo", ["Seco", "Refrigerado"], 
                                            index=0 if datos_act['Tipo_Producto']=="Seco" else 1,
                                            key="edit_tipo")
                edit_prior = col_p.selectbox("Prioridad", ["Alta", "Media", "Baja"],
                                             index=["Alta", "Media", "Baja"].index(datos_act['Prioridad']),
                                             key="edit_prior")
                
                col_time2, col_dur2 = st.columns(2)
                edit_time = col_time2.time_input("Hora Llegada", value=datos_act['Hora_Llegada_Est'].time())
                edit_dur = col_dur2.number_input("Duración", value=int(datos_act['Duracion_Min']), key="edit_dur")
                
                col_save, col_del = st.columns(2)
                if col_save.button("💾 Guardar", use_container_width=True):
                    idx = st.session_state.df_input[st.session_state.df_input['ID_Camion'] == camion_sel].index[0]
                    new_dt = datetime.combine(datetime.now().date(), edit_time)
                    
                    st.session_state.df_input.at[idx, 'Producto'] = edit_prod
                    st.session_state.df_input.at[idx, 'Tipo_Producto'] = edit_tipo
                    st.session_state.df_input.at[idx, 'Prioridad'] = edit_prior
                    st.session_state.df_input.at[idx, 'Hora_Llegada_Est'] = new_dt
                    st.session_state.df_input.at[idx, 'Duracion_Min'] = edit_dur
                    
                    st.success("✅ Actualizado")
                    st.rerun()
                
                if col_del.button("🗑️ Eliminar", use_container_width=True):
                    st.session_state.df_input = st.session_state.df_input[
                        st.session_state.df_input['ID_Camion'] != camion_sel
                    ]
                    st.rerun()
        else:
            st.info("No hay camiones. Agrega uno o genera un escenario.")

# ═══════════════════════════════════════════════════════════
# TAB 3: ANALYTICS
# ═══════════════════════════════════════════════════════════
with tab_analytics:
    if st.session_state.df_input.empty:
        st.info("📊 Los analytics aparecerán cuando haya datos para analizar")
    else:
        optimizer = DockOptimizerPro(
            num_docks=num_muelles, 
            dock_config=st.session_state.config_muelles,
            start_hour=hora_inicio
        )
        resultado_df, _ = optimizer.agendar_camiones(st.session_state.df_input)
        
        st.markdown("### 📊 Análisis de Rendimiento")
        
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            # Distribución por prioridad
            if 'Prioridad' in resultado_df.columns:
                prioridad_counts = resultado_df['Prioridad'].value_counts()
                fig_prior = go.Figure(data=[
                    go.Pie(
                        labels=prioridad_counts.index,
                        values=prioridad_counts.values,
                        marker=dict(colors=['#ef4444', '#f59e0b', '#10b981']),
                        hole=0.4
                    )
                ])
                fig_prior.update_layout(
                    title="<b>Distribución por Prioridad</b>",
                    height=350,
                    font=dict(family="Inter, sans-serif")
                )
                st.plotly_chart(fig_prior, use_container_width=True)
        
        with col_chart2:
            # Tiempo de espera por prioridad
            if 'Prioridad' in resultado_df.columns and 'Espera_Min' in resultado_df.columns:
                espera_por_prior = resultado_df.groupby('Prioridad')['Espera_Min'].mean().reset_index()
                
                fig_wait = go.Figure(data=[
                    go.Bar(
                        x=espera_por_prior['Prioridad'],
                        y=espera_por_prior['Espera_Min'],
                        marker_color=['#ef4444', '#f59e0b', '#10b981'],
                        text=espera_por_prior['Espera_Min'].round(1),
                        textposition='auto'
                    )
                ])
                fig_wait.update_layout(
                    title="<b>Tiempo de Espera Promedio por Prioridad</b>",
                    yaxis_title="Minutos",
                    height=350,
                    font=dict(family="Inter, sans-serif")
                )
                st.plotly_chart(fig_wait, use_container_width=True)
        
        # Resumen estadístico
        st.markdown("### 📈 Métricas Clave")
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        
        with col_stat1:
            tasa_exito = (len(resultado_df[resultado_df['Estado'].str.contains('✅')]) / len(resultado_df) * 100) if len(resultado_df) > 0 else 0
            st.metric("Tasa de Éxito", f"{tasa_exito:.1f}%")
        
        with col_stat2:
            max_espera = resultado_df['Espera_Min'].max() if not resultado_df.empty else 0
            st.metric("Máxima Espera", f"{max_espera:.0f} min")
        
        with col_stat3:
            eficiencia = (resultado_df['Duracion_Min'].sum() / ((resultado_df['Duracion_Min'].sum() + resultado_df['Espera_Min'].sum()) if (resultado_df['Duracion_Min'].sum() + resultado_df['Espera_Min'].sum()) > 0 else 1) * 100) if not resultado_df.empty else 0
            st.metric("Eficiencia Operativa", f"{eficiencia:.1f}%")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #64748b; padding: 20px;'>
        <p>SmartDock Pro Enterprise Edition | Sistema de Gestión Logística Avanzado</p>
        <p style='font-size: 0.85rem;'>Optimizado con algoritmos de prioridad y restricciones de muelle</p>
    </div>
""", unsafe_allow_html=True)