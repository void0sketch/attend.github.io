from nicegui import ui
import os
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials

# Load environment variables from .env file
load_dotenv()

# Build credentials dictionary from environment variables
credentials_dict = {
    "type": os.getenv("TYPE"),
    "project_id": os.getenv("PROJECT_ID"),
    "private_key_id": os.getenv("PRIVATE_KEY_ID"),
    "private_key": os.getenv("PRIVATE_KEY").replace("\\n", "\n"),
    "client_email": os.getenv("CLIENT_EMAIL"),
    "client_id": os.getenv("CLIENT_ID"),
    "auth_uri": os.getenv("AUTH_URI"),
    "token_uri": os.getenv("TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
    "universe_domain": os.getenv("UNIVERSE_DOMAIN")
}

# Define required Google API scopes
scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# Authorize Google Sheets client with scopes
credentials = Credentials.from_service_account_info(credentials_dict, scopes=scopes)
gc = gspread.authorize(credentials)

# Google Sheets setup
SHEET_NAME = 'User Data'
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
