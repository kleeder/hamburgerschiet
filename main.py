import random
import time


def check_if_sublist(list, sublist):
    if len(list) < len(sublist):
        return False
    if "".join([str(x) for x in list]).find("".join([str(x) for x in sublist])) > -1:
        return True
    return False


class Player:
    def __init__(self, name):
        self.score = 0
        self.temp_points = 0
        self.name = name


class Game:
    def __init__(self, player_amount):
        self.player_amount = player_amount
        self.players = []
        for i in range(player_amount):
            self.players.append(Player(i + 1))
        self.win_score = 10000
        self.min_score = 300
        self.dice_amount = 6
        self.win_score_reached = False
        self.rolled_street = [
            ("111111", [1, 2, 3, 4, 5, 6], 1000)
        ]
        self.rolled_options = [
            (5, "000010", [5], 50),
            (5, "000020", [5, 5], 100),
            (5, "000030", [5, 5, 5], 500),
            (5, "000040", [5, 5, 5, 5], 550),
            (5, "000050", [5, 5, 5, 5, 5], 600),
            (5, "000060", [5, 5, 5, 5, 5, 5], 5000),

            (1, "100000", [1], 100),
            (1, "200000", [1, 1], 200),
            (1, "300000", [1, 1, 1], 1000),
            (1, "400000", [1, 1, 1, 1], 1100),
            (1, "500000", [1, 1, 1, 1, 1], 1200),
            (1, "600000", [1, 1, 1, 1, 1, 1], 10000),

            (2, "030000", [2, 2, 2], 200),
            (2, "060000", [2, 2, 2, 2, 2, 2], 2000),

            (3, "003000", [3, 3, 3], 300),
            (3, "006000", [3, 3, 3, 3, 3, 3], 3000),

            (4, "000300", [4, 4, 4], 400),
            (4, "000600", [4, 4, 4, 4, 4, 4], 4000),

            (6, "000003", [6, 6, 6], 600),
            (6, "000006", [6, 6, 6, 6, 6, 6], 6000),
        ]

    def validate_roll_dice(self, dice_result):
        dice_res = f"{dice_result.count(1)}{dice_result.count(2)}{dice_result.count(3)}{dice_result.count(4)}{dice_result.count(5)}{dice_result.count(6)}"
        if dice_res == "111111":
            return ["111111"]

        options = []
        for option in self.rolled_options:
            if check_if_sublist(dice_result, option[2]):
                options.append(option)

        dice_select_options = set()
        for i in range(1, 7):
            for option in options:
                if option[0] == i:
                    dice_select_options.add(option[1])
                    for other_option in options:
                        if other_option[0] != i:
                            dice_select_options.add(str(int(option[1]) + int(other_option[1])).zfill(6))
                            for third_option in options:
                                if third_option[0] != other_option[0] and third_option[0] != i:
                                    dice_select_options.add(
                                        str(int(option[1]) + int(other_option[1]) + int(third_option[1])).zfill(6))

        all_options = []
        for select_option in dice_select_options:
            dice_count = str(select_option).zfill(6)
            dice_total = sum([int(i) for i in dice_count])
            if dice_total == 6:
                return [dice_count]
            all_options.append(dice_count)

        return all_options

    def convert_to_dice_list_and_sum(self, dice_res):
        dice_list = []
        dice_sum = 0
        dice_list.extend([1] * int(dice_res[0]))
        dice_list.extend([2] * int(dice_res[1]))
        dice_list.extend([3] * int(dice_res[2]))
        dice_list.extend([4] * int(dice_res[3]))
        dice_list.extend([5] * int(dice_res[4]))
        dice_list.extend([6] * int(dice_res[5]))

        if dice_res != "111111":
            for i in range(0, 6):
                if dice_res[i] != "0":
                    for option in self.rolled_options:
                        if option[1][i] == dice_res[i]:
                            dice_sum += option[3]
            return dice_list, dice_sum
        return dice_list, 1000

    def roll_dice(self):
        dice_result = []
        for _ in range(self.dice_amount):
            dice_result.append(random.randint(1, 6))
        return dice_result


wrong_input = True
while wrong_input:
    y = input("How many players?\n")
    try:
        y_num = int(y)
        if 1 < y_num <= 6:
            wrong_input = False
        else:
            print("Not a valid input. Choose Players between 2 and 6")
    except ValueError:
        print("Not a valid input. Choose Players between 2 and 6")


game = Game(y_num)

print(f"Game started with {game.player_amount} players.")
time.sleep(1)
round_amount = 0
while not game.win_score_reached:
    round_amount += 1
    print(f"Start of Round {round_amount}")
    time.sleep(1)
    for player in game.players:
        print(f"Turn for player {player.name}. Your current total points are {player.score}")
        round_active = True
        while round_active:
            input("Press any key to roll dice")
            dice_roll = game.roll_dice()
            print(f"You rolled: {dice_roll}")
            time.sleep(1)
            print("Your options:")
            point_options = game.validate_roll_dice(sorted(dice_roll))
            total_option = 0
            if len(point_options) > 0:
                for i, point_option in enumerate(point_options):
                    point_option_list, point_option_sum = game.convert_to_dice_list_and_sum(point_option)
                    print(f"Option {i} :: {point_option_list} -> {point_option_sum} Points")
                    total_option = i
                wrong_input = True
                while wrong_input:
                    x = input("Please input which option you choose:\n")
                    try:
                        x_num = int(x)
                        if 0 <= x_num <= total_option:
                            wrong_input = False
                        else:
                            print("Not a valid input.")
                    except ValueError:
                        print("Not a valid input.")
                dice_list, dice_sum = game.convert_to_dice_list_and_sum(point_options[x_num])
                print(f"You chose option {x}. {dice_sum} Points will be added to your current balance.")
                player.temp_points += dice_sum
                game.dice_amount -= len(dice_list)
                if game.dice_amount == 0:
                    game.dice_amount = 6
                print(f"You now have {player.temp_points} Points for this round.")
                time.sleep(1)
                if player.temp_points < game.min_score:
                    print(f"You don't have {game.min_score} points yet. Round will continue.")
                elif player.temp_points >= game.min_score and game.dice_amount == 6:
                    print("Continuing game with 6 dices.")
                else:
                    wrong_input = True
                    while wrong_input:
                        x = input(f"Do you wanna continue with {game.dice_amount} dices? Y/N\n")
                        if x.lower() == "n":
                            print(
                                f"A total of {player.temp_points} points was added to your total {player.score} points.")
                            player.score += player.temp_points
                            player.temp_points = 0
                            game.dice_amount = 6
                            if player.score >= game.win_score:
                                print(
                                    f"The winning score of {game.win_score} points was reached. Remaining players will finish their round before winner is confirmed.")
                                game.win_score_reached = True
                            round_active = False
                            wrong_input = False
                        elif x.lower() == "y":
                            wrong_input = False
                        else:
                            print("Not a valid input.")
            else:
                print("No options available. You lose all your points for this round.")
                player.temp_points = 0
                game.dice_amount = 6
                round_active = False
                wrong_input = False

print("We have reached the end of the game!")

winners = {}
for player in game.players:
    winners.update(
        {
            player.name: player.score
        }
    )
highscores = dict(sorted(winners.items(), key=lambda item: item[1], reverse=True))
rank = 0
for k, v in highscores.items():
    rank += 1
    print(f"RANK {rank}: Player {k} - {v} Points")
