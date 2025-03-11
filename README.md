# Учебный ETL Проект с Apache Airflow, PostgreSQL и MongoDB

## Описание проекта

Этот проект представляет собой учебный ETL-процесс для репликации данных из MongoDB в PostgreSQL с использованием Apache Airflow. 

Проект включает в себя несколько ключевых сервисов:

### Стек технологий
- **Apache Airflow** – отвечает за управление и автоматизацию выполнения ETL-пайплайнов. Каждый DAG в Airflow реализует процесс извлечения, трансформации и загрузки данных.
- **MongoDB** – источник данных, в котором хранятся сырые данные о пользовательских сессиях, поисковых запросах, истории цен товаров, обращениях в поддержку и других сущностях.
- **PostgreSQL** – хранилище обработанных данных. В него загружаются очищенные, нормализованные и подготовленные для аналитики данные.
- **Генератор данных** – отдельный сервис, который заполняет MongoDB случайными данными, имитируя реальные сущности.
- **Docker** – для контейнеризации всех сервисов и удобного развертывания проекта.
- **Python** – язык программирования для написания ETL-скриптов, а также генерации данных.

Основная цель проекта – научиться настраивать и автоматизировать процессы обработки данных, подготовки их для последующего анализа, а также реализация витрин данных, которые можно использовать для бизнес-аналитики.


## Структура проекта
Проект организован следующим образом:
```plaintext
DE2025_ETL_PROJECT/
├── .env                        # Переменные окружения для настройки всех сервисов
├── docker-compose.yml          # Конфигурация Docker Compose
├── README.md                   # Документация проекта
├── PROJECT_TASK.md             # Задание на учебный проект
├── airflow/                    # Сервис Airflow
│   ├── Dockerfile              # Докерфайл Airflow
│   ├── requirements.txt        # Зависимости Airflow
│   ├── config/
│   │   └── airflow.cfg         # Конфигурация Airflow
│   ├── dags/                   # DAG-файлы для Airflow
│   │   │
│   │   ├── user_sessions_etl.py            # DAG для репликации user_sessions
│   │   ├── event_logs_etl.py               # DAG для репликации event_logs
│   │   ├── search_queries_etl.py           # DAG для репликации search_queries
│   │   ├── user_recommendations_etl.py     # DAG для репликации user_recommendations
│   │   ├── moderation_queue_etl.py         # DAG для репликации moderation_queue
│   │   ├── support_tickets_etl.py          # DAG для репликации support_tickets
│   │   └── product_price_history_etl.py    # DAG для репликации product_price_history
│   │
│   ├── logs/                   # Логи Airflow
│   └── plugins/                # Плагины Airflow  
│
├── data_generator/             # Сервис генератора данных для MongoDB
│   ├── Dockerfile                      # Докерфайл генератора данных
│   ├── generate_data.py                # Python-скрипт генерирующий данные
│   └── requirements.txt                # Зависимости сервиса генератора данных
│
└── db/                         # Сервисы баз данных проекта
    ├── mongo/                          # Сервис MongoDB
    └── postgres/                       # Сервис PostgeSQL
```  

## Развертывание проекта
1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/SkyRanger2010/DE2025_ETL_PROJECT.git
   cd DE2025_ETL_PROJECT
   ```
2. **Запустите Docker-контейнеры:**
   ```bash
   docker-compose up -d
   ```
3. **Откройте Airflow в браузере:**
   ```
   http://localhost:8080
   ```
4. **Запустите DAG'и в Airflow:**
   - Перейдите в интерфейс Apache Airflow.
   - Запустите выполнение необходимых DAG'ов вручную.

## Генератор данных

Генератор данных предназначен для создания тестовых данных в MongoDB. Он используется для наполнения базы случайными значениями, имитируя реальный поток данных.

### Данные, генерируемые скриптом

1. **user_sessions** – информация о сессиях пользователей.
   - `session_id` – уникальный идентификатор сессии.
   - `user_id` – идентификатор пользователя.
   - `start_time` – время начала сессии.
   - `end_time` – время завершения сессии.
   - `pages_visited` – список посещенных страниц.
   - `device` – информация об устройстве пользователя.
   - `actions` – список действий пользователя.

2. **product_price_history** – история изменения цен на товары.
   - `product_id` – идентификатор товара.
   - `price_changes` – список изменений цен (дата и цена).
   - `current_price` – текущая цена товара.
   - `currency` – валюта цены.

3. **event_logs** – логи событий пользователей.
   - `event_id` – уникальный идентификатор события.
   - `timestamp` – временная метка события.
   - `event_type` – тип события (например, вход, выход, ошибка, клик).
   - `details` – дополнительная информация о событии.

4. **support_tickets** – обращения пользователей в поддержку.
   - `ticket_id` – уникальный идентификатор тикета.
   - `user_id` – идентификатор пользователя.
   - `status` – статус тикета (открыт, закрыт, в ожидании).
   - `issue_type` – тип проблемы (ошибка, запрос на новую функцию и т. д.).
   - `messages` – список сообщений в тикете.
   - `created_at` – дата создания тикета.
   - `updated_at` – дата последнего обновления тикета.

5. **user_recommendations** – рекомендации товаров пользователям.
   - `user_id` – идентификатор пользователя.
   - `recommended_products` – список рекомендованных товаров.
   - `last_updated` – время последнего обновления рекомендаций.

6. **moderation_queue** – очередь на модерацию отзывов.
   - `review_id` – идентификатор отзыва.
   - `user_id` – идентификатор пользователя.
   - `product_id` – идентификатор товара.
   - `review_text` – текст отзыва.
   - `rating` – оценка товара.
   - `moderation_status` – статус модерации (на проверке, одобрен, отклонен).
   - `flags` – список флагов (например, жалобы на отзыв).
   - `submitted_at` – дата отправки отзыва.

7. **search_queries** – поисковые запросы пользователей.
   - `query_id` – уникальный идентификатор запроса.
   - `user_id` – идентификатор пользователя.
   - `query_text` – текст запроса.
   - `timestamp` – время выполнения запроса.
   - `filters` – список примененных фильтров.
   - `results_count` – количество результатов запроса.

### Запуск генератора данных
Генератор данных автоматически разворачивается после сервиса MongoDB и заполняет MongoDB тестовыми записями. 
По умолчанию, генератор использует параметры из `.env`-файла для определения количества генерируемых записей в каждой коллекции.

## Описание пайплайнов

### Общие сведения

В проекте используются следующие инструменты и подходы для реализации ETL-пайплайнов:
- **Извлечение данных (`extract`)**: Данные извлекаются из MongoDB с использованием библиотеки `pymongo`, обеспечивающей подключение к базе и выполнение запросов.
- **Трансформация данных (`transform`)**: Для обработки данных используются библиотеки `pandas` (для манипуляций с DataFrame, для нормализации данных, удаления дубликатов и преобразования форматов).
- **Загрузка данных (`load`)**: Данные записываются в PostgreSQL с помощью `sqlalchemy` и `pandas.to_sql()`, что позволяет автоматизировать создание таблиц и загрузку данных.
- **Автоматизация процессов**: Управление пайплайнами осуществляется с помощью **Apache Airflow**, где DAG'и выполняют поэтапное выполнение задач в зависимости от установленного расписания.


### 1. Репликация данных user_sessions
- **Извлечение (`extract`)**: данные загружаются из MongoDB (коллекция `user_sessions`).
- **Трансформация (`transform`)**: преобразование массивов, нормализация данных, удаление дубликатов.
- **Загрузка (`load`)**: создание индексов, переупорядочивание колонок, запись данных в PostgreSQL (`source.user_sessions`).

### 2. Репликация данных event_logs
- **Извлечение (`extract`)**: данные загружаются из MongoDB (коллекция `event_logs`).
- **Трансформация (`transform`)**: удаление дубликатов, заполнение пропущенных значений, нормализация данных.
- **Загрузка (`load`)**: создание индексов, переупорядочивание колонок, запись данных в PostgreSQL (`source.event_logs`).

### 3. Репликация данных search_queries
- **Извлечение (`extract`)**: данные загружаются из MongoDB (коллекция `search_queries`).
- **Трансформация (`transform`)**: преобразование массива `filters` в строку, удаление дубликатов, нормализация данных.
- **Загрузка (`load`)**: создание индексов, переупорядочивание колонок, запись данных в PostgreSQL (`source.search_queries`).

### 4. Репликация данных user_recommendations
- **Извлечение (`extract`)**: данные загружаются из MongoDB (коллекция `user_recommendations`).
- **Трансформация (`transform`)**: разворачивание массива `recommended_products` в строки, нормализация данных.
- **Загрузка (`load`)**: создание индексов, переупорядочивание колонок, запись данных в PostgreSQL (`source.user_recommendations`).

### 5. Репликация данных moderation_queue
- **Извлечение (`extract`)**: данные загружаются из MongoDB (коллекция `moderation_queue`).
- **Трансформация (`transform`)**: преобразование массива `flags`, удаление дубликатов, нормализация данных.
- **Загрузка (`load`)**: создание индексов, переупорядочивание колонок, запись данных в PostgreSQL (`source.moderation_queue`).

### 6. Репликация данных support_tickets
- **Извлечение (`extract`)**: данные загружаются из MongoDB (коллекция `support_tickets`).
- **Трансформация (`transform`)**: удаление дубликатов, заполнение пропущенных значений, нормализация данных.
- **Загрузка (`load`)**: создание индексов, переупорядочивание колонок, запись данных в PostgreSQL (`source.support_tickets`).

### 7. Репликация данных product_price_history
- **Извлечение (`extract`)**: данные загружаются из MongoDB (коллекция `product_price_history`).
- **Трансформация (`transform`)**: разворачивание истории цен, нормализация данных.
- **Загрузка (`load`)**: создание индексов, переупорядочивание колонок, запись данных в PostgreSQL (`source.product_price_history`).

## Контакты
Автор: *Василий Сатанцев*  
Email: *vasily.satantsev@gmail.com*  
GitHub: [DE2025_ETL_PROJECT](https://github.com/SkyRanger2010/DE2025_ETL_PROJECT)
