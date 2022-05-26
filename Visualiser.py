from Classes import Neutron, Electron, Proton, Engine, set_force_multiplier, set_speed_limit, set_max_move_per_tick
import pygame


set_force_multiplier(4)
set_speed_limit(100)
set_max_move_per_tick(1)


DARK_GREY = (30, 30, 30)

VECTOR_COLOR = (193, 42, 42)

NEUTRON_COLOR = (198, 198, 198)
NEUTRON_RADIUS = 10

PROTON_COLOR = (192, 32, 32)
PROTON_RADIUS = 10

ELECTRON_COLOR = (90, 90, 0)
ELECTRON_RADIUS = 5


pygame.init()

screen = pygame.display.set_mode()


def drawNeutron(neutron):
    pygame.draw.ellipse(screen, NEUTRON_COLOR, [neutron.position.x - NEUTRON_RADIUS, neutron.position.y - NEUTRON_RADIUS,
                                                NEUTRON_RADIUS*2, NEUTRON_RADIUS*2])
    pygame.draw.line(screen, VECTOR_COLOR, [neutron.position.x, neutron.position.y],
                     [neutron.position.x + neutron.vector.x, neutron.position.y + neutron.vector.y])


def drawProton(proton):
    pygame.draw.ellipse(screen, PROTON_COLOR, [proton.position.x - PROTON_RADIUS, proton.position.y - PROTON_RADIUS,
                                                PROTON_RADIUS*2, PROTON_RADIUS*2])
    pygame.draw.line(screen, VECTOR_COLOR, [proton.position.x, proton.position.y],
                     [proton.position.x + proton.vector.x, proton.position.y + proton.vector.y])


def drawElectron(electron):
    pygame.draw.ellipse(screen, ELECTRON_COLOR,
                        [electron.position.x - ELECTRON_RADIUS, electron.position.y - ELECTRON_RADIUS,
                         ELECTRON_RADIUS * 2, ELECTRON_RADIUS * 2])
    pygame.draw.line(screen, VECTOR_COLOR, [electron.position.x, electron.position.y],
                     [electron.position.x + electron.vector.x * 50, electron.position.y + electron.vector.y * 50])


drawlst = [drawNeutron, drawProton, drawElectron]


def visualise(objects):
    for obj in objects:
        drawlst[obj.t](obj)


running = True


engine = Engine()
clock = pygame.time.Clock()


while running:
    engine.dotick()
    screen.fill(DARK_GREY)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            pass
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                engine.append(Neutron(*event.pos))
            if event.button == pygame.BUTTON_MIDDLE:
                engine.append(Proton(*event.pos))
            if event.button == pygame.BUTTON_RIGHT:
                engine.append(Electron(*event.pos))
            if event.button == 6:
                engine.clear()

    visualise(engine.objects)
    pygame.display.flip()
    clock.tick(144)
