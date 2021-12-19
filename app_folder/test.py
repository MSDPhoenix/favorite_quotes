from datetime import time, datetime, timedelta

now = datetime.now()
print('now',now)
minimum_age = timedelta(days=4848)
birthday = now - minimum_age
print('birthday',birthday)



# birthday = postData['birthday']
