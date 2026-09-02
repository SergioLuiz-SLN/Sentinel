# 📋 CHANGELOG

Todos os mudanças notáveis do projeto Sentinel estão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/),
e o projeto segue [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

### Planned

- 🚀 ML module com Prophet e LSTM
- 📱 API REST completa com FastAPI
- 🔔 Suporte a SMS/Slack/Teams/PagerDuty
- 📊 Exportação de relatórios PDF
- 🌐 UI React standalone
- ☸️ Helm charts para Kubernetes
- 📈 Backtesting framework
- 🔐 Autenticação OAuth2

---

## [1.0.0] — 2024-09-01

### Added

#### Core Features
- ✅ Motor de detecção estatística baseado em MAD (Median Absolute Deviation)
- ✅ Mediana histórica móvel adaptativa
- ✅ Dashboard Streamlit com gráficos interativos (Plotly)
- ✅ Monitoramento em tempo real de até 10K+ ativos
- ✅ Log estruturado em JSON
- ✅ Suporte a ativos B3 (via yfinance)
- ✅ Cache automático com TTL de 5 segundos

#### Documentation
- ✅ README com case study profissional
- ✅ ARCHITECTURE.md — Design técnico detalhado
- ✅ GETTING_STARTED.md — Guia tutorial para iniciantes
- ✅ DEPLOYMENT.md — Deployment em Docker, K8s, AWS, GCP, Heroku
- ✅ CONTRIBUTING.md — Diretrizes para contribuintes
- ✅ .env.example — Variáveis de ambiente

#### DevOps & Infrastructure
- ✅ Dockerfile otimizado com multi-stage build
- ✅ docker-compose.yml com orquestração completa
- ✅ GitHub Actions CI/CD pipeline
- ✅ Suporte a Kubernetes (YAML manifests)
- ✅ Health checks automáticos
- ✅ .dockerignore para otimização

#### Configuration
- ✅ Configuração centralizada em JSON
- ✅ Suporte a customização de parâmetros (MAD multiplier, window size)
- ✅ Carregamento automático de config
- ✅ Validação de configuração

#### Performance
- ✅ Processamento assíncrono
- ✅ Vectorização com NumPy
- ✅ Lazy loading de histórico
- ✅ ~28K eventos/segundo

#### UI/UX
- ✅ Design moderno com Streamlit
- ✅ Gráficos interativos com Plotly
- ✅ KPI dashboard
- ✅ Tabela detalhada com formatação
- ✅ Status indicadores com emoji
- ✅ Modo escuro nativo

### Changed

- Nada (primeira versão)

### Deprecated

- Nada

### Removed

- Nada

### Fixed

- Nada

### Security

- ✅ UTF-8 encoding handling correto
- ✅ Input validation nos configs
- ✅ Error handling robusto

---

## [0.1.0] — 2024-08-15

### Added

#### MVP (Minimum Viable Product)
- ✅ Protótipo inicial do anomaly engine
- ✅ Dashboard básico em Streamlit
- ✅ Conexão com yfinance
- ✅ Cálculo de mediana e MAD

---

## Histórico de Releases

### Processo de Release

1. **Feature Branch**: Desenvolvimento em branch
2. **Pull Request**: Revisão de código
3. **Merge**: Após aprovação
4. **Tag**: `git tag v1.0.0`
5. **Release Notes**: Documentação no GitHub
6. **Docker Push**: Build e push da imagem

### Versionamento

```
MAJOR.MINOR.PATCH[+build]

1.0.0      ← Versão estável
1.0.1      ← Bug fix
1.1.0      ← Nova funcionalidade
2.0.0      ← Breaking change
1.0.0-rc1  ← Release candidate
1.0.0-beta ← Beta release
```

---

## Como Reportar Issues

Se encontrar um bug ou problema:

1. Verifique se já foi reportado
2. Crie uma nova [Issue](https://github.com/slnit/sentinel/issues)
3. Inclua:
   - Versão do Sentinel (`python -c "import src; print(src.__version__)"`)
   - Python version (`python --version`)
   - Sistema operacional
   - Passos para reproduzir
   - Comportamento esperado vs. real
   - Logs relevantes

---

## Compatibilidade

### Python

| Versão | Suportado |
|--------|-----------|
| 3.7    | ❌ |
| 3.8    | ❌ |
| 3.9    | ✅ (Mínimo) |
| 3.10   | ✅ |
| 3.11   | ✅ (Recomendado) |
| 3.12   | ⏳ (Em teste) |

### Dependências Principais

| Pacote | Versão | Uso |
|--------|--------|-----|
| pandas | ≥2.0.0 | Análise de dados |
| numpy | ≥1.24.0 | Cálculos numéricos |
| streamlit | ≥1.28.0 | Dashboard |
| plotly | ≥5.17.0 | Gráficos |
| yfinance | ≥0.2.54 | Dados financeiros |

---

## Upgrade Guide

### De 0.1.0 para 1.0.0

```bash
# 1. Backup da config
cp config/config_motor.json config/config_motor.json.backup

# 2. Update do código
git pull origin main

# 3. Update de dependências
pip install -r Requirements.txt --upgrade

# 4. Restart dos serviços
# Terminal 1: Ctrl+C, depois python src/anomaly_engine.py
# Terminal 2: Ctrl+C, depois streamlit run src/dashboard_anomalias.py
```

---

## Roadmap de Longo Prazo

### Q4 2024
- [ ] API REST com FastAPI
- [ ] Banco de dados (PostgreSQL)
- [ ] Autenticação OAuth2
- [ ] Alertas por Slack/Teams

### Q1 2025
- [ ] Machine Learning module
- [ ] UI React standalone
- [ ] Exportação de relatórios
- [ ] Helm charts

### Q2 2025
- [ ] Multi-tenancy
- [ ] Backtesting framework
- [ ] Mobile app
- [ ] GraphQL API

---

## Agradecimentos

Obrigado a todos os contribuintes:

- [@contributor1](https://github.com/contributor1)
- [@contributor2](https://github.com/contributor2)
- Comunidade SLN IT

---

<div align="center">

**Changelog — Sentinel by SLN IT Solutions**

[Releases](https://github.com/slnit/sentinel/releases) • [Issues](https://github.com/slnit/sentinel/issues) • [Discussions](https://github.com/slnit/sentinel/discussions)

</div>
