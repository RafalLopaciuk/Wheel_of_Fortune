import random
from datetime import datetime
from .models import Player, Server, User


def zakrec_kolem(cant_death=False):
    if cant_death:
        kolo = [50, 100, 150, 200, 250, 300, 500, 700, 1000, 1200, 1500, 2000]
    else:
        kolo = [50, 100, 150, 200, 250, 300, 500, 700, 1000, 1200, 1500, 2000, "BANKRUT"]
    return kolo[random.randint(0, len(kolo)-1)]


def wylosuj_haslo():
    hasla = {
        "Informatyka": ["RAM", "Procesor", "Klawiatura"],
        "Natura": ["Drzewo", "Krzewy", "Rzeka"],
    }

    entry_list = list(hasla.items())
    random_entry = random.choice(entry_list)
    kategoria = random_entry[0]
    haslo = random.choice(random_entry[1])
    return kategoria, haslo


def game_starto(command, link):
    username = command.split(":\t")[0]
    message = command.split(":\t")[1]
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    server_message = current_time + "\t"
    new_round = False
    game_message = ""
    samogloski = ['A', 'Ą', 'E', 'Ę', 'I', 'O', 'U', 'Y']

    try:
        user = User.objects.get(username=username)
        player = Player.objects.get(user=user)
        user_game = player.active_game
        game = Server.objects.get(link_string=link)
        player_qs = Player.objects.all().filter(active_game=game)
    except:
        return "Gra została zakończona."

    if message == "":
        return None

    if user_game != game:
        return None

    if message.split(" ")[0].upper() == "CZAT":
        server_message += "--- Gracz " + username + " pisze: " + message[5:]
        return server_message

    if game.ended:
        return None

    if player_qs[game.actual_player_number].user != user:
        return None
    # print(game.started)
    # print(player_qs[game.actual_player_number].user == user)
    # print(game.actual_player_number)
    # print(player_qs[game.actual_player_number].user)
    # print(user)

    if game.started and player_qs[game.actual_player_number].user == user:
        opcja = message.split(" ")[0].upper()
        game_message = " "
        new_player = False
        if opcja == "KUP":
            message = message[4].upper()
            if message not in samogloski:
                server_message += "Kupić możesz tylko samogłoskę"
            else:
                server_message += "Brak środków do kupienia samogłoski"
        elif opcja == "ODGADUJE":
            message = message[9:].upper()
            if message == game.actual_word:
                game_message = "PODAŁEŚ POPRAWNE HASŁO!!"
                new_round = True
            else:
                game_message = "NIESTETY, to hasło jest niepoprawne."
                new_player = True
        else:
            # server_message += "NIC"
            message = message[0].upper()
            if message in samogloski:
                game_message = "Nie można podawać samogłosek"
                new_player = True
            elif message not in game.actual_word.upper() :
                game_message = "Nie ma takiej litery w haśle."
                new_player = True
            elif message in game.actual_word_progres.upper():
                game_message = "Podana litera już była."
                new_player = True
            else:
                count = 0
                word = list(game.actual_word)
                progress = list(game.actual_word_progres)
                for x in range(len(word)):
                    # print(word[x])
                    if message == word[x].upper():
                        count += 1
                        progress[x] = message
                wygrana = count * player.actual_coins
                player.actual_winning_coins += wygrana
                player.actual_coins = 0
                new_coins = zakrec_kolem()
                if new_coins == "BANKRUT":
                    player.actual_coins = 0
                    new_player = True
                    game_message += "Tura gracza - " + str(player_qs[game.actual_player_number].user.username) + \
                                    " - NIESTETY BANKRUTUJESZ!\n\t\t"
                else:
                    player.actual_coins = new_coins
                player.save()
                # print(" ".join(progress))
                game.actual_word_progres = "".join(progress)
                game.save()
                game_message += "HASŁO: " + " ".join(game.actual_word_progres) + "\n\t\t"
                game_message += "POPRAWNA litera x" + str(count) + ", wygrana: " + str(wygrana)

            while new_player:
                lim = (game.actual_player_number + 1) % game.count_players
                game.actual_player_number = lim
                value = zakrec_kolem(True)
                if value == "BANKRUT":
                    game_message = "Tura gracza - " + str(player_qs[game.actual_player_number].user.username) + \
                                    " - NIESTETY BANKRUTUJESZ!\n\t\t" + game_message
                else:
                    try:
                        player = Player.objects.get(user=player_qs[game.actual_player_number].user)
                        player.actual_coins = value
                        player.save()
                        new_player = False
                    except:
                        pass

            server_message += "Tura gracza - " + str(player_qs[game.actual_player_number].user.username) + \
                              " - grasz o " + str(player_qs[game.actual_player_number].actual_coins) + " coinów\n\t\t"

    if (game.user_create == user and not game.started and message.split(" ")[0].upper() == "START") or new_round:
        if new_round:
            game.actual_round += 1
            try:
                player = Player.objects.get(user=player_qs[game.actual_player_number].user)
                player.actual_winning_coins = player.actual_coins
                player.actual_coins = 0
                player.save()
            except:
                pass
            if game.actual_round >= game.max_rounds:
                game.ended = True
                game.save()
                return server_message + "WYGRYWA " + player.user.username + "\n\t\tKONIEC GRY"

        kategoria, haslo = wylosuj_haslo()
        game.started = True
        game.actual_round = 1
        game.actual_word = haslo.upper()
        game.actual_word_hint = kategoria
        game.actual_word_progres = "_" * len(haslo)
        game_message = " "
        if not new_round:
            game.actual_player_number = 0

        value = zakrec_kolem(True)
        # print(value)
        try:
            player = Player.objects.get(user=player_qs[game.actual_player_number].user)
            player.actual_coins = value
            player.save()
        except:
            pass
        player_qs[0].actual_coins = value
        player_qs[0].save()
        game.save()
        # print(str(game.actual_word_progres))

        server_message += "Tura gracza - " + str(player_qs[game.actual_player_number].user.username) + \
                          " - grasz o " + str(player_qs[game.actual_player_number].actual_coins) + " coinów\n\t\t"
        server_message += "HASŁO: " + game.actual_word_progres.replace("", " ") + "\n\t\t"
        server_message += "KATEGORIA: " + game.actual_word_hint + "\n\t\t"
        server_message += "RUNDA " + str(game.actual_round) + "\n\t\t"
        if not new_round:
            server_message += "START GRY!"
        else:
            new_round = False
        game.start_send_count += 1
        game.save()
    if len(server_message) < 5:
        return None
    return server_message + game_message
    # print(user_game)
    # print(game)
    # print(game.user_create)
    # print(user)
    # print(game.user_create == user)
    # print(game.activate)
    # print(message.split(" ")[0].upper() == "START")
    # return None
