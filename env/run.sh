#!/usr/bin/env sh

if [ -d env/$PROFILES_ACTIVE -a `ls env/$PROFILES_ACTIVE | wc -c` -gt 0 ]; then
    \cp -r env/$PROFILES_ACTIVE/* app/config/
fi

/usr/local/redis/bin/redis-server /usr/local/redis/redis.conf &\
 celery -A app.celery_task  worker --loglevel=info &\
  python3 server.py
