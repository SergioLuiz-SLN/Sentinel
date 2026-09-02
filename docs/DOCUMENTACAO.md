# 📚 Documentação Completa — Sentinel

> **Guia Centralizado de Toda a Documentação do Sentinel**

Bem-vindo à documentação oficial do Sentinel! Este arquivo te ajuda a encontrar o que você precisa.

---

## 🗺️ Mapa de Documentação

### Para Começar

| Documento | Descrição | Tempo |
|-----------|-----------|-------|
| [README.md](../README.md) | Visão geral, case study e features | 5min |
| [GETTING_STARTED.md](../GETTING_STARTED.md) | Tutorial passo-a-passo para iniciantes | 10min |
| [.env.example](../.env.example) | Variáveis de ambiente disponíveis | 2min |

### Desenvolvimento & Técnico

| Documento | Descrição | Público |
|-----------|-----------|---------|
| [ARCHITECTURE.md](../ARCHITECTURE.md) | Design técnico, algoritmos e componentes | Desenvolvedor |
| [CONTRIBUTING.md](../CONTRIBUTING.md) | Como contribuir com código | Contribuidor |
| [CHANGELOG.md](../CHANGELOG.md) | Histórico de versões e roadmap | Todo mundo |

### Operações & Deployment

| Documento | Descrição | Público |
|-----------|-----------|---------|
| [DEPLOYMENT.md](../DEPLOYMENT.md) | Guia de deployment (Docker, K8s, Cloud) | DevOps/SRE |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Resolução de problemas | Todos |

### Configuração & Uso

| Arquivo | Descrição |
|---------|-----------|
| `config/config_motor.json` | Configuração do engine (ativos, parâmetros) |
| `.env.example` | Template de variáveis de ambiente |
| `Dockerfile` | Container do Sentinel |
| `docker-compose.yml` | Orquestração completa |

### Código Fonte

| Arquivo | Descrição | Linhas |
|---------|-----------|--------|
| `src/anomaly_engine.py` | 🔧 Motor de detecção estatística | ~100 |
| `src/dashboard_anomalias.py` | 📊 Dashboard Streamlit | ~400 |

---

## 📖 Guias por Perfil

### 👤 Usuário Final / Analista

**Meta**: Usar o Sentinel para monitorar ativos

**Leia nesta ordem:**
1. [README.md](../README.md) — Entender o que é
2. [GETTING_STARTED.md](../GETTING_STARTED.md) — Instalar e rodar
3. [TROUBLESHOOTING.md](TROUBLESHOOTING.md) — Se algo não funcionar

**Tempo total**: ~20 minutos

---

### 👨‍💻 Desenvolvedor / Engenheiro de Software

**Meta**: Entender e estender o Sentinel

**Leia nesta ordem:**
1. [README.md](../README.md) — Visão geral
2. [ARCHITECTURE.md](../ARCHITECTURE.md) — Design técnico
3. [GETTING_STARTED.md](../GETTING_STARTED.md) — Setup local
4. [CONTRIBUTING.md](../CONTRIBUTING.md) — Como contribuir
5. `src/anomaly_engine.py` — Código fonte

**Tempo total**: ~45 minutos

---

### 🚀 DevOps / SRE

**Meta**: Deployar e operar o Sentinel em produção

**Leia nesta ordem:**
1. [DEPLOYMENT.md](../DEPLOYMENT.md) — Todas as opções de deploy
2. [ARCHITECTURE.md](../ARCHITECTURE.md) — Para entender scale
3. [TROUBLESHOOTING.md](TROUBLESHOOTING.md) — Operações
4. `.env.example` → `.env` — Configurar variáveis

**Tempo total**: ~30 minutos

---

### 🤝 Contribuidor

**Meta**: Contribuir com melhorias

**Leia nesta ordem:**
1. [CONTRIBUTING.md](../CONTRIBUTING.md) — Diretrizes
2. [ARCHITECTURE.md](../ARCHITECTURE.md) — Entender design
3. [CHANGELOG.md](../CHANGELOG.md) — Roadmap
4. `src/` — Explorar código

**Tempo total**: Variável (depende da contribuição)

---

## 🎯 Tópicos Comuns

### "Como instalar?"

→ [GETTING_STARTED.md](../GETTING_STARTED.md) (Seção 1-2)

### "Como configurar para meus ativos?"

→ [GETTING_STARTED.md](../GETTING_STARTED.md) (Seção 4)

### "Como ajustar sensibilidade?"

→ [GETTING_STARTED.md](../GETTING_STARTED.md) (Seção 5)

### "Como funciona o algoritmo?"

→ [ARCHITECTURE.md](../ARCHITECTURE.md) (Seção "Algoritmo de Detecção")

### "Como deployer em produção?"

→ [DEPLOYMENT.md](../DEPLOYMENT.md)

### "Como usar Docker?"

→ [DEPLOYMENT.md](../DEPLOYMENT.md) (Seção "Docker Deployment")

### "Como usar Kubernetes?"

→ [DEPLOYMENT.md](../DEPLOYMENT.md) (Seção "Kubernetes Deployment")

### "Algo não funciona!"

→ [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

### "Como contribuir?"

→ [CONTRIBUTING.md](../CONTRIBUTING.md)

### "Qual é o roadmap?"

→ [CHANGELOG.md](../CHANGELOG.md) (Seção "Roadmap")

---

## 📁 Estrutura de Arquivos

```
Sentinel/
│
├── 📄 README.md                  ← COMECE AQUI
├── 📄 ARCHITECTURE.md            ← Design técnico
├── 📄 DEPLOYMENT.md              ← Como deployar
├── 📄 GETTING_STARTED.md         ← Tutorial passo-a-passo
├── 📄 CONTRIBUTING.md            ← Como contribuir
├── 📄 CHANGELOG.md               ← Histórico de versões
├── 📄 .env.example               ← Variáveis de ambiente
│
├── 📁 docs/
│   └── 📄 TROUBLESHOOTING.md     ← Resolvendo problemas
│
├── 📁 config/
│   └── config_motor.json         ← Configuração (edite aqui!)
│
├── 📁 data/
│   └── log_sistema.txt           ← Saída do engine (gerado)
│
├── 📁 src/
│   ├── anomaly_engine.py         ← 🔧 Motor de análise
│   ├── dashboard_anomalias.py    ← 📊 Dashboard
│   └── data/
│       └── log_sistema.txt
│
├── 📄 Dockerfile                 ← Imagem Docker
├── 📄 docker-compose.yml         ← Orquestração
├── 📄 .dockerignore              ← Otimização Docker
├── 📄 Requirements.txt           ← Dependências Python
└── 📄 .gitignore                 ← Arquivos ignorados no Git
```

---

## 🔄 Fluxo de Documentação

### Usuário Novo

```
README
  ↓
GETTING_STARTED (instalação)
  ↓
Dashboard funcionando!
  ↓
Quer customizar?
  ├→ GETTING_STARTED (Seção 4-5)
  └→ TROUBLESHOOTING (se problema)
```

### Desenvolvedor Novo

```
README
  ↓
ARCHITECTURE
  ↓
GETTING_STARTED (dev setup)
  ↓
CONTRIBUTING
  ↓
Explorar código fonte
  ↓
Fazer PR!
```

### Deploy em Produção

```
DEPLOYMENT
  ├→ Docker ✅
  ├→ Docker Compose ✅
  ├→ Kubernetes
  │  ├→ Setup k8s/
  │  └→ kubectl apply
  └→ Cloud Platforms
     ├→ AWS ECS
     ├→ GCP Run
     └→ Heroku
```

---

## 📌 Checklist de Leitura

### Para usar o Sentinel

- [ ] Li o README.md
- [ ] Completei GETTING_STARTED.md
- [ ] Dashboard está rodando
- [ ] Configurei meus ativos

### Para contribuir

- [ ] Li CONTRIBUTING.md
- [ ] Entendi ARCHITECTURE.md
- [ ] Explorei o código fonte
- [ ] Configurei ambiente local

### Para deployar

- [ ] Li DEPLOYMENT.md
- [ ] Escolhi minha plataforma (Docker/K8s/Cloud)
- [ ] Testei localmente
- [ ] Deployei com sucesso

---

## 🆘 Encontrou um Erro na Documentação?

Se achou:
- ❌ Informação incorreta
- ❌ Link quebrado
- ❌ Typos
- ❌ Falta de informação

**Por favor:**
1. Abra uma [Issue](https://github.com/slnit/sentinel/issues)
2. Ou crie um [Pull Request](https://github.com/slnit/sentinel/pulls)

Sua contribuição nos ajuda a melhorar!

---

## 📊 Estatísticas da Documentação

| Item | Valor |
|------|-------|
| Documentos | 8 |
| Linhas totais | ~3,500 |
| Exemplos código | 50+ |
| Screenshots/Diagramas | 15+ |
| Tópicos coberidos | 100+ |
| Idiomas | Português (PT-BR) |

---

## 🌐 Recursos Externos

### Tecnologias Usadas

- [Python Documentation](https://docs.python.org/3/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [NumPy Documentation](https://numpy.org/doc/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Documentation](https://plotly.com/python/)
- [yfinance Documentation](https://github.com/ranaroussi/yfinance)
- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)

### Conceitos Relacionados

- [Median Absolute Deviation (Wikipedia)](https://en.wikipedia.org/wiki/Median_absolute_deviation)
- [Statistical Process Control](https://en.wikipedia.org/wiki/Statistical_process_control)
- [Anomaly Detection (Medium)](https://medium.com/@mohamedvip111/anomaly-detection-using-median-absolute-deviation-mad-7d5b3de82c8c)

---

## 📞 Contato & Suporte

- 🐛 **Bugs/Issues**: [GitHub Issues](https://github.com/slnit/sentinel/issues)
- 💬 **Discussões**: [GitHub Discussions](https://github.com/slnit/sentinel/discussions)
- 📧 **Email**: support@slnit.com.br
- 🔗 **LinkedIn**: [@slnit](https://linkedin.com/company/slnit)
- 🌐 **Website**: [www.slnit.com.br](https://www.slnit.com.br)

---

<div align="center">

**Documentação Oficial — Sentinel by SLN IT Solutions**

**v1.0** | Última atualização: 2024-09-01

[README](../README.md) • [Issues](https://github.com/slnit/sentinel/issues) • [Contato](mailto:support@slnit.com.br)

</div>
