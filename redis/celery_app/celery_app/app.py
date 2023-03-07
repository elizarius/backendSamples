from celery import Celery

celery_app: Celery = Celery("worker")
celery_app.config_from_object("celery_app.celeryconfig")


@celery_app.task
def hello(name: str) -> str:
    return f"Hello AELZ"
