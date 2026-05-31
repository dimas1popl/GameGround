import pygame

pygame.init()

pygame.font.init()
font = pygame.font.SysFont(None, 24)

display = pygame.display.set_mode((800, 600))
pygame.display.set_caption('game')

dollar = 0

box_w1, box_h1 = 100, 100
GRID_ROWS = 4
GRID_COLS = 4
START_X, START_Y = 30, 30
GAP = 2

menu = pygame.image.load("menu.png")
menu_resized = pygame.transform.scale(menu, (100, 50))

serp = pygame.image.load("serp.png")
serp_resized = pygame.transform.scale(serp, (94, 92))
serp_hand = pygame.transform.scale(serp, (47, 46))
seeds_green = pygame.image.load("seeds_green.png")
seeds_green_resized = pygame.transform.scale(seeds_green, (52, 88))
seeds_green_hand = pygame.transform.scale(seeds_green, (26, 44))

dirt_images = []
for i in range(7):
    img = pygame.image.load(f"dirt{i}.png")
    img_resized = pygame.transform.scale(img, (box_w1, box_h1))
    dirt_images.append(img_resized)

plots = []
for row in range(GRID_ROWS):
    for col in range(GRID_COLS):
        px = START_X + col * (box_w1 + GAP)
        py = START_Y + row * (box_h1 + GAP)

        plot_data = {
            "x": px,
            "y": py,
            "current_dirt_index": 0,
            "growth_active": 0,
            "current_wait_time": 15 * 1000,
            "step_increase": 5 * 1000,
            "start_time": 0,
            "seconds_left": 2
        }
        plots.append(plot_data)

grab = 0
is_on = True
clock = pygame.time.Clock()


def rect_info(mx, my, time_left):
    display.blit(menu_resized, (mx + 5, my + 10))
    if time_left > 0:
        text_string = f"Время: {time_left}s"
    else:
        text_string = "Макс. рост"
    text_surface = font.render(text_string, True, (0, 0, 0))
    display.blit(text_surface, (mx + 14, my + 21))


def check_mouse_area_ground(x1, y1, x2, y2):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    return x1 <= mouse_x <= x2 and y1 <= mouse_y <= y2


while is_on:
    clock.tick(60)
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_on = False

    for plot in plots:
        if plot["growth_active"] == 1:
            time_passed = current_time - plot["start_time"]

            if plot["current_dirt_index"] < 6:
                plot["seconds_left"] = (plot["current_wait_time"] - time_passed + 999) // 1000

                if time_passed >= plot["current_wait_time"]:
                    plot["current_dirt_index"] += 1
                    plot["start_time"] = current_time
                    plot["current_wait_time"] += plot["step_increase"]
            else:
                plot["seconds_left"] = 0
        else:
            plot["seconds_left"] = plot["current_wait_time"] // 1000

    mouse_x_game, mouse_y_game = pygame.mouse.get_pos()
    display.fill((1, 50, 32))

    for plot in plots:
        display.blit(dirt_images[plot["current_dirt_index"]], (plot["x"], plot["y"]))

        is_hovered = check_mouse_area_ground(plot["x"], plot["y"], plot["x"] + box_w1, plot["y"] + box_h1)

        if grab == 1 and pygame.mouse.get_pressed()[0] and is_hovered and plot["growth_active"] == 0:
            plot["growth_active"] = 1
            plot["start_time"] = current_time
            plot["current_wait_time"] = 2 * 1000
            grab = 0

        if grab == 2 and pygame.mouse.get_pressed()[0] and is_hovered and plot["seconds_left"] <= 0 and plot["growth_active"] == 1:
            plot["growth_active"] = 0
            plot["current_dirt_index"] = 0
            grab = 0
            dollar += 25

    for plot in plots:
        is_hovered = check_mouse_area_ground(plot["x"], plot["y"], plot["x"] + box_w1, plot["y"] + box_h1)
        if plot["growth_active"] == 1 and is_hovered:
            rect_info(mouse_x_game, mouse_y_game, plot["seconds_left"])
    dollar_text = f"Денег: {dollar}"
    dollar_surface = font.render(dollar_text, True, (144, 238, 144))
    display.blit(dollar_surface, (600, 30))

    display.blit(seeds_green_resized, (700, 200))
    full_grand_text = f"Засеять всё"
    full_grand_surface = font.render(full_grand_text, True, (144, 238, 144))
    display.blit(full_grand_surface, (640, 170))

    if pygame.mouse.get_pressed()[0] and check_mouse_area_ground(640, 170, 800, 190):
        for plot in plots:
            if plot["growth_active"] == 0:
                plot["growth_active"] = 1
                plot["start_time"] = current_time
                plot["current_wait_time"] = 2 * 1000

    if pygame.mouse.get_pressed()[2] and check_mouse_area_ground(700, 200, 752, 288):
        grab = 1

    if grab == 1:
        display.blit(seeds_green_hand, (mouse_x_game, mouse_y_game))

    display.blit(serp_resized, (650, 300))
    if pygame.mouse.get_pressed()[2] and check_mouse_area_ground(650, 300, 744, 392):
        grab = 2

    if grab == 2:
        display.blit(serp_hand, (mouse_x_game, mouse_y_game))

    if pygame.mouse.get_pressed()[1]:
        grab = 0

    pygame.display.update()

pygame.quit()
quit()
