import PySimpleGUI as sg
import re

def is_valid_license_plate(license_plate):#
    if license_plate == "valid":
      return True
    # Add your license plate validation logic here
    # For simplicity, let's assume any non-empty string is valid
    return False

def is_valid_date(date):
    if date == "valid":
      return True
    # Add your date validation logic here
    # For simplicity, let's assume any non-empty string is valid
    return False

def is_valid_credit_card(credit_card):
    if credit_card == "valid":
      return True
    # Add your credit card validation logic here
    # For simplicity, let's assume any non-empty string is valid
    return False

def main():
    sg.theme('LightGrey1')

    layout = [
        [sg.Text('License Plate:'), sg.InputText(key='license_plate')],
        [sg.Text(size=(30, 1), key='license_plate_error', text_color='red')],
        [sg.Text('Date:'), sg.InputText(key='date')],
        [sg.Text(size=(30, 1), key='date_error', text_color='red')],
        [sg.Text('Credit Card:'), sg.InputText(key='credit_card')],
        [sg.Text(size=(30, 1), key='credit_card_error', text_color='red')],
        [sg.Button('Search')]
    ]

    window = sg.Window('Input Validation', layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        if event == 'Search':
            license_plate = values['license_plate']
            date = values['date']
            credit_card = values['credit_card']

            # Validate input
            if not is_valid_license_plate(license_plate):
                window['license_plate_error'].update('Invalid License Plate. Please enter a valid value.')

            if not is_valid_date(date):
                window['date_error'].update('Invalid Date. Please enter a valid value.')

            if not is_valid_credit_card(credit_card):
                window['credit_card_error'].update('Invalid Credit Card. Please enter a valid value.')

            # Reset error messages
            #window['license_plate_error'].update('')
            #window['date_error'].update('')
            #window['credit_card_error'].update('')

    window.close()

if __name__ == "__main__":
    main()