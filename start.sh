#!/bin/bash

# Убедитесь, что все команды будут остановлены при возникновении ошибки
set -e

echo "Введите токен бота"
read TOKEN
export BOT_TOKEN=TOKEN

echo "Запуск FastAPI-приложения..."
python -u main.py &
UVICORN_PID=$!




sleep 5

# Второй шаг: Открытие Serveo туннеля
echo "Открытие Serveо туннеля..."
ssh -R 80:localhost:8000 serveo.net -T > serveo_output.txt 2>&1 &

sleep 5

# Извлечение URL с помощью sed
SERVEO_URL=$(sed -n 's/.*\(https:\/\/[a-zA-Z0-9]*\.serveo\.net\).*/\1/p' serveo_output.txt)

# Добавьте проверку, чтобы увидеть, что URL извлечен правильно
echo "Извлеченный URL: $SERVEO_URL"

# Убедитесь, что URL не пустой
if [ -z "$SERVEO_URL" ]; then
  echo "Не удалось извлечь URL от Serveo."
  exit 1
fi

# Третий шаг: Установка вебхука Telegram
echo "Установка вебхука Telegram..."

curl -X POST "https://api.telegram.org/bot$TOKEN/setWebhook" -d "url=$SERVEO_URL/webhook"

echo "Бот запущен и подключен!"


# Ожидание завершения всех процессов
wait $UVICORN_PID
