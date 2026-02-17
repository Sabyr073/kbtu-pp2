from datetime import timedelta,date

today = date.today()
result = today - timedelta(days = 5)

print(result)