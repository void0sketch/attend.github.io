from nicegui import ui
import gspread

# Google Sheets setup
SHEET_NAME = 'User Data'  # Replace with your actual sheet name
CREDENTIALS_FILE = 'credentials.json'  # Make sure this matches your file

gc = gspread.service_account(filename=CREDENTIALS_FILE)
sh = gc.open(SHEET_NAME)
worksheet = sh.sheet1

# Ensure headers exist (run once)
EXPECTED_HEADERS = ['Name', 'Role', 'Number', 'Email']
if worksheet.row_count < 1 or worksheet.row_values(1) != EXPECTED_HEADERS:
    worksheet.clear()
    worksheet.append_row(EXPECTED_HEADERS)

# Validation functions
def validate_name(value):
    return len(value.strip()) > 0

def validate_role(value):
    return len(value.strip()) > 0

def validate_number(value):
    return value.isdigit() and len(value) == 10

def validate_email(value):
    return "@" in value and "." in value

# Form submission handler
def submit_form():
    name = name_input.value.strip()
    role = role_input.value.strip()
    number = number_input.value.strip()
    email = email_input.value.strip()

    errors = []
    if not validate_name(name):
        errors.append("Name is required.")
    if not validate_role(role):
        errors.append("Role is required.")
    if not validate_number(number):
        errors.append("Number must be exactly 10 digits.")
    if not validate_email(email):
        errors.append("Invalid email address.")

    if errors:
        ui.notify('\n'.join(errors), type='negative')
        return

    worksheet.append_row([name, role, number, email])
    ui.notify('Data saved!', type='positive')
    name_input.value = ''
    role_input.value = ''
    number_input.value = ''
    email_input.value = ''

# UI Layout
ui.markdown('## General Attendance')

with ui.card().classes('w-96'):
    name_input = ui.input('Name').props('required')
    role_input = ui.select(
        ['Student Presenter', 'Judge', 'General Participant'],
        label='Role'
    ).props('required')
    number_input = ui.input('Number').props('type=number required')
    email_input = ui.input('Email').props('type=email required')
    ui.button('Submit', on_click=submit_form)

ui.run()
