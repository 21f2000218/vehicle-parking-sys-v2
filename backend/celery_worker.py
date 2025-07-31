from app import celery
from app.factory import create_app
from app.celery_utils import init_celery
from utils.celery_task.daily_reminder import daily_reminders
from utils.celery_task.monthly_report import monthly_reports


app = create_app()
init_celery(celery, app)

