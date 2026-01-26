from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def normalize_phone_num(self, phone_num):
        if not phone_num[:4] == "+996":
            raise ValueError("phone number incorrect (+996...)")
        return phone_num
    
    def create_user(self, username, phone_num=None , password=None, **extra_fields):
        if not username:
            raise ValueError("username is not none")
        if phone_num:
            phone_num = self.normalize_phone_num(phone_num)
        user = self.model(username=username, phone_num=phone_num, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, username, phone_num, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True")
        
        if not username:
            raise ValueError("username is not none")
        if not phone_num:
            raise ValueError("phone_num is not null for superuser")
        phone_num = self.normalize_phone_num(phone_num)
        user = self.model(username=username, phone_num=phone_num, **extra_fields)
        user.set_password(password)
        user.save()
        return self.create_user(username, phone_num, password, **extra_fields)