import redis
from datetime import datetime

class DataBaseCashManager():
    # Подключение к Redis
    redisCacheManager= redis.Redis(host='127.0.0.1', port=6379, db=0)

    # Расписание (в формате часов и минут)
    schedule = [7, 11, 13, 15]  # 7:00, 11:00, 13:00, 15:00

    # Константы
    THRESHOLD_MINUTES = 30
    FALLBACK_TTL = 20 * 60  # 20 минут в секундах

    def setCacheValue(self, key, value):
        # Текущее время
        now = datetime.now()
        # Поиск ближайшего времени из расписания
        next_time = None
        for hour in sorted(self.schedule):
            target_time = now.replace(hour=hour, minute=0, second=0, microsecond=0)
            if target_time < now:
                target_time += datetime.timedelta(days=1)  # переносим на следующий день
            if next_time is None or target_time < next_time:
                next_time = target_time

        # Вычисляем разницу в секундах до ближайшего времени
        delta_seconds = int((next_time - now).total_seconds())

        # Устанавливаем TTL
        if delta_seconds > self.THRESHOLD_MINUTES * 60:
            ttl_seconds = self.FALLBACK_TTL
        else:
            ttl_seconds = delta_seconds

        # Сохраняем в Redis с TTL
        self.redisCacheManager.setex(key, ttl_seconds, value)