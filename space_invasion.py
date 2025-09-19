import math
import pygame
import random
from pygame import mixer

# Inicializar Pygame
pygame.init()

# Crear la pantalla
pantalla = pygame.display.set_mode((800, 600))

# Titulo e icono
pygame.display.set_caption("Invacion Espacial")
icono = pygame.image.load("assets/espacio-exterior.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load("assets/beautiful-shining-stars-night-sky.jpg")

# Agregar musica
mixer.music.load('assets/MusicaFondo.mp3')
mixer.music.set_volume(0.1)
mixer.music.play(-1)

# Variables jugador
img_jugador = pygame.image.load("assets/cohete-espacial.png")
jugador_x = 368
jugador_y = 500
jugador_x_cambio = 0

# Variables enemigo
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8

for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load("assets/nave-espacial.png"))
    enemigo_x.append(random.randint(0,736))
    enemigo_y.append(random.randint(50,200))
    enemigo_x_cambio.append(0.3)
    enemigo_y_cambio.append(50)

# Variables Bala
balas = []
img_bala = pygame.image.load("assets/bala.png")
bala_x = 0
bala_y = 500
bala_x_cambio = 0
bala_y_cambio = 3
bala_visible = False

# Variable puntaje
puntaje = 0
fuente = pygame.font.SysFont("Bauhaus93", 30)
text_x = 10
text_y = 10

# Pantalla en negro game over
game_over = pygame.image.load("assets/fondo.png")

# Texto final de juego
fuente_final = pygame.font.SysFont("Bauhaus93", 50)

# Texto ganaste el juego
ganaste_juego = pygame.font.SysFont("Bauhaus93", 50)

def texto_ganaste():
    mi_fuente_ganaste = ganaste_juego.render("GANASTE", True, (255,255,255))
    pantalla.blit(mi_fuente_ganaste, (300, 250))

def texto_final():
    mi_fuente_final = fuente_final.render("JUEGO TERMINADO", True, (255,255,255))
    pantalla.blit(mi_fuente_final, (185, 250))

# Funcion mostrar puntake
def mostrar_puntaje(x, y):
    texto = fuente.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
    pantalla.blit(texto, (x, y))

# Funcion jugador
def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))

# Funcion enemigo
def enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))

# Funcion disparar bala
def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 16, y + 10))

# Funcion detectar colisiones
def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_1 - y_2, 2))
    if distancia < 50:
        return True
    else:
        return False

# Loop del juego
se_ejecuta = True
while se_ejecuta:

    # Imagen de fondo
    pantalla.blit(fondo, (0,0))

    # Iterar eventos
    for evento in pygame.event.get():

        # Evento cerrar
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        pygame.event.get(  )
        # Evento presionar flecha izq. - der. o letras 'a' - 'd'
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                jugador_x_cambio = -0.3
            if evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                jugador_x_cambio = 0.3
            if evento.key == pygame.K_SPACE:
                mixer.Sound('assets/disparo.mp3').play().set_volume(0.2)
                nueva_bala = {
                    "x": jugador_x,
                    "y": jugador_y,
                    "velocidad": -2
                }
                balas.append(nueva_bala)

        # Evento soltar flecha izq. - der. o letras 'a' - 'd'
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                jugador_x_cambio = 0
            if evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                jugador_x_cambio = 0


    # Modificar posicion del jugador
    jugador_x += jugador_x_cambio

    # Mantener dentro de bordes al jugador
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736

    # Modificar posicion del enemigo
    for e in range(cantidad_enemigos):

        # Fin del juego
        if puntaje == 50:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            #pantalla.blit(game_over, (0, 0))
            texto_ganaste()
            break
        if enemigo_y[e] > 500:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            #pantalla.blit(game_over, (0, 0))
            texto_final()
            break
        if enemigo_y[e] == jugador_y:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            #pantalla.blit(game_over, (0, 0))
            texto_final()
            break

        enemigo_x[e] += enemigo_x_cambio[e]

    # Mantener dentro de bordes
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 0.3
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -0.3
            enemigo_y[e] += enemigo_y_cambio[e]

        # Colision
        for bala in balas:
            colision_bala_enemigo = hay_colision(enemigo_x[e], enemigo_y[e], bala["x"], bala["y"])
            if colision_bala_enemigo:
                mixer.Sound("assets/Golpe.mp3").play().set_volume(0.2)
                balas.remove(bala)
                puntaje += 1
                enemigo_x[e] = random.randint(0, 736)
                enemigo_y[e] = random.randint(20, 200)
                break

        enemigo(enemigo_x[e], enemigo_y[e], e)

    # Movimiento bala
    for bala in balas:
        bala["y"] += bala["velocidad"]
        pantalla.blit(img_bala, (bala["x"] + 16, bala["y"] + 10))
        if bala["y"] < 0:
            balas.remove(bala)


    jugador(jugador_x, jugador_y)

    mostrar_puntaje(text_x, text_y)

    # Actualizar pantalla
    pygame.display.update()

    # Movimiento del jugador


