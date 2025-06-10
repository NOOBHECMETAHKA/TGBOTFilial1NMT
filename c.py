from diskcache import Cache
import time

# Указываем, что данные старше 10 секунд будут считаться устаревшими
cache = Cache('./user_cache', ttl=10)

cache['user_123'] = {'visits': 1}
print(cache.get('user_123'))  # Выведет данные

time.sleep(20)  # Ждём дольше TTL
cache.clear()

print(cache.get('user_123'))  # Вернёт None — данные удалены