from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property
import logging

logger = logging.getLogger(__name__)

def get_all_properties():
    """
    Get all properties with low-level caching for 1 hour.
    """
    all_properties = cache.get('all_properties')
    
    if all_properties is not None:
        return all_properties
    
    all_properties = Property.objects.all()
    cache.set('all_properties', all_properties, 3600)
    return all_properties

def get_redis_cache_metrics():
    """
    Retrieve and analyze Redis cache hit/miss metrics.
    """
    redis_conn = get_redis_connection("default")
    info = redis_conn.info()
    
    # Get keyspace_hits and keyspace_misses
    hits = info.get('keyspace_hits', 0)
    misses = info.get('keyspace_misses', 0)
    
    # Calculate hit ratio
    total_requests = hits + misses
    if total_requests > 0:
        hit_ratio = hits / total_requests
    else:
        hit_ratio = 0
    
    metrics = {
        'keyspace_hits': hits,
        'keyspace_misses': misses,
        'hit_ratio': hit_ratio,
        'total_operations': total_requests
    }
    
    # Log metrics (using logger.info as required)
    logger.info(f"Cache Metrics - Hits: {hits}, Misses: {misses}, Hit Ratio: {hit_ratio:.4f}")
    
    return metrics
