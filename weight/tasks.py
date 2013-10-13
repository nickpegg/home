import celery

@celery.task
def fetch_weight():
    return None