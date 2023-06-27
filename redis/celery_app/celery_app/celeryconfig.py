broker_url: str = "redis://100.76.169.30:6379/0"
result_backend: str = "redis://100.76.169.30:6379/0"
task_default_queue: str = "Project-Celery-App"
imports: tuple = (
    "celery_app.tasks",
)
accept_content=['json', 'pickle']