import tkinter as tk
from PIL import Image, ImageTk
from functools import partial
from tkinter.colorchooser import askcolor

root = tk.Tk()
game_frm = ''
name_label = ''
active_player = ''
game_window = ''
lines_table = []
lines_dict = {}
spaces_table = []
players_dict = {}

for i in range(11):
    temp_list = []
    if i % 2 == 0:
        for j in range(5):
            temp_list.append('black')
    else:
        for j in range(6):
            temp_list.append('black')
    lines_table.append(temp_list)

# Checking winner every turn
def check_winner():
    blacks = 0
    for k in range(5):
        i = k*2
        temp_list1 = lines_table[i]
        temp_list2 = lines_table[i + 1]
        temp_list3 = lines_table[i + 2]
        try:

            # Algorithm for checking if a square has been completed
            for j in range(5):

                # In case a square has been completed by a player, changing its color and updating player's score
                if temp_list1[j] == temp_list2[j] and temp_list2[j] == temp_list2[j + 1] and temp_list2[j+1] == temp_list3[j] and temp_list1[j] != 'black':
                    color = (players_dict[temp_list1[j]])[1]
                    (spaces_table[int(i / 2)])[j].config(bg = color)
                    continue
                # Counting the number of lines that have not been captured yet. This will let the program know when 
                # the end screen should be displayed
                if temp_list1[j] == 'black':
                    blacks += 1
                if temp_list2[j] == 'black':
                    blacks += 1
                if temp_list2[j + 1] == 'black':
                    blacks += 1
                if temp_list3[j] == 'black':
                    blacks += 1
        except:
            pass
    if blacks == 0:
        # Updating player's score
        for k in range(5):
            i = k*2
            temp_list1 = lines_table[i]
            temp_list2 = lines_table[i + 1]
            temp_list3 = lines_table[i + 2]
            for j in range(5):
                if temp_list1[j] == temp_list2[j] and temp_list2[j] == temp_list2[j + 1] and temp_list2[j+1] == temp_list3[j] and temp_list1[j] != 'black':
                    score = (players_dict[temp_list1[j]])[0]
                    (players_dict[temp_list1[j]])[0] = score + 1
        print(players_dict)
        end_screen()


# Method for changing the color of the
# buttons ( lines ) when pressed
def change_line_colour(button):
    global active_player, name_label
    # Changing player's turn, changing the main list
    # according to what buttons are pressed
    column = int(lines_dict[button][:-2])
    if column == 10:
        line = int(lines_dict[button][3:])
    else:
        line = int(lines_dict[button][2:])
    temp_list = lines_table[column]
        
    # Changing players' turn and buttons' background color
    # For the first player '(list(players_dict.keys()))[0]'
    if active_player == (list(players_dict.keys()))[0]:
        # Changing the color of the line according to the color stored in 'players_dict'
        button.config(bg=(players_dict[(list(players_dict.keys()))[0]])[1])
        button['state'] = 'disabled'
        # Assigning the active_player to the temp_list[line] so we can later on check if a square has been completed
        temp_list[line] = active_player
        # Changing players' turn
        active_player = (list(players_dict.keys()))[1]
        name_label.config(text=f'{active_player}`s turn')
    # For the second player '(list(players_dict.keys()))[1]'
    elif active_player == (list(players_dict.keys()))[1]:
        button.config(bg=(players_dict[(list(players_dict.keys()))[1]])[1])
        button['state'] = 'disabled'
        temp_list[line] = active_player
        active_player = (list(players_dict.keys()))[0]
        name_label.config(text=f'{active_player}`s turn')

    check_winner()

# Creating the game frame, with all its elements
def creating_game_window():
    global game_frm, players_dict, name_label, game_window
    players = {}

    # In case it'a replay, destroying the previous game_window
    try:
        game_window.destroy()
    except:
        pass

    # Method that creates a 'color chosing dialog window', 
    # which will be accesed by the player to select their color
    def choose_player_color(button):
        color = askcolor()
        button.config(bg=color[1])

    # Method for retrieving player's name and color
    # and initializes the game itself
    def getting_info():
        global active_player
        for i in range(2):
            player_name = (players[i])[0].get()
            player_color = (players[i])[1]['bg']
            players_dict[player_name] = [0, player_color]
        active_player = (list(players_dict.keys()))[0]
        players_frm.destroy()
        submit_button.destroy()
        game_frm.pack()
        name_label.pack(pady=10, padx=(300,0))
        name_label.config(text=f'{active_player}`s turn')


    game_window = tk.Toplevel(root)
    game_window.config(bg='white')
    # Creating fields for users to add their names and colours
    players_frm = tk.Frame(game_window, bg='white')
    players_frm.columnconfigure([0,1], minsize=200)
    players_frm.rowconfigure(2, minsize=100)
    for i in range(2):
        player_lbl = tk.Label(players_frm, bg='white', fg='black', text=f'Player {i + 1}', font=('Helvetica', 20))
        player_name = tk.Entry(players_frm, bg='white', fg='black', font=('Helvetica', 20))
        colour_picker = tk.Button(players_frm, bg='grey', font=('',20), relief=None, bd=0, highlightthickness=0, highlightbackground=None)
        colour_picker.config(command=partial(choose_player_color, colour_picker))
        player_lbl.grid(row=0, column=i, pady=20, padx=150, sticky='nsew')
        player_name.grid(row=1, column=i, pady=20, padx=50, sticky='nsew')
        colour_picker.grid(row=2, column=i, padx=50, sticky='nsew')
        players[i] = [player_name, colour_picker]

    submit_button = tk.Button(game_window, bg='green', fg='white', text='START', font=('Helvetica', 20), width=15, height=2, relief=None, bd=0, highlightthickness=0, highlightbackground=None, command=getting_info)
    players_frm.pack()
    submit_button.pack(pady=50)

    # Creating the game area
    game_frm = tk.Frame(game_window, bg='white')
    for j in range(11):
        temp_list = []
        if j % 2 == 0:
            for i in range(11):

                # The rows with circles and horizontal lines
                # Adding just the circles
                if i % 2 == 0:
                    img_temp = Image.open('circle.png')
                    img_temp = img_temp.resize((60,60), Image.ANTIALIAS)
                    img = ImageTk.PhotoImage(img_temp)
                    label1 = tk.Label(game_frm, bg='white', image=img)
                    label1.image = img
                    label1.grid(row=j, column=i)

                # The rows with just vertical lines
                else:
                    line = tk.Button(game_frm, bg='black', height=1, width=20, font=('', 6), relief=None, bd=0, highlightthickness=0, highlightbackground=None)
                    line.config(command=partial(change_line_colour, line))
                    line.grid(row=j, column=i)
                    lines_dict[line] = f'{j}-{int(i / 2)}'
        else:
            # The rows with circles and horizontal lines
            # Adding just the lines, next to the circles ( code above )
            for i in range(11):
                if i % 2 == 0:
                    line = tk.Button(game_frm, bg='black', width=1, height=8, relief=None, bd=0, highlightthickness=0, highlightbackground=None)
                    line.config(command=partial(change_line_colour, line))
                    line.grid(row=j, column=i)
                    lines_dict[line] = f'{j}-{int(i / 2)}'
            
                # Next to the vertical lines, adding empty space to separate lines
                # These spaces will later be colored according to what square is completed by the players
                else:
                    empty = tk.Frame(game_frm, bg='white', width=120, height=120)
                    empty.grid(row=j, column=i)
                    temp_list.append(empty)
            spaces_table.append(temp_list)
    name_label = tk.Label(game_window, bg='white', fg='black', text='Player`s turn', font=('Helvetica', 35))


# When all the lines have been captured, end screen is shown, displaying the player with the most points,
# or 'it'a tie' in case both players had the same number of points
def end_screen():
    global game_window
    game_frm.destroy()
    name_label.destroy()
    end_frame = tk.Frame(game_window, bg='white')
    winner = tk.Label(end_frame, bg='white', fg='black', text='WE HAVE A WINNER', font=('Helvetica', 50))
    player = tk.Label(end_frame, bg='white', fg='black', text='Player wins with X points.', font=('Helvetica', 30))
    replay = tk.Button(end_frame, bg='#05dffc', fg='white', text='Replay', font=('Helvetica', 30), highlightthickness = 0, bd = 0, relief=None, command=creating_game_window)

    # Checking players' score and choosing the winner. In case it's a tie, we display a coresponding message.
    player1 = list(players_dict.keys())[0]
    player2 = list(players_dict.keys())[1]
    if (players_dict[player1])[0] > (players_dict[player2])[0]:
        player.config(text=f'{player1} wins with {(players_dict[player1])[0]} points.')
    elif (players_dict[player1])[0] < (players_dict[player2])[0]:
        player.config(text=f'{player2} wins with {(players_dict[player2])[0]} points.')
    else:
        winner.config(text="IT'S A TIE!")
        player.config(text=f'Both players got {(players_dict[player1])[0]} points')
    winner.pack(pady=(50, 30), padx=20)
    player.pack(pady=(0, 30))
    replay.pack(pady=(0, 50))
    end_frame.pack()


# Method for creating the main menu, where players cand start the game, manage settings and exit
def main_menu():
    root.columnconfigure(0, minsize=300)
    root.rowconfigure([0,1,2,3], minsize=120)
    root.config(bg='white')
    buttons = ['Title', 'Play', 'Settings', 'Exit']
    commands = ['', creating_game_window, '', root.destroy]
    for i in range(len(buttons)):
        if buttons[i] == 'Title':
            title = tk.Label(root, font=('Helvetica', 35), text='Lines Game', bg='white', fg='black')
            title.grid(row=0, column=0, padx=10, sticky='nsew')
        else:
            button = tk.Button(root, text=buttons[i], bg='#c4c4c4', fg='black', font=('Helvetica', 20), highlightthickness = 0, bd = 0, relief=None, command=commands[i])
            if buttons[i] == 'Play':
                button.config(bg='#05dffc', fg='white')
            elif buttons[i] == 'Exit':
                button.config(bg='#a82121', fg='white')
            button.grid(row=i, column=0, pady=(0,40), padx=10, sticky='nsew')


main_menu()

root.mainloop()