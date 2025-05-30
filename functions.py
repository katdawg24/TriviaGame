from PyQt5.QtWidgets import QGridLayout, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5 import QtCore
from urllib.request import urlopen
import json
import pandas as pd
import random
from settings import SettingsWindow



#default settings
preferences = {
    "difficulty": "Normal",  # or "Easy"
    "question_limit": 5
}

settings_window = None


#open api link to database
with open("questions.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    df = pd.DataFrame(data["results"])

#load 1 instance of questions & answers at a time from the database
def preload_data(idx):
    #idx parm: selected randomly time and again at function call
    question = df["question"][idx]
    correct = df["correct_answer"][idx]
    wrong = df["incorrect_answers"][idx]

    #fixing charecters with bad formatting
    formatting = [
        ("#039;", "'"),
        ("&'", "'"),
        ("&quot;", '"'),
        ("&lt;", "<"),
        ("&gt;", ">")
        ]

    #replace bad charecters in strings
    for tuple in formatting:
        question = question.replace(tuple[0], tuple[1])
        correct = correct.replace(tuple[0], tuple[1])
    #replace bad charecters in lists
    for tuple in formatting:
        wrong = [char.replace(tuple[0], tuple[1]) for char in wrong]

    #store local values globally
    parameters["question"].append(question)
    parameters["correct"].append(correct)

    
    random.shuffle(wrong) 
    all_answers = [correct] + wrong
    if preferences["difficulty"] == "Easy":
        all_answers = all_answers[:2]

    random.shuffle(all_answers)  # Shuffle the answers to randomize their order

    for i in range(4):
        parameters[f"answer{i+1}"].append(all_answers[i] if i < len(all_answers) else "")


#dictionary to store local pre-load parameters on a global level
parameters = {
    "question": [],
    "answer1": [],
    "answer2": [],
    "answer3": [],
    "answer4": [],
    "correct": [],
    "score": [],
    "index": []
    }

#global dictionary of dynamically changing widgets
widgets = {
    "logo": [],
    "button": [],
    "score": [],
    "question": [],
    "answer1": [],
    "answer2": [],
    "answer3": [],
    "answer4": [],
    "message": [],
    "message2": []
}

#function to open settings window
def open_settings():
    global settings_window
    settings_window = SettingsWindow(save_settings)
    settings_window.show()

#function to save settings
def save_settings(difficulty, question_limit):
    preferences["difficulty"] = "Easy" if "Easy" in difficulty else "Normal"
    preferences["question_limit"] = question_limit


#initialliza grid layout
grid = QGridLayout()

def clear_widgets():
    ''' hide all existing widgets and erase
        them from the global dictionary'''
    for widget_list in widgets.values():
        while widget_list:
            widget = widget_list.pop()
            widget.hide()
            widget.setParent(None)  # Fully remove it from the layout

def clear_parameters():
    #clear the global dictionary of parameters
    for parm in parameters:
        if parameters[parm] != []:
            for i in range(0, len(parameters[parm])):
                parameters[parm].pop()
    #populate with initial index & score values
    parameters["index"].append(random.randint(0,49))
    parameters["score"].append(0)

def start_game():
    #start the game, reset all widgets and parameters
    clear_widgets()
    clear_parameters()
    preload_data(parameters["index"][-1])
    #display the game frame
    frame2()

def create_buttons(answer, l_margin, r_margin):
    #create identical buttons with custom left & right margins
    button = QPushButton(answer)
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setFixedWidth(485)
    button.setStyleSheet(
        #setting variable margins
        "*{margin-left: " + str(l_margin) +"px;"+
        "margin-right: " + str(r_margin) +"px;"+
        '''
        border: 4px solid '#BC006C';
        color: white;
        font-family: 'shanti';
        font-size: 16px;
        border-radius: 25px;
        padding: 15px 0;
        margin-top: 20px;
        }
        *:hover{
            background: '#BC006C';
        }
        '''
    )
    button.clicked.connect(lambda x: is_correct(button))
    return button

def is_correct(btn):
    if btn.text() == parameters["correct"][-1]:
        parameters["score"][-1] += 10

        if parameters["score"][-1] >= preferences["question_limit"] * 10:
            clear_widgets()
            frame3()
        else:
            parameters["index"][-1] = random.randint(0, len(df) - 1)
            preload_data(parameters["index"][-1])
            update_game_frame()
    else:
        clear_widgets()
        frame4()

def update_game_frame():
    widgets["score"][-1].setText(str(parameters["score"][-1]))
    widgets["question"][0].setText(parameters["question"][-1])
    
    answer_buttons = [widgets["answer1"][0], widgets["answer2"][0]]
    if preferences["difficulty"] == "Normal":
        answer_buttons += [widgets["answer3"][0], widgets["answer4"][0]]

    for i, btn in enumerate(answer_buttons):
        btn.setText(parameters[f"answer{i+1}"][-1])


#*********************************************
#                  FRAME 1
#*********************************************

def frame1():
    clear_widgets()
    #logo widget
    image = QPixmap("logo.png")
    logo = QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet("margin-top: 100px;")
    widgets["logo"].append(logo)

    #button widget
    button = QPushButton("PLAY")
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setStyleSheet(
        '''
        *{
            border: 4px solid '#BC006C';
            border-radius: 45px;
            font-size: 35px;
            color: 'white';
            padding: 25px 0;
            margin: 10px 20px;
        }
        *:hover{
            background: '#BC006C';
        }
        '''
    )
    #button callback
    button.clicked.connect(start_game)
    widgets["button"].append(button)

    #settings button widget
    settings_button = QPushButton("SETTINGS")
    settings_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    settings_button.setStyleSheet(
        '''
        *{
            border: 2px solid '#BC006C';
            border-radius: 25px;
            font-size: 20px;
            color: 'white';
            padding: 10px;
            margin: 10px;
        }
        *:hover{
            background: '#BC006C';
        }
        '''
    )
    settings_button.clicked.connect(open_settings)
    widgets["button"].append(settings_button)

    #place global widgets on the grid
    grid.addWidget(widgets["logo"][-1], 0, 0, 1, 2)
    grid.addWidget(widgets["button"][-2], 1, 0, 1, 2)
    grid.addWidget(widgets["button"][-1], 2, 0, 1, 2)

#*********************************************
#                  FRAME 2
#*********************************************

def frame2():
    #score widget
    score = QLabel(str(parameters["score"][-1]))
    score.setAlignment(QtCore.Qt.AlignRight)
    score.setStyleSheet(
        '''
        font-size: 35px;
        color: 'white';
        padding: 15px 10px;
        margin: 20px 200px;
        background: '#64A314';
        border: 1px solid '#64A314';
        border-radius: 35px;
        '''
    )
    widgets["score"].append(score)

    #question widget
    question = QLabel(parameters["question"][-1])
    question.setAlignment(QtCore.Qt.AlignCenter)
    question.setWordWrap(True)
    question.setStyleSheet(
        '''
        font-family: 'shanti';
        font-size: 25px;
        color: 'white';
        padding: 75px;
        '''
    )
    widgets["question"].append(question)

        # Dynamically generate answer buttons based on non-empty answers
    answer_keys = ["answer1", "answer2", "answer3", "answer4"]
    margins = [(85, 5), (5, 85), (85, 5), (5, 85)]
    row = 2
    col = 0

    for i, key in enumerate(answer_keys):
        answer_text = parameters[key][-1]
        if answer_text.strip() != "":
            btn = create_buttons(answer_text, *margins[i])
            widgets[key].append(btn)
            grid.addWidget(btn, row, col)
            if col == 1:
                row += 1
                col = 0
            else:
                col = 1

    #logo widget
    image = QPixmap("logo_bottom.png")
    logo = QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet("margin-top: 75px; margin-bottom: 30px;")
    widgets["logo"].append(logo)

    #place widget on the grid
    grid.addWidget(widgets["score"][-1], 0, 1)
    grid.addWidget(widgets["question"][-1], 1, 0, 1, 2)
    grid.addWidget(widgets["logo"][-1], 4, 0, 1,2)

#*********************************************
#             FRAME 3 - WIN GAME
#*********************************************

def frame3():
    #congradulations widget
    message = QLabel("Congradulations! You\nare a true programmer!\n your score is:")
    message.setAlignment(QtCore.Qt.AlignRight)
    message.setStyleSheet(
        "font-family: 'Shanti'; font-size: 25px; color: 'white'; margin: 100px 0px;"
        )
    widgets["message"].append(message)

    #score widget
    score = QLabel()
    score.setText(str(parameters["score"][-1]))
    score.setStyleSheet("font-size: 100px; color: #8FC740; margin: 0 75px 0px 75px;")
    widgets["score"].append(score)

    #go back to work widget
    message2 = QLabel("OK. Now go back to WORK.")
    message2.setAlignment(QtCore.Qt.AlignCenter)
    message2.setStyleSheet(
        "font-family: 'Shanti'; font-size: 30px; color: 'white'; margin-top:0px; margin-bottom:75px;"
        )
    widgets["message2"].append(message2)

    #button widget
    button = QPushButton('TRY AGAIN')
    button.setStyleSheet(
        "*{background:'#BC006C'; padding:25px 0px; border: 1px solid '#BC006C'; color: 'white'; font-family: 'Arial'; font-size: 25px; border-radius: 40px; margin: 10px 300px;} *:hover{background:'#ff1b9e';}"
        )
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.clicked.connect(frame1)

    widgets["button"].append(button)

    #logo widget
    pixmap = QPixmap('logo_bottom.png')
    logo = QLabel()
    logo.setPixmap(pixmap)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet(
        "padding :10px; margin-top:75px; margin-bottom: 20px;"
    )
    widgets["logo"].append(logo)

    #place widgets on the grid
    grid.addWidget(widgets["message"][-1], 2, 0)
    grid.addWidget(widgets["score"][-1], 2, 1)
    grid.addWidget(widgets["message2"][-1], 3, 0, 1, 2)
    grid.addWidget(widgets["button"][-1], 4, 0, 1, 2)
    grid.addWidget(widgets["logo"][-1], 5, 0, 2, 2)


#*********************************************
#                  FRAME 4 - FAIL
#*********************************************
def frame4():
    clear_widgets()
    #sorry widget
    message = QLabel("Sorry, this answer \nwas wrong\n your score is:")
    message.setAlignment(QtCore.Qt.AlignRight)
    message.setStyleSheet(
        "font-family: 'Shanti'; font-size: 35px; color: 'white'; margin: 75px 5px; padding:20px;"
        )
    widgets["message"].append(message)

    #score widget
    score = QLabel(str(parameters["score"][-1]))
    score.setStyleSheet("font-size: 100px; color: white; margin: 0 75px 0px 75px;")
    widgets["score"].append(score)

    #button widget
    button = QPushButton('TRY AGAIN')
    button.setStyleSheet(
        '''*{
            padding: 25px 0px;
            background: '#BC006C';
            color: 'white';
            font-family: 'Arial';
            font-size: 35px;
            border-radius: 40px;
            margin: 10px 200px;
        }
        *:hover{
            background: '#ff1b9e';
        }'''
        )
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.clicked.connect(frame1)

    widgets["button"].append(button)

    #logo widget
    pixmap = QPixmap('logo_bottom.png')
    logo = QLabel()
    logo.setPixmap(pixmap)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet(
        "padding :10px; margin-top:75px;"
    )
    widgets["logo"].append(logo)

    #place widgets on the grid
    grid.addWidget(widgets["message"][-1], 1, 0)
    grid.addWidget(widgets["score"][-1], 1, 1)
    grid.addWidget(widgets["button"][-1], 2, 0, 1, 2)
    grid.addWidget(widgets["logo"][-1], 3, 0, 1, 2)
