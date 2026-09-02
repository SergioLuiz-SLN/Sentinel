# 🤝 CONTRIBUTING — Guia para Contribuintes

Obrigado por considerar contribuir para o Sentinel! Seu feedback e código são valiosos para melhorar este projeto.

---

## 📋 Código de Conduta

Este projeto segue um Código de Conduta para garantir um ambiente acolhedor e inclusivo. Ao participar, você concorda em:

- ✅ Ser respeitoso com outros contribuintes
- ✅ Fornecer feedback construtivo
- ✅ Aceitar críticas técnicas com graça
- ✅ Focar no que é melhor para a comunidade

---

## 🐛 Reportando Bugs

### Antes de Criar uma Issue

1. Verifique se já existe uma issue similar
2. Atualize para a versão mais recente
3. Teste sem customizações para isolar o problema

### Como Reportar

Clique em [New Issue](https://github.com/slnit/sentinel/issues/new) e inclua:

```markdown
## Descrição
Descrição clara do bug

## Passos para Reproduzir
1. Execute...
2. Observe...
3. Resultado esperado vs real

## Ambiente
- OS: [Windows/Linux/Mac]
- Python: 3.9 / 3.10 / 3.11
- Sentinel Version: 1.0.0

## Logs
[Copie logs relevantes aqui]
```

---

## 💡 Sugerindo Melhorias

### Tipos de Sugestões Bem-Vindas

- 🎯 Novos algoritmos de detecção
- 📊 Melhorias no dashboard
- 🚀 Performance otimizations
- 📚 Documentação melhorada
- 🔧 Suporte a novas datasources
- 🔗 Integrações (Slack, Teams, etc.)

### Como Sugerir

Crie uma [Discussion](https://github.com/slnit/sentinel/discussions) com:

```markdown
## Título Descritivo
Uma frase clara da sua ideia

## Problema que Resolve
Como isso melhora o Sentinel?

## Solução Proposta
Sua implementação sugerida

## Alternativas Consideradas
Outras abordagens exploradas
```

---

## 🔨 Pull Requests (PRs)

### Antes de Começar

1. Faça fork do repositório
2. Crie uma branch: `git checkout -b feature/sua-feature`
3. Instale dependências de dev: `pip install -r Requirements-dev.txt`

### Workflow

```bash
# 1. Clone seu fork
git clone https://github.com/seu-usuario/sentinel.git
cd sentinel

# 2. Crie uma branch descritiva
git checkout -b fix/bug-nome
# ou
git checkout -b feature/nova-funcionalidade

# 3. Faça suas mudanças
# Edite os arquivos, teste localmente

# 4. Commit com mensagem clara
git add .
git commit -m "Fix: Descrição clara do que foi feito"

# 5. Push para seu fork
git push origin fix/bug-nome

# 6. Abra um PR no GitHub
# Vá para https://github.com/slnit/sentinel/pulls
```

### Padrões de Commit

Use prefixos convencionais:

```
feat:  Nova funcionalidade
fix:   Correção de bug
docs:  Documentação
style: Formatação (sem lógica)
refactor: Reestruturação (sem mudança de comportamento)
perf:  Melhoria de performance
test:  Testes
chore: Tarefas de build/dependencies
ci:    Mudanças em CI/CD
```

**Exemplos:**
```
git commit -m "feat: Add webhook notifications"
git commit -m "fix: Resolve mediana calculation for empty arrays"
git commit -m "docs: Update deployment guide for Kubernetes"
git commit -m "perf: Optimize dataframe filtering with numba"
```

### Abrindo um Pull Request

Sua PR deve:

1. **Título claro**: `[fix/feat/docs] Descrição breve`
2. **Descrição detalhada**: O que muda e por quê
3. **Issue relacionada**: `Closes #123`
4. **Testes**: Incluir testes para novas funcionalidades
5. **Documentação**: Atualizar docs se necessário

**Template:**
```markdown
## Descrição
Breve descrição das mudanças

## Tipo de Mudança
- [ ] Bug fix
- [ ] Nova funcionalidade
- [ ] Breaking change
- [ ] Atualização de docs

## Relacionado à Issue
Closes #123

## Como foi Testado
- [ ] Teste unitário adicionado
- [ ] Testado localmente
- [ ] Não quebra testes existentes

## Checklist
- [ ] Código segue style guide
- [ ] Comentários adicionados
- [ ] Documentação atualizada
- [ ] Sem warning gerados
```

---

## 📝 Estilo de Código

### Python

```python
# ✅ BOM
def calcular_desvio_percentual(valor_atual: float, baseline: float) -> float:
    """Calcula desvio em relação ao baseline.
    
    Args:
        valor_atual: Valor observado
        baseline: Valor esperado
        
    Returns:
        Percentual de desvio
    """
    return ((valor_atual / baseline - 1) * 100) if baseline > 0 else 0


# ❌ RUIM
def calc(a,b):
    return (a/b-1)*100 if b>0 else 0
```

### Conventions

- **Nomes**: `snake_case` para funções/variáveis, `PascalCase` para classes
- **Docstrings**: Formato Google (veja exemplo acima)
- **Imports**: Organize com `isort`
- **Formatting**: Use `black` (88 caracteres)
- **Linting**: `flake8` com 88 chars
- **Type hints**: Sempre use para funções públicas

### Instalando ferramentas

```bash
pip install black flake8 isort pytest
```

Antes de committar:
```bash
black src/
isort src/
flake8 src/
pytest
```

---

## 🧪 Testes

### Estrutura

```
tests/
├── test_anomaly_engine.py
├── test_dashboard.py
└── fixtures/
    └── sample_data.json
```

### Exemplos

```python
# tests/test_anomaly_engine.py
import pytest
from src.anomaly_engine import calcular_mediana, calcular_mad

def test_calcular_mediana_valores_simples():
    dados = [1, 2, 3, 4, 5]
    assert calcular_mediana(dados) == 3

def test_calcular_mediana_valores_pares():
    dados = [1, 2, 3, 4]
    assert calcular_mediana(dados) == 2.5

def test_calcular_mediana_array_vazio():
    with pytest.raises(ValueError):
        calcular_mediana([])

def test_calcular_mad():
    dados = [1, 2, 3, 4, 5]
    mad = calcular_mad(dados)
    assert mad == 1  # Mediana dos desvios

def test_detectar_anomalia_valor_alto():
    valores = [100, 110, 105, 120, 115]
    limiar = 150
    assert detectar_anomalia(200, limiar) == True

def test_detectar_anomalia_valor_normal():
    valores = [100, 110, 105, 120, 115]
    limiar = 150
    assert detectar_anomalia(120, limiar) == False
```

### Executar Testes

```bash
# Todos os testes
pytest

# Com coverage
pytest --cov=src

# Teste específico
pytest tests/test_anomaly_engine.py::test_calcular_mediana_valores_simples

# Modo verbose
pytest -v
```

---

## 📚 Melhorando Documentação

Documentação é código! Bem-vindo para:

### Tipos de Docs

1. **README.md**: Visão geral do projeto
2. **ARCHITECTURE.md**: Design técnico
3. **DEPLOYMENT.md**: Como colocar em produção
4. **GETTING_STARTED.md**: Tutorial para iniciantes
5. **Docstrings**: Comentários inline no código
6. **Examples**: Notebooks e scripts de exemplo

### Como Contribuir

```bash
# 1. Edite o arquivo
vim ARCHITECTURE.md

# 2. Verifique formatação Markdown
# (Use um preview no VS Code ou GitHub)

# 3. Commit
git commit -m "docs: Expand ARCHITECTURE.md with examples"

# 4. Push e PR
git push origin docs/expand-architecture
```

---

## 🎯 Roadmap & Oportunidades

### Buscamos Contribuições Em

- ✨ **Algoritmos ML**: Prophet, LSTM, Isolation Forest
- 🔗 **Integrações**: Slack, Teams, PagerDuty
- 🌐 **UI Moderna**: React dashboard standalone
- 📊 **Analytics**: Relatórios, exportação PDF
- ☸️ **DevOps**: Terraform, Helm charts
- 🧪 **Testes**: Aumentar cobertura

Veja [Issues com label "good first issue"](https://github.com/slnit/sentinel/labels/good%20first%20issue)

---

## 🚀 Processo de Review

1. **Automated Checks**: GitHub Actions valida código
2. **Code Review**: Maintainers revisam mudanças
3. **Feedback**: Sugestões e perguntas
4. **Approval**: Após aprovação, merge na main

### Expectativa de Resposta

- Bug fixes: ~24h
- Features: ~48h
- Docs: ~12h

---

## 📦 Release Process

Versioning segue [Semantic Versioning](https://semver.org/):
- `MAJOR.MINOR.PATCH` (1.2.3)
- MAJOR: Breaking changes
- MINOR: Nova funcionalidade
- PATCH: Bug fixes

---

## 💬 Comunicação

- 💻 **Issues/PRs**: Para discussões técnicas
- 📧 **Email**: support@slnit.com.br
- 💬 **Discussions**: Para ideias e debates
- 🔗 **LinkedIn**: @slnit

---

## 🙏 Agradecimentos

Muito obrigado por contribuir! Seu nome aparecerá em:
- [CONTRIBUTORS.md](CONTRIBUTORS.md)
- Release notes
- GitHub contributors

---

<div align="center">

**Juntos, construindo o futuro da detecção de anomalias**

[Guidelines](CONTRIBUTING.md) • [Code of Conduct](CODE_OF_CONDUCT.md) • [License](LICENSE)

</div>
