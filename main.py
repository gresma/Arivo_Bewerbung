import PySimpleGUI as gui


def is_valid_license_plate(license_plate=''):
    if license_plate == "valid":
        return True
    return False

def is_valid_date(date=''):
    if date == "valid":
        return True
    return False

def is_valid_card(card=''):
    if card == "valid":
        return True
    return False


def search_reciept(license_plate, date, card_numbers):
    return

def gui_loop(window: gui.Window) -> list[any]:

    event, values = window.read()
    retval = []

    if event == gui.WINDOW_CLOSED or event == 'Exit':
        retval.append(gui.WINDOW_CLOSED)
        return retval
    if event == 'Search':
        license_plate = values['license_plate']
        date = values['date']
        card = values['card']
        invalid = []

        print(license_plate + date + card)

        if not is_valid_license_plate(license_plate):
            window['license_plate'].update(value='', background_color='salmon')
            invalid.append("License Plate")
        else:
            window['license_plate'].update(background_color='white')
            retval.append(license_plate)

        if not is_valid_date(date):
            window['date'].update(background_color='salmon')
            invalid.append("Date")
        else:
            window['date'].update(background_color='white')
            retval.append(date)


        if not is_valid_card(card):
            window['card'].update(background_color='salmon')
            invalid.append("Card Number")
        else:
            window['card'].update(background_color='white')
            retval.append(card)



        if invalid:
            error_message = "Your input for:\n"
            match len(invalid):
                case 1:
                    error_message += invalid[0] + " is invalid."
                case 2:
                    error_message += invalid[0] + " and " + invalid[1] + " are invalid."
                case 3:
                    error_message += invalid[0] + ", " + invalid[1] + " and " + invalid[2] + " are invalid."
                case _:
                    error_message += "Something went wrong."
            error_message +=  "\nDouble check your Input's Format."
            gui.popup_error(error_message)
        else:
            return license_plate, date, card
            





def main():

    input_and_options = [[gui.Text("License Plate:"), gui.Push(), gui.InputText("License Plate", key='license_plate')],
                        [gui.Text("Date of Payment:"), gui.Push(), gui.InputText(key='date')],
                        [gui.Text("Last 4 digits of your Card:"), gui.Push(), gui.InputText(key='card')],
                        [gui.Push(), gui.Button("Search"), gui.Button("Exit")]
            ]

    search_results = [[gui.Button("Click me! I crash everything!")]]

    layout = [[gui.Column(input_and_options),
                gui.VSeperator(),
                gui.Column(search_results)]
                ]

    window = gui.Window("Arivo Reciept Search Engine", layout, size=(1000, 800))
    retval =[]
    while True:
        retval = gui_loop(window)
        if(retval[0] == gui.WINDOW_CLOSED):
            break
        print(retval)





if __name__ == "__main__":
  main()