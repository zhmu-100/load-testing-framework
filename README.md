# load-testing-framework
 репозиторий на GitHub для нагрузочного тестирования на 10k пользователей


Как установить зависимости: pip install -r requirements.txt.

Как запустить тест: locust -f tests/basic_load_test.py.


## Масштабирование для 10 000 пользователей

1. Запустите мастер-ноду:
   ```bash
   locust -f tests/basic_load_test.py --master --expect-workers 5

2. Запустите воркеров (на каждой машине):
    locust -f tests/basic_load_test.py --worker --master-host=<MASTER_IP>

3. Откройте веб-интерфейс Locust по адресу http://<MASTER_IP>:8089 и запустите тест.
    