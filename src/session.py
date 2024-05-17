import os
from typing import Dict
from requests import Session
from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket
from pyrate_limiter import Duration, RequestRate, Limiter

from etl import get_project_root

class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
    pass

sessions: Dict[str, CachedLimiterSession] = {} 

def generate_rate_limiter(requests_a_minute:int) -> CachedLimiterSession:
    save_path = os.path.join(get_project_root(),"data/cache/alpha.cache")
    return CachedLimiterSession(
        limiter=Limiter(
            RequestRate(requests_a_minute, Duration.MINUTE)
        ),
        bucket_class=MemoryQueueBucket,
        backend=SQLiteCache(save_path),
    )
