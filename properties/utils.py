def get_redis_cache_metrics():
    """Retrieve Redis cache hit/miss metrics."""
    redis_conn = get_redis_connection("default")
    info = redis_conn.info()
    
    hits = info.get('keyspace_hits', 0)
    misses = info.get('keyspace_misses', 0)
    
    # Calculate hit ratio
    total_requests = hits + misses
    
    # Initialize hit_ratio
    hit_ratio = 0.0
    
    # Calculate only if we have requests
    if total_requests > 0:
        hit_ratio = hits / total_requests
    
    metrics = {
        'keyspace_hits': hits,
        'keyspace_misses': misses,
        'hit_ratio': hit_ratio,
        'total_operations': total_requests
    }
    
    logger.info(f"Cache metrics: hits={hits}, misses={misses}, hit_ratio={hit_ratio}")
    
    return metrics
