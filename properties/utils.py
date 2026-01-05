from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property
import logging

logger = logging.getLogger(__name__)

def get_all_properties():
    """
    Get all properties with low-level caching for 1 hour.
    
    Returns:
        QuerySet: All Property objects
    """
    cache_key = 'all_properties'
    
    # Try to get from cache
    cached_properties = cache.get(cache_key)
    
    if cached_properties is not None:
        logger.info(f"Cache hit for key: {cache_key}")
        return cached_properties
    
    # Cache miss - fetch from database
    logger.info(f"Cache miss for key: {cache_key}")
    properties = Property.objects.all()
    
    # Store in cache for 1 hour (3600 seconds)
    cache.set(cache_key, properties, 3600)
    
    return properties

def get_redis_cache_metrics():
    """
    Retrieve Redis cache hit/miss metrics.
    
    Returns:
        dict: Cache metrics including hits, misses, and hit ratio
    """
    try:
        redis_conn = get_redis_connection("default")
        info = redis_conn.info()
        
        # Get keyspace hits and misses from Redis INFO
        hits = info.get('keyspace_hits', 0)
        misses = info.get('keyspace_misses', 0)
        
        # Calculate hit ratio
        total = hits + misses
        if total > 0:
            hit_ratio = hits / total
        else:
            hit_ratio = 0
        
        metrics = {
            'keyspace_hits': hits,
            'keyspace_misses': misses,
            'hit_ratio': round(hit_ratio, 4),
            'total_operations': total
        }
        
        # Log metrics (using logger.info as specified, not logger.error)
        logger.info(f"Redis Cache Metrics: hits={hits}, misses={misses}, hit_ratio={hit_ratio:.4f}")
        
        return metrics
        
    except Exception as e:
        # Log any errors in retrieving metrics
        logger.info(f"Error retrieving Redis cache metrics: {str(e)}")
        return {
            'keyspace_hits': 0,
            'keyspace_misses': 0,
            'hit_ratio': 0.0,
            'total_operations': 0,
            'error': str(e)
        }