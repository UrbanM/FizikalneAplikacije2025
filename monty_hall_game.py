import numpy as np
import matplotlib.pyplot as plt
import random

def monty_hall():
    # Imamo 3 vrata: 1, 2 in 3
    print("Pozdravljeni v igri Monty Hall!")
    print("Za enim od 3 vrat je nagrada. Poskusite jo najti.")

    # Nagrada je naključno postavljena za ena vrata
    nagrada = random.randint(1, 3)

    # Tekmovalec izbere vrata
    print("Izberi ena vrata: 1, 2 ali 3.")
    izbira = int(input("Tvoja izbira: "))

    # Voditelj mora odpreti vrata, ki:
    # niso tista, ki jih je izbral tekmovalec
    # in za njimi ni nagrade

    # Preverimo katera vrata lahko odpre
    if izbira != 1 and nagrada != 1:
        vrata_za_odpreti = 1
    elif izbira != 2 and nagrada != 2:
        vrata_za_odpreti = 2
    else:
        vrata_za_odpreti = 3

    print("Voditelj odpre vrata številka", vrata_za_odpreti, "in za njimi ni nagrade.")

    # Tekmovalca vprašamo, ali želi zamenjati izbiro
    print("Ali želiš zamenjati izbiro na druga še zaprta vrata?")
    odgovor = input("Vpiši 'da' ali 'ne': ")

    if odgovor == "da":
        # Zamenjamo na edina še zaprta vrata
        if izbira != 1 and vrata_za_odpreti != 1:
            izbira = 1
        elif izbira != 2 and vrata_za_odpreti != 2:
            izbira = 2
        else:
            izbira = 3

    # Preverimo, ali je tekmovalec zmagal
    if izbira == nagrada:
        print("Čestitke! Zadel si nagrado!")
    else:
        print("Žal, nisi zadel nagrade.")

    print("Nagrada je bila za vrati številka", nagrada)

# Zagon igre
monty_hall()
