import pygame
import random
import sys

# Inizializzazione di Pygame
pygame.init()
larghezza_schermo, altezza_schermo = 800, 600
schermo = pygame.display.set_mode((larghezza_schermo, altezza_schermo))
pygame.display.set_caption("Gioco dell'Oca")

# Definizione Colori e Font
NERO = (0, 0, 0)
BIANCO = (255, 255, 255)
ROSSO = (100, 20, 20)  # Modifica del colore ROSSO

# Costanti del Gioco
DIMENSIONE_QUADRATO = 50
LARGHEZZA_SCACCHIERA = 10  # 10 caselle per riga
ALTEZZA_SCACCHIERA = 7  # 7 righe

# Carica gli sfondi personalizzati
sfondo_benvenuto = pygame.image.load('Sfondo1.png')
sfondo_benvenuto = pygame.transform.scale(sfondo_benvenuto, (larghezza_schermo, altezza_schermo))

sfondo_inserimento_giocatori = pygame.image.load('Sfondo2.png')
sfondo_inserimento_giocatori = pygame.transform.scale(sfondo_inserimento_giocatori, (larghezza_schermo, altezza_schermo))

sfondo_regole = pygame.image.load('Sfondo3.png')
sfondo_regole = pygame.transform.scale(sfondo_regole, (larghezza_schermo, altezza_schermo))

sfondo_tabellone = pygame.image.load('Sfondo3.png')
sfondo_tabellone = pygame.transform.scale(sfondo_tabellone, (larghezza_schermo, altezza_schermo))

# Carica il font di default
font = pygame.font.Font(None, 36)
font_regole = pygame.font.Font("Font1.ttf", 24)
font_input1 = pygame.font.Font("Font4.ttf", 32)
font_input3 = pygame.font.Font("Font5.ttf", 20)

# Carica le immagini delle pedine
pedina1_img = pygame.image.load('PedinaRE.png')
pedina1_img = pygame.transform.scale(pedina1_img, (DIMENSIONE_QUADRATO - 20, DIMENSIONE_QUADRATO - 20))
pedina2_img = pygame.image.load('PedinaREG.png')
pedina2_img = pygame.transform.scale(pedina2_img, (DIMENSIONE_QUADRATO - 20, DIMENSIONE_QUADRATO - 20))
pedina3_img = pygame.image.load('PedinaALF.png')
pedina3_img = pygame.transform.scale(pedina3_img, (DIMENSIONE_QUADRATO - 20, DIMENSIONE_QUADRATO - 20))
pedina4_img = pygame.image.load('PedinaCAV.png')
pedina4_img = pygame.transform.scale(pedina4_img, (DIMENSIONE_QUADRATO - 20, DIMENSIONE_QUADRATO - 20))
pedina5_img = pygame.image.load('PedinaTO.png')
pedina5_img = pygame.transform.scale(pedina5_img, (DIMENSIONE_QUADRATO - 20, DIMENSIONE_QUADRATO - 20))
pedina6_img = pygame.image.load('PedinaNORM.png')
pedina6_img = pygame.transform.scale(pedina6_img, (DIMENSIONE_QUADRATO - 20, DIMENSIONE_QUADRATO - 20))

# Crea le pedine come una lista di tuple (immagine_pedina, posizione)
pedine = [(pedina1_img, 0), (pedina2_img, 0), (pedina3_img, 0), (pedina4_img, 0), (pedina5_img, 0), (pedina6_img, 0)]  # Inizializza le pedine alla casella di partenza (posizione 0)

def disegna_scacchiera(sfondo):
    schermo.blit(sfondo, (0, 0))
    x_scacchiera = (larghezza_schermo - LARGHEZZA_SCACCHIERA * DIMENSIONE_QUADRATO) // 2
    y_scacchiera = (altezza_schermo - ALTEZZA_SCACCHIERA * DIMENSIONE_QUADRATO) // 2

    # Disegna le caselle con riempimento nero e testo bianco
    for riga in range(ALTEZZA_SCACCHIERA):
        for colonna in range(LARGHEZZA_SCACCHIERA):
            numero_casella = riga * LARGHEZZA_SCACCHIERA + colonna
            if numero_casella <= 63:
                rect = pygame.Rect(x_scacchiera + colonna * DIMENSIONE_QUADRATO,
                                   y_scacchiera + riga * DIMENSIONE_QUADRATO,
                                   DIMENSIONE_QUADRATO, DIMENSIONE_QUADRATO)
                pygame.draw.rect(schermo, NERO, rect)  # Riempi la casella con il colore nero
                pygame.draw.rect(schermo, BIANCO, rect, 1)  # Contorno bianco
                if numero_casella == 0:  # Se è la casella di partenza
                    testo_numero_casella = font.render("START", True, BIANCO)
                    testo_numero_casella = pygame.transform.scale(testo_numero_casella,
                                                                  (int(testo_numero_casella.get_width() * 0.5),
                                                                   int(testo_numero_casella.get_height() * 0.5)))
                    schermo.blit(testo_numero_casella,
                                 (x_scacchiera + colonna * DIMENSIONE_QUADRATO + 5,
                                  y_scacchiera + riga * DIMENSIONE_QUADRATO + 5))
                else:
                    testo_numero_casella = font.render(str(numero_casella), True, BIANCO)
                    schermo.blit(testo_numero_casella,
                                 (x_scacchiera + colonna * DIMENSIONE_QUADRATO + 10,
                                  y_scacchiera + riga * DIMENSIONE_QUADRATO + 10))

     # Disegna le pedine sulla scacchiera
    for pedina_img, posizione in pedine:
        x_pedina = x_scacchiera + (posizione % LARGHEZZA_SCACCHIERA) * DIMENSIONE_QUADRATO
        y_pedina = y_scacchiera + (posizione // LARGHEZZA_SCACCHIERA) * DIMENSIONE_QUADRATO
        schermo.blit(pedina_img, (x_pedina, y_pedina))

def mostra_schermata_benvenuto():
    schermo.blit(sfondo_benvenuto, (0, 0))
    testo_benvenuto = font_input1.render("BENVENUTI NEL GIOCO DELL'OCA", True, NERO)
    rettangolo_benvenuto = testo_benvenuto.get_rect(center=(larghezza_schermo / 2, altezza_schermo / 2 - 100))
    schermo.blit(testo_benvenuto, rettangolo_benvenuto)
    testo_avvio = font_input3.render("Premi AVVIO per cominciare", True, NERO)
    rettangolo_avvio = testo_avvio.get_rect(center=(larghezza_schermo / 2, altezza_schermo / 2))
    schermo.blit(testo_avvio, rettangolo_avvio)
    pygame.display.flip()
    in_attesa_avvio = True
    while in_attesa_avvio:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    in_attesa_avvio = False

def inserisci_input_giocatori():
    num_giocatori = 0
    continuare = True
    testo_input = ''
    while continuare:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    if testo_input.isdigit() and 2 <= int(testo_input) <= 6:
                        num_giocatori = int(testo_input)
                        continuare = False
                    else:
                        testo_input = ''
                elif evento.key == pygame.K_BACKSPACE:
                    testo_input = testo_input[:-1]
                elif evento.key in [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                    testo_input += evento.unicode
        schermo.blit(sfondo_inserimento_giocatori, (0, 0))
        if testo_input and (not testo_input.isdigit() or not 2 <= int(testo_input) <= 6):
            testo_errore = font_input3.render('Errore, devi inserire un numero compreso tra 2 e 6', True, ROSSO)
            rettangolo_errore = testo_errore.get_rect(center=(larghezza_schermo/2, altezza_schermo/2 + 50))
            schermo.blit(testo_errore, rettangolo_errore)
        blocco = font_input3.render('Inserisci il numero di giocatori (2-6): ' + testo_input, True, NERO)
        rettangolo = blocco.get_rect(center=(larghezza_schermo/2, altezza_schermo/2))
        schermo.blit(blocco, rettangolo)
        pygame.display.flip()
    return num_giocatori

def mostra_schermata_regole():
    schermo.blit(sfondo_benvenuto, (0, 0))
    testo_titolo = font_regole.render("REGOLE DEL GIOCO", True, NERO)
    rettangolo_titolo = testo_titolo.get_rect(center=(larghezza_schermo / 2, 50))
    schermo.blit(testo_titolo, rettangolo_titolo)

    regole_text = [
        "- Se si capita sulla casella 6: si va direttamente alla casella 12",
        "- Se i dadi usciti sono il 6 e 3: si va diretti alla casella 26",
        "- Se i dadi usciti sono il 5 e 4: si va diretti alla casella 53",
        "- Se si capita sulla casella 19: si torna alla casella 7",
        "- Se si capita sulla casella 26: si rimane fermi 2 turni",
        "- Se si capita sulla casella 42: si torna alla casella 39",
        "- Se si capita sulla casella 52: si rimane fermi 1 turno",
        "- Se si capita sulla casella 58: si torna alla casella di",
          "partenza(quindi alla casella START)",
        "- Vince chi raggiunge per primo la casella 63, con un lancio esatto,",
        "altrimenti si retrocede dei punti in eccesso",
    ]
    y_pos = 150
    for rule in regole_text:
        text_surface = font_input3.render(rule, True, NERO)  # Utilizza il font personalizzato "Font1.ttf"
        text_rect = text_surface.get_rect(topleft=(50, y_pos))
        schermo.blit(text_surface, text_rect)
        y_pos += 20
    
    testo_conferma = font_regole.render("Premi 0 per confermare la lettura delle regole", True, NERO)
    rettangolo_conferma = testo_conferma.get_rect(center=(larghezza_schermo / 2, altezza_schermo - 100))
    schermo.blit(testo_conferma, rettangolo_conferma)
    
    pygame.display.flip()
    attesa()


def attesa():
    attesa = True
    while attesa:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_0:
                    attesa = False

def gestisci_effetti_casella(posizione_attuale, dado1, dado2):
    somma_dadi = dado1 + dado2
    nuova_posizione = posizione_attuale + somma_dadi

    # Regole speciali per determinate caselle
    if nuova_posizione == 6:
        return 12
    elif dado1== 6 and dado2 == 3 or dado1==3 and dado2==6:
        return 26
    elif dado1== 5 and dado2 == 4 or dado1==4 and dado2==5:
        return 53
    elif nuova_posizione == 19:
        return 7
    elif nuova_posizione == 26:
        return 26, 2  # Rimani fermi per 2 turni
    elif nuova_posizione == 42:
        return 39
    elif nuova_posizione == 52:
        return 52, 1  # Rimani fermo per 1 turno
    elif nuova_posizione == 58:
        return 0  # Torna alla casella di partenza
    elif nuova_posizione > 63:
        # Retrocedi dei punti in eccesso
        nuova_posizione = 63 - (nuova_posizione - 63)
    return nuova_posizione

def main():
    schermata_benvenuto_mostrata = False
    num_giocatori = 0
    while not num_giocatori:
        if not schermata_benvenuto_mostrata:
            mostra_schermata_benvenuto()
            schermata_benvenuto_mostrata = True
        num_giocatori = inserisci_input_giocatori()
    turni_inattivo = [0] * num_giocatori  # Inizializza il conteggio dei turni inattivi
    mostra_schermata_regole()
    posizioni = [0] * num_giocatori  # Inizializza le posizioni dei giocatori a 0
    info_mosse = []
    turno_giocatore = 0
    clock = pygame.time.Clock()
    in_esecuzione = True
    primo_lancio = True
    while in_esecuzione:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                in_esecuzione = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    dado1, dado2 = random.randint(1, 6), random.randint(1, 6)
                    info_mosse.append(f"Giocatore {turno_giocatore+1} tira {dado1} e {dado2} = {dado1 + dado2}")
                    if turni_inattivo[turno_giocatore] == 0:  # Verifica se il giocatore è inattivo
                        nuova_posizione = gestisci_effetti_casella(posizioni[turno_giocatore], dado1, dado2)
                        posizioni[turno_giocatore] = nuova_posizione  # Aggiorna la posizione del giocatore
                        pedine[turno_giocatore] = (pedine[turno_giocatore][0], nuova_posizione)  # Aggiorna la posizione della pedina
                        if posizioni[turno_giocatore] == 52:
                            turni_inattivo[turno_giocatore] = 1  # Fermati per un turno
                        elif posizioni[turno_giocatore] == 26:
                            turni_inattivo[turno_giocatore] = 2  # Fermati per due turni
                        info_mosse[-1] += f" | Nuova posizione: {posizioni[turno_giocatore]}"
                        if posizioni[turno_giocatore] == 63:
                            info_mosse[-1] += " | Vince!"
                            in_esecuzione = False

                    else:
                        info_mosse.append(f"Giocatore {turno_giocatore+1} è inattivo per questo turno")
                        turni_inattivo = [max(0, t - 1) for t in turni_inattivo]  # Riduci il conteggio dei turni inattivi
                    turno_giocatore = (turno_giocatore + 1) % num_giocatori
                    if len(info_mosse) > 20:
                        info_mosse.pop(0)
        disegna_scacchiera(sfondo_tabellone)
        if primo_lancio:  # Disegna la frase solo al primo lancio
            testo_lancio = font.render("Premi SPAZIO per lanciare i dadi", True, NERO)
            schermo.blit(testo_lancio, (10, altezza_schermo - 50))
            primo_lancio = False
        # Disegna info sui dadi sopra la scacchiera
        x_info_dadi = (larghezza_schermo - LARGHEZZA_SCACCHIERA * DIMENSIONE_QUADRATO) // 2
        y_info_dadi = (altezza_schermo - ALTEZZA_SCACCHIERA * DIMENSIONE_QUADRATO) // 2 - 30
        for indice, info in enumerate(info_mosse[::-1]):
            superficie_testo = font.render(info, True, NERO)
            # Ridimensiona la dimensione del testo delle mosse
            superficie_testo = pygame.transform.scale(superficie_testo, (int(superficie_testo.get_width() * 0.5),
                                                                         int(superficie_testo.get_height() * 0.5)))
            schermo.blit(superficie_testo, (x_info_dadi, y_info_dadi - indice * 15))  # Riduci anche lo spazio tra le righe
        # Disegna info sul turno del giocatore corrente
        testo_turno_giocatore = font.render(f"Giocatore {turno_giocatore+1} premi SPAZIO per lanciare i dadi", True, NERO)
        schermo.blit(testo_turno_giocatore, (10, altezza_schermo - 50))
        
        # Controlla se un giocatore ha vinto e mostra la scritta di vittoria
        if any(pos == 63 for pos in posizioni):
            testo_vittoria = font.render("Hai vinto!", True, ROSSO)
            testo_vittoria_grande = pygame.transform.scale(testo_vittoria, (800, 100))
            rettangolo_vittoria = testo_vittoria_grande.get_rect(center=(larghezza_schermo / 2, altezza_schermo / 2))
            schermo.blit(testo_vittoria_grande, rettangolo_vittoria)
            
            # Aggiungi testo per indicare le azioni da compiere
            testo_istruzioni = font.render("Premi ESC per uscire, CTRL per ricominciare", True, NERO)
            rettangolo_istruzioni = testo_istruzioni.get_rect(center=(larghezza_schermo / 2, altezza_schermo / 2 + 200))
            schermo.blit(testo_istruzioni, rettangolo_istruzioni)
            pygame.display.flip()
            while True:
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                        elif evento.key == pygame.K_LCTRL:  # Se viene premuto CTRL
    # Ricomincia il gioco resettando le variabili
                            num_giocatori = 0
                            posizioni = []
                            turni_inattivo = []
                            main()  # Ricomincia il gioco
                            return

                        # Altrimenti, aspetta che l'utente decida di chiudere manualmente
                        # o ricominciare premendo ESC o CTRL
                        # Nessuna istruzione qui per evitare un loop infinito
                        # Il gioco continuerà ad attendere che l'utente prema ESC o CTRL

        pygame.display.flip()
        clock.tick(10)
    pygame.quit()
    sys.exit()  

if __name__ == "__main__":
    main()

 
