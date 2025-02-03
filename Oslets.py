# -*- coding: latin-1 -*-

from random import *
import time

def retirerDe (colonne, de): # Romain
    """'retirerDe (colonne, de)' Retire tous les dés similaire à 'de' dans la colonne 'colonne'."""
    col = list(colonne)
    for i in [0, 0, 0]:
        for c in col:
            if (c == de):
                col.pop(col.index(c))
                break
                # Ici on utilise break, car la taille de la liste parcourue a été modifié ('col.pop()').
                # Pour ne pas faire d'erreur, on sort de la boucle et on reparcoure la nouvelle.
    while len(col) < 3:col.append(0)
    return col

def colonnesValides (grille): # Romain
    """'colonnesValides (grille)' Retourne la liste des indexes des colonnes jouable dans 'grille'."""
    result = []
    for i in range(len(grille)):
        if (0 in grille[i]):result.append(i)
    return result

def grille_pleine(grille): # Clément
    """Retourne si une grille est pleine"""
    for ligne in grille:
        for case in ligne:
            if case == 0:
                return False
    return True

def afficherPartie (grille1, grille2, scores1, scores2, nom1, nom2): # Romain
    """'afficherPartie (grille1, grille2, scores1, scores2, nom1, nom2)' dessine la partie."""
    
    drawText("[echap] quitter", (-65, 94), 20, False)
    size = 28
    h = 55

    for s in sprites:
        s.set_alpha(255)

    for i in [0, 1, 2]:
        for j in [0, 1, 2]:
            drawImage(sprites[grille1[j][i]], ((j-1)*size, ((i-1)*size) + h))
    for pos in [0, 1, 2]:
        drawText(str(scores1[pos]), ((pos-1)*size, 8), 40, True)

    h = -h
    for i in [0, 1, 2]:
        for j in [0, 1, 2]:
            drawImage(sprites[grille2[j][i]], ((j-1)*size, (1 - (i-1)*size) + h))
    for pos in [0, 1, 2]:
        drawText(str(scores2[pos]), ((pos-1)*size, -8), 40, True)

    drawText(nom1, (85, 50 + 20), 30, True)
    drawText(nom2, (-85, -50 + 20), 30, True)

    drawImage(dropImg, (85, 40))
    drawImage(dropImg, (-85, -60))

    drawText(str(sum(scores1)) + " pts", (85, 12), 40, True)
    drawText(str(sum(scores2)) + " pts", (-85, -88), 40, True)


def ajouterDe (colonne, de): # Romain
    """'ajouterDe (colonne, de)' ajoute un dé 'de' dans la colonne 'colonne'."""
    colonneCop = list(colonne)
    i = 0
    while colonneCop[i] != 0:
        i += 1
    colonneCop[i] = de
    return colonneCop

def calcul_score(grille): # Yliane
    """calcul le score de chaque colonne de la grille et revoie les resulats dans une liste"""
    score = []
    for ligne in grille:
        somme = 0
        for nombre in ligne:
            repetition = ligne.count(nombre) #verifie si un nombre se repete dans la colonne
            if repetition == 2:
                somme += repetition * repetition * nombre
                somme -= 2 * nombre
            elif repetition == 3:
                somme = repetition * repetition * nombre
            elif repetition == 1:
                somme += nombre
        score.append(somme)

    return score

def copie(grille): # Romain
    """permet de copier une liste de liste. utile pour faire des testes pour les bots."""
    cop = []
    for i in grille:cop.append(list(i)) # list() permet de faire une copie
    return cop

def elementsEgaux(liste): # Romain
    """Retourne si tous les éléments de la liste 'liste' sont égaux."""
    resutat = True
    elementPrecedent = liste[0]
    for e in liste:
        if elementPrecedent != e:
            resutat = False
        elementPrecedent = e
    return resutat

def dianthea (de, choix, grilleAdversaire): # Romain
    """retourne le choix du bot Dianthéa"""
    meilleurChoix = None
    meilleurScore = 1
    listeDesTest = []
    for colonne in choix:
        test = copie(grilleAdversaire)
        scoreAvant = sum(calcul_score(test))
        test[colonne] = retirerDe(test[colonne], de)
        scoreApres = sum(calcul_score(test))
        if (scoreApres - scoreAvant < meilleurScore):
            meilleurScore = scoreApres - scoreAvant
            meilleurChoix = colonne
        listeDesTest.append(scoreApres - scoreAvant)
    if elementsEgaux(listeDesTest): meilleurChoix = choix[randint(0, len(choix)-1)]
    return meilleurChoix

def Peter(de, choix, grilleBot): # Yliane
    """retourne le choix du bot Peter"""
    meilleurChoix = -1
    meilleurScore = -1
    listeDesTest = []
    for colonne in choix:
        test = copie(grilleBot)
        scoreBase = sum(calcul_score(test))
        test[colonne] = ajouterDe(test[colonne], de)
        scoreEnsuite = sum(calcul_score(test))
        if scoreEnsuite - scoreBase > meilleurScore:
            meilleurScore = scoreEnsuite - scoreBase
            meilleurChoix = colonne
        listeDesTest.append(scoreEnsuite - scoreBase)
    if elementsEgaux(listeDesTest):
        meilleurChoix = choix[randint(0, len(choix)-1)]
    return meilleurChoix

def element_aleatoire(liste): # Clément
    """retourne le choix du bot Tarak"""
    import random
    return random.choice(liste)

def lancer_de(): # Clément
    """lance un dé et affiche le résultat"""
    resultat = randint(1,6)
    # print("le dé est",resultat)
    return resultat

def cynthia (de, choix, grilleAdversaire, grilleBot): # Romain
    """retourne le choix du bot Cynthia"""
    meilleurChoix = 0
    meilleurScore = -1
    listeDesTest = [] # on garde les scores de chaque choix possible.

    for colonne in choix:

        # on fait une copie de chaque grille pour faire des tests
        testBot = copie(grilleBot)
        testAdversaire = copie(grilleAdversaire)

        # on calcule les scores avant de faire le teste
        scoreAdversaireAvant = sum(calcul_score(testAdversaire))
        scoreBotAvant = sum(calcul_score(testBot))

        # on place le dé dans la colonne et on retire les dés
        testBot[colonne] = ajouterDe(testBot[colonne], de)
        testAdversaire[colonne] = retirerDe(testAdversaire[colonne], de)

        # on calcule le score apres le teste
        scoreAdversaireApres = sum(calcul_score(testAdversaire))
        scoreBotApres = sum(calcul_score(testBot))

        # on vérifie si c'est le meilleur score
        # (on additionne la diférence des scores d'avant et des scores d'apres)
        if (abs(scoreAdversaireAvant - scoreAdversaireApres) + (scoreBotApres - scoreBotAvant) > meilleurScore):
            meilleurScore = abs(scoreAdversaireAvant - scoreAdversaireApres) + (scoreBotApres - scoreBotAvant)
            meilleurChoix = colonne

        # on ajoute le score à la listes des scores de chaque choix
        listeDesTest.append(abs(scoreAdversaireAvant - scoreAdversaireApres) + (scoreBotApres - scoreAdversaireApres))

    if elementsEgaux(listeDesTest): # on vérifie si chaque choix sont équivalents
        meilleurChoix = -1
        meilleurTaille = -1
        for colonne in choix:
            if (grilleBot[colonne].count(0) + grilleAdversaire[colonne].count(0) > meilleurTaille):
                meilleurChoix = colonne
                meilleurTaille = grilleBot[colonne].count(0) + grilleAdversaire[colonne].count(0)

    return meilleurChoix


# mise en place de la fenetre pyGame

import pygame as game
game.init()

from pygame.locals import *

fenetre = game.display.set_mode((800, 600))
game.display.set_caption("Osselets")
background = game.Surface(fenetre.get_size())
background = background.convert()

bgColor = (35, 61, 77)
fgColor = (255, 255, 255)


def drawText (text, posi, size, centerX): # Romain
    """fonction pour pygame : déssine du texte"""
    posi = (float(posi[0])/(100 + (1.0/3.0*100.0)) * 400, float(posi[1])/100 * 300)
    font = game.font.Font("ressources/pusab.otf", size)
    text = font.render(text, 1, fgColor)
    
    if (abs(posi[1]) >= 200) and centerX == False:
        text.set_alpha(120)
        
    textpos = text.get_rect()
    
    if (centerX == True):
        textpos.centerx = background.get_rect().centerx
    else:
        textpos[0] = fenetre.get_width()//2 + posi[0]
    textpos.centery = background.get_rect().centery
    background.blit(text, (textpos[0] + posi[0], textpos[1] - posi[1]))
    return text

def drawImage(sprite, posi): # pygame : Romain
    """fonction pour pygame : déssine une image"""
    posi = (float(posi[0])/(100 + (1.0/3.0*100.0)) * 400, float(posi[1])/100 * 300)
    spriteX = sprite.get_size()[0]
    spriteY = sprite.get_size()[1]
    posX = posi[0] - (spriteX//2)
    posY = posi[1] + (spriteY//2)

    background.blit(sprite, (posX+400, -posY + 300))
    return sprite

def createMenu (title, tabs): # pygame : Romain
    """fonction pour pygame : déssine un menu"""
    drawText(title, (0, 80), 60, True)
    for pos in range(len(tabs)):
        drawText(tabs[(len(tabs) - 1) - pos], (-30, (pos*15)-(len(tabs)*15//2)), 40, False)
    return len(tabs)

def hauteur (colonne): # pygame : Romain
    """fonction pour pygame : retourne la hauteur où le joeur peut placer le dé dans une colonne."""
    h = 0
    for i in colonne:
        if (i == 0):
            h = colonne.index(i)
    return h

# mise en place des ressources du jeu

running = True
flecheMenu = -1
menu = "menuPrincipale"
tailleMenu = 0

dropImg = game.image.load("ressources/dropBox.png").convert()
tutoImg = game.image.load("ressources/screenTuto.png").convert()
tutoImg2 = game.image.load("ressources/screenTuto2.png").convert()

rickRolls = []
for i in range(14):
    img = game.image.load("ressources/rickGif/rickroll-roll"+str(i)+".png").convert()
    img = game.transform.scale(img, (50, 50))
    rickRolls.append(img)
rickI = 0

sprites = []
for de in range(7):
    sprites.append(game.image.load("ressources/sprites/e"+str(de)+".png").convert())

grille1 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
grille2 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

scores1 = calcul_score(grille1)
scores2 = calcul_score(grille2)

bots = ["Tarak", "Dianthéa", "Peter", "Cynthia"]
timer = 0

game.time.Clock().tick(60)
refresh = True

while running: # boucle plrincipale

    Up = False
    Down = False
    Enter = False
    Right = False
    Left = False
    Escape = False
    for event in game.event.get():
        if event.type == QUIT:
            running = False
        if (event.type == KEYDOWN):
            if (event.key == K_UP):
                Up = True
            if (event.key == K_DOWN):
                Down = True
            if (event.key == K_RETURN):
                Enter = True
            if (event.key == K_LEFT):
                Right = True
            if (event.key == K_RIGHT):
                Left = True
            if (event.key == K_ESCAPE):
                Escape = True

    timer += 1

    background.fill(bgColor)

    if (flecheMenu == -1 and (Up == True or Down == True) and tailleMenu > 0):
        flecheMenu = tailleMenu - 1

    elif flecheMenu != -1:
        if Up:
            flecheMenu += 1
            if (flecheMenu > tailleMenu - 1): flecheMenu = tailleMenu - 1
        if Down:
            flecheMenu += -1
            if (flecheMenu < 0): flecheMenu = 0

    if (menu == "menuPrincipale"):
        de = 0
        grille1 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        grille2 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        scores1 = calcul_score(grille1)
        scores2 = calcul_score(grille2)
        joueur = 0
        posiDe = (85, 40)
        lance = False

        tailleMenu = createMenu("Osselets", ["Tutoriel", "Solo", "Multijoueur", "Crédits", "Quiter"])
        drawText("'flèches' pour naviguer. 'entrer' pour choisir.", (-65, -94), 20, False)
        if (flecheMenu == 3 and Enter == True):
            menu = "choixBots"
            flecheMenu = -1
            modeDeJeux = "solo"

        if (flecheMenu == 4 and Enter == True):
            menu = "tutoriel"
            flecheMenu = -1
            Enter = False
            t1 = time.monotonic()

        if (flecheMenu == 2 and Enter == True):
            menu = "game"
            flecheMenu = -1
            Enter = False
            modeDeJeux = "multi"
            nomJ1 = "invitée 1"
            nomJ2 = "invitée 2"
            tStart = time.monotonic()
            t1 = time.monotonic()
            
        if (flecheMenu == 1 and Enter == True):
            menu = "credits"
            flecheMenu = -1
            Enter = False
            t1 = time.monotonic()
            
        if (flecheMenu == 0 and Enter == True):
            menu = "quiter"
            flecheMenu = -1
            Enter = False
            t1 = time.monotonic()
            
    if (menu == "quiter"):
        tailleMenu = createMenu("", ["oui", "retour"])
        drawText("êtes vous sûre de vouloir", (0, 75), 40, True)
        drawText("quitter ce jeu maserclass ?", (0, 60), 40, True)
        if (flecheMenu == 1 and Enter == True):
            game.quit()
            print(" au revoir !")
            
        if (flecheMenu == 0 and Enter == True):
            menu = "menuPrincipale"
            flecheMenu = -1
            Enter = False

    if (menu == "credits"):
        tailleMenu = createMenu("Crédits", [])
        drawText("Clément  MOUQUET", (0, 0), 30, True)
        drawText("Yliane  HISSAR", (0, 15), 30, True)
        drawText("Romain  THEROND", (0, -15), 30, True)
        
        if (time.monotonic() - t1 > 1):
            drawText("[ENTRER] ok", (0, -90), 30, True)
            if (Enter == True):
                menu = "menuPrincipale"
                flecheMenu = -1
                Enter = False

    if (menu == "tutoriel"):
        tailleMenu = createMenu("tutoriel", [])
        drawImage(tutoImg, (0, -10))
        if (time.monotonic() - t1 > 1):
            drawText("[ENTRER] suivant", (0, -90), 30, True)
            if (Enter == True):
                menu = "tutoriel2"
                flecheMenu = -1
                Enter = False
                t1 = time.monotonic()
                
    if (menu == "tutoriel2"):
        tailleMenu = createMenu("tutoriel", [])
        drawImage(tutoImg2, (8, -10))
        
        if (time.monotonic() - t1 > 1):
            drawText("[ENTRER] ok", (0, -90), 30, True)
            if (Enter == True):
                menu = "menuPrincipale"
                flecheMenu = -1
                Enter = False

    if (menu == "choixBots"):
        tailleMenu = createMenu("Choix de l'adversaire", ["Tarak", "Dianthéa", "Peter", "Cynthia", "retour"])
        if (flecheMenu == 0 and Enter == True):
            menu = "menuPrincipale"
            flecheMenu = -1
            Enter = False
        for i in range(4):
            if (flecheMenu == i+1 and Enter == True):
                menu = "game"
                bot = 3 - i
                flecheMenu = -1
                Enter = False
                nomJ1 = "invitée 1"
                nomJ2 = bots[bot]
                tStart = time.monotonic()
                t1 = time.monotonic()

    if (menu == "game"):
        if (grille_pleine(grille1) or grille_pleine(grille2)):

            if (time.monotonic() - t1 < 1.5):
                scores1 = calcul_score(grille1)
                scores2 = calcul_score(grille2)
                afficherPartie(grille1, grille2, scores1, scores2, nomJ1, nomJ2)
                tStop = time.monotonic()
            else:
                if (sum(scores1) == sum(scores2)):
                    drawText("égalité !", (0, 60), 50, True)
                elif (sum(scores1) > sum(scores2)):
                    drawText(nomJ1+" a gagné !", (0, 60), 50, True)
                else:
                    drawText(nomJ2+" a gagné !", (0, 60), 50, True)
                drawText("score "+nomJ1+" : "+str(sum(scores1))+" pts", (0, 40), 30, True)
                drawText("score "+nomJ2+" : "+str(sum(scores2))+" pts", (0, 30), 30, True)
                temps = (tStop - tStart)/60
                tmp = str(round(temps//1)) + "." +  str(round(((temps%1)*10)//1))
                drawText("temp de jeu : "+tmp+" min", (0, 10), 30, True)

                drawImage(rickRolls[(rickI//11)%14], (0, -70))
                rickI += 1

                if (time.monotonic() - t1 > 3):
                    drawText("[ENTRER] ok", (0, -90), 30, True)
                    if (Enter == True):
                        menu = "menuPrincipale"
                        flecheMenu = -1
                        Enter = False

        else:

            if (Escape == True):
                menu = "menuPrincipale"
                flecheMenu = -1
                Enter = False

            scores1 = calcul_score(grille1)
            scores2 = calcul_score(grille2)
            afficherPartie(grille1, grille2, scores1, scores2, nomJ1, nomJ2)
            
            if (joueur % 2 == 0):
                grilleJoueur = grille1
                grilleAdversaire = grille2
                h = 55
            else:
                grilleJoueur = grille2
                grilleAdversaire = grille1
                h = 2

            choixPossibles = colonnesValides(grilleJoueur)
            
            if (lance == False):
                de = lancer_de()
                choix = -1
                if (time.monotonic() - t1 > 0.5):
                    lance = True

            deImg = sprites[de]

            if (joueur%2 == 1 and modeDeJeux == "solo"):
                if (time.monotonic() - t1 < 1.5):
                    deImg.set_alpha(255)
                    drawImage(sprites[de], (-85, -60))
                else:
                    if (botChosed == False):
                        if (bot == 0):
                            choix = element_aleatoire(choixPossibles)
                        elif (bot == 1):
                            choix = dianthea(de, choixPossibles, grilleAdversaire)
                        elif (bot == 2):
                            choix = Peter(de, choixPossibles, grilleJoueur)
                        elif (bot == 3):
                            choix = cynthia(de, choixPossibles, grilleAdversaire, grilleJoueur)
                        else:
                            print("/!\, le bot n°"+str(bot), "n'existe pas.  D:")
                        botChosed = True
                    deImg.set_alpha(120)
                    drawImage(deImg, ((choix-1)*28, ( -hauteur(grilleJoueur[choix])-1)*28 + 2))
                    if (time.monotonic() - t1 > 2.5):
                        Enter = True
            else:
                if lance == False or time.monotonic() - t1 < 1:
                    Right = False
                    Left = False
                    Enter = False
                    
                if ((Right or Left) and choix == -1):
                    choix = 0

                if (choix == -1):
                    deImg.set_alpha(255)
                else:
                    deImg.set_alpha(120)

                if Right:
                    choix -= 1
                    if (choix < 0):
                        choix = 0
                elif Left:
                    choix += 1
                    if (choix > len(choixPossibles)-1):
                        choix = len(choixPossibles)-1

                if (choix == -1):
                    if (joueur%2 == 0):
                        drawImage(sprites[de], (85, 40))
                    else:
                        drawImage(sprites[de], (-85, -60))
                else:
                    if (joueur%2 == 0):
                        offSet = 1
                    else: offSet = -1
                    drawImage(sprites[de], ((choixPossibles[choix]-1)*28, (offSet * hauteur(grilleJoueur[choixPossibles[choix]])-1)*28 + h))

            if (Enter and choix > -1):
                if (modeDeJeux == "multi" or joueur%2 == 0):
                    choix = choixPossibles[choix]
                grilleJoueur[choix] = ajouterDe(grilleJoueur[choix], de)
                grilleAdversaire[choix] = retirerDe(grilleAdversaire[choix], de)
                lance = False
                choix = -1
                joueur += 1
                t1 = time.monotonic()
                botChosed = False
                Right = False
                Left = False

    if (flecheMenu > -0.5) and menu != "game":
        drawText(">", (-70, (flecheMenu - (tailleMenu/2))*15), 40, True)

    fenetre.blit(background, (0, 0))
    game.display.flip()

game.quit()
