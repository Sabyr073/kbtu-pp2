from datetime import timedelta,date

today = date.today()
yesterday = today - timedelta(days = 1)
tomorrow  = today + timedelta(days = 1)

print(yesterday.strftime("%d"), today.strftime("%d"), tomorrow.strftime("%d"))