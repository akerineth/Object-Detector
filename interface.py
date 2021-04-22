import PySimpleGUI as sg
import detector as kt
import os
import random as rd
from PIL import Image
import cv2


def topng(path):
    img = Image.open(path)
    img = img.resize((400, 300))
    a = path.split("\\")[-1]
    newpath = os.getcwd() + r"\tmp\\" + str(a.split('.')[0]) + ".png"
    img.save(newpath)
    return newpath


left = [[sg.Text("Введите адрес папки с изображениями")],
        # [sg.Text("Введите адрес папки с изображениями")]
        [sg.Input(key='-INPUT1-')],
        [sg.Text('Введите номера необходимых объектов через пробел')],
        [sg.Input(key="-INPUT2-")],
        [sg.Text('Введите необходимую точность (от 0 до 1)')],
        [sg.Input(key="-INPUT3-")],
        [sg.Text(size=(40, 1), key='-OUTPUT-')],
        [sg.Button('Ok'), sg.Button('Quit')],
        [
            sg.Listbox(
                values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
            )
        ]]

n = "\n".join(kt.CLASSES)

right = [
    [sg.Text(n)],
    [sg.Text(key="-TOUT-")]
]
right1 = [
    [sg.Text("")],
    [sg.Text(size=(40, 1), key="-TOUT1-")],
    [sg.Image(key="-IMAGE-")],
]

layout = [[sg.Column(left),
           sg.VSeparator(),
           sg.Column(right),
           sg.VSeparator(),
           sg.Column(right1)]
          ]

window = sg.Window('Классификатор изображений', layout)
#window.Maximize()
images = {}
a = 0
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break
    path = values["-INPUT1-"]
    """if a == 0:
        for dirs, folders, files in os.walk(path):
            for file in files:
                topng(str(os.path.join(path, file)))
            break
        a += 1"""
    path += '\\'
    path1 = os.getcwd() + '\\tmp'
    obj = list(map(int, values["-INPUT2-"].split(" ")))
    conf = float(values["-INPUT3-"])
    if event == "Ok":
        files = (kt.main_cycle(path, obj, conf))
        window["-FILE LIST-"].update(files)
    if event == "-FILE LIST-":  # A file was chosen from the listbox
        try:
            filename = os.path.join(
                path, values["-FILE LIST-"][0][0]
            )
            #print(filename)
            if filename not in images.keys():
                #filename_png = topng(filename)
                images[filename] = topng(filename)
                im = cv2.imread(images[filename])

            #print(filename)
            window["-TOUT1-"].update(filename)
            window["-IMAGE-"].update(filename=images[filename])

        except:
            print("ASHIPKA")
            pass

for dirs, folders, files in os.walk(os.getcwd() + '\\tmp'):
    for file in files:
        delt = os.path.join(os.getcwd() + '\\tmp', file)
        os.remove(delt)
    break

# print(path, obj)
window.close()