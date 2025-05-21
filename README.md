# nanimai-test

Это REST API-приложение на Python, позволяющее сохранять и получать данные пользователей из MongoDB

To run:

```bash
docker run -d -p 27017:27017 --name test-mongo mongo

uvicorn app.main:app --reload
```

Or

```bash
docker-compose up --build
```

