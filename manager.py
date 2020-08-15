import dicer


def greet():
    return "Привет"


def roll_a_dice(n):
    if n>0:
        return dicer.d(n)