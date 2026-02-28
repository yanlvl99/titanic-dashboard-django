## Dashboard do Dataset Titanic com Django

Se você não fez o tutorial flashcards fazer antes: https://github.com/leandrocl2005/flashcards

## Repositório do projeto

- https://github.com/leandrocl2005/titanic-dashboard-django

### Commit f638233

## Setup inicial

- Crie uma pasta chamada *titanic* (será a pasta raiz do projeto)
- Abra esta pasta com o Vs Code
- Crie um ambiente virtual: `python -m venv env`
- Ative o ambiente virtual: `. env/Scripts/activate`
- Conecte seu VS code ao seu ambiente virtual
- Adicione a raíz do projeto as configurações .vscode (ver repositório flashcards)
- Adicione a raíz do projeto o arquivo .gitignore (ver repositório flashcards)
- Instale o django: `pip install django`
- Crie o projeto Django: `django-admin startproject config .`
- Crie o app flash cards: `python manage.py startapp dashboard`
- Adicione 'dashboard' em *config/settings.py* em `INSTALLED_APPS`
- Teste se a página do Django está sendo renderizada: `python manage.py runserver`
- Crie uma pasta *templates* na raiz do projeto
- No settings troque `"DIRS": [],` por `"DIRS": [BASE_DIR / "templates"],`
- Em *config/urls* adicionar `path("", include("dashboard.urls")),`
- Criar um arquivo *dashboard/urls.py* com o código:
```python
from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="index"),
]
```
- Em *dashboard/views.py* colocar o código
```python
from django.shortcuts import render

def index(request):
    return render(request, "dashboard/index.html")
```
- Em *templates* adicionar a pasta *dashboard*
- Em *templates/dashboard* mover o arquivo *index.html* para dentro
- Teste se o index.html está sendo renderizado: `python manage.py runserver`
- Em *config/urls* adicionar `urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)`
- Em *config/settings.py* adicionar `STATICFILES_DIRS = [BASE_DIR / "static"]`
- Colocar a tag jinja `{% load static %}` no começo de *index.html*
- Alterar `href="static/css/styles.css"` para `href="{% static 'css/styles.css' %}"`
- Alterar `src="./static/js/scripts.js"` para `src="{% static 'js/scripts.js' %}"`
- Alterar `src="/static/assets/titanic.png"` para `src="{% static 'assets/titanic.png' %}"`
- Instale pandas: `pip install pandas`
- Veja a lista de bibliotecas instaladas: `pip freeze`
- Crie o arquivo *requiments.txt* com as dependências do projeto

## Commit 47ddad9

- Enviar dados do CSV para o contexto da view e, então, para o template! (ver vídeo)

## Commit 7b624fd

- Enviar dados do DB para o contexto da view e, então, para o template! (ver vídeo)

## Commit 86448e0

- Completar o código em dashboard/views.py para enviar todo o contexto com dados extraídos do bando de dados.

## Commit 585e943

- Adiciona suite completa de testes com pytest
- Configura pytest com pytest.ini para integração com Django
- Implementa testes unitários para modelos, views, URLs e dados CSV
- Adiciona testes de integração para funcionalidade completa do dashboard
- Corrige injeção de variáveis Django para JavaScript via objeto global window.djangoData
- Atualiza views.py para processamento correto de dados CSV e KPIs do banco
- Importa dados dos passageiros do CSV para o banco de dados SQLite
- Corrige renderização do template com filtros |safe adequados
- Separa arquivos JavaScript dos templates para melhor organização
- Adiciona tratamento de erro para divisão por zero no cálculo de taxas

### Como executar os testes

```bash
# Instalar dependências de teste
pip install pytest pytest-django

# Executar todos os testes
pytest

# Executar testes com detalhes
pytest -v

# Executar apenas testes do dashboard
pytest dashboard/tests.py

# Executar testes de integração
pytest test_integration.py
```

### Estrutura dos testes

- **Model Tests**: Testa criação, contagem e validação de passageiros
- **View Tests**: Testa renderização, contexto e KPIs do dashboard
- **CSV Tests**: Testa integridade e estrutura dos dados do CSV
- **URL Tests**: Testa resolução e nomes das URLs
- **Integration Tests**: Testa fluxo completo e consistência de dados

### População do banco de dados

O projeto agora importa automaticamente os dados do arquivo `titanic.csv` para o banco de dados SQLite:

```bash
# Importar dados do CSV para o banco
python manage.py shell -c "
import pandas as pd
from dashboard.models import TitanicPassenger

df = pd.read_csv('static/data/titanic.csv')
if 'SAgeex' in df.columns:
    df['Sex'] = df['SAgeex'].apply(lambda x: str(x).split()[0] if isinstance(x, str) and ' ' in str(x) else x)
    df['Age'] = df['SAgeex'].apply(lambda x: float(str(x).split()[1]) if isinstance(x, str) and ' ' in str(x) and len(str(x).split()) > 1 else None)

count = 0
for _, row in df.iterrows():
    TitanicPassenger.objects.create(
        name=row['Name'],
        sex=row['Sex'] if pd.notna(row['Sex']) else None,
        age=row['Age'] if pd.notna(row['Age']) else None,
        fare=row['Fare'] if pd.notna(row['Fare']) else None,
        survived=bool(row['Survived']),
        embarked=row['Embarked'] if pd.notna(row['Embarked']) else None,
        pclass=int(row['Pclass']) if pd.notna(row['Pclass']) else None
    )
    count += 1

print(f'Importados {count} passageiros')
"
```

### Variáveis JavaScript

As variáveis Django agora são injetadas no JavaScript através do objeto global `window.djangoData`:

```javascript
// Disponível no scripts.js
window.djangoData = {
    classes: {{classes|safe}},
    total_male: {{total_male|safe}},
    total_female: {{total_female|safe}},
    total_fare: "{{total_fare|safe}}",
    total_survived: {{total_survived|safe}},
    survived_rate: {{survived_rate|safe}},
    countByClass: {{count_by_class|safe}},
    top10: {{top_10_fares|safe}},
    survivedByClass: {{survived_by_class|safe}},
    diedByClass: {{died_by_class|safe}},
    ports: {{ports|safe}},
    embarkedData: {{embarked_by_class|safe}}
};