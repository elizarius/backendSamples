broker_url: str = "redis://127.0.0.1:6379/0"
result_backend: str = "redis://127.0.0.1:6379/0"
task_default_queue: str = "Project-Celery-App"
imports: tuple = (
    "celery_app.tasks",
)
accept_content=['json', 'pickle']