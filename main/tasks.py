from django.core.mail import send_mail
from stackoverflowapi._celery import app


@app.task
def notify_user_task(email):
    send_mail(
        '新しいポストができた, You have created a new request...',
        'サンキュー, for using our site...',
        'test@mail.com',
        [email]
    )
    return 'Success'
