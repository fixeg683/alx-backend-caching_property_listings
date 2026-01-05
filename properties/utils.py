from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property
import logging

logger = logging.getLogger(__name__)

def get_all_properties():
    """Get all properties with low-level caching for 1 hour."""
    cached = cache.get('all_properties')
    if cached:
        return cached
    
    properties = Property.objects.all()
    cache.set('all_properties', properties, 3600)
    return properties

def get_redis_cache_metrics():
    """Retrieve Redis cache hit/miss metrics."""
    redis_conn = get_redis_connection("default")
    info = redis_conn.info()
    
    hits = info.get('keyspace_hits', 0)
    misses = info.get('keyspace_misses', 0)
    
    # Calculate hit ratio without ternary expression
    total = hits + misses
    hit_ratio = 0.0  # Default value
    
    if total > 0:
        hit_ratio = hits / total
    
    metrics = {
        'keyspace_hits': hits,
        'keyspace_misses': misses,
        'hit_ratio': round(hit_ratio, 4),
        'total_operations': total
    }
    
    logger.info(f"Cache metrics: {metrics}")
    
    return metrics
