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


def main():

  input_and_options = [[gui.Text("License Plate:"), gui.Push(), gui.InputText(key='license_plate')],
                       [gui.Text("Date of Payment:"), gui.Push(), gui.InputText(key='date')],
                       [gui.Text("Last 4 digits of your Card:"), gui.Push(), gui.InputText(key='card')],
                       [gui.Push(), gui.Button("Search"), gui.Button("Exit")]
            ]

  search_results = [[gui.Button("Click me! I don't do anything!")]]

  layout = [[gui.Column(input_and_options),
            gui.VSeperator(),
            gui.Column(search_results)]
            ]

  window = gui.Window("Arivo Reciept Search Engine", layout, size=(1000, 800))

  while True:


    event, values = window.read()

    if event == gui.WINDOW_CLOSED or event == 'Exit':
      break
    if event == 'Search':
      print(values)
      license_plate = values['license_plate']
      date = values['date']
      card = values['card']

      print(license_plate + date + card)

      if not is_valid_license_plate(license_plate):
        window['license_plate'].update(value='', background_color='salmon')
        gui.popup_error('Invalid License Plate. Please enter a valid value')
      else:
        window['license_plate'].update(background_color='white')

      if not is_valid_date(date):
        window['date'].update(background_color='salmon')
        gui.popup_error('Invalid Date. Please enter a valid value')
      else:
        window['date'].update(background_color='white')


      if not is_valid_card(card):
        window['card'].update(background_color='salmon')
        gui.popup_error('Invalid card number. Please enter a valid value')
      else:
        window['card'].update(background_color='white')







if __name__ == "__main__":
  main()