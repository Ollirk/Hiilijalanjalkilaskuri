# TIE-02101 Johdatus ohjelmointiin


"""Graafinen käyttöliittymä projekti
Olli Kivioja, 284459, olli.r.kivioja@tuni.fi
Päivän ruokailujen hiilijalanjälkilaskuri.

Työllä tavoitellaan "skaalautuvaa projektia"
Skaalaus näkyy esimerkiksi. Kuvien määrittelyssä, jotka on listassa määritelty.
Painikkeiden lisäämisessä sekä pääikkunaan sekä aukeavaan uuteen ikkunaan.
Uudessa ikkunassa Entry ikkunoiden lisäys ja niihin liittyvien tekstien lisäys
tietokannan tietojen avulla.

Keskimääräisen suomalaisen ruoan päivittäinen hiilijalanjälki,
jonka alle pyritään on 5 kgCO2e/päivä (1800kgCO2e/vuosi jaettuna 365 päivälle)
Lukemat on saatu SITRAN artikkelista "Keskivertosuomalaisen hiilijalanjälki"
https://www.sitra.fi/artikkelit/keskivertosuomalaisen-hiilijalanjalki/

Käyttäjä asettaa ohjelmaan päivien ruoka-annostensa määriä grammoina.
Ohjelma laskee päivön hiilijalanjäljen ja aktivoi sivussa olevia kuvia harmaasta
kirkkaaksi sen mukaan. Mikäli tavoite 5kgCO2/päivä ylittyy, aktvioituu
viimeinen punainen jalka ylittämisen merkiksi.

Ohjelma vaatii tuekseen liitteenä olevat tiedostot:
kuvat: "CO1.gif", "CO2.gif", "CO3.gif", "CO4.gif", "CO5.gif", "COX.gif"
tietokanta: ruokalajit.txt"

Ohjelmaa on yksinkertaista testata avaamalla ateriavalikot ja lisäämällä
esimerkiksi viiniä 400g joka aterialle (400g = 1kgCO2)niin huomaa kuinka
jalanjäljet lisääntyvät pääikkunassa yksi kerrallaan.
Samaan ateriaan voi lisätä myös saman ruokalajin useaan kertaan.
Laskennan voi nollata "Nollaa" painikkeella.

"""
from tkinter import *
#Alustetaan kuvat ja päivän ateriat ohjelmaan
COALPRINTS = [ "CO1.gif", "CO2.gif", "CO3.gif", "CO4.gif", "CO5.gif", "COX.gif" ]
MEALS = ["Aamupala", "Lounas", "Päivällinen", "Iltapala"]
TAVOITECOKULUTUS = 5


def lue_tietokanta():
    """
    Ohjelma lukee aluksi ohjelman tukena olevan tietokannan ruokalajien
    hiilijalan jäljistä, jotka on talletettu tekstimuotoon.

    Tulevaisuudessa tietokantaan voisi lisätä viivakooditunnukset, kun yksit-
    täisillä tuotteille julkistetaan hiilijalanjäljet.
    Tällä hetkellä hiilijalan jäljet on merkitty ruokalajeittain sataa grammaa
    kohti.
    esim. Viini;0.25kgCO2e/100g

    Ohjelma palauttaa tietokannan pyhtonin dict muodossa avaimina ruokalajien
    nimet ja arvoina hiilijalanjäljet sadalle grammalle esim. Viini:0.25

    """
    file = open ("ruokalajit.txt", "r")
    kirjasto = {}
    for line in file:
        line = line.rstrip()
        tiedot = line.split(";") #Alkiossa 0 ruoan nimi ja alkiossa 1 CO2kg/100g
        ruokalaji = tiedot[0]
        COjälki = tiedot[1]
        kirjasto[ruokalaji] = COjälki

    return kirjasto


class Hiililaskuri:
    #Graafinen käyttöliittymä hiilijalanjälkilaskuriin


    def __init__(self):
        #Alustetaan laskurin perusikkuna otsikolla
        self.__window = Tk()
        self.__window.title("Hiilijalanjälki laskuri")
        self.__kulutus = 0 #Käyttäjän hiilijalanjälki jota seurataan

        # Alustetaan päävalikko
        self.__aloitusteksti = Label (self.__window,
                                      text="Lasketaan päivän annoksien hiilijalan"
                                           "jälki ja tavoitellaan suomalaisen keskiarvoista"
                                           "lukemaa 5 kgCO2e. \n"
                                           "Avaa valikot ruokalajien lisäämistä varten")
        self.__aloitusteksti.grid (row=1, column=1)
        self.__lopeta_button = Button(self.__window, text="Lopeta",
                                       command=self.lopeta, background="white")
        self.__lopeta_button.grid(row=8,column=0)

        self.__nollaus = Button(self.__window, text="Nollaa", command=self.nollaa_laskin)
        self.__nollaus.grid(row=7,column=0)

        #Alustetaan kuvat ikkunaan vektoriin, jotta niihin voidaan myöhemmin viitata
        self.__footprints = []
        for picfile in COALPRINTS:
            pic = PhotoImage(file=picfile)
            self.__footprints.append(pic)

        #Lisätään kaikki kulutuskuvat oikeaan reunaan DISABLED tilassa
        self.__kuvat = [] #lisätään kuvat listaat niiden yksittäistä konfigurointia varten
        for i in range(len(COALPRINTS)):
            self.__kuva = Label(self.__window, image=self.__footprints[i], state=DISABLED)
            self.__kuvat.append(self.__kuva)
            self.__kuva.grid (row=1+i, column=4,sticky=S)

        #Lisätään annosvalintapainikkeet, jotka kaikki avaavat saman uuden ikkunan
        for i in range(len(MEALS)):
            self.__annosvalinta = Button(self.__window,
                                       text=MEALS[i], command=self.annosikkuna)
            self.__annosvalinta.grid (row=2+i, column=1)


    def start(self): #Kutsuttaessa käynnistetään ikkuna
        self.__window.mainloop()


    def lopeta(self): #kutsuttaessa lopetetaan ohjelma
        self.__window.destroy()


    def nollaa_laskin(self):
        #Aloitetaan laskenta alusta, joten nollataan arvot ja päivitetään kuvat
        self.__kulutus = 0
        self.__CO2_jäljet = int(0)
        self.päivitä_kuvat()

    def virheilmoitus(self):
        #Ilmoitetaan virheestä syöteikkunoiden yläpuolella virheestä
        #esimerkiksi kirjaimista.
        self.__ohje1.configure(text="Virheellinen syöte!")


    def lue_entryt(self):
        #Luetaan ruokalajien lukumäärät ja kasvatetaan hiilijalanjälkeä
        #sanakirjasta löytyvän hiilijalanjälkipitoisuuden avulla

        self.__CO2_jäljet = 0
        aterian_jälki = []
        #Oletetaan,että syöte on yrityskerralla oikein ennen testausta
        self.__ohje1.configure (text="Anna lukumäärä grammoissa")
        try:
            for i in range(len(self.__syötteet)):
                co2 = float(self.__syötteet[i].get()) #Haetaan entryjen tiedot
                kgco2_kerroin = float(self.__kgCO2jäljet[i]) #Haetaan ruokien jäljet
                ruokalajin_jälki = co2 * kgco2_kerroin/100
                aterian_jälki.append(int(ruokalajin_jälki))
                #alustetaan syöteikkunatvektorissa takaisin nolliksi
                self.__syötteet[i].delete(0,END)
                self.__syötteet[i].insert(0,0)
        except: #Mikäli syöte on virheellinen laskentaa varten tehdään ilmoitus
            self.virheilmoitus()

        self.__CO2_jäljet += int(sum(aterian_jälki))
        self.__kulutus += self.__CO2_jäljet
        self.päivitä_kuvat()


    def päivitä_kuvat(self):
        #Aktivoidaan kuvia hiilijalanjäljistä riippuen käyttäjän kulutuksesta

        # Nollaus toiminnon vuoksi varmistetaan että kaikki on aluksi disabled tilassa
        for i in range(len(COALPRINTS)):
            self.__kuvat[i].configure(state=DISABLED)

        #Aktivoidaan niin monta kuvaa kuin kulutus osoittaa
        for i in range(self.__kulutus):
            # jos maximisuositus ylittää asteikon, configuroi vain punaiseen asti
            if i >= len(self.__kuvat):
                break
            else:
                self.__kuvat[i].configure(state=NORMAL)


    def annosikkuna(self):
        #Uusi ikkuna joka aukeaa annospainikkeista

        tietokanta = lue_tietokanta()
        self.__ruokalajit = [] #Ruokalajien nimet tietokannasta
        self.__kgCO2jäljet= [] #Ruokalajien COjäljet tietokannasta
        self.__syötteet = [] #Käyttäjän sijoittamat syötteet

        #Lisätään tiedot sanakirjasta listaan ikkunan auetessa
        for ruokalaji in tietokanta:
            self.__ruokalajit.append(ruokalaji)
            self.__kgCO2jäljet.append(tietokanta[ruokalaji])

        #Luodaan uusi ikkuna ja sijoitellaan pääobjektit
        annosikkuna = Toplevel(self.__window)

        self.__ohje1 = Label(annosikkuna, text="Anna lukumäärä grammoissa")
        self.__ohje1.grid(row=0,column=2)

        self.__ohje2 = Label(annosikkuna, text="kgCO2e/100g pitoisuus")
        self.__ohje2.grid(row=0, column=4)



        self.__laske = Button (annosikkuna, text="LASKE", command=self.lue_entryt)
        self.__laske.grid (row=0, column=1)

        #Sijoitellaan tietokannan tiedot, sekä entrylabelit ikkunaan
        #ja alustetaan entryjen arvot
        for i in range(len(self.__ruokalajit)):
            self.__ruoka = Label(annosikkuna, text=self.__ruokalajit[i])
            self.__ruoka.grid(row=1+i, column=0)

            self.__annosikkuna = Entry(annosikkuna)
            self.__annosikkuna.grid(row=1+i, column=2, sticky=E)
            self.__annosikkuna.delete(0,END) #Tietojen tyhjennys
            self.__annosikkuna.insert(0, 0)#Arvojen asettaminen nollaan
            self.__syötteet.append(self.__annosikkuna)

            self.__yksikkö = Label(annosikkuna, text="g")
            self.__yksikkö.grid(row=1+i, column=3, sticky=W)

            yksikkö_i = self.__kgCO2jäljet[i]+" kgCO2e/100g"
            self.__COjalki = Label(annosikkuna, text=yksikkö_i)
            self.__COjalki.grid(row=1+i, column=4, sticky=W)


def main():
    ui = Hiililaskuri()
    ui.start()


main()

