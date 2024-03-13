from datetime import datetime
from collections import defaultdict

def get_birthdays_per_week(users):
    today = datetime.today().date()
    birthdays = defaultdict(list)
    res = ""

    for user in users:
        name = users[user].name.value
        if users[user].birthday is None or users[user].birthday.birthday is None:
            continue
        birthday = (users[user].birthday.birthday).date()
    
        birthday_this_year = birthday.replace(year=today.year)

        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)

        delta_days = (birthday_this_year - today).days

        if delta_days < 7:
            day_of_week = birthday_this_year.weekday()
            if day_of_week >= 5:  # if it's weekend then move to Monday
                day_of_week = 0
            birthdays[day_of_week].append(name)
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    for i, day in enumerate(days_of_week):
        if birthdays[i]:
            res += f"{day}: {', '.join(birthdays[i])}\n"
    return res.strip()
