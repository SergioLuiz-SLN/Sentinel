# 🔧 TROUBLESHOOTING — Guia de Resolução de Problemas

Este guia ajuda a diagnosticar e resolver problemas comuns no Sentinel.

---

## 🆘 Troubleshooting Rápido

### Engine não inicia

**Erro:**
```
ModuleNotFoundError: No module named 'yfinance'
```

**Solução:**
```bash
pip install -r Requirements.txt
# ou
pip install yfinance pandas numpy
```

---

### Dashboard mostra "Aguardando primeira leitura"

**Problema**: O painel aparece vazio

**Causa mais comum**: Engine não foi executado ainda

**Solução:**
```bash
# Terminal 1: Execute PRIMEIRO
python src/anomaly_engine.py

# Aguarde 5-10 segundos

# Terminal 2: Depois execute
streamlit run src/dashboard_anomalias.py
```

---

### Porta 8501 já em uso

**Erro:**
```
Address already in use
Port 8501 is already in use.
```

**Opção 1: Use outra porta**
```bash
streamlit run src/dashboard_anomalias.py --server.port 8502
```

**Opção 2: Mate o processo anterior**

Linux/Mac:
```bash
lsof -i :8501
# encontre o PID
kill -9 <PID>
```

Windows (PowerShell):
```powershell
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

---

## 📋 Problemas por Categoria

### ⚙️ Instalação & Setup

#### Problema: Python não encontrado

**Erro:**
```
'python' is not recognized as an internal or external command
```

**Solução:**
1. Verifique instalação: `python --version`
2. Se não aparecer, instale Python em: https://python.org
3. Adicione ao PATH (Windows):
   - Controle+Painel > Sistema > Variáveis de Ambiente
   - Adicione `C:\Users\YourUser\AppData\Local\Programs\Python\Python311`

---

#### Problema: pip não funciona

**Erro:**
```
'pip' is not recognized
```

**Solução:**
```bash
# Tente com módulo
python -m pip install -r Requirements.txt

# Ou upgrade pip
python -m pip install --upgrade pip
```

---

#### Problema: Venv não ativa

**Windows PowerShell:**
```
cannot be loaded because running scripts is disabled
```

**Solução:**
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.venv\Scripts\Activate.ps1
```

**Mac/Linux:**
```bash
# Se não funciona com source
bash .venv/bin/activate
```

---

### 📡 Conectividade & Dados

#### Problema: yfinance connection timeout

**Erro:**
```
ConnectTimeout: HTTPSConnectionPool(host='query1.finance.api.yahoo.com')
ReadTimeout: Read timed out
```

**Causas:**
- Sem conexão de internet
- Servidor Yahoo Finance fora do ar
- VPN bloqueando conexão
- Rate limiting do Yahoo

**Soluções:**

1. **Verifique conectividade:**
   ```bash
   ping 8.8.8.8
   # Se falhar, seu internet está down
   ```

2. **Aumente timeout:**
   ```python
   # No anomaly_engine.py, linha ~30
   stock = yf.Ticker(ticker, timeout=30)  # Aumentar de 10 para 30
   ```

3. **Use proxy (se necessário):**
   ```python
   import os
   os.environ['http_proxy'] = 'http://proxy:port'
   os.environ['https_proxy'] = 'https://proxy:port'
   ```

4. **Tente ticker alternativo:**
   ```bash
   # Alguns tickers podem estar indisponíveis
   # PETR4.SA pode estar bloqueado, tente VALE3.SA
   ```

---

#### Problema: "No such file or directory: log_sistema.txt"

**Erro:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'data/log_sistema.txt'
```

**Causa**: Engine nunca foi executado

**Solução:**
```bash
# 1. Crie o diretório
mkdir data

# 2. Execute o engine (cria o arquivo)
python src/anomaly_engine.py

# 3. Aguarde alguns segundos
# 4. Abra o dashboard
streamlit run src/dashboard_anomalias.py
```

---

#### Problema: Histórico muito curto

**Sintoma**: Dashboard mostra "Mediana: —" ou valores estranhos

**Causa**: Menos de 20 candles de histórico (período muito curto)

**Solução:**
```json
// config/config_motor.json
{
  "parametros": {
    "periodo_dados_meses": 3,  // Aumentar de 2 para 3
    "window_mediana": 10       // Reduzir de 20 para 10
  }
}
```

Reinicie o engine.

---

### 📊 Dashboard & Visualização

#### Problema: Gráfico não atualiza

**Sintoma**: Dados estão desatualizados

**Causa**: Cache ainda não expirou (TTL=5s)

**Solução:**
```bash
# Clique em "🔄 Atualizar" no painel
# Ou limpe o cache:
```

```python
# Adicione ao dashboard_anomalias.py
st.cache_data.clear()
```

---

#### Problema: Tabela truncada no navegador

**Sintoma**: Colunas cortadas na tela

**Solução:**
```bash
# 1. Maximize a janela do navegador
# 2. Ou zoom-out (Ctrl + - no navegador)
# 3. Ou abra em tela cheia (F11)
```

---

#### Problema: Emojis não aparecem

**Erro:**
```
UnicodeDecodeError: 'utf-8' codec can't decode byte
```

**Solução:**
```python
# anomaly_engine.py linha ~10
# Adicione encoding explícito:
with open(caminho_log, "w", encoding="utf-8") as f:
    f.write(resultado)
```

---

### 🔧 Configuração

#### Problema: config_motor.json não encontrado

**Erro:**
```
FileNotFoundError: [Errno 2] config/config_motor.json
```

**Solução:**
```bash
# Crie o arquivo manualmente
mkdir config
cat > config/config_motor.json << 'EOF'
{
  "paths": {
    "log_processado": "data/log_sistema.txt"
  },
  "parametros": {
    "ativos": ["PETR4.SA", "VALE3.SA"]
  }
}
EOF
```

---

#### Problema: Configuração inválida (JSON syntax)

**Erro:**
```
json.JSONDecodeError: Expecting ',' delimiter
```

**Causa**: Erro no JSON (falta vírgula, aspas não balanceadas)

**Solução:**
1. Abra config/config_motor.json
2. Use validador JSON: https://jsonlint.com
3. Verifique:
   - Aspas duplas `"`, não simples `'`
   - Vírgulas entre elementos
   - Sem vírgula após último elemento
   - Chaves/colchetes balanceados

**Exemplo correto:**
```json
{
  "parametros": {
    "ativos": ["PETR4.SA", "VALE3.SA"],
    "mad_multiplier": 3.0
  }
}
```

---

#### Problema: Ativo inválido

**Erro:**
```
No data found for ticker INVALID.SA
```

**Causa**: Ticker não existe ou não tem dados no Yahoo Finance

**Solução:**
```bash
# Verifique tickers válidos B3:
# https://www.b3.com.br

# Use tickers populares:
# PETR4.SA, VALE3.SA, ITUB4.SA, BBDC4.SA, ABEV3.SA

# Teste no Python:
python -c "import yfinance; print(yfinance.Ticker('PETR4.SA').history(period='1mo'))"
```

---

### 🐳 Docker

#### Problema: Docker não encontrado

**Erro:**
```
docker: command not found
```

**Solução:**
- Instale Docker: https://www.docker.com/products/docker-desktop
- Verifique instalação: `docker --version`

---

#### Problema: Imagem não builda

**Erro:**
```
failed to solve with frontend dockerfile.v0
```

**Solução:**
```bash
# 1. Verifique arquivo Requirements.txt existe
ls Requirements.txt

# 2. Limpe cache Docker
docker builder prune

# 3. Force rebuild
docker build --no-cache -t sentinel:latest .
```

---

#### Problema: Container para ao iniciar

**Sintoma**: `docker ps` mostra exit code ≠ 0

**Solução:**
```bash
# Veja os logs
docker logs sentinel-engine

# Debug interativo
docker run -it sentinel:latest bash

# Teste manualmente
docker run -it sentinel:latest python src/anomaly_engine.py
```

---

#### Problema: Volume permissions denied

**Erro:**
```
Permission denied: './data/log_sistema.txt'
```

**Linux:**
```bash
chmod 777 data
docker run -v $(pwd)/data:/app/data sentinel:latest
```

**Docker Compose:**
```yaml
services:
  engine:
    user: "0:0"  # Run as root
    # ou usar volumes nomeados
    volumes:
      - data_volume:/app/data
volumes:
  data_volume:
```

---

### ☸️ Kubernetes

#### Problema: Pod não inicia

**Erro:**
```
ImagePullBackOff
CrashLoopBackOff
```

**Verificar:**
```bash
kubectl describe pod sentinel-engine
kubectl logs sentinel-engine
```

**Soluções:**
```bash
# 1. Verifique imagem existe
docker images | grep sentinel

# 2. Verifique config map
kubectl describe configmap sentinel-config

# 3. Verifique persistência
kubectl get pvc
```

---

### 🔍 Performance & Otimização

#### Problema: Processamento lento

**Sintoma**: Engine demora >5min por ciclo

**Causa comum**: Muitos ativos (>1000) ou histórico longo

**Solução:**
```python
# Paralelizar processamento
from multiprocessing import Pool

def processar_ativos_paralelo(tickers):
    with Pool(processes=4) as pool:
        resultados = pool.map(processar_ativo, tickers)
    return resultados
```

---

#### Problema: Alto consumo de memória

**Sintoma**: RAM >1GB

**Causa**: Histórico muito longo

**Solução:**
```json
{
  "parametros": {
    "periodo_dados_meses": 1,  // Reduzir de 2 para 1
    "window_mediana": 10       // Reduzir de 20 para 10
  }
}
```

---

#### Problema: Dashboard carrega lentamente

**Sintoma**: Demora >5s para recarregar

**Causa**: Cache expirou, muitos dados

**Solução:**
```python
# Aumente TTL do cache
@st.cache_data(ttl=30)  # De 5 para 30 segundos
def ler_log_processado():
    # ...
```

---

### 🔐 Segurança

#### Problema: Arquivo sensível exposto

**Causa**: Config com senhas em git

**Solução:**
```bash
# 1. Adicione ao .gitignore
echo "config/config_motor.json" >> .gitignore
echo ".env" >> .gitignore

# 2. Use .env.example para template
cp .env.example .env

# 3. Configure via variáveis de ambiente
export SENTINEL_CONFIG_PATH="/secure/path/config.json"
```

---

#### Problema: Não tem permissão para escrever logs

**Erro:**
```
PermissionError: [Errno 13] Permission denied: 'data/log_sistema.txt'
```

**Linux/Mac:**
```bash
# Verifique permissões
ls -la data/

# Ajuste se necessário
chmod 755 data
chmod 644 data/log_sistema.txt
```

---

## 📞 Escalação

### Se nenhuma solução funcionar:

1. **Colete informações:**
   ```bash
   python --version
   pip list
   docker --version  # se aplicável
   uname -a  # Sistema operacional
   ```

2. **Reproduza o erro com minimal example:**
   ```bash
   # Teste sem customizações
   git clone https://github.com/slnit/sentinel.git
   cd sentinel
   pip install -r Requirements.txt
   python src/anomaly_engine.py
   ```

3. **Abra uma issue:**
   - https://github.com/slnit/sentinel/issues
   - Inclua:
     - Versões (Python, packages)
     - Sistema operacional
     - Erro completo (stack trace)
     - Passos para reproduzir
     - Logs (use `--log-level DEBUG`)

4. **Contate suporte:**
   - Email: support@slnit.com.br
   - LinkedIn: @slnit

---

## 💡 Debug Avançado

### Modo Debug

```bash
# Engine com logging detalhado
python src/anomaly_engine.py --log-level DEBUG

# Dashboard com logging
streamlit run src/dashboard_anomalias.py --logger.level=debug
```

### Inspecionando o Log

```bash
# Ver conteúdo
cat data/log_sistema.txt

# Últimas 20 linhas
tail -20 data/log_sistema.txt

# Procurar ANOMALIA
grep ANOMALIA data/log_sistema.txt

# Contar linhas
wc -l data/log_sistema.txt
```

### Python REPL

```python
import pandas as pd
import json

# Ler log
with open("data/log_sistema.txt") as f:
    conteudo = f.read()
    print(conteudo)

# Processar com pandas
# (implementar parsing)

# Testar config
with open("config/config_motor.json") as f:
    config = json.load(f)
    print(config)
```

---

<div align="center">

**Troubleshooting — Sentinel by SLN IT Solutions**

[Issues](https://github.com/slnit/sentinel/issues) • [Discussions](https://github.com/slnit/sentinel/discussions) • [Email](mailto:support@slnit.com.br)

</div>
