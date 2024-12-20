# Cервис для взаимодействия пользователя с сущностью тарифа

Этот проект реализует сервис на REST API для расчёта стоимости страхования в зависимости от типа груза и объявленной стоимости, а также поддерживает авторизацию пользователей для логирования их действий. Тарифы для расчёта загружаются из файла JSON или могут быть переданы в JSON-формате через API. В ответ сервис возвращает стоимость страховки, которая рассчитывается как произведение объявленной стоимости на ставку тарифа.

## Описание функционала

1. **Загрузка тарифов** — тарифы для различных типов грузов и дат загружаются через API, либо могут быть переданы в виде файла JSON. Каждый тариф содержит дату, тип груза и ставку (rate).
2. **Расчёт стоимости страховки** — сервис принимает запрос с типом груза, датой и объявленной стоимостью, затем использует актуальный тариф для расчёта (объявленная стоимость умножается на ставку тарифа).
3. **Управление тарифами** — сервис поддерживает функции создания, редактирования и удаления тарифов.
4. **Логирование** — все изменения тарифов, а также запросы на расчёт стоимости, логируются с использованием Kafka. Логи содержат информацию о действии, ID пользователя, типе груза и времени события.
5. **Хранение данных** — тарифы и данные о пользователях хранятся в базе данных PostgreSQL.


## Развёртывание в Docker
Создать файл `.env`:
```commandline
touch .env
```
Пропишите команду:
```commandline
docker compose up --build
```
_Для простоты развораичвания сервиса переменная `JWT_SECRET` также была проинициализирована в `config.py`. При разворачивании в проде обязательно нужно её заменить._


