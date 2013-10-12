import celery

@celery.task
def echo_test(thing):
	return thing