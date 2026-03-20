##  Описание

Проект моделирует систему логирования пользовательских действий на форуме и выполняет агрегацию данных.

Реализован полный pipeline:

* генерация пользовательских событий (логи)
* загрузка в PostgreSQL
* агрегация по дням
* экспорт результата в CSV

---

##  Стек

* Python (psycopg2 / SQLAlchemy / pandas)
* PostgreSQL
* Docker / docker-compose

---

## Рассчитываемые метрики

Для каждого дня вычисляются:

* количество новых пользователей
* общее количество сообщений
* процент анонимных сообщений
* процент изменения количества тем относительно предыдущего дня

---

##  Структура проекта

```
.
├── db_handle/
│   ├── db_gen.py        # Заполнение БД
│   ├── db_init.py       # Создание БД
│   └── core.py          # Ядро модуля
├── aggregation.py       # агрегация данных
├── main.py              # pipeline (всё вместе)
├── docker-compose.yml
├── Dockerfile
├── .env.example
└── data/
    └── result.csv       # итоговый файл
```

---

## Запуск (рекомендуемый)

```bash
cp .env.example .env
docker-compose up --build
```

После запуска результат появится в:

```
data/result.csv
```

---

## Альтернативный запуск через Docker Hub (необходимо поменять .env)

```bash
docker pull norvent/data_engineer_labuz_gordey
```

# Windows (PowerShell)
```bash
docker run --env-file .env -v ${PWD}/data:/app/data norvent/data_engineer_labuz_gordey
```

# Linux / Mac
```bash
docker run --env-file .env -v $(pwd)/data:/app/data norvent/data_engineer_labuz_gordey
```

---

## Пример результата

```
day,new_users,total_posts,anon_posts_pct,topics_growth_pct
2026-03-01,6,8,50.0,0.0
2026-03-02,7,9,66.67,-100.0
2026-03-03,9,6,50.0,0.0
```

---

## Особенности реализации

* Использованы оконные функции SQL (`LAG`, `OVER`)
* Реализована генерация данных с заданными ограничениями
* Проект полностью воспроизводим через Docker
* Разделение логики: генерация / хранение / агрегация

---

## Автор

Лабуз Гордей Максимович