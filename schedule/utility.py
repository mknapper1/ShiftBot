import re

from twilio.rest import Client

from django.conf import settings

shifts = ["1. Tuesday-11am-3pm", "2. Thursday-5pm-Close"]
manager_phone = '+12692816610'
employee_name = 'Stephen'


def clean_message(message):
    return re.sub('[!@#$)(]', '', message)


def get_weekday(day):
    if day == 0:
        return 'Sun'
    elif day == 1:
        return 'Mon'
    elif day == 2:
        return 'Tue'
    elif day == 3:
        return 'Wed'
    elif day == 4:
        return 'Thu'
    elif day == 5:
        return 'Fri'
    elif day == 6:
        return 'Sat'


def get_client():
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    return Client(account_sid, auth_token)


def send_schedule(employee, schedule):
    body = 'Schedule: \n'
    for shift in schedule:
        body += f'{get_weekday(shift.weekday)} - {shift.start_time} to {shift.end_time}\n'
    body += 'Text (y) to confirm\n' \
            'Text (n) to reject'
    client = get_client()
    client.messages.create(body=body, from_='+16162131665', to=employee.phone_number)
    employee.message_shift = 0
    employee.last_message = 1
    employee.save()
