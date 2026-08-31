# AI Assistant Platform

Модульная backend-платформа для создания персонального AI-ассистента с поддержкой текстового общения, долговременной памяти и поиска актуальной информации в интернете.

## Возможности

* регистрация и авторизация пользователей;
* JWT-аутентификация;
* управление чатами;
* история сообщений;
* генерация ответов через локальную LLM;
* автоматическая генерация названий чатов;
* краткосрочная память в виде истории диалога;
* долговременная память пользователя;
* поиск актуальной информации в интернете;
* автоматическое определение необходимости интернет-поиска;
* голосовой ввод и распознавание речи.

---

# Технологический стек

## Backend

* Python 3.12+
* FastAPI
* Uvicorn
* Pydantic

## Database

* SQLite
* SQLAlchemy
* Alembic

## Authentication

* JWT
* python-jose

## AI

### AI Runtime

* Ollama

### LLM

* Llama 3.1 8B

## Web Search

* Tavily API

## Speech-to-Text

* faster-whisper
* Systran/faster-whisper-large-v3

## HTTP

* httpx

---

# Архитектура

Проект использует многослойную архитектуру:

```text
Client
  │
  ▼
API
  │
  ▼
Services
  │
  ├── Repositories ──► Database
  │
  ├── AI Manager ────► AI Providers ──► Ollama
  │
  └── Speech Manager ► Speech Providers ► Whisper
```

# Основные сервисы

## MessageService

Основной сервис обработки сообщений.

Отвечает за:

* получение и сохранение сообщений;
* получение истории чата;
* передачу сообщений в `AIService`;
* сохранение информации в долгосрочную память;
* генерацию названия нового чата.

---

## AIService

Собирает контекст и передает запрос AI-модели.

Использует:

* `MemoryService`;
* `DecisionService`;
* `WebSearchService`;
* `AIManager`.

Порядок работы:

```text
История сообщений
        │
        ├──► Долговременная память
        │
        └──► DecisionService
                    │
                    ├── Нет поиска
                    │
                    └── Да ──► Tavily
                                   │
                                   ▼
                            Результаты поиска
                                   │
                                   ▼
                                 Ollama
```

---

## MemoryService

Отвечает за работу с долговременной памятью пользователя:

* сохранение фактов;
* получение памяти;
* формирование контекста для AI.

---

## DecisionService

Определяет, требуется ли для последнего сообщения пользователя поиск актуальной информации в интернете.

---

## WebSearchService

Выполняет поиск через Tavily API и подготавливает результаты для передачи AI-модели.


---

# Структура проекта

```text
app/
│
├── ai/
│   ├── base.py
│   ├── manager.py
│   └── prompts/
│
├── api/
│
├── core/
│
├── models/
│
├── repositories/
│
├── schemas/
│
├── services/
│   ├── ai_service.py
│   ├── decision_service.py
│   ├── memory_service.py
│   ├── message_service.py
│   ├── speech_service.py
│   └── web_search_service.py
│
├── speech/
│   ├── manager.py
│   └── providers/
│
├── web/
│   ├── manager.py
│   └── providers/
│
└── utils/
```

---

# Быстрый запуск

## 1. Клонирование репозитория

```bash
git clone <repository-url>
cd backend
```

## 2. Создание виртуального окружения

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

## 4. Настройка переменных окружения

Создать `.env` на основе `.env.example`.

### Windows

```bash
copy .env.example .env
```

### Linux

```bash
cp .env.example .env
```

После этого необходимо указать реальные значения:

* `SECRET_KEY`;
* `TAVILY_API_KEY`.

## 5. Установка Ollama

Установить Ollama и скачать используемую модель:

```bash
ollama pull llama3.1:8b
```

После запуска Ollama должен быть доступен по адресу:

```text
http://localhost:11434
```

## 6. Миграции базы данных

```bash
alembic upgrade head
```

## 7. Запуск приложения

```bash
uvicorn app.main:app --reload
```

После запуска API будет доступно по адресу:

```text
http://127.0.0.1:8000
```

Swagger-документация:

```text
http://127.0.0.1:8000/docs
```

---

# Безопасность

В репозиторий запрещено добавлять:

* `.env`;
* API-ключи;
* JWT-секреты;
* пароли;
* production-базы данных;
* пользовательские данные;
* скачанные AI-модели.

Для передачи настроек используется файл `.env.example`.

---
