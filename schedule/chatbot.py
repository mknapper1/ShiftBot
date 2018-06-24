import re

from twilio.rest import Client

from django.conf import settings
from .models import Employee, WorkWeek, Shift

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


def go_chatbot(message, phone_number):
    message = clean_message(message.lower())
    print(message)
    phone_number = re.sub('[^0-9]', '', phone_number)
    print(phone_number)
    employee = Employee.objects.get(phone_number=phone_number)
    print(employee)
    print(employee.last_message)
    if employee.last_message == Employee.SENT_SCHEDULE:
        print("EMPLOYEE SENT SCHEDULE")
        if message.startswith('y'):
            employee.last_message = Employee.CONFIRMED_SCHEDULE
            employee.save()
        elif message.startswith('n'):
            send_reject_schedule(employee)
    elif employee.last_message == Employee.REJECTED_SCHEDULE:
        id = re.sub('[^0-9]', '', message)
        if id:
            try:
                shift = Shift.objects.get(pk=id)
            except Shift.DoesNotExist:
                shift = None
            if shift:
                send_confirm_reject_shift(employee, shift)
            else:
                send_reject_schedule(employee)
    elif employee.last_message == Employee.REJECTED_SHIFT or employee.last_message == 4:
        print('here at rejected shift' + message)
        if message.startswith('y'):
            send_emp_change_request(employee, employee.message_shift)
        elif message.startswith('n'):
            send_reject_schedule(employee)
    elif employee.last_message == Employee.PICKUP_REQUEST:
        if message.startswith('y'):
            send_finalize_swap(employee)
        elif message.startswith('n'):
            send_reject_pickup(employee)
    else:
        send_nice(employee.phone_number)


def send_nice(phone_number):
    body = 'Let me know if there is anything you need!'
    client = get_client()
    client.messages.create(body=body, from_='+16162131665', to=phone_number)


def send_help_message(phone_number):
    body = 'Text (s) for Schedule \n' \
           'Text (r) to Request Off'
    client = get_client()
    client.messages.create(body=body, from_='+16162131665', to=phone_number)


def send_schedule(employee_id, workweek_id):
    employee = Employee.objects.get(pk=employee_id)
    schedule = Shift.objects.get(work_week_id=workweek_id, employee=employee)
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


def send_reject_schedule(employee):
    schedule = Shift.objects.filter(employee=employee)
    body = 'Which Shift Do You Reject: \n'
    for shift in schedule:
        body += f'text ({shift.id}) {get_weekday(shift.weekday)} - {shift.start_time} to {shift.end_time}\n'
    client = get_client()
    client.messages.create(body=body, from_='+16162131665', to=employee.phone_number)
    employee.message_shift = 0
    employee.last_message = Employee.REJECTED_SCHEDULE
    employee.save()


def send_confirm_reject_shift(employee, shift):
    body = f'To Confirm: \n' \
           'You would like some to work for you\n'
    body += f'{get_weekday(shift.weekday)} - {shift.start_time} to {shift.end_time}\n text (y) to confirm'
    client = get_client()
    client.messages.create(body=body, from_='+16162131665', to=employee.phone_number)
    employee.message_shift = shift.id
    employee.last_message = Employee.REJECTED_SHIFT
    employee.save()


def send_emp_change_request(employee, shift_id):
    print('sending change request for ' + employee.name)
    shift = Shift.objects.get(pk=shift_id)
    employees = shift.job.employee_set.all()
    for emp in employees:
        print(emp)
        if emp.id != employee.id:
            send_pickup_shift_request(employee, emp, shift)


def send_pickup_shift_request(slacker, employee, shift):
    body = f'{slacker} is looking for someone to work: \n' \
           f'{get_weekday(shift.weekday)} - {shift.start_time} to {shift.end_time}\n' \
           'text (y) to accept\n' \
           'text (n) to decline'
    client = get_client()
    client.messages.create(body=body, from_='+16162131665', to=employee.phone_number)
    employee.message_shift = shift.id
    employee.last_message = Employee.PICKUP_REQUEST
    employee.save()


def send_finalize_swap(employee):
    shift = Shift.objects.get(id=employee.message_shift)
    slacker = shift.employee
    shift.employee = employee
    shift.save()
    body = f'Thanks you now work \n' \
           f'{get_weekday(shift.weekday)} - {shift.start_time} to {shift.end_time}'
    client = get_client()
    client.messages.create(body=body, from_='+16162131665', to=employee.phone_number)
    employee.message_shift = 0
    employee.last_message = Employee.CONFIRMED_SCHEDULE
    employee.save()
    body = f'{employee} picked up your shift!'
    client = get_client()
    client.messages.create(body=body, from_='+16162131665', to=slacker.phone_number)
    slacker.message_shift = 0
    slacker.last_message = Employee.CONFIRMED_SCHEDULE
    slacker.save()


def send_reject_pickup(employee):
    shift = Shift.objects.get(id=employee.message_shift)
    slacker = shift.employee

#
# def sms_response(user_response):
#     # Get the users response and phone number
#     params = user_response.POST
#
#     user_txt = params['Body']
#     user_phone = params['From']
#
#     # Start our TwiML response
#     # end_response = MessagingResponse()
#
#     # choose path based on last responses
#     confirm_schedule(params)
#
#     change_shift_request(params)
#
#     # return HttpResponse(str(end_response))
#
#
# def confirm_schedule(params):
#     user_txt = params['Body']
#     user_phone = params['From']
#
#     # response for confirming employee schedule
#     if user_txt.lower() == 'yes':  # if the employee confirms schedule, no more work is needed
#         response = "Awesome!"
#         send_response(user_phone, response)
#     elif user_txt.lower() == 'no':
#         response = ("What day would you like to request off? \n"
#                     + "1. Tuesday 11am-3pm\n"
#                     + "2. Thursday 5pm-Close")
#         send_response(user_phone, response)
#     else:
#         send_schedule(user_phone)
#
#
# def change_shift_request(params):
#     user_txt = params['Body']
#     user_phone = params['From']
#     send_schedule(user_phone)
#
#     # response for asking a shift off
#     if user_txt.lower() == str(shifts[0]).split('.')[0] or user_txt.lower() == str(shifts[0]).split('.')[1]:
#         response = "You're requesting " + shifts[0] + " off? \n[yes/no]"
#         shift_requested_off = shifts[0].split(' ')[1]
#         send_response(user_phone, response)
#         if user_txt.lower() == 'yes':
#             response = "Okay"
#             send_response(user_phone, response)  # bot will then text manager asking for approval
#             # find available employees
#             available_employees = "Sam and Keith"
#             shift_requested_off = shifts[1].split(' ')[1]
#             ask_manager_approval(employee_name, shift_requested_off, available_employees)
#         elif user_txt.lower() == 'no':
#             send_schedule(user_phone)
#         else:
#             print("I'm repeating my last question")
#
#     elif user_txt.lower() == str(shifts[1]).split('.')[0] or user_txt.lower() == str(shifts[1]).split('.')[1]:
#         response = "You're requesting " + shifts[1] + " off? \n[yes/no]"
#         shift_requested_off = shifts[1].split(' ')[1]
#         send_response(user_phone, response)
#         if user_txt.lower() == 'yes':
#             response = "Okay"
#             send_response(user_phone, response)  # bot will then text manager asking for approval
#             # find available employees
#             available_employees = "Sam and Keith"
#             shift_requested_off = shifts[1].split(' ')[1]
#             ask_manager_approval(employee_name, shift_requested_off, available_employees)
#         elif user_txt.lower() == 'no':
#             send_schedule(user_phone)
#         else:
#             print("I'm repeating my last question")
#     else:
#         response = "I'm repeating my last question."
#         send_response(user_phone, response)  # will send last question asked
#
#
# def send_response(phone_number, response_text):
#     client = get_client()
#     client.messages \
#         .create(
#         body=response_text,
#         from_='+16162131665',
#         to=phone_number
#     )
#
#
# def ask_manager_approval(employee_name, shift_requested_off, available_employees):
#     client = get_client()
#     manager_response = 'yes'
#     client.messages \
#         .create(
#         body=employee_name + " requested " + shift_requested_off +
#              " off. " + available_employees + " are available. Should I text them? [yes/no]",
#         from_='+16162131665',
#         to=str(manager_phone)
#     )
#
#     if manager_response.lower() == 'yes':
#         print("")
#         # Text available employees
#     elif manager_response.lower() == 'no':
#         response = ("Is " + employee_name + " still able to take " + shift_requested_off +
#                     " off? [yes/no]")
#         send_response(manager_phone, response)
#
# #
# # def find_available_employees():
# #
# #     return "hi"
#
# #
# # def text_available_employees_to_cover(available_employees, employee_requesting_off, shift_requested_off):
# #     for x in range(len(available_employees)):
# #         client.messages \
# #             .create(
# #             body=employee_requesting_off + " is requesting " + shift_requested_off
# #                 + " off. Do you want to cover their shift? [yes/no]",
# #             from_='+16162131665',
# #             to=available_employees[x].phone_number
# #         )
#
#
# # def find_last_messages(phone_number):
# #     messages_sent = client.messages.list(
# #         from_='+16162131665',
# #         to=str(phone_number)
# #     )
# #     messages_recieved = client.messages.list(
# #         from_=str(phone_number),
# #         to='+16162131665'
# #     )
# #     # !@# is used to seperate the messages
# #     if messages_sent is not None:
# #         both_messages = client.messages(messages_sent[-1].sid).fetch().body +
# #             "!@#" + client.messages(messages_recieved[-1].sid).fetch().body
# #     else:
# #         both_messages = None
# #     return both_messages
