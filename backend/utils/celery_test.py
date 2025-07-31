from celery_task.daily_reminder import daily_reminders
from celery_task.monthly_report import monthly_reports
from celery_task.export import export_user_csv

daily_reminders.delay()
monthly_reports.delay()
export_user_csv.delay(1) 