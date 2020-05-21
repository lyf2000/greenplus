import datetime

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.db.models import Case, When, Q, Value, IntegerField, BooleanField
from django.template.loader import render_to_string
from django.utils import timezone

from blog.models import Meet


@shared_task
def remind_meets(meet_id):
    meet = Meet.objects.get(id=meet_id)
    mail_subject = 'MEETIIIING AAAAA.'
    for user in meet.participants.all():
        print(user)
        context = {
            'username': user.username,
            'meet_date': meet.meet_date.strftime('%d/%m/%Y %H:%M'),
            'title': meet.title
        }
        send_message.delay('blog/meeting_remind.html', context, mail_subject, user.email)


@shared_task
def send_message(template_name, message_context, mail_subject, to_email):
    message = render_to_string(template_name, message_context)
    msg = EmailMultiAlternatives(mail_subject, '', '', [to_email])
    msg.attach_alternative(message, "text/html")
    msg.send()
    print('remind_meets send_message to', to_email)


@shared_task
def check_to_remind_meets():
    meets_to_be_reminded = Meet.objects.annotate(in_hour=Case(
    When(Q(meet_date__gte=timezone.now() - datetime.timedelta(hours=3))
         & Q(meet_date__lte=timezone.now() - datetime.timedelta(hours=1)),
         then=Value(True)),
    default=Value(False),
    output_field=BooleanField())).filter(in_hour=True)



