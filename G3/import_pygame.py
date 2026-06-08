import pygame
import random  # pa todo lo que necesite numeros aleatorios, como la energia y los obstaculos

# tamaño de la pantalla
pygame.init()
tile_size = 60
board_cells = 15

width = tile_size * board_cells
height = tile_size * board_cells
fondo_original = pygame.image.load("G3/data/fondo.png")
background = pygame.transform.scale(fondo_original, (width, height))

def dibujar_cuadricula():
    for x in range(0, width, tile_size):
        pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, height)) 
    for y in range(0, height, tile_size):
        pygame.draw.line(screen, (40, 40, 40), (0, y), (width, y))

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
text_font = pygame.font.SysFont("Arial", 24)

# Sonidos
sonido_comer = pygame.mixer.Sound("G3/data/comer.wav")
sonido_muerte = pygame.mixer.Sound("G3/data/muerte.wav")

# variable del contador de energia
energia_count = 0

#fuente de texto
font_meme = pygame.font.SysFont("impact", 22)

# Tamaño de la snake
snake_size = tile_size

# tamaño enemigo
enemy_size = 120
enemy_x = (width // 2) - (enemy_size // 2)
enemy_y = 0

# Posición inicial
snake_x = 7 * tile_size
snake_y = 7 * tile_size

# Movimiento
x_change = 0
y_change = 0
angulo_cabeza = 0

# Obstaculos
obstaculos = []
tacho1 = pygame.image.load("G3/data/tacho verde.png")
tacho1 = pygame.transform.scale(tacho1, (tile_size, tile_size))
tacho2 = pygame.image.load("G3/data/tacho negro.png")
tacho2 = pygame.transform.scale(tacho2, (tile_size, tile_size))
modelos_obstaculos = [tacho1, tacho2]

# Inicio del juego
running = True
game_over = False

# Imagen de la pantalla de inicio
imagen_inicio_original = pygame.image.load("G3/data/Fondo Copia.png")
imagen_inicio = pygame.transform.scale(imagen_inicio_original, (width, height))
# Imagen de la pantalla de derrota
imagen_derrota_original = pygame.image.load("G3/data/Fondo Derrota.png")
imagen_derrota = pygame.transform.scale(imagen_derrota_original, (width, height))
# Estados del juego:
estado_juego = "INICIO"

# Imagen cara snake
face_img = pygame.image.load("G3/data/pasted-image.png")
face_img = pygame.transform.scale(face_img, (snake_size, snake_size))

# Imagen cuerpo snake
body_img = pygame.image.load("G3/data/torso.png")
body_img = pygame.transform.scale(body_img, (snake_size, snake_size))

snake_body = []
snake_length = 1

# Imagen planeta (visible)
planeta_img = pygame.image.load("G3/data/pngtree-real-hamburger.png")
planeta_img = pygame.transform.scale(planeta_img, (snake_size, snake_size))

# enemigo vagabundo
homeless_idle = pygame.image.load("G3/data/vagabundo.png")
homeless_idle = pygame.transform.scale(homeless_idle, (enemy_size, enemy_size))

homeless_throw = pygame.image.load("G3/data/vagabundo_2.png")
homeless_throw = pygame.transform.scale(homeless_throw, (enemy_size, enemy_size))

enemy_state = "idle"
enemy_timer = 0
spawn_timer = 0
planeta_spawned = False

# Función spawn planeta
def generar_planeta():
    intentando = True
    while intentando:
        x = random.randrange(0, board_cells) * tile_size
        y = random.randrange(2, board_cells) * tile_size 
        encima_de_obstaculo = False
        for ob in obstaculos:
            if x == ob["pos"][0] and y == ob["pos"][1]:
                encima_de_obstaculo = True
                break
        if not encima_de_obstaculo:
            intentando = False
            return x, y

# contador energia
def contador_energia():
    texto = text_font.render(f"energia: {energia_count}", True, (255, 255, 255))
    screen.blit(texto, (10, 10))

# función lanzar planeta
def lanzar_planeta():
    global planeta_x, planeta_y, enemy_state, enemy_timer, planeta_spawned

    if enemy_state == "throw": return
    enemy_state = "throw"
    enemy_timer = 12
    planeta_spawned = False

planeta_x, planeta_y = generar_planeta()

# Función muerte, para activar la pantalla de game over cuando la snake muere
def activar_muerte():
    global game_over, x_change, y_change
    if not game_over:
        sonido_muerte.play()
        game_over = True
        x_change = 0
        y_change = 0

#Función reiniciar nivel, para colocar la snake y los obstáculos en posiciones aleatorias cada vez que se reinicie el nivel
def reiniciar_nivel():
    global snake_x, snake_y, x_change, y_change, snake_body, snake_length, energia_count, obstaculos
    
    # Spawn aleatorio de la snake
    snake_x = random.randrange(1, board_cells - 1) * tile_size
    snake_y = random.randrange(3, board_cells - 1) * tile_size
    
    x_change = 0
    y_change = 0
    snake_body = []
    snake_length = 1
    energia_count = 0
    
    # Generar los tachos
    obstaculos = []
    for i in range(8): # Número de obstáculos (ideal no mover)
        ob_x = random.randrange(0, board_cells) * tile_size
        ob_y = random.randrange(2, board_cells) * tile_size
        diseño = random.choice(modelos_obstaculos)
        
        if ob_x != snake_x or ob_y != snake_y:
            obstaculos.append({"pos": [ob_x, ob_y], "imagen": diseño})

#Se inicia el nivel llamando a la función reiniciar_nivel para colocar la snake y los obstáculos
reiniciar_nivel()
planeta_x, planeta_y = generar_planeta()

#Velocidad de la snake
contador_pasos = 0
velocidad_snake = 6

# Bucle principal
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
                
            # Controles cuando estas en el INICIO (recien iniciado el juego)
            if estado_juego == "INICIO":
                if event.key == pygame.K_ESCAPE:
                    running = False # En el inicio, ESC cierra el juego
                elif event.key == pygame.K_RETURN:
                    reiniciar_nivel()
                    planeta_x, planeta_y = generar_planeta()
                    game_over = False
                    estado_juego = "JUGANDO"
                elif event.key == pygame.K_i:
                    estado_juego = "INSTRUCCIONES"
                    
            #CONTROLES cuando estás en la pantalla de instrucciones (pa los pollos) 
            elif estado_juego == "INSTRUCCIONES":
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN: 
                    # Con ESC o ENTER vuelves al inicio sin cerrar el juego (Bug que pasaba que si apretabas ESC en las instrucciones se cerraba el juego)
                    estado_juego = "INICIO"
                    
            # Controles pa cuando estas en modo jugar
            elif estado_juego == "JUGANDO":
                if game_over:
                    if event.key == pygame.K_ESCAPE:
                        running = False # Si moriste, ESC cierra el juego
                    elif event.key == pygame.K_r:
                        reiniciar_nivel()
                        planeta_x, planeta_y = generar_planeta()
                        game_over = False
                else:
                    if event.key == pygame.K_ESCAPE:
                        running = False # Jugando en vivo, ESC también cierra el juego
                    elif event.key == pygame.K_a and x_change == 0:
                        x_change = -snake_size
                        y_change = 0
                        angulo_cabeza = 180
                    elif event.key == pygame.K_d and x_change == 0:
                        x_change = snake_size
                        y_change = 0
                        angulo_cabeza = 0
                    elif event.key == pygame.K_w and y_change == 0:
                        y_change = -snake_size
                        x_change = 0
                        angulo_cabeza = 90
                    elif event.key == pygame.K_s and y_change == 0:
                        y_change = snake_size
                        x_change = 0
                        angulo_cabeza = 270
# Acotación de Rick, Se hizo un ajuste para que el inicio del juego tambien dependa del ESTADO_JUEGO, asi no se mueve la snake ni nada hasta que el jugador decida empezar a jugar, y para que no se puedan mover las teclas antes de empezar a jugar diavlo que quedo largo este texto el weso
    if estado_juego == "JUGANDO" and not game_over:
        contador_pasos += 1 
        if contador_pasos >= velocidad_snake:
            snake_x += x_change
            snake_y += y_change
            
            # Colision con obstaculos
            for ob in obstaculos:
                if snake_x == ob["pos"][0] and snake_y == ob["pos"][1]:
                    activar_muerte()
                    break
            
            # Energia 
            if snake_x == planeta_x and snake_y == planeta_y:
                sonido_comer.play()
                snake_length += 1
                energia_count += 1
                lanzar_planeta()

            # Actualización del cuerpo
            snake_head = [snake_x, snake_y]
            snake_body.append(snake_head)
            if len(snake_body) > snake_length:
                del snake_body[0]

            contador_pasos = 0

        # bordes
        if snake_x < 0 or snake_x >= width or snake_y < (tile_size * 2) or snake_y >= height:
            activar_muerte()

        # timer del vagabundo
        spawn_timer += 1
        if spawn_timer >= 480: 
            lanzar_planeta()
            spawn_timer = 0

        # animación enemigo
        if enemy_state == "throw":
            enemy_timer -= 1

            # planeta aparece a mitad del lanzamiento
            if enemy_timer == 6 and not planeta_spawned:
                planeta_x, planeta_y = generar_planeta()
                planeta_spawned = True

            if enemy_timer <= 0:
                enemy_state = "idle"

    # Dibujar todo (Fondo, energia, snake, enemigo)
    screen.fill((0, 0, 0))

    # INICIO DEL JUEGO
    if estado_juego == "INICIO":
        screen.blit(imagen_inicio, (0, 0))

    # MODO INSTRUCCIONES 
    elif estado_juego == "INSTRUCCIONES":
        # fondo oscuro simple para leer bien
        screen.fill((20, 20, 20))
        titulo_ins = font_meme.render("INSTRUCCIONES DE AMBIENTACIÓN", True, (255, 255, 0))
        linea1 = text_font.render("- Usa W, A, S, D para mover al personaje.", True, (255, 255, 255))
        linea2 = text_font.render("- Atrapa los planetas que lanza el vagabundo.", True, (255, 255, 255))
        linea3 = text_font.render("- Evita chocar con los tachos de basura o los bordes.", True, (255, 255, 255))
        linea4 = text_font.render("Presiona ESC o cualquier tecla para volver al menú.", True, (0, 255, 0))
        
        # Dibujar el texto en la pantalla
        screen.blit(titulo_ins, ((width - titulo_ins.get_width()) // 2, 100))
        screen.blit(linea1, (100, 200))
        screen.blit(linea2, (100, 260))
        screen.blit(linea3, (100, 320))
        screen.blit(linea4, ((width - linea4.get_width()) // 2, height - 150))

    # MODO JUGAR ACTIVO Y dibujo de Todo al jugar
    elif estado_juego == "JUGANDO":
        screen.blit(background, (0, 0))
        dibujar_cuadricula()

        # obstaculos
        for ob in obstaculos:
            screen.blit(ob["imagen"], (ob["pos"][0], ob["pos"][1]))

        # planetas (visibles)
        screen.blit(planeta_img, (planeta_x, planeta_y))

        # snake
        for i in range(len(snake_body)):
            if i == len(snake_body) - 1:
                cabeza_rect = face_img.get_rect(topleft=(snake_body[i][0], snake_body[i][1]))
                cabeza_rotada = pygame.transform.rotate(face_img, angulo_cabeza)
                cabeza_rotada_rect = cabeza_rotada.get_rect(center=cabeza_rect.center)
                screen.blit(cabeza_rotada, cabeza_rotada_rect)
            else:
                if i == 0: # Si es la cola
                    cola = pygame.transform.scale(body_img, (snake_size - 20, snake_size - 20))
                    pos_x = snake_body[i][0] + 10
                    pos_y = snake_body[i][1] + 10
                    screen.blit(cola, (pos_x, pos_y))
                else: # Segmento normal del cuerpo
                    screen.blit(body_img, (snake_body[i][0], snake_body[i][1]))

        # enemigo vagabundo dibujo    
        if enemy_state == "idle":
            screen.blit(homeless_idle, (enemy_x, enemy_y))
        else:
            if enemy_timer > 8: w, h = enemy_size + 20, enemy_size - 15
            elif enemy_timer > 4: w, h = enemy_size - 15, enemy_size + 20
            else: w, h = enemy_size, enemy_size

            img_animada = pygame.transform.scale(homeless_throw, (w, h))
            draw_x = enemy_x - (w - enemy_size) // 2
            draw_y = enemy_y + (enemy_size - h)
            screen.blit(img_animada, (draw_x, draw_y))

            grito = font_meme.render("!FABIAN, ATRAPA!", True, (255, 0, 0))
            screen.blit(grito, (enemy_x - 30, enemy_y + 60))
        
        # Mostrar el puntaje solo mientras se juega
        contador_energia()

        # Cartel de Game Over (se dibuja encima si pierdes)
        if game_over:
            screen.blit(imagen_derrota, (0, 0))

    pygame.display.update()
    clock.tick(40)

pygame.quit()
