import PySimpleGUI as gui
import datetime
import json


error = "Error. No receipt matches the data you have entered."

def is_valid_license_plate(license_plate: list[str]):
    #The license plates stored in the json file are all of format Bundesland:KeyWord:Number
    #This function will only validate license plates of that type, regular austrian license plates
    #or license plates from outside the country will be seen as invalid for the purpose of this example
    if len(license_plate) < 3:
        return False
    if (len(license_plate[0]) > 2 or not license_plate[0].isalpha()):
        return False
    if not license_plate[1].isalnum():
        return False
    if not license_plate[2].isnumeric():
        return False
    return True

def is_valid_date(date=''):
    date = date.replace(".", "-")
    format = "%d-%m-%Y"
    res = True
    try:
        res = bool(datetime.datetime.strptime(date, format))
    except ValueError:
        res = False

    return res

def is_valid_card(card=''):
    if (not len(card) == 4 or not card.isnumeric()):
        return False
    return True




def gui_loop(window: gui.Window) -> list[any]:

    event, values = window.read()
    retval = []

    if event == gui.WINDOW_CLOSED or event == 'Exit':
        retval.append(gui.WINDOW_CLOSED)
        return retval
    if event == 'Search':
        license_plate = [values['license_plate:bl'], values['license_plate:kw'], values['license_plate:nr']]
        date = values['date']
        card = values['card']
        invalid = []


        if not is_valid_license_plate(license_plate):
            window['license_plate:bl'].update(value='', background_color='salmon')
            window['license_plate:kw'].update(value='', background_color='salmon')
            window['license_plate:nr'].update(value='', background_color='salmon')
            window['lp-format'].update(value="Format: State Word Number (e.g.: G ARIVO 1)")
            invalid.append("License Plate")
        else:
            window['license_plate:bl'].update(background_color='white')
            window['license_plate:kw'].update(background_color='white')
            window['license_plate:nr'].update(background_color='white')
            window['lp-format'].update(value="")
            retval.append(license_plate)



        if not is_valid_date(date):
            window['date'].update(value="",background_color='salmon')
            window['date-format'].update(value="Format: DD.MM.YYYY (e.g.: 24.12.2023)")
            invalid.append("Date")
        else:
            window['date'].update(background_color='white')
            window['date-format'].update(value="")
            retval.append(date)



        if not is_valid_card(card):
            window['card'].update(value="",background_color='salmon')
            window['card-format'].update(value="Format: XXXX (e.g: 1234)")
            invalid.append("Card Number")
        else:
            window['card'].update(background_color='white')
            window['card-format'].update(value="")
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
            retval.insert(0, 0)
            return retval
        else:
            lp_final = ""
            for str in license_plate:
                lp_final += str
            return lp_final, date, card

def setupGUI() -> gui.Window:
    input_and_options = [[gui.Text("License Plate:"), gui.Push(), gui.InputText(size=5, key='license_plate:bl'),
                          gui.InputText(size=11,key='license_plate:kw'),
                          gui.InputText(size=5,key='license_plate:nr')],
                        [gui.Text("Date of Payment:"), gui.Push(), gui.InputText(size=25, key='date')],
                        [gui.Text("Last 4 digits of your Card:"), gui.Push(), gui.InputText(size=25,key='card')],
                        [gui.Push(), gui.Button("Search"), gui.Button("Exit")]
            ]

    format_specifiers = [[gui.Text(text="", key='lp-format')],
                         [gui.Text(text="", key='date-format')],
                         [gui.Text(text="", key='card-format')], [gui.Text("")]]

    search_results = [[gui.Text(text="", visible=True, key='receipt')]]

    layout = [[gui.Column(input_and_options), gui.VSeparator(), gui.Column(format_specifiers)],
                [gui.HSeparator()],
                [gui.Column(search_results, key='receipt_column', scrollable=True, vertical_scroll_only=True,
                            visible=False, size=(700, 850))]
                ]

    window = gui.Window("Arivo Reciept Search Engine", layout, size=(700, 1000))
    return window


def readData()-> list[any]:
    file = open("logs.json")
    data = []
    for jsonObj in file:
            object = json.loads(jsonObj)
            data.append(object)
    return data

def reformatDateObject(dateobj):
    dateobj_destructed = str(dateobj).split("-")
    final_string = ""

    for i in range(len(dateobj_destructed)):
        final_string += dateobj_destructed[-(i + 1)]
        if(i < len(dateobj_destructed)-1):
            final_string += "."

    return final_string

def reformatCardNumber(cardnumber: str):
    cardnumber = cardnumber.replace(" ", "")
    cardnumber = cardnumber.replace("E", "")
    cardnumber = cardnumber.replace("F", "")
    return cardnumber

def search_receipt(values: list[any], data: list[any]):
    #License-Plat can be found in: payload.om_payload
    #Date can be found in: payload.timestamp (in unix time)
    #Card can be found in: payload.payment_payload.extra.card_number
    for entry in data:
        if entry[0] == "count":
            continue
        payload_dict = entry[1]
        str = payload_dict["om_payload"]["id"]
        p_license_plate = str.replace(" ", "")
        #check if license plates match
        if values[0].upper() != p_license_plate:
            continue
        #check if date matches
        timestamp = payload_dict["timestamp"]
        dateobj = datetime.date.fromtimestamp(timestamp)
        date_string = reformatDateObject(dateobj)
        print(date_string)
        if values[1] != date_string:
            continue
        try:
            card = payload_dict["payment_payload"]["extra"]["card_number"]
        except KeyError:
            continue
        card_string = reformatCardNumber(card)
        if values[2] != card_string:
            continue
        both_receipts = payload_dict["receipt"]
        receipts = both_receipts.split("KUNDENBELEG")
        receipt = "** KUNDENBELEG" #not a pretty solution but we dont want to display the vendors receipt just in case
        receipt += receipts[1]
        return receipt
    return error



def main():

    data = readData()
    window = setupGUI()
    retval =[]
    while True:
        retval = gui_loop(window)
        if(retval[0] == gui.WINDOW_CLOSED):
            break
        if(retval[0] == 0):
            continue

        receipt = search_receipt(retval, data)
        if receipt == error:
            gui.popup_error(error)
            continue
        window['receipt'].update(value=receipt)
        window['receipt_column'].update(visible=True)





if __name__ == "__main__":
  main()