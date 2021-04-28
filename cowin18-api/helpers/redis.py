import redis


class Redis(object):
    def __init__(self, host, port):
        self.r = redis.StrictRedis(host=host, port=port)

    def get(self, key):
        return self.r.get(key)

    def set(self, key, value, ex=None, nx=None):
        self.r.set(key, value, ex=ex, nx=nx)

    def push(self, key, value, side="tail"):
        pusher = self.r.rpush if side == "tail" else self.r.lpush
        pusher(key, value)

    def get_list(self, key, start=None, end=None):
        return self.r.lrange(key, start=start or 0, end=end or self.len_list(key))

    def len_list(self, key):
        return self.r.llen(key)

    def ttl(self, key):
        return self.r.ttl(key)

    def exists(self, key):
        return self.r.exists(key)
