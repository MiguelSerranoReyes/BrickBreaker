# Bibliotecas a importar
import pygame
import os, sys

# Inicializar Pygame
pygame.init()

# Crear un reloj para controlar la velocidad de actualización de la pantalla
reloj = pygame.time.Clock()

# Crear la pantalla del juego con tamaño 800x600
pantalla = pygame.display.set_mode((800, 600))

# Establecer el título de la ventana del juego
pygame.display.set_caption('Brick Breaker')

# Crear un color negro para usarlo en la pantalla
negro = pygame.Color(0,0,0)

# Cargar la imagen de la plataforma del jugador
plataforma = pygame.image.load('plataforma.png')

# Obtener las dimensiones de la imagen de la plataforma
plataforma_area = plataforma.get_rect()

# Establecer la coordenada y del jugador
coord_y_jugador = 540

# Establecer la posición inicial del ratón
coord_x_raton, coord_y_raton = (0, coord_y_jugador)

# Cargar la imagen de la pelota
pelota = pygame.image.load('ball.png')

# Obtener las dimensiones de la imagen de la pelota
pelota_area = pelota.get_rect()

# Establecer la posición inicial de la pelota
coord_x_pelota, coord_y_pelota = (24, 200)

# Establecer la posición de la pelota en la pantalla
pelota_area.topleft = (coord_x_pelota, coord_y_pelota)

# Establecer el estado inicial de la pelota
pelota_servida = False
pelota_velocidad = 5
velocidad_x, velocidad_y = (pelota_velocidad, pelota_velocidad)

# Cargar la imagen del ladrillo
ladrillo = pygame.image.load('brick.png')

# Obtener las dimensiones del ladrillo
ancho = ladrillo.get_width()
alto = ladrillo.get_height()

# Crear una lista de ladrillos
ladrillos = []

# Crear los ladrillos y añadirlos a la lista
for y in range(5):
    coord_ladrillo_y = (y * 24) + 100
    for x in range(10):
        coord_ladrillo_x = (x * 31) + 245
        ladrillo_area = pygame.Rect(coord_ladrillo_x, coord_ladrillo_y, ancho, alto)
        ladrillos.append(ladrillo_area)

# Bucle principal del juego
while True:
    
    # Llenar la pantalla con color negro
    pantalla.fill(negro)
    
    # Dibujar la plataforma del jugador
    pantalla.blit(plataforma, plataforma_area)
    
    # Dibujar la pelota
    pantalla.blit(pelota, pelota_area)
    
    # Dibujar los ladrillos
    for lad_area in ladrillos:
        pantalla.blit(ladrillo, lad_area)
        
    # Manejar los eventos del juego
    for evento in pygame.event.get():
        # Si se presiona el botón de salir, cerrar el juego
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Si se suelta el botón del ratón y la pelota aún no se ha servido, comenzar el juego
        elif evento.type == pygame.MOUSEBUTTONUP and not pelota_servida:
            pelota_servida = True
        # Si se mueve el ratón, mover la plataforma del jugador
        elif evento.type==pygame.MOUSEMOTION:
            coord_x_raton,coord_y_raton=evento.pos
            if coord_x_raton<800-55:
                plataforma_area.topleft=(coord_x_raton,coord_y_jugador)
            else:
                plataforma_area.topleft=(800-55,coord_y_jugador)
    
    #Actualizar la posición de la pelota si ha sido servida
    if pelota_servida:
        coord_x_pelota+=velocidad_x
        coord_y_pelota+=velocidad_y
        pelota_area.topleft=(coord_x_pelota,coord_y_pelota)
    
    #Si la pelota toca la parte inferior de la pantalla
    if coord_y_pelota>=600-8:
        pelota_servida=False
        coord_x_pelota,coord_y_pelota=(24,200)
        velocidad_x,velocidad_y=(pelota_velocidad,
                                 pelota_velocidad)
        pelota_area.topleft=(coord_x_pelota,coord_y_pelota)
    
    #Si la pelota toca alguna coordenada de la plataforma
    if pelota_area.colliderect(plataforma_area):
        coord_y_pelota=coord_y_jugador-8
        velocidad_y*=-1
        
    #Si la pelota toca el lado derecho de la pantalla
    if coord_x_pelota>=800-8:
        coord_x_pelota=800-8
        velocidad_x*=-1
        
    #Si la pelota toca la parte superior de la pantalla
    if coord_y_pelota<=0:
        coord_y_pelota=0
        velocidad_y*=-1
     
    #Si la pelota toca la parte izquierda de la pantalla
    if coord_x_pelota<=0:
        coord_x_pelota=0
        velocidad_x*=-1
    
    #Si la pelota toca un ladrillo
    i=pelota_area.collidelist(ladrillos)
    if i>=0:
        ladrillo_golpeado=ladrillos[i]
        m_x=coord_x_pelota+4
        m_y=coord_y_pelota+4
        lg=ladrillo_golpeado
        if m_x>lg.x+lg.width or m_x<lg.x:
            velocidad_x*=-1
        else:
            velocidad_y*=-1
        del ladrillos[i]
    
    # Actualizar la pantalla
    pygame.display.update()
    
    # Establecer la velocidad de actualización de la pantalla
    reloj.tick(30)