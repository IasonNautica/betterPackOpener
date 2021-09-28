import webbrowser
from PIL import ImageQt
import requests
import PySimpleGUI as sg
from io import BytesIO


def image_to_data(im):
    """
    Image object to bytes object.
    : Parameters
      im - Image object
    : Return
      bytes object.
    """
    with BytesIO() as output:
        im.save(output, format="PNG")
        data = output.getvalue()
    return data


def main(packlist):
    """
    Given a packlist, graphically shows your pulls. It does so by creating a window interface with rows of max size 5
    :param packlist: List, contains multiple other lists of cards
    """
    quit = False
    sg.theme('DarkBlue')
    for pack in packlist:
        if (quit):
            break
        layout = [[]]
        n = 0
        c = 0
        for card in pack:
            # print(card)
            url = card['image']
            response = requests.get(url, stream=True)
            response.raw.decode_content = True
            img = ImageQt.Image.open(response.raw)
            data = image_to_data(img)

            layout[c].append(sg.Frame(title=card['rarity'], title_location='s', relief='ridge',
                                      layout=[[sg.Image(data=data, size=(165, 245), enable_events=True,
                                                        k='SC-' + str(card['id']) + '-' + str(c) + str(n),
                                                        tooltip=card['name'])]]))


            n += 1
            if (n == 5):
                n = 0
                layout.append([])
                c += 1

        layout[c].append(sg.Button('Next', enable_events=True, key='N'))
        layout[c].append(sg.Button('Quit', enable_events=True, key='Q'))
        window = sg.Window('Card Display', layout, finalize=True)

        while True:  # Event Loop
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Q':
                quit = True
                window.close()
                break
            if event.startswith('SC-'):
                split = event.split('-')
                webbrowser.open('https://db.ygoprodeck.com/card/?search=' + split[1], 2)
            if event == 'N':
                window.close()
                break


if __name__ == '__main__':
    main([])
