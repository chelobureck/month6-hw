from datetime import date


def validated_birthday(birthday):
    today = date.today()
    age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
    
    if age < 18:
        raise ValueError("Возраст должен быть 18 лет или старше.")
    
    return birthday