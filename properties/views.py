from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .models import Property
from .utils import get_all_properties, get_redis_cache_metrics

# Task 1: Cache Property List View for 15 minutes
@cache_page(60 * 15)  # Cache for 15 minutes
def property_list(request):
    """Return all properties (cached at view level)"""
    properties = Property.objects.all()
    data = [
        {
            'id': prop.id,
            'title': prop.title,
            'description': prop.description,
            'price': str(prop.price),
            'location': prop.location,
            'created_at': prop.created_at.isoformat()
        }
        for prop in properties
    ]
    return JsonResponse({'properties': data})

# Task 2: Updated view using low-level caching
def property_list_low_level(request):
    """Return all properties using low-level caching"""
    properties = get_all_properties()
    data = [
        {
            'id': prop.id,
            'title': prop.title,
            'description': prop.description,
            'price': str(prop.price),
            'location': prop.location,
            'created_at': prop.created_at.isoformat()
        }
        for prop in properties
    ]
    return JsonResponse({'properties': data})

def cache_metrics(request):
    """Return Redis cache metrics"""
    metrics = get_redis_cache_metrics()
    return JsonResponse(metrics)