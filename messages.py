import random
import datetime

def today_msg(account_name, wins, loses, points):
    emote = emote_points(points)
    return (f'Dzisiaj {account_name} {wins}-{loses} [{points:+}p.] {emote}')


def yesterday_msg(account_name, wins, loses, points):
    emote = emote_points(points)
    return (f'Wczoraj {account_name} {wins}-{loses} [{points:+}p.] {emote}')


def points_msg(account_name, points):
    return (f'Punkty {account_name}: {points} peepoBlush')


def versus_msg(account_name, wins, loses, points, opponent):
    emote = emote_wins(wins, loses)
    return (f'{account_name} vs. {opponent}: {wins}-{loses} [{points:+}p.] {emote}')


def update_account_msg(new_active_account, points, rating):
    return (f'Aktywne konto to teraz {new_active_account} - Punkty {points}, Top {rating} Hota AYAYASmile')


def on_failed_account_swap_msg(new_active_account):
    return (f'Nie udało się przełączyć konta na {new_active_account} AYAYAS Wielkość liter ma znaczenie! Wpisałeś poprawnie? peepoBlush')


def detailed_match_msg(enemy_name, wins, loses):
    return (f'{wins}-{loses} {enemy_name}, ')


def last_match_msg(match):
    wins = int(int(match.rating_change) > 0)
    loses = int(int(match.rating_change) < 0)
    enemy_name = match.enemy_name
    hour = match.end_date_time.hour
    minutes = match.end_date_time.minute

    return (f'Ostatni mecz zakończył się: {hour}:{minutes} {wins}-{loses} {enemy_name} {emote_wins(wins,loses)} ')

def negative_emote():
    negative_emotes = ['classic', 'Pain', 'depresso', 'Smadge', 'Weirdge','ApuApustaja', 
                      'xddinside', 'xddWalk', 'PepeHands', 'AYAYAS']
    return random.choice(negative_emotes)


def positive_emote():
    positive_emotes = ['leosiaKiss', 'fifka', 'leosiaJAM', 'AYAYAHYPER', 'AYAYABASS',
                      'pajac', 'AYAYASmile', 'WICKED', 'PagMan', 'AYAYALove']
    return random.choice(positive_emotes)


def neutral_emote():
    neutral_emotes = ['HUH', 'hmjj', 'AYAYAWeird', 'Stare']
    return random.choice(neutral_emotes)


def emote_points(points):
    if points > 0:
        return positive_emote()
    elif points < 0:
        return negative_emote()
    else:
        return neutral_emote()


def emote_wins(wins, loses):
    if wins > loses:
        return positive_emote()
    elif loses > wins:
        return negative_emote()
    else:
        return neutral_emote()
