import random

def todayMsg(accountName, wins, loses, points):
    emote = emotePoints(points)
    return (f'Dzisiaj {accountName} wygrał {wins}, przegrał {loses}, punkty {points:+} {emote}')


def yesterdayMsg(accountName, wins, loses, points):
    emote = emotePoints(points)
    return (f'Wczoraj {accountName} wygrał {wins}, przegrał {loses}, punkty {points:+} {emote}')


def pointsMsg(accountName, points):
    return (f'Punkty {accountName}: {points} peepoBlush')


def versusMsg(accountName, wins, loses, opponent):
    emote = emoteWins(wins, loses)
    return (f'{accountName} vs. {opponent}: wygranych {wins}, przegranych {loses} {emote}')


def updateAccountMsg(newActiveAccount, points, rating):
    return (f'Aktywne konto to teraz {newActiveAccount} - Punkty {points}, Top {rating} Hota AYAYASmile')

def onFailedAccountSwap(newActiveAccount):
    return (f'Nie udało się przełączyć konta na {newActiveAccount} AYAYAS Wielkość liter ma znaczenie! Wpisałeś poprawnie? peepoBlush')

def negativeEmote():
    negativeEmotes = ['classic', 'Pain', 'depresso',
                      'xddinside', 'xddWalk', 'PepeHands', 'AYAYAS']
    return random.choice(negativeEmotes)


def positiveEmote():
    positiveEmotes = ['leosiaKiss', 'fifka', 'leosiaJAM',
                      'pajac', 'AYAYASmile', 'WICKED', 'PagMan']
    return random.choice(positiveEmotes)


def neutralEmote():
    neutralEmotes = ['HUH', 'hmjj']
    return random.choice(neutralEmotes)


def emotePoints(points):
    if points > 0:
        return positiveEmote()
    elif points < 0:
        return negativeEmote()
    else:
        return neutralEmote()


def emoteWins(wins, loses):
    if wins > loses:
        return positiveEmote()
    elif loses > wins:
        return negativeEmote()
    else:
        return neutralEmote()
