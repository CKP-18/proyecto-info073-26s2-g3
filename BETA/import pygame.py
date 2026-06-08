import pygame
import random  # pa todo lo que necesite numeros aleatorios, como la comida y los obstaculos

# tamaño de la pantalla
pygame.init()
tile_size = 60
board_cells = 15

width = tile_size * board_cells
height = tile_size * board_cells
fondo_original = pygame.image.load("assets/fondo.png")
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
sonido_comer = pygame.mixer.Sound("assets/comer.wav")
sonido_muerte = pygame.mixer.Sound("assets/muerte.wav")

# variable del contador de comida
food_count = 0

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

# Obstaculos
obstaculos = []
tacho1 = pygame.image.load("assets/tacho verde.png")
tacho1 = pygame.transform.scale(tacho1, (tile_size, tile_size))
tacho2 = pygame.image.load("assets/tacho negro.png")
tacho2 = pygame.transform.scale(tacho2, (tile_size, tile_size))
modelos_obstaculos = [tacho1, tacho2]

# Inicio del juego
running = True
game_over = False

# Imagen cara snake
face_img = pygame.image.load("assets/pasted-image.png")
face_img = pygame.transform.scale(face_img, (snake_size, snake_size))

snake_body = []
snake_length = 1

# Imagen comida
food_img = pygame.image.load("assets/pngtree-real-hamburger.png")
food_img = pygame.transform.scale(food_img, (snake_size, snake_size))

# enemigo vagabundo
homeless_idle = pygame.image.load("assets/vagabundo.png")
homeless_idle = pygame.transform.scale(homeless_idle, (enemy_size, enemy_size))

homeless_throw = pygame.image.load("assets/vagabundo_2.png")
homeless_throw = pygame.transform.scale(homeless_throw, (enemy_size, enemy_size))

enemy_state = "idle"
enemy_timer = 0
spawn_timer = 0
food_spawned = False

# Función spawn comida
def generar_comida():
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

# contador comida
def contador_comida():
    texto = text_font.render(f"comida: {food_count}", True, (255, 255, 255))
    screen.blit(texto, (10, 10))

# función lanzar hamburguesa
def lanzar_hamburguesa():
    global food_x, food_y, enemy_state, enemy_timer, food_spawned

    if enemy_state == "throw": return
    enemy_state = "throw"
    enemy_timer = 12
    food_spawned = False

food_x, food_y = generar_comida()

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
    global snake_x, snake_y, x_change, y_change, snake_body, snake_length, food_count, obstaculos
    
    # Spawn aleatorio de la snake
    snake_x = random.randrange(1, board_cells - 1) * tile_size
    snake_y = random.randrange(3, board_cells - 1) * tile_size
    
    x_change = 0
    y_change = 0
    snake_body = []
    snake_length = 1
    food_count = 0
    
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
food_x, food_y = generar_comida()

#Velocidad de la snake
contador_pasos = 0
velocidad_snake = 6

# Bucle principal
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif game_over:
                if event.key == pygame.K_r:
                    reiniciar_nivel()
                    food_x, food_y = generar_comida()
                    game_over = False
            else:
                if event.key == pygame.K_a and x_change == 0:
                    x_change = -snake_size
                    y_change = 0
                elif event.key == pygame.K_d and x_change == 0:
                    x_change = snake_size
                    y_change = 0
                elif event.key == pygame.K_w and y_change == 0:
                    y_change = -snake_size
                    x_change = 0
                elif event.key == pygame.K_s and y_change == 0:
                    y_change = snake_size
                    x_change = 0

    if not game_over:
        contador_pasos += 1 
        if contador_pasos >= velocidad_snake:
            snake_x += x_change
            snake_y += y_change
            
            # Colision con obstaculos
            for ob in obstaculos:
                if snake_x == ob["pos"][0] and snake_y == ob["pos"][1]:
                    activar_muerte()
                    break
            
            # Comida 
            if snake_x == food_x and snake_y == food_y:
                sonido_comer.play()
                snake_length += 1
                food_count += 1
                lanzar_hamburguesa()

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
            lanzar_hamburguesa()
            spawn_timer = 0

        # animación enemigo
        if enemy_state == "throw":
            enemy_timer -= 1

            # hamburguesa aparece a mitad del lanzamiento
            if enemy_timer == 6 and not food_spawned:
                food_x, food_y = generar_comida()
                food_spawned = True

            if enemy_timer <= 0:
                enemy_state = "idle"

    # Dibujar todo (Fondo, comida, snake, enemigo)
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    dibujar_cuadricula()

    #obstaculos
    for ob in obstaculos:
        screen.blit(ob["imagen"], (ob["pos"][0], ob["pos"][1]))

    # comida
    screen.blit(food_img, (food_x, food_y))

    # snake
    for i in range(len(snake_body)):
        if i == len(snake_body) - 1:
            screen.blit(face_img, (snake_body[i][0], snake_body[i][1]))
        else:
            pygame.draw.rect(screen,(0, 255, 0), [snake_body[i][0], snake_body[i][1], snake_size, snake_size])

# enemigo vagabundo dibujo    
    if enemy_state == "idle":
        screen.blit(homeless_idle, (enemy_x, enemy_y))

    else:
        # efecto resorte
        if enemy_timer > 8:
            w, h = enemy_size + 20, enemy_size - 15

        elif enemy_timer > 4:
            w, h = enemy_size - 15, enemy_size + 20

        else:
            w, h = enemy_size, enemy_size

        img_animada = pygame.transform.scale(homeless_throw, (w, h))

        # para que lanze desde el centro del vagabundo y mantenga la base en la misma posición
        draw_x = enemy_x - (w - enemy_size) // 2
        draw_y = enemy_y + (enemy_size - h)

        screen.blit(img_animada, (draw_x, draw_y))

        grito = font_meme.render("!FABIAN, ATRAPA!", True, (255, 0, 0))
        screen.blit(grito, (enemy_x - 30, enemy_y + 60))
    
    if game_over:
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        game_over_text = text_font.render("GAME OVER", True, (255, 255, 255))
        restart_text = text_font.render("Presiona R para reiniciar", True, (255, 255, 255))
        quit_text = text_font.render("Presiona ESC para salir", True, (255, 255, 255))

        screen.blit(game_over_text, ((width - game_over_text.get_width()) // 2, height // 2 - 60))
        screen.blit(restart_text, ((width - restart_text.get_width()) // 2, height // 2))
        screen.blit(quit_text, ((width - quit_text.get_width()) // 2, height // 2 + 40))
    
    contador_comida()

    pygame.display.update()

    clock.tick(30)

pygame.quit()