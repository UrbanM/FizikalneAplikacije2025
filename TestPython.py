# Let's make a deal! - Google pravi, da je to aka Monty-Hallov problem:
# - imam trojna vrata,
# - izberem si recimo vrata 2,
# - Neodvisno od naše izbire, voditelj ofne vrata za katerimi VE, da je žival,
# - vpraša, če bi si mogoče izbral druga,
# - catch je, da maš v nasprotnem primeru (če rečeš "ja, premislil sem si") 2/3 šans, da dobiš nekej lepiga, če pa ne, pa 1/3.
# Špila? Špila.

import random
import numpy as np
import matplotlib.pyplot as plt

# En način kako izdelati program:

#----------------------ŠPIL-----------------------#
def monty_python():

    # grem po deske, da nareim vrata, ne?
    vrata = [1, 2, 3]
    chaChing = random.choice(vrata)

    #------pREVERIM---------#
    #print(f"{vrata}")
    #print(f"{chaChing}")

    # Tule definiramo input (konzola tokrat tudi nekaj pričakuje, ne samo da izpisuje.)
    while True:
        try:
            pizbira = int(input(f"\n Izbiraj med vrati {vrata}: "))
            if pizbira not in vrata:
                print("Izbrati je treba naravno število iz seznama ponujenih!")
            else:
                print(f"Super!")
                break
        except ValueError:
            bruh = [
                "*sigh* - Še enkrat ...",
                "Resno?",
                "si že mislu.",
                "Izberi PROSIM številko iz seznama.",
                "Anarchist!",
                "Hey! Im walkin 'ere!",
                "NUH-UH.",
                "Nice try, diddy!",
                "what the sigma?",
                "Boga-mi!"
            ]
            print(np.random.choice(bruh))

    # Voditelj odpre vrata za katerimi je žival (NE naših izbranih vrat) - otanejo dvojna vrata
    ost_vr_ž = [
        vr for vr in vrata
        if vr != pizbira and vr != chaChing
    ]
    Odpre = random.choice(ost_vr_ž)

    # Vpšraša nas, če bi si premislili
    alt_izb = [vr for vr in vrata if vr != pizbira and vr != Odpre][0]
    alt = input(f"Voditelj je odrpl vrata {Odpre}. Bi si premislili, in raje odprili {alt_izb}? (da / ne):").lower()
            
    # določi zadnjo izbiro
    F = alt_izb if alt == "da" else pizbira

    # rezultat
    if F == chaChing:
        print("Odlično! Dobili ste nagrado :D")
    else:
        živ = [
            "meketanje",
            "čričkanje",
            "mukanje",
            "lajanje",
            "mjavkanje",
            "rjovenje"
        ]
        print(f"*{np.random.choice(živ)} intensifies*. (Nagrada je bila za vrati {chaChing})")
#monty_python()

#--------------SIMULACIJA IN ANALIZA--------------#
# - če nas zanima, kako se "obnaša" verjetnost,
# naredimo več simulacij in narišemo razmerje zmag (porazov) v
# odvisnosti od števila iger približno tako (če ma sploh smisel to delat):

def sim_mh(št_ig):
    """Simulira montyHallovo igro, da je nam ni treba špilat"""
    ostr = []
    premr = []
    ostzm, premzm = 0, 0 # ostzm=zmage, kjer si ne premislim, premzm=zmage kjer si premislim

    for ig in range(1, št_ig + 1):
        nag = random.randint(1, 3) # 1, 2 ali 3
        pizb = random.randint(1, 3) # 1, 2 ali 3

        # Voditelj odpre vrata (prvič - vedno žival)
        vododp = random.choice([vr for vr in [1, 2, 3] if vr != pizb and vr != nag])
        premizb = [vr for vr in [1, 2, 3] if vr != pizb and vr != vododp][0] # 0 => prvič

        # števec zmag, če ostanemo pri prvi izbiri in števec zmag, če si premislimo
        if pizb == nag:
            ostzm += 1
        if premizb == nag:
            premzm += 1
        
        # za risanje si tukaj zapisujem zmage,
        # kot razmerje iger kjer ostanem (ali si premislim) z vsemi igrami
        ostr.append(ostzm / ig)
        premr.append(premzm / ig)

    if št_ig == 1:
        print(f"\nPo {št_ig} igri je stanje sledeče:")
    else:
        print(f"\nPo {št_ig} igrah je stanje sledeče:")
    print(f"Zmage, če si nismo premislili: {ostzm / št_ig:.2%}")
    print(f"Zmage, če smo si premislili: {premzm / št_ig:.2%}")

    return ostr, premr

def Grafi(ostr, premr):
    """Generira grafe razmerij zmag (gldede na to ali ostanem pri prvi izbiri
    ali si premislim) v odvisnosti od števila iger"""
    plt.figure(figsize=(10, 10))
    ig = range(1, len(ostr) + 1)

    # skupno ševilo zmag
    plt.plot(ig, ostr, label="Ostanem", color="red", alpha = 0.7)
    plt.plot(ig, premr, label="Premislim", color="green", alpha = 0.7)

    # Verjetnostna krivulja (zanima me, kaj dobim, če teoretično napoverm rezultat)
    plt.axhline(1/3, color="red", linestyle="--",
                label="Teortična napoved zmag, če ostanem pri prvi izbiri")
    plt.axhline(2/3, color="green", linestyle="--",
                label="Teoretična napoved zmag, če si premislim")

    plt.xlabel("Št skupnih iger")
    plt.ylabel("Razmerje zmag")
    plt.title(f"Razmerje zmag v dovisnosti od števila iger")
    plt.legend()
    plt.grid(True, alpha = 0.3)
    plt.show()

ostr, premr = sim_mh(1000)
Grafi(ostr, premr)
