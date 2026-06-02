import streamlit as st
import pandas as pd
import joblib
import os # <-- Adicionado para lidar com caminhos de pastas

# 1. Configuração da Página
st.set_page_config(page_title="SafeOrbit - Centro de Controle", page_icon="🚀", layout="wide")

# 2. Carregar o Modelo e as Colunas (ATUALIZADO PARA A NUVEM)
@st.cache_resource
def load_model():
    # Descobre a pasta exata onde este arquivo (app.py) está rodando
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    
    # Monta o caminho completo até os arquivos .pkl
    caminho_modelo = os.path.join(pasta_atual, 'safeorbit_xgboost.pkl')
    caminho_colunas = os.path.join(pasta_atual, 'colunas_modelo.pkl')
    
    model = joblib.load(caminho_modelo)
    cols = joblib.load(caminho_colunas)
    return model, cols

modelo, colunas_treino = load_model()

# 3. Interface Visual - Título
st.title("🛰️ SafeOrbit: Triagem de Emergência LEO")
st.markdown("---")

# 4. Barra Lateral - Entrada de Dados da Telemetria (O "Sinal" recebido)
st.sidebar.header("📡 Receber Novo Sinal (Beacon)")

altitude = st.sidebar.slider("Altitude (m)", 0, 6500, 2500)
temp = st.sidebar.slider("Temperatura (°C)", -30.0, 40.0, 15.0)
freq_cardiaca = st.sidebar.number_input("Frequência Cardíaca (bpm)", min_value=0, max_value=220, value=80)
bateria = st.sidebar.slider("Bateria do Beacon (%)", 1, 100, 50)
idade = st.sidebar.number_input("Idade do Usuário", min_value=18, max_value=80, value=30)

clima = st.sidebar.selectbox("Condição Climática", ['Ceu_Limpo', 'Chuva_Forte', 'Nevasca', 'Neblina'])
terreno = st.sidebar.selectbox("Tipo de Terreno", ['Floresta_Densa', 'Montanha_Rochosa', 'Pico_Nevado', 'Corpo_D_Agua', 'Deserto'])

latitude = st.sidebar.number_input("Latitude", value=-23.55)
longitude = st.sidebar.number_input("Longitude", value=-46.63)

# 5. O Botão de Ação
if st.sidebar.button("🚨 Analisar Prioridade de Resgate"):
    
    # Montar o dicionário com os dados brutos inseridos
    input_data = {
        'latitude': latitude, 'longitude': longitude, 'altitude_m': altitude,
        'temperatura_c': temp, 'bateria_beacon_pct': bateria, 
        'frequencia_cardiaca_bpm': freq_cardiaca, 'idade_usuario': idade,
        'clima': clima, 'tipo_terreno': terreno
    }
    
    df_input = pd.DataFrame([input_data])
    
    # Aplicar o One-Hot Encoding exatamente como fizemos no treino
    df_encoded = pd.get_dummies(df_input, columns=['clima', 'tipo_terreno'])
    
    # Garantir que a ordem e as colunas sejam IDÊNTICAS ao que o modelo aprendeu
    df_final = pd.DataFrame(columns=colunas_treino)
    # Preencher com os dados recebidos, os que faltarem viram 0 (False)
    for col in df_final.columns:
        if col in df_encoded.columns:
            df_final[col] = df_encoded[col]
        else:
            df_final[col] = 0
            
    df_final = df_final.fillna(0) # Segurança extra
    
    # 6. Fazer a Previsão
    predicao_num = modelo.predict(df_final)[0]
    
    # 7. Renderizar o Resultado na Tela Principal
    mapa_reverso = {0: 'BAIXA', 1: 'MÉDIA', 2: 'ALTA', 3: 'CRÍTICA'}
    prioridade = mapa_reverso[predicao_num]
    
    st.subheader("Resultado da Triagem da IA:")
    
    if prioridade == 'CRÍTICA':
        st.error(f"## 🔴 PRIORIDADE {prioridade}\nDespacho aéreo imediato recomendado. Risco de morte ininente.")
    elif prioridade == 'ALTA':
        st.warning(f"## 🟠 PRIORIDADE {prioridade}\nPreparar equipe de resgate. Condições severas detectadas.")
    elif prioridade == 'MÉDIA':
        st.info(f"## 🟡 PRIORIDADE {prioridade}\nMonitorar situação. Alocar recursos logísticos padrão.")
    else:
        st.success(f"## 🟢 PRIORIDADE {prioridade}\nSem risco imediato à vida. Encaminhar para resgate terrestre de rotina.")

    st.markdown("---")
    st.write("**Dados Brutos Recebidos:**", input_data)

# --- A MÁGICA DA TELA INICIAL (EMPTY STATE) ---
else:
    st.info("📡 **SISTEMA EM PRONTIDÃO**")
    st.write("O Centro de Controle LEO está operante e aguardando interceptação de sinais SOS...")
    st.markdown("👈 *Configure os parâmetros de telemetria no painel lateral e clique em **Analisar Prioridade de Resgate** para iniciar a triagem da Inteligência Artificial.*")
    
    # Ícone centralizado para dar um visual legal de "esperando"
    st.markdown("<h1 style='text-align: center; color: grey; font-size: 80px;'>🛰️🌍</h1>", unsafe_allow_html=True)