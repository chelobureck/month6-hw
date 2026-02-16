from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from decouple import config

from users.models import CustomUserModel as CustomUser


@shared_task
def delete_temp_files(user_id):
	try:
		user = CustomUser.objects.get(id=user_id)
		print(f"Delete temp files for user {user.id}")
		return 'done'
	except CustomUser.DoesNotExist:
		return 'error'


@shared_task
def cleanup_unconfirmed_users():
	three_days_ago = timezone.now() - timedelta(days=3)
	unconfirmed_users = CustomUser.objects.filter(date_joined__lt=three_days_ago)
	
	count = unconfirmed_users.count()
	unconfirmed_users.delete()
	
	print(f"Deleted {count} unconfirmed users")
	return f"deleted {count}"


@shared_task
def send_welcome_email(user_id):
	try:
		user = CustomUser.objects.get(id=user_id)
		
		send_mail(
			subject='Добро пожаловать!',
			message=f'Привет {user.email}, добро пожаловать в Cinema!',
			from_email=config('EMAIL_HOST_USER'),
			recipient_list=[user.email],
			fail_silently=False,
		)
		
		print(f"Welcome email sent to {user.email}")
		return 'done'
		
	except CustomUser.DoesNotExist:
		return 'error'
	except Exception as e:
		print(f"Error: {str(e)}")
		return 'error'


@shared_task
def send_otp(email, code):
	send_mail(
		subject='OTP для регистрации',
		message=f'Ваш код подтверждения: {code}',
		from_email=config('EMAIL_HOST_USER'),
		recipient_list=[email],
		fail_silently=False,
	)
	print(f"OTP sent to {email}")
