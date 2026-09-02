# 🚀 SENTINEL — Getting Started Guide

**Tempo estimado**: 5 minutos ⏱️

Bem-vindo ao Sentinel! Este guia vai te colocar em operação em minutos.

---

## ✨ O que é o Sentinel?

Sentinel detecta **anomalias automáticas** em dados financeiros usando inteligência estatística. Ele aprende padrões normais e avisa quando algo sai do esperado.

```
Valor Normal: 1.2M
Valor Atual:  8.9M ← ANOMALIA DETECTADA! 🚨
```

---

## 📋 Pré-requisitos

Você precisa de:

- **Python 3.9+** (Verifique: `python --version`)
- **pip** (Gerenciador de pacotes Python)
- **Conexão de internet** (para baixar dados)
- **~500MB de espaço** em disco

---

## 1️⃣ Instalação (2 minutos)

### Passo 1: Abra o Terminal

**Windows:**
- Pressione `Win + R`
- Digite `cmd` e pressione Enter

**Mac/Linux:**
- Abra o Terminal (Cmd + Espaço, digite "terminal")

### Passo 2: Navegue para o projeto

```bash
cd Desktop/Sistemas/Sentinel
```

### Passo 3: Crie um ambiente virtual

Um ambiente virtual isola as dependências do Python.

```bash
python -m venv .venv
```

### Passo 4: Ative o ambiente

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

Se receber erro de permissão, execute:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

**Windows (CMD):**
```cmd
.venv\Scripts\activate.bat
```

**Mac/Linux:**
```bash
source .venv/bin/activate
```

Você deve ver `(.venv)` no início do seu terminal.

### Passo 5: Instale dependências

```bash
pip install -r Requirements.txt
```

Isso vai levar 2-3 minutos. Você verá:
```
Collecting pandas>=2.0.0
Collecting numpy>=1.24.0
...
Successfully installed pandas-2.0.0 numpy-1.24.0 ...
```

✅ **Pronto!** Tudo instalado.

---

## 2️⃣ Executar (1 minuto)

### Abra DOIS terminais

Você precisa rodar duas coisas simultaneamente:
1. **Engine** (processa dados)
2. **Dashboard** (mostra resultados)

### Terminal 1: Execute o Motor

```bash
python src/anomaly_engine.py
```

Você verá:
```
MOTOR: 01/09/2026 14:30:45
NORMAL | Serviço: PETR4 | Data: 01/09 14:30 | Preço: 28.45 | Atual: 1.2M | Mediana: 1.1M | Limite: 1.5M
ANOMALIA | Serviço: VALE3 | Data: 01/09 14:31 | Preço: 67.89 | Atual: 8.9M | Mediana: 2.1M | Limite: 3.2M
```

### Terminal 2: Execute o Dashboard

```bash
streamlit run src/dashboard_anomalias.py
```

Você verá:
```
Collecting usage statistics. To deactivate, set browser.gatherUsageStats to false.
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.100:8501
```

### Abra no Navegador

Clique no link ou acesse: **http://localhost:8501**

🎉 **Dashboard está ativo!**

---

## 3️⃣ Entender o Dashboard

### Seção Superior: KPIs

```
┌─────────────────────────────────────────────┐
│  5 Ativos  │  1 Alerta  │  80% Normal  │ ... │
└─────────────────────────────────────────────┘
```

- **Ativos Monitorados**: Número de ações sendo analisadas
- **Alertas Críticos**: Anomalias detectadas
- **Estabilidade**: Porcentagem normal (verde ✅ se >90%)

### Gráfico Principal

```
Volume
  ▲
  │         ┌─ PETR4 (Normal)
  │    ╱╲   │
  │   ╱  ╲  │
  │  ╱    ╲╱
  ├───────────► Tempo
  │    VALE3  ╱╲  ← ANOMALIA!
  │          ╱  ╲
```

- **Barras azuis**: Volume atual (normal)
- **Barras vermelhas**: Volume anômalo
- **Linha verde**: Baseline esperado
- **Linha amarela pontilhada**: Limite (3σ)

### Recomendações

```
⚡ RECOMENDAÇÕES
🚨 1 Alerta
VALE3 está 324% acima do limite. 
Ação recomendada: Investigar imediatamente
```

### Tabela Detalhada

```
Status  │ Ativo │ Data      │ Preço  │ Volume Atual │ Mediana │ Limite │ Desvio %
────────┼───────┼───────────┼────────┼──────────────┼─────────┼────────┼─────────
🟢 Normal│ PETR4 │ 01/09 14:30│ R$ 28.45│   1.2M    │  1.1M   │ 1.5M   │  +9.1%
🔴 Atenção│VALE3│ 01/09 14:31│ R$ 67.89│   8.9M    │  2.1M   │ 3.2M   │ +324%
```

---

## 4️⃣ Configurar Ativos (5 minutos)

### Adicionar/Remover Ativos

Edite `config/config_motor.json`:

```json
{
  "parametros": {
    "ativos": [
      "PETR4.SA",      ← Petrobras
      "VALE3.SA",      ← Vale
      "ITUB4.SA",      ← Itau
      "BBDC4.SA",      ← Bradesco
      "ABEV3.SA"       ← Ambev
    ]
  }
}
```

### Adicionar Nova Ação

1. Abra `config/config_motor.json`
2. Adicione um novo ticker à lista:
```json
"ativos": [
  "PETR4.SA",
  "VALE3.SA",
  "WEGE3.SA"  ← Novo ativo
]
```
3. Salve o arquivo
4. Reinicie o engine (Ctrl+C no Terminal 1, depois execute novamente)

### Ações Populares B3

| Ticker | Empresa |
|--------|---------|
| PETR4.SA | Petrobras |
| VALE3.SA | Vale |
| ITUB4.SA | Itaú Unibanco |
| BBDC4.SA | Banco Bradesco |
| ABEV3.SA | Ambev |
| WEGE3.SA | Weg |
| JBSS3.SA | JBS |
| GOLL4.SA | Gol Linhas Aéreas |

---

## 5️⃣ Ajustar Sensibilidade

### Entender os Parâmetros

```json
{
  "parametros": {
    "periodo_dados_meses": 2,      ← Quanto histórico analisar
    "window_mediana": 20,          ← Últimos N candles
    "mad_multiplier": 3.0          ← Sensibilidade (2=mais, 4=menos)
  }
}
```

### Cenários Comuns

**Mais Alertas (Sensível):**
```json
"mad_multiplier": 2.0,    ← Dispara mais fácil
"window_mediana": 10      ← Menos contexto
```

**Menos Alertas (Conservador):**
```json
"mad_multiplier": 4.0,    ← Menos sensível
"window_mediana": 30      ← Mais contexto
```

**Recomendado (Balanceado):**
```json
"mad_multiplier": 3.0,    ← Bom equilíbrio
"window_mediana": 20
```

---

## 🔄 Usar com Docker (Opcional)

Se preferir não instalar Python localmente:

```bash
# Build
docker build -t sentinel:latest .

# Run
docker-compose up -d

# Acesse
# http://localhost:8501

# Stop
docker-compose down
```

---

## 🆘 Problemas Comuns

### ❌ "ModuleNotFoundError: No module named 'streamlit'"

**Causa**: Dependências não instaladas  
**Solução**:
```bash
pip install -r Requirements.txt
```

### ❌ "Connection refused: http://localhost:8501"

**Causa**: Dashboard não está rodando  
**Solução**:
```bash
# Terminal 2
streamlit run src/dashboard_anomalias.py
```

### ❌ "No such file or directory: log_sistema.txt"

**Causa**: Engine ainda não foi executado  
**Solução**:
```bash
# Terminal 1 (primeiro!)
python src/anomaly_engine.py

# Aguarde 5-10 segundos
# Terminal 2
streamlit run src/dashboard_anomalias.py
```

### ❌ "Porta 8501 já em uso"

**Causa**: Outro programa usando a porta  
**Solução 1**: Use outra porta
```bash
streamlit run src/dashboard_anomalias.py --server.port 8502
```

**Solução 2**: Mateu o processo anterior
```bash
# Linux/Mac:
lsof -i :8501 | grep LISTEN | awk '{print $2}' | xargs kill -9

# Windows:
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

### ❌ "No internet connection" (yfinance)

**Causa**: Sem conexão com servidor Yahoo Finance  
**Solução**: Aguarde ou verifique seu WiFi
```bash
ping 8.8.8.8
```

---

## 📞 Próximos Passos

### Explorar Mais

- 📖 [Documentação Técnica](ARCHITECTURE.md)
- 🚀 [Guia de Deployment](DEPLOYMENT.md)
- 🔧 [Troubleshooting Avançado](docs/TROUBLESHOOTING.md)

### Integrar com Outros Sistemas

- 🔗 Enviar alertas por Email
- 📱 Integrar com Slack/Teams
- 📊 Exportar relatórios PDF
- 🌐 Publicar em produção

### Contribuir

```bash
git clone https://github.com/slnit/sentinel.git
git checkout -b minha-feature
# ... faça suas mudanças
git push origin minha-feature
# Abra um Pull Request
```

---

## 💡 Dicas & Tricks

### Executar Engine em Background

**Linux/Mac:**
```bash
nohup python src/anomaly_engine.py > sentinel.log 2>&1 &
```

**Windows (PowerShell):**
```powershell
Start-Process python -ArgumentList "src/anomaly_engine.py" -NoNewWindow
```

### Usar systemd (Linux)

Crie `/etc/systemd/system/sentinel.service`:
```ini
[Unit]
Description=Sentinel Anomaly Engine
After=network.target

[Service]
Type=simple
User=sentinel
WorkingDirectory=/path/to/sentinel
ExecStart=/path/to/sentinel/.venv/bin/python src/anomaly_engine.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Depois:
```bash
sudo systemctl enable sentinel
sudo systemctl start sentinel
```

---

## 📧 Suporte

- 🐛 **Bugs**: https://github.com/slnit/sentinel/issues
- 💬 **Discussões**: https://github.com/slnit/sentinel/discussions
- 📧 **Email**: support@slnit.com.br

---

<div align="center">

**Desenvolvido por SLN IT Solutions**

Transforme Dados em Inteligência | Detecte Anomalias Antes Que Se Tornem Crises

[🌐 Website](https://www.slnit.com.br) • [🔗 LinkedIn](https://linkedin.com/company/slnit) • [📧 Contato](mailto:contact@slnit.com.br)

</div>
