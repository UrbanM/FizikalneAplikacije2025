import random

def monty_hall_igra():
    print("Dobrodošeli v Monty Hall igri!")

    nagrada = random.choice([1, 2, 3])
    izbira = int(input("Izberi vrata (1, 2 ali 3): "))

    moznosti = [1, 2, 3]
    moznosti.remove(izbira)
    if nagrada in moznosti:
        moznosti.remove(nagrada)
    vrata_za_odpreti = random.choice(moznosti)

    print(f"Voditelj odpre vrata {vrata_za_odpreti}, za njimi ni nagrade.")
    sprememba = input("Ali želite zamenjati izbiro? (da/ne): ")

    if sprememba.lower() == "da":
        preostala = [vrata for vrata in [1, 2, 3] if vrata != izbira and vrata != vrata_za_odpreti]
        izbira = preostala[0]

    if izbira == nagrada:
        print("Čestitam, zadel si nagrado")
    else:
        print("Ups, nisi zadel.")
    print(f"Nagrada je bila za vrati {nagrada}.")

monty_hall_igra()
