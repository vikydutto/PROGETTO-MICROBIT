#--------------------------------------------------------------------------------------------------------#
#------------------------------------------DUTTO VITTORIA 4AROB------------------------------------------#
#---------------------------------------------  BUTTON-TRIS ---------------------------------------------#
#--------------------------------------------------------------------------------------------------------#

from pickle import FALSE
import serial
import pygame as pg
import threading, queue
import time
#from microbit import *

button_a = False #il pulsante A per default non è premuto
button_b = False #il pulsante B per default non è premuto
#VISUALIZZAZIONE SCHERMO
pg.init()
altezza =500
larghezza = 500
global running
running = True

screen = pg.display.set_mode((altezza, larghezza))
clock = pg.time.Clock()

#print(ground_game)

q = queue.Queue()#crea la coda

class Read_Microbit(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._running = True
      
    def terminate(self):
        self._running = False
        
    def run(self):
        #serial config
        print("Thread avviato prova")
        port = "COM14"
        s = serial.Serial(port)
        s.baudrate = 115200
        while self._running:
            data = s.readline().decode() 
            global button_a
            global button_b
            if "ATrue" in data:
                button_a = True
            else:
                button_a=False
            if "BTrue" in data:
                button_b = True
            else:
                button_b=False
            time.sleep(0.01)

terreno = [] #memorizza le celle occupate
for _ in range (0,3):
    riga = ["","",""]
    terreno.append(riga) #matrice inizializzata con celle vuote

def stampaCursore(x,y):
    pg.draw.circle(screen, (255,   0, 0),
                 [x, y],10,1)
#--------------------------------------------------------------------------------------------------------#
#------------------------------------------------STAMPA--------------------------------------------------#
#--------------------------------------------------------------------------------------------------------#

def stampa (): #è il numero della casella partendo da quella in alto a sinistra
    player1 = pg.image.load("./x.png") #immagine simbolo giocatore x
    player1=pg.transform.scale(player1,(larghezza/6,altezza/6))
    player2 = pg.image.load("./o.png")
    player2=pg.transform.scale(player2,(larghezza/6,altezza/6))
    global terreno

    for y,riga in enumerate(terreno):
        for x,casella in enumerate(riga):
            if casella!= "":
                if casella=="x":
                    player_rect=player1.get_rect()
                    player_rect.centerx =  (larghezza/100*70)/3*(x)+larghezza/6+(larghezza/100*10)
                    player_rect.centery =  (altezza/100*70)/3*int(y)+altezza/6+(altezza/100*20) 
                    screen.blit(player1,player_rect)
                else:
                    player_rect=player2.get_rect()
                    player_rect.centerx =  (larghezza/100*70)/3*(x)+larghezza/6+(larghezza/100*10)
                    player_rect.centery =  (altezza/100*70)/3*int(y)+altezza/6+(altezza/100*20) 
                    screen.blit(player2,player_rect)

#--------------------------------------------------------------------------------------------------------#
#-------------------------------------------CONTROLLO VITTORIA-------------------------------------------#
#--------------------------------------------------------------------------------------------------------#

def controlloVittoria(griglia, simbolo):
    """controllo se il giocatore ha creato una combinazione da tre"""
    if griglia[0][0] == griglia[0][1] == griglia[0][2] == simbolo:
        return True
    elif griglia[1][0] == griglia[1][1] == griglia[1][2] == simbolo:
        return True
    elif griglia[2][0] == griglia[2][1] == griglia[2][2] == simbolo:
        return True
    elif griglia[0][0] == griglia[1][0] == griglia[2][0] == simbolo:
        return True
    elif griglia[0][1] == griglia[1][1] == griglia[2][1] == simbolo:
        return True
    elif griglia[0][2] == griglia[1][2] == griglia[2][2] == simbolo:
        return True
    elif griglia[0][0] == griglia[1][1] == griglia[2][2] == simbolo:
        return True
    elif griglia[0][2] == griglia[1][1] == griglia[2][0] == simbolo:
        return True
    else:
        return False
#--------------------------------------------------------------------------------------------------------#
#-------------------------------------------------MAIN---------------------------------------------------#
#--------------------------------------------------------------------------------------------------------#

def main():
    ground_game = pg.image.load("tris.png") #immagine campo di gioco
    global altezza
    global larghezza
    ground_game=pg.transform.scale(ground_game,(larghezza,altezza))
    ground_rect = ground_game.get_rect()
    ground_rect.centerx = altezza // 2
    ground_rect.centery = larghezza // 2
    screen.blit(ground_game,ground_rect)
    global running
    player=True
    posizioneCursore=0
    x,y=0,0
    global button_a
    global button_b
    rm = Read_Microbit()
    rm.start()
    while running:


        screen.fill((255, 255, 255))
        screen.blit(ground_game, ground_rect)
        
        clock.tick(10)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                pg.quit()
                           
        if button_a:
            posizioneCursore+=1
            posizioneCursore=posizioneCursore%9  

        if button_b:
                    if terreno[int(posizioneCursore/3)][posizioneCursore%3]== "":
                        if player == True:  
                            terreno[int(posizioneCursore/3)][posizioneCursore%3]= "x"
                            player=False
                            if controlloVittoria(terreno, "x"):
                                print("Fine")
                                #pg.blit()
                                #time.sleep(3)
                                #rm.terminate()
                                #rm.join()
                                #pg.quit()
                                #quit()"""
                                
                        
                        else:      
                            terreno[int(posizioneCursore/3)][posizioneCursore%3]= "o"
                            player=True
                            if controlloVittoria(terreno, "o"):
                                print("Fine")
                            #pg.image . blit
                                #time.sleep(3)
                                #rm.terminate()
                                #rm.join()
                                #pg.quit()
                                #quit()"""
                        posizioneCursore=0

        x= (larghezza/100*70)/3*(posizioneCursore%3)+larghezza/6+(larghezza/100*10)
        y=(altezza/100*70)/3*int(posizioneCursore/3)+altezza/6+(altezza/100*20)
        stampa()
        stampaCursore(x,y)
        pg.display.update()
        pg.display.flip()
    rm.terminate()
    rm.join()

if __name__=="__main__":
    main()