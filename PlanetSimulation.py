import pygame
import math

# Initialize Pygame
pygame.init()

# Set window dimensions
win_width, win_height = 2000, 1000
pygame_win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Planet Simulation")
FONT = pygame.font.SysFont("Verdana",16)

class Planet:
    # Assigning constant values
    AstroUnit = 149.6e6 * 1000  # Distance of Earth from the Sun in meters
    G = 6.67428e-11
    base_scale = 250 / AstroUnit  

    timeStep = 3600 * 24  # ~ Number of seconds in an hour X 24 = 1 day in seconds

    def __init__(self, x, y, radius, color, mass, planetname, scale_factor=1.0):
        self.x = x  
        self.y = y  
        self.radius = radius
        self.color = color
        self.name = planetname
        self.mass = mass
        self.scale_factor = scale_factor  

        self.orbit = []
        self.Sun = False
        self.distance_to_Sun = 0
        self.x_val = 0
        self.y_val = 0

    def draw(self, pygame_win):
        scale = self.base_scale * self.scale_factor

        x = int(self.x * scale + win_width / 2)
        y = int(self.y * scale + win_height / 2)

        # Draw orbit path
        if len(self.orbit) >= 2:
            updated_point = [(int(px * scale + win_width / 2), int(py * scale + win_height / 2)) for px, py in self.orbit]
            pygame.draw.lines(pygame_win, self.color, False, updated_point, 1)
        name_text = FONT.render(self.name, 1, (255, 255, 255))
        pygame_win.blit(name_text, (x + 10, y - 20))
        if not self.Sun:
            distance_text = FONT.render(f"{round(self.distance_to_Sun/1000,1)}km",1,(255,192,203))
            pygame_win.blit(distance_text,(x,y))

        # Draw the planet
        pygame.draw.circle(pygame_win, self.color, (x, y), self.radius)

    def attraction(self, other):
        distance_x = other.x - self.x
        distance_y = other.y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.Sun:
            self.distance_to_Sun = distance

        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        return math.cos(theta) * force, math.sin(theta) * force

    def update_pos(self, planets):
        total_fx = total_fy = 0

        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_val += total_fx / self.mass * self.timeStep
        self.y_val += total_fy / self.mass * self.timeStep

        self.x += self.x_val * self.timeStep
        self.y += self.y_val * self.timeStep

        self.orbit.append((self.x, self.y))

def main():
    run = True
    clock = pygame.time.Clock()

    # Sun
    sun = Planet(0, 0, 30, (255, 255, 0), 1.98892 * 10**30,"")
    sun.Sun = True

    Mercury = Planet(0.387 * Planet.AstroUnit, 0, 4, (112, 128, 144), 3.285 * 10**23,"Mercury", scale_factor=1.5)
    Mercury.y_val = -47.4 * 1000  

    Venus = Planet(0.72 * Planet.AstroUnit, 0, 6, (255, 69, 0), 4.87 * 10**24,"Venus", scale_factor=1.5)
    Venus.y_val = -35.02 * 1000

    Earth = Planet(-1 * Planet.AstroUnit, 0, 8, (30, 144, 255), 5.9742 * 10**24,"Earth", scale_factor=1.5)
    Earth.y_val = 29.783 * 1000

    Mars = Planet(-1.524 * Planet.AstroUnit, 0, 6, (178, 34, 34), 6.39 * 10**23,"Mars", scale_factor=1.5)
    Mars.y_val = 24.077 * 1000

    Jupiter = Planet(5.20 * Planet.AstroUnit, 0, 12, (197, 179, 88), 1.898 * 10**27,"Jupiter", scale_factor=0.5)
    Jupiter.y_val = 13.07 * 1000

    Saturn = Planet(9.58 * Planet.AstroUnit, 0, 10, (238, 232, 170), 5.68 * 10**26,"Saturn", scale_factor=0.3)
    Saturn.y_val = 9.69 * 1000

    Uranus = Planet(19.18 * Planet.AstroUnit, 0, 8, (95, 158, 160), 8.68 * 10**25,"Uranus", scale_factor=0.2)
    Uranus.y_val = 6.81 * 1000

    Neptune = Planet(30.07 * Planet.AstroUnit, 0, 8, (0, 0, 255), 1.02 * 10**26,"Neptune", scale_factor=0.1)
    Neptune.y_val = 5.43 * 1000

    planets = [sun, Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune]

    while run:
        clock.tick(60)
        pygame_win.fill((0, 0, 0))  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False  

        for planet in planets:
            planet.update_pos(planets)
            planet.draw(pygame_win)

        pygame.display.update()  

    pygame.quit()

main()
