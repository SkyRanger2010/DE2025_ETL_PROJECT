FROM postgres:latest

# Устанавливаем gettext для envsubst
RUN apt-get update && apt-get install -y gettext

# Копируем шаблон init.sql.template
COPY init.sql.template /docker-entrypoint-initdb.d/init.sql.template

# Генерируем init.sql при запуске контейнера
ENTRYPOINT ["/bin/bash", "-c", "envsubst < /docker-entrypoint-initdb.d/init.sql.template > /docker-entrypoint-initdb.d/init.sql && exec docker-entrypoint.sh postgres"]
