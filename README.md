#  MedControl — Controlador de Medicamentos para Idosos

![CI Status](https://github.com/SEU_USUARIO/medcontrol/actions/workflows/ci.yml/badge.svg)
![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.9%2B-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## Problema Real

Idosos e pessoas com doenças crônicas frequentemente precisam tomar múltiplos medicamentos em horários diferentes ao longo do dia. Esquecer uma dose ou confundir remédios pode causar sérios riscos à saúde. Cuidadores e familiares também enfrentam dificuldade em organizar e lembrar esses horários.

## Proposta da Solução

O **MedControl** é uma aplicação CLI (linha de comando) simples e acessível que permite cadastrar medicamentos com seus respectivos horários e dosagens, consultar a lista a qualquer momento e verificar quais remédios devem ser tomados agora.

## Público-Alvo

- Idosos com autonomia para usar o computador
- Cuidadores e familiares de pacientes com doenças crônicas
- Qualquer pessoa que precise controlar múltiplos medicamentos

## ✅ Funcionalidades

- Cadastrar medicamento (nome, dose, horários)
- Listar todos os medicamentos cadastrados
- Remover medicamento por ID
- Buscar medicamento por nome (parcial, sem diferença de maiúsculas/minúsculas)
- Ver alertas: quais medicamentos devem ser tomados no horário atual
- Persistência em arquivo JSON (os dados ficam salvos entre sessões)

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Finalidade |
|---|---|
| Python 3.9+ | Linguagem principal |
| json (stdlib) | Persistência de dados |
| pytest | Testes automatizados |
| ruff | Linting e análise estática |
| GitHub Actions | Integração Contínua (CI) |

## 📁 Estrutura do Projeto

```
medcontrol/
├── src/
│   ├── __init__.py
│   └── medicamentos.py      # Lógica da aplicação + CLI
├── tests/
│   ├── __init__.py
│   └── test_medicamentos.py # Testes automatizados
├── .github/
│   └── workflows/
│       └── ci.yml           # Pipeline CI
├── .gitignore
├── CHANGELOG.md
├── LICENSE
├── pyproject.toml           # Configuração do projeto e versão
├── requirements.txt         # Dependências
└── README.md
```

## ⚙️ Instalação

**Pré-requisitos:** Python 3.9 ou superior instalado.

```bash
# 1. Clone o repositório
git clone https://github.com/giovannahamu/medcontrol.git
cd medcontrol

# 2. (Opcional, mas recomendado) Crie um ambiente virtual
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 3. Instale as dependências de desenvolvimento
pip install -r requirements.txt
```

## ▶️ Como Executar

```bash
python src/medicamentos.py
```

Você verá o menu interativo:

```
==========================================
   💊 MedControl - Controle de Medicamentos
==========================================
  1. Cadastrar medicamento
  2. Listar medicamentos
  3. Remover medicamento
  4. Buscar medicamento
  5. Ver alertas do momento
  0. Sair
==========================================
```

**Exemplo de uso:**
1. Escolha `1` para cadastrar
2. Digite o nome: `Losartana`
3. Digite a dose: `1 comprimido`
4. Digite os horários: `08:00,20:00`
5. Escolha `5` para ver se há algum remédio para tomar agora

## 🧪 Como Rodar os Testes

```bash
pytest tests/ -v
```

Saída esperada: todos os testes passando ✅

## 🔍 Como Rodar o Lint

```bash
ruff check src/ tests/
```

Saída esperada: nenhum erro de estilo ou qualidade.

## 📦 Versão

**1.0.0** — Versão inicial com funcionalidades principais.

Veja o histórico completo em [CHANGELOG.md](CHANGELOG.md).

## 👤 Autora

**Giovanna Hamú Borba de Carvalho**  
Repositório: [https://github.com/giovannahamu/medcontrol](https://github.com/giovannahamu/medcontrol)
