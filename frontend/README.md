# Frontend service

Данный проект разработан под telegram mini apps, работа происходит обычно в devtools на устройстве iphone se.

---

## Архитектура

В данном проекте используется архитектура FSD: [https://feature-sliced.design/ru/docs](URL)

- `/app` : настройки, стили и провайдеры для всего приложения.
  - `/app/tg` : получение информации из Telegram mini apps API
- `/entities(сущности)` : сущности принимающие информацию практически без логики.
- `/pages(страницы)` : композиционный слой для сборки полноценных страниц из сущностей, фич и виджетов.
- `/shared` : переиспользуемый код, не имеющий отношения к специфике приложения/бизнеса.
- `/widgets (виджеты)` : композиционный слой для соединения сущностей и фич в самостоятельные блоки.

---

## Запуск npm run dev

> Во всем проекте используется переменная окружения определяемая сборщиком VITE, для понимания можете почитать: [https://vitejs.dev/guide/env-and-mode](URL)

Хоть весь проект и запускается через docker-compose, но там он не обновляется при каждом изменении в коде.

1. Чтобы запустить npm run dev нужно создать в корне frontend .env файл и прописать переменную окружения: `VITE_API_URL=https://$SERVER_NAME` ($PROTOCOL = https, $SERVER_NAME = localhost)

2. Как задать переменную окружения в windows:

Переходим в директорию frontend и прописываем: `$env:VITE_API_URL="$PROTOCOL://$SERVER_NAME"` ($PROTOCOL = https, $SERVER_NAME = localhost)

3. Как задать переменную окружения в linux:

Переходим в директорию frontend и прописываем: `VITE_API_URL=$PROTOCOL://$SERVER_NAME` ($PROTOCOL = https, $SERVER_NAME = localhost)

4. `npm run dev`
