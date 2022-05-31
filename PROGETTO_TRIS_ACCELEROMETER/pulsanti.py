from microbit import *

while True:
    button= ""
    if button_a.is_pressed():
        button += "ATRUE"
    else:
        button = "AFALSE"
    if button_b.is_pressed():
        button_b = " BTRUE"
    else:
        button_b = " BFALSE"
    print(button_a, button_b)
    sleep(100)