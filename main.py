from nicegui import ui
import csv

# Path to the CSV file
CSV_FILE = 'userdata.csv'

# Ensure CSV file has headers
def ensure_csv_headers():
    try:
        with open(CSV_FILE, 'x', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Name','Role', 'Age', 'Email'])
    except FileExistsError:
        pass

ensure_csv_headers()

# Validation functions
def validate_name(value):
    return len(value.strip()) > 0

def validate_age(value):
    return value.isdigit() and 0 < int(value) < 120

def validate_email(value):
    return "@" in value and "." in value

# Form submission handler
def submit_form():
    name = name_input.value.strip()
    role=name_input.value.strip()
    age = age_input.value.strip()
    email = email_input.value.strip()

    errors = []
    if not validate_name(name):
        errors.append("Name is required.")
    if not validate_age(age):
        errors.append("Role is required")
    if not validate_email(email):
        errors.append("Invalid email address.")

    if errors:
        ui.notify('\n'.join(errors), type='negative')
        return

    with open(CSV_FILE, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([name,role, age, email])

    ui.notify('Data saved!', type='positive')
    name_input.value = ''
    # role_input.value = ''
    age_input.value = ''
    email_input.value = ''

# UI Layout
ui.markdown('## General Attendance')

with ui.card().classes('w-96'):
    name_input = ui.input('Name').props('required')
    with ui.dropdown_button("Role",auto_close=True).props('required') as role:
        ui.item("Student Presenter",on_click=lambda : ui.radio(["Senior","Junior"]))
        ui.item("Judge",on_click=lambda : ui.radio(["Senior","Junior"]))
        ui.item("General Participant",on_click=lambda : ui.checkbox("If you are a bachelor graduate or above, will you be considered in being a judge?").classes("color-red"))
    ui.label("If you are a bachelor graduate or above, will you be considered in being a judge?")
    age_input = ui.input('Age').props('type=number required')
    email_input = ui.input('Email').props('type=email required')
    ui.button('Submit', on_click=submit_form)

# Optionally, add a button to download the CSV file
def export_csv():
    ui.download(CSV_FILE)

ui.button('Download CSV', on_click=export_csv).props('color=primary')

ui.run()
