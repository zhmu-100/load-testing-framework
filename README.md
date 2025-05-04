# MAD Gateway Load Testing

 **Нагрузочное тестирование для MAD Gateway**  
Этот проект реализует сценарии нагрузочного тестирования для микросервисной архитектуры MAD (Mobile Athletic Development) через API Gateway, используя [Locust](https://locust.io/).

---

##  Стек

- **Locust** — для эмуляции пользовательской нагрузки.
- **Python 3.10+** и виртуальное окружение (`venv`)
- **Gradle** — для запуска тестов через таски
- **JWT** — авторизация через токены
- **Ktor API Gateway** — целевой сервис

##  Настройка

### 1. Установи зависимости

Создай и активируй виртуальное окружение Python:

```bash
python -m venv .venv
source .venv/bin/activate  # или .venv\Scripts\activate на Windows
pip install -r requirements.txt
pip install pyjwt

Укажи переменные окружения
Создай .env файл (или настрой ENV в системе):

env
JWT_SECRET=development_secret_key
JWT_ISSUER=com.mad.gateway
JWT_AUDIENCE=mad-mobile-app


**Запуск нагрузочного теста через Gradle
bash
./gradlew runLocustTest
По умолчанию:

Кол-во пользователей: 10000

Скорость запуска: 100 пользователей/сек

Хост: http://188.225.77.13



**Сценарии, покрытые в Locust
Locust отправляет запросы к следующим API:

/api/auth/register — регистрация пользователя

/api/auth/login — вход

/api/profiles/me — получить профиль

/api/notebook/notes — создание заметки

/api/training/workouts — список тренировок

/api/feed/posts — создание поста

/api/diet/foods — список продуктов

/api/statistics/calories — загрузка калорий

/api/db/read — произвольный SQL-запрос

**Советы
Убедись, что Auth-сервис доступен перед запуском, иначе login/register вызовут ошибки.

Используй curl или Postman для ручной отладки ошибок (например, авторизации).

Логи доступны через gateway.log, если включено логирование.