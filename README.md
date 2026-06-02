# 🚀 SafeOrbit: Cérebro de Triagem de Emergências LEO

**Global Solution FIAP 2026 - Indústria Espacial: O Código que Move o Universo**
**Disciplina:** Generative AI For Engineering (GAIE)

---

## 🌍 Contexto do Problema
Com a expansão da Economia Espacial e constelações de satélites em Low Earth Orbit (LEO), a conectividade global em áreas remotas tornou-se uma realidade. No entanto, quando múltiplos sinais de emergência (SOS de *Personal Locator Beacons*) são retransmitidos simultaneamente por satélites para um Centro de Controle Terrestre, surge um gargalo operacional: **quem a equipe de resgate deve salvar primeiro?**

O **SafeOrbit** é um motor de Inteligência Artificial desenhado para atuar na recepção dessa telemetria. O modelo cruza os dados vitais da vítima e as condições ambientais (clima, terreno, altitude) para classificar automaticamente a severidade do resgate, priorizando o despacho aéreo para casos de risco iminente à vida (ex: hipotermia ou parada cardíaca).

## 📊 Fonte dos Dados
Para simular as requisições de telemetria satelital, utilizamos Inteligência Artificial Generativa para criar um **dataset sintético rigoroso** (`safeorbit_telemetry.csv`), contendo 1.000 registros e 11 colunas. 
Os dados foram gerados respeitando regras rígidas de correlação física e médica:
* A `temperatura_c` é inversamente proporcional à `altitude_m`.
* Terrenos como `Pico_Nevado` só ocorrem em altas altitudes e temperaturas negativas.
* A classe alvo `prioridade_resgate` (Baixa, Média, Alta, Crítica) é matematicamente dependente de combinações de risco, como bateria do beacon acabando, idade avançada em altitudes extremas, ou anomalias na frequência cardíaca.

## ⚙️ Metodologia Utilizada
O pipeline de Machine Learning foi estruturado seguindo as melhores práticas de Engenharia de Software:
1. **Pré-processamento:** Remoção de identificadores únicos (`id_alerta`) para evitar overfitting.
2. **Engenharia de Atributos:** Aplicação de *One-Hot Encoding* (`pd.get_dummies`) para transformar variáveis categóricas (Clima, Terreno) em matrizes numéricas esparsas.
3. **Divisão de Dados:** `train_test_split` com proporção 80/20, utilizando `stratify` para garantir o balanceamento das classes de prioridade.
4. **Métrica de Negócio (O Custo do Erro):** A otimização focou no **Recall** da classe "Crítica". Em um cenário de resgate, o custo de um Falso Negativo (classificar emergência crítica como baixa) é fatal. 

## 🤖 Modelos Testados e Comparação
Foram testadas duas arquiteturas baseadas em árvores de decisão:

1. **Random Forest Classifier (Baseline):** * Acurácia Global: 93%
   * Recall da classe Crítica: 93%
2. **XGBoost Classifier (Modelo Campeão):**
   * Acurácia Global: **97%**
   * Recall da classe Crítica: **99%**

**Justificativa de Escolha:** O XGBoost foi o escolhido não apenas pela maior acurácia, mas por ter zerado os Falsos Negativos fatais na matriz de confusão durante os testes.

## 🔍 Interpretabilidade com SHAP
Para garantir que o Centro de Controle possa auditar as decisões da IA, aplicamos a biblioteca SHAP (*SHapley Additive exPlanations*). O *Summary Plot* revelou a seguinte hierarquia de importância na tomada de decisão do modelo:
1. **Frequência Cardíaca:** Principal gatilho para a prioridade `Crítica` (coração parando ou em taquicardia severa).
2. **Altitude e Temperatura:** Cruzamento essencial para prever risco de Mal da Montanha e Hipotermia.
3. **Bateria do Beacon:** Peso alto para acelerar despachos antes da perda definitiva de telemetria satelital.

## 🛠️ Instruções para Execução do Projeto

Siga os passos abaixo para rodar o pipeline de treinamento e o Dashboard do Centro de Controle em sua máquina local:

**1. Clone o repositório:**
```bash
git clone [[https://github.com/SEU-USUARIO/safeorbit-ai.git](https://github.com/SEU-USUARIO/safeorbit-ai.git](https://github.com/Leonardo-Valerio/GS-Generative-AI)
cd safeorbit-ai
````

## Link do Projeto
https://gs-generative-ai-lwgyd6tyeqtgadyzyecziv.streamlit.app/

## Imagens do Projeto
<img width="1911" height="851" alt="image" src="https://github.com/user-attachments/assets/f4cb19a5-8fe4-41b6-b2fd-dfaea6a8ca13" />
<img width="1899" height="863" alt="image" src="https://github.com/user-attachments/assets/6ba9559c-31d9-4526-a743-fb3493849ad1" />

