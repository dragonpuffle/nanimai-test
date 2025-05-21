# Async event API with FastAPI and MongoDB


Это REST API-приложение на Python, позволяющее сохранять и получать данные пользователей из MongoDB


## Описание:

*В данном проекте использовались следующие навыки:*

- API на FastAPI с валидацией Pydantic

- Асинхронное программирование

- Работа с MongoDB с использование Motor

- Контейнеризация с Docker и Docker Compose

- Организованная архитектура по модулям и возможностью расширения

- Использование DI для подключения к бд


## Возможности API:

- POST /events - создание события

- GET /events - получить все события события

- GET /events/range - получить все события события, пересекающие данные интервал

- GET /events/{event_id} - получить определенное событие

- PUT /events/{event_id} - обновление события

- DELETE /events/{event_id} - удаление события


## Запуск:

### Склонировать репозиторий:

```bash
git clone https://github.com/dragonpuffle/nanimai-test.git

cd nanimai-test
```

### 1 способ: Запустить через Docker Compose:

```bash
docker-compose up --build
```

### 2 способ: Запустить вручную (если установлен Docker):

```bash
docker run -d -p 27017:27017 --name test-mongo mongo

uvicorn app.main:app --reload
```

### Доступ к API:

Через ```http://localhost:8000/docs```
