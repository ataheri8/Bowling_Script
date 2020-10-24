import re
import time
import os
import sys

spare_pattern = "^[0-9]{1} [/]{1}$"
openframe_pattern = "^[0-9]{1} [0-9]{1}$"
name_pattern = "^[a-z]+$"
current_turn = 1
current_turn_name = ""
frame_counter = 1
frame_max_counter = 0
player_counter = 0
counter = 1
players = {}
template = "{0:6}"
template_name = "{0:10}"


class Bowler:

    def __init__(self, name, order):
        self.name = name
        self.score = 0
        self.order = order
        self.frames = {}

    def roll(self, roll):
        frame_score = roll.split(" ")
        if roll == 'x':
            self.add_score("x")
        elif re.search(spare_pattern, roll) is not None:
            self.add_score(int(frame_score[0]), frame_score[1])
        elif re.search(openframe_pattern, roll) is not None:
            if int(frame_score[0]) + int(frame_score[1]) > 9:
                print("The two numbers combined cannot be greater than 9")
                time.sleep(1)
                main_game()
            else:
                self.add_score(int(frame_score[0]), int(frame_score[1]))
        else:
            print("Incorrect format")
            time.sleep(1)
            main_game()

    def add_score(self, roll_1, roll_2=""):
        roll_score = 0
        print(roll_1, roll_2)
        if roll_1 == "x":
            if frame_counter > 2:
                if self.frames[frame_counter - 2] == "x" and self.frames[frame_counter - 1] == "x":
                    roll_score += 20
            elif frame_counter > 1:
                if self.frames[frame_counter - 1] == "x":
                    roll_score += 10
                elif type(roll_2) == type("") and "/" in str(self.frames[frame_counter - 1]):
                    roll_score += 10
            self.frames[frame_counter] = "x"
            roll_score += 10

        elif type(roll_2) == type("") and "/" in roll_2:
            if frame_counter > 1:
                if self.frames[frame_counter - 1] == "x":
                    roll_score += 10
                elif "/" in str(self.frames[frame_counter - 1]):
                    roll_score += int(roll_1)
            self.frames[frame_counter] = "{} /".format(roll_1)
            roll_score += 10

        else:
            if frame_counter > 1:
                if self.frames[frame_counter - 1] == "x":
                    roll_score += int(roll_1 + roll_2)
                elif "/" in str(self.frames[frame_counter - 1]):
                    roll_score += int(roll_1)
            self.frames[frame_counter] = str(roll_1 + roll_2)
            roll_score += int(roll_1 + roll_2)

        self.score += roll_score
        print("You have gotten a score of {}!".format(roll_score))
        next_turn()


def next_turn():
    global current_turn
    global current_turn_name

    for keys in players.keys():
        if players[keys].order == current_turn + 1:
            current_turn_name = keys
            break

    current_turn += 1

    update_screen()


def add_players(play_counter):
    global current_turn_name
    for i in range(play_counter):
        while True:
            name = input("What is the name for player {}?: ".format(i + 1))
            if re.search(name_pattern, name) is not None:
                break
            else:
                print("Please only use letters and no empty entries")
        players[name] = Bowler(name, i + 1)
        if i == 0:
            current_turn_name = name


def endgame():
    os.system('cls')
    winner = ""
    score = 0
    print("The game is over! Let's see who won...")
    time.sleep(2)

    for names in players.keys():
        print("\n{} has gotten a score of: {}".format(names, players[names].score))
        if players[names].score > score:
            winner = names
            score = players[names].score
        elif players[names].score == score:
            winner += (", " + names)
        time.sleep(1)

    final = winner.split(",")
    if len(final) > 1:
        print("\n\nThis game is tied between", end=": ")
        for i in final:
            print(i, end=" ")
        print("!!!")
    else:
        print("The winner is {} with a score of {}!!!".format(winner, score))

    time.sleep(1)

    print("\nThanks for playing! Come back another time")
    time.sleep(2)
    sys.exit()


def update_screen():
    global counter
    global frame_counter
    global current_turn

    end_frame = 75 - 6 * (10 - int(frame_max_counter))

    os.system('cls')

    print("Names     ", end='')
    for i in range(1, frame_max_counter + 1, 1):
        print(str(i) + " --- ", end='')
    print("score")

    if current_turn == 1:
        counter += 1

    template_score = "{0:" + str(int(end_frame) - 6 * counter) + "}"

    for names in players.keys():
        if players[names].order < current_turn:
            counter += 1
            template_score = "{0:" + str(int(end_frame) - 6 * counter) + "}"
            counter -= 1

        print(template_name.format(names), end='')
        for key, value in players[names].frames.items():
            print(template.format(value), end='')
        print(template_score.format(players[names].score))
        print("\n")
        template_score = "{0:" + str(int(end_frame) - 6 * counter) + "}"

    if current_turn - 1 >= player_counter:
        if frame_counter >= frame_max_counter:
            endgame()
        print("Next frame!")
        time.sleep(1)
        frame_counter += 1
        current_turn = 0
        next_turn()

    main_game()


def main_game():
    roll = input("It is now {}'s turn! What is your roll?: ".format(current_turn_name))
    players[current_turn_name].roll(roll)

    
def initialize_game():

    global frame_max_counter
    global player_counter
    global players

    try:
        while True:
            player_counter = int(input("How many players will there be? (1-6): "))
            if 1 <= player_counter <= 6:
                add_players(player_counter)
                break
            else:
                print("Please enter a value between 1 and 6")

        while True:
            frame_max_counter = int(input("How many frames will there be? (1-10): "))
            if 1 <= frame_max_counter <= 10:
                break
            else:
                print("Please enter a value between 1 and 10")

    except ValueError:
        print("Please only use numbers")
        players = {}
        initialize_game()

    print("Lets begin!")
    time.sleep(2)
    update_screen()


if __name__ == "__main__":
    initialize_game()
    main_game()