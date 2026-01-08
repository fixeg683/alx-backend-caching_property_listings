import logging
from celery import shared_task
from django.utils import timezone
import requests

logger = logging.getLogger(__name__)

@shared_task
def generate_crm_report():
    """
    Generate CRM report by fetching data via GraphQL query
    and log to /tmp/crm_report_log.txt
    """
    try:
        # GraphQL query to fetch CRM data
        graphql_query = """
        query {
            totalCustomers
            totalOrders
            totalRevenue
        }
        """
        
        # Make GraphQL request to your API endpoint
        # Replace with your actual GraphQL endpoint
        response = requests.post(
            'http://localhost:8000/graphql/',
            json={'query': graphql_query},
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json().get('data', {})
            
            total_customers = data.get('totalCustomers', 0)
            total_orders = data.get('totalOrders', 0)
            total_revenue = data.get('totalRevenue', 0)
            
            # Format the timestamp
            timestamp = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Create the log message
            log_message = f"{timestamp} - Report: {total_customers} customers, {total_orders} orders, {total_revenue} revenue\n"
            
            # Log to file
            log_file_path = '/tmp/crm_report_log.txt'
            with open(log_file_path, 'a') as log_file:
                log_file.write(log_message)
            
            # Also log to Django's logger
            logger.info(f"CRM report generated: {log_message.strip()}")
            
            return {
                'status': 'success',
                'total_customers': total_customers,
                'total_orders': total_orders,
                'total_revenue': total_revenue,
                'log_file': log_file_path
            }
        else:
            error_msg = f"Failed to fetch GraphQL data: {response.status_code}"
            logger.error(error_msg)
            return {'status': 'error', 'message': error_msg}
            
    except requests.exceptions.RequestException as e:
        error_msg = f"Network error: {str(e)}"
        logger.error(error_msg)
        return {'status': 'error', 'message': error_msg}
    except Exception as e:
        error_msg = f"Error generating CRM report: {str(e)}"
        logger.error(error_msg)
        return {'status': 'error', 'message': error_msg}