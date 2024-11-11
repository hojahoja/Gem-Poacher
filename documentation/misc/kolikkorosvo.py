# Original code of the Mooc submission. This is here only for reference
# and to inform the course teachers.
# The proper version of this game will be rewritten from scratch in English
# following along the timetable and instructions of the course.

import pygame
import os
from sys import exit
import sys
from random import randint, choice


#Yleinen Olio luokka joka toimii pohjana pelin Robotti. Mörkö ja Kolikko luokille
#Leveys ja korkeus ovat olion omia pituuksia ja sijainnit sijainti näytöllä pikselien mukaan.
class Olio:
    def __init__(self, leveys = 1, korkeus = 1, x_sijainti = 0, y_sijainti = 0):
        self.__x = x_sijainti
        self.__y = y_sijainti
        self.__leveys = leveys
        self.__korkeus = korkeus
    
    @property
    def x(self):
        return self.__x
    
    @x.setter
    def x(self, x: int):
        self.__x = x
        
    @property
    def y(self):
        return self.__y
    
    @y.setter
    def y(self, y: int):
        self.__y = y
        
    @property
    def leveys(self):
        return self.__leveys

    @property
    def korkeus(self):
        return self.__korkeus
    
    #annetaan sijainti suoraan tuplena
    @property
    def sijainti(self):
        return (self.__x, self.__y)

#Robotti perii luokan Olio. sen leveys ja korkeus on kovakoodattu robo.png:n perusteella.
#Robotti luokka pitää tallella pelaajan elämät ja sen onko se vahinkoa saavassa tilassa.
class Robotti(Olio):
    
    def __init__(self, leveys=1, korkeus=1, x_sijainti=0, y_sijainti=0, elamia = 9):
        super().__init__(50, 86, x_sijainti, y_sijainti)
        self.__elamia = elamia
        self.__saa_vahinkoa = True
        
    @property
    def elamia(self):
        return self.__elamia
    
    @elamia.setter
    def elamia(self, muutos: int):
        if self.__elamia + muutos <= 0:
            self.__elamia = 0
        else:
            self.__elamia += muutos
    
    @property
    def saa_vahinkoa(self):
        return self.__saa_vahinkoa
    
    #Robotille annetaan true kun sen halutaan ottavan vahinkoa ja false kun se ei saa vahinkoa.
    @saa_vahinkoa.setter
    def saa_vahinkoa(self, vahinkoaltis: bool):
        if isinstance(vahinkoaltis, bool):
            self.__saa_vahinkoa = vahinkoaltis
        else:
            raise TypeError(f"{repr(vahinkoaltis)} is not an instance of bool")
            
#Perii luokan olio. Morolla on x ja y suunta. Suunta käsittelee sekä Mörön nopeutta että suuntaa pelitilassa.
#Suunnan koko päättää nopeuden ja positiivisuus suunnan.
class Morko(Olio):
    
    def __init__(self, leveys=1, korkeus=1, x_sijainti=0, y_sijainti=0, x_suunta = 1, y_suunta = 1):
        super().__init__(50, 70, x_sijainti, y_sijainti)
        self.__x_suunta = x_suunta
        self.__y_suunta = y_suunta
        
    @property
    def x_suunta(self):
        return self.__x_suunta
    
    @x_suunta.setter
    def x_suunta(self, suunta: int):
        if isinstance(suunta, int):
            self.__x_suunta = suunta
        else:
            raise TypeError(suunta)

    @property
    def y_suunta(self):
        return self.__y_suunta
    
    @y_suunta.setter
    def y_suunta(self, suunta: int):
        if isinstance(suunta, int):
            self.__y_suunta = suunta
        else:
            raise TypeError(f"{repr(suunta)} is not an instance of int")

#Kolikolla ei ole muuta Olio luokasta poikkeavaa kuin kovakoodattu leveys ja korkeus
class Kolikko(Olio):
    
    def __init__(self, leveys=1, korkeus=1, x_sijainti=0, y_sijainti=0):
        super().__init__(40, 40, x_sijainti, y_sijainti)

#Pelin tilan tiedot on talletettu oliohin tai Kolikkorosvo luokkaan. Pelilogiikka vain käsittelee näitä tietoja. Se ei pidä niistä kirjaa
#Peli käsittelee olioiden itsenäistä liikkumista törmäyksiä ja pelin tilaa.
class Pelilogiikka:
    
    #leveys ja korkeus ovat peliruudun leveys ja korkeus vahinkokäsittelyaika liittyy ohjattavaan hahmoon
    def __init__(self, leveys: int, korkeus: int) -> None:
        self.__leveys = leveys
        self.__korkeus = korkeus
        self.__vahinkokasittelyaika = 0
    
    #tarkistaa onko annettu olio pelialueen sisällä
    def seinien_sisalla(self, olio: Olio, siirto_x = 0, siirto_y = 0):        
        sisalla = True
        
        if olio.x + siirto_x > self.__leveys - olio.leveys or olio.x + siirto_x < 0:
            sisalla = False
        if olio.y + siirto_y > self.__korkeus - olio.korkeus or olio.y + siirto_y < 0:
            sisalla = False            
        return sisalla
    
    #Tarkistaa osuuko pelihahmo(robotti) kolikkoon. Jos osuu poistetaan kolikko pelistä ja lisätään peliin piste
    def tormayksen_kasittely_kolikoille(self, botti: Robotti, pisteet: list, kolikot: list):        
        poistettavat = [kolikko for kolikko in kolikot if self.tormays(botti, kolikko)]
        for poistettava in poistettavat:
            kolikot.remove(poistettava)
            pisteet[0] += 1
    
    #Tarkistaa osuuko pelihahmo mörköön. Osuessaan funktio aloittaa vahinkokäsittelyn robotille
    def tormayksen_kasittely_moroille(self, botti: Robotti, morot: list):
        for morko in morot:
            if self.tormays(botti, morko) and botti.saa_vahinkoa:
                self.vahingoittamattomuuden_kasittely_botille(botti, True)
    
    #Tarkistaa onko kaikki tason kolikot kerätty        
    def taso_lapi(self, kolikot: list, taso: list):
        if len(kolikot) == 0:
            taso[0] += 1
            return True
        return False

    #Tarkistaa törmäävätkö kaksi oliota toisiinsa vertaamalla niiden "vahinkolaatikoita" eli osuuko tietty neliön pinta ala toisen sisälle
    def tormays(self, olio1: Olio, olio2: Olio):
        if(olio1.x < olio2.x + olio2.leveys and
           olio1.x + olio1.leveys > olio2.x and
           olio1.y < olio2.y + olio2.korkeus and
           olio1.y + olio1.korkeus > olio2.y):
            return True
        else:
            False
    
    #liikuttaa jokaista mörköä
    def liikuta_kaikkia_morkoja(self, morot: list):
        for morko in morot:
            self.__liikuta_morkoa(morko)
    
    #liikuttaa yhtä mörköä jos mörkö osuu seinään se vaihtaa suuntaa muuttamalla mörön suunta_muuttujien arvojen positiivisuutta.
    def __liikuta_morkoa(self, morko: Morko):
        if not self.seinien_sisalla(morko, siirto_x = morko.x_suunta):
            morko.x_suunta = -morko.x_suunta
        if not self.seinien_sisalla(morko, siirto_y = morko.y_suunta):
            morko.y_suunta = -morko.y_suunta
        
        morko.x += morko.x_suunta
        morko.y += morko.y_suunta
    
    #metodille annetaan sai_osuman arvoksi True jos halutaan aloittaa robotin vahinkokäsittely. Kun robotti saa osuman sei ei pysty hetkeen ottamaan vahinkoa
    #kun Pelilogiikan vahinkokäsittelyaika palaa takaisin 0:aan. Robotin tila muutetaan, niin että se pystyy taas ottamaan vahinkoa.
    #Kun metodia kutsutaan ilman sai_osuman arvoa True. metodi vain vähentää vahinkokäsittelyaikaa joka kerta kuin se kutsutaan.
    def vahingoittamattomuuden_kasittely_botille(self, botti, sai_osuman = False):
        if sai_osuman:
            botti.elamia = -1
            botti.saa_vahinkoa = False
            self.__vahinkokasittelyaika = 100
            
        if self.__vahinkokasittelyaika > 0:
            self.__vahinkokasittelyaika -= 1
        else:
            botti.saa_vahinkoa = True
        
# Pelin pääluokka. Käynnistää pelin ja pyörittää pelisilmukkaa. Sisältää pelin tilan tiedot ja piirtää pelin näytölle.
class Kolikkorosvo:
    def __init__(self):
        
        self.alusta_peli()
        self.peli_paalla = True     
        self.pelaa()
    
    #Alustaa kaikki pelin tarvittavat osat ja tiedot
    def alusta_peli(self):
        pygame.init()
        pygame.mouse.set_visible(False)
        
        self.leveys, self.korkeus = 1280, 720
        self.naytto = pygame.display.set_mode((self.leveys, self.korkeus))
        self.kuvat = self.lataa_kuvat()
        self.kello = pygame.time.Clock()
        self.logiikka = Pelilogiikka(self.leveys, self.korkeus)
        self.tekstit = self.luo_tekstit()
        self.pisteet = [0]
        self.taso = [1]
        self.botti = Robotti()
        self.oliot =  {"hirvio": [], "kolikko": []}
        self.vaikeustaso = {"helppo" : [1,-1], "perus" : [2,-2], "haastava" : [3,-3]}        
        self.luo_seuraava_taso()
                
        pygame.display.set_caption("Kolikkorosvo")
    
    #luo pelin tarvittavat fonttioliot. Osa render kommenoista suoritetaan vasta piirtovaiheessa, koska ne muuttuvat pelin aikana.
    def luo_tekstit(self):
        elamia = pygame.font.SysFont("Arial", 24)
        pisteet = pygame.font.SysFont("Arial", 24)
        taso = pygame.font.SysFont("Arial", 24)
        peli_ohi = pygame.font.SysFont("Arial", 72).render("Peli on Päättynyt", True, (255, 0, 0))
        napit = pygame.font.SysFont("Arial", 34).render("F1 = Uusi peli, Esc = Sammuta", True, (255, 0, 0))
        return {"pisteet": pisteet, "taso": taso, "elamat": elamia, "peli_ohi": peli_ohi, "napit": napit}
    
    # Luo aina seuraavan tason pelille ja nostaa vaikeusastetta pelin self.vaikeustaso listojen mukaan.
    # vaikeustaso kasvaa mörköjen nopeuden ja määrän avulla.
    # tasolla 6+ vaikeustason kasvu on vakio
    # Pelilogiikka luokka huolehtii siitä milloin uusi taso pitää luoda.
    def luo_seuraava_taso(self):
        if self.taso[0] == 1:
            self.lisaa_morko(3)
            self.lisaa_kolikko(5)
        elif 2 <= self.taso[0] <= 5:
            self.lisaa_morko(1, "perus")
            self.lisaa_kolikko(4 + self.taso[0])
        elif 6 <= self.taso[0]:
            self.lisaa_morko(1, "haastava")
            self.lisaa_kolikko(4 + self.taso[0])
      
    #lisää yhden tai annetun määrän mörköjä. Vaikeustaso kuvastaa mörön nopeutta. 
    # self.vaikeustaso listassa on kolme vaihtehtoa(ne näkyvät luokan __init__ metodissa)
    def lisaa_morko(self, maara = 1, valittu_vaikeustaso = "helppo"):
        for i in range(maara):
            self.oliot["hirvio"].append(Morko(x_sijainti = randint(0, self.leveys - self.kuvat["hirvio"].get_width()),
                                              y_sijainti = randint(0, self.korkeus - self.kuvat["hirvio"].get_height()),
                                              x_suunta = choice(self.vaikeustaso[valittu_vaikeustaso]),
                                              y_suunta = choice(self.vaikeustaso[valittu_vaikeustaso])))
    
    #Lisää peliin kolikoita
    def lisaa_kolikko(self, maara = 1):
        for i in range(maara):
            self.oliot["kolikko"].append(Kolikko(x_sijainti = randint(0, self.leveys - self.kuvat["kolikko"].get_width()),
                                              y_sijainti = randint(0, self.korkeus - self.kuvat["kolikko"].get_height())))
    
    # lataa pelin käyttämät kuvat tekstitiedostoista. 
    # Luo myös läpinäkyvän version robotin kuvasta joka piirretään, kun robotti ei pysty saamaan vahinkoa.
    def lataa_kuvat(self):
        kuvat = {nimi : pygame.image.load(resource_path(nimi + ".png")) for nimi in ["robo", "hirvio", "kolikko"]}
        kuvat["robo_dmg"] = pygame.image.load("robo.png").convert_alpha()
        kuvat["robo_dmg"].set_alpha(128)
        return kuvat
    
    # asettaa ohjattavan hahmon eli robotin kursorin paikalle ja käsittelee pelin uudelleenkäynnistyksen ja sulkemisen.
    def tapahtuma_kasittelija(self):
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.MOUSEMOTION and self.peli_paalla:
                    self.botti.x = tapahtuma.pos[0] - self.botti.leveys/2
                    self.botti.y = tapahtuma.pos[1] - self.botti.korkeus/2
                    if not self.logiikka.seinien_sisalla(self.botti) and self.botti.saa_vahinkoa:
                        self.logiikka.vahingoittamattomuuden_kasittely_botille(self.botti, True)

            
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_ESCAPE:
                    exit()
                if tapahtuma.key == pygame.K_F1:
                    self.uusi_peli()
            
            if tapahtuma.type == pygame.QUIT:
                exit()
 
    # Piirtää pelissä näkyvät teksit ruudulle
    # kun self.peli_päällä on False piirretään pelin päätöstekstit
    def piirra_teksti(self):
        elamat = self.tekstit["elamat"].render(f"Elämät: {self.botti.elamia}", True, (255, 0, 0))
        taso = self.tekstit["taso"].render(f"taso: {self.taso[0]}", True, (255, 0, 0))
        pisteet = self.tekstit["pisteet"].render(f"Pisteet: {self.pisteet[0]}", True, (255, 0, 0))
        self.naytto.blit(pisteet, (self.leveys-200, 10))
        self.naytto.blit(taso, (self.leveys-320, 10))
        self.naytto.blit(elamat, (self.leveys-200, self.korkeus -30))
        
        if not self.peli_paalla:
            peli_ohi = self.tekstit["peli_ohi"]
            napit = self.tekstit["napit"]
            self.naytto.blit(peli_ohi, ((self.leveys - peli_ohi.get_width())/2, (self.korkeus - peli_ohi.get_height())/2))
            self.naytto.blit(napit, ((self.leveys - napit.get_width())/2, (self.korkeus - napit.get_height())/2 + 75))
    
    #Piirtää kaikki pelin tapahtumat ja valkoisen taustan
    def piirra_naytto(self):
        self.naytto.fill((255, 255, 255))
        
        for kolikko in self.oliot["kolikko"]:
            self.naytto.blit(self.kuvat["kolikko"], kolikko.sijainti)
            
        for hirvio in self.oliot["hirvio"]:
            self.naytto.blit(self.kuvat["hirvio"], hirvio.sijainti)
            
        if self.botti.saa_vahinkoa:
            self.naytto.blit(self.kuvat["robo"], self.botti.sijainti)
        else:
            self.naytto.blit(self.kuvat["robo_dmg"], self.botti.sijainti)
        
        self.piirra_teksti()
        
        pygame.display.flip()
    
    #Tämä metodi kutsutaan kun peli päättyy eli robotin elämät ovat nolla
    def peli_ohi(self):
        self.peli_paalla = False
        while True:
            self.tapahtuma_kasittelija()
            self.naytto.fill((0,0,0))
            self.piirra_teksti()
            pygame.display.flip()
    
    # Pelin pääsilmukka tästä kutsutaan pelin tapahtumia ja logiikkaa käsittelevät kutsust sekä piirtokutsut.
    # peli on laitetty pyörimään tickrate on kovakoodattu jotta peli pyörii 120 FPS pelin logiikka on suuniteltu sen toimimaan sen mukaan
    def pelaa(self):
        self.peli_paalla = True
        while self.botti.elamia > 0:
            self.tapahtuma_kasittelija()
            self.logiikka.liikuta_kaikkia_morkoja(self.oliot["hirvio"])
            self.logiikka.tormayksen_kasittely_kolikoille(self.botti, self.pisteet, self.oliot["kolikko"])
            self.logiikka.tormayksen_kasittely_moroille(self.botti, self.oliot["hirvio"])
            self.logiikka.vahingoittamattomuuden_kasittely_botille(self.botti)
            self.piirra_naytto()
            
            if self.logiikka.taso_lapi(self.oliot["kolikko"], self.taso):
                self.luo_seuraava_taso()
            
            self.kello.tick(120)
        
        self.peli_ohi()
    
    #Asettaa kaikik tarvittavat asetukset uusiksi ja käynnistää taas pelin alkuasetelmista.
    def uusi_peli(self):
        self.alusta_peli()
        self.pelaa()

if __name__ == "__main__":
    Kolikkorosvo()