Запуск приложения:
```docker-compose up```
После запуска приложение доступно по адресу http://localchost:8080/

Запуск тестов:
```docker-compose run api /app/wait-for-it.sh pytest```