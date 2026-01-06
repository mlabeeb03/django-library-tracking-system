from celery import shared_task
from .models import Loan
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

import logging
logger = logging.Logger(__name__)

@shared_task
def send_loan_notification(loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        member_email = loan.member.user.email
        book_title = loan.book.title
        send_mail(
            subject='Book Loaned Successfully',
            message=f'Hello {loan.member.user.username},\n\nYou have successfully loaned "{book_title}".\nPlease return it by the due date.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
    except Loan.DoesNotExist:
        pass

@shared_task
def check_overdue_loans():
    overdue_loans = Loan.objects.filter(is_returned=False, due_date__lt=timezone.now().date()).select_related("member__user", "book")
    for loan in overdue_loans:
        try:
            logger.info(f"Email sending to {loan.member.user.email}.")
            send_mail(
                subject='Book Loaned Successfully',
                message=f'Hello {loan.member.user.username},\n\nThis is a reminder to return book "{loan.book.title}".\n',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[loan.member.user.email],
                fail_silently=False,
            )
        except Exception as e:
            logger.error(f"Error while sending email: {e}")
