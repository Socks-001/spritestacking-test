import pygame
import math

pygame.init()

class screen_setup:
    screen_size = 256
    screen = pygame.display.set_mode((screen_size, screen_size), pygame.SCALED)
    pygame.display.set_caption("Sprite Stack Test")


class SpriteStackTest:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.screen_size = self.screen.get_size()
        self.clock = pygame.time.Clock()
        self.debug_slice = 0  # Start with full stack display
        self.debug_enabled = False
        self.input_cooldown = 20  # Cooldown in milliseconds
        self.last_input_time = 0  # Tracks the last time an input was processed

        # Load the horizontal sprite sheets
        self.blue_car_sprite_sheet = pygame.image.load("ss_blue_car.png").convert_alpha()
        self.green_car_sprite_sheet = pygame.image.load("ss_green_car.png").convert_alpha()
        self.green_truck_sprite_sheet = pygame.image.load("ss_green_truck.png").convert_alpha()
        self.barrel_sprite_sheet = pygame.image.load("ss_barrel.png").convert_alpha()
        self.chest_sprite_sheet = pygame.image.load("ss_chest.png").convert_alpha()
        self.stairs_sprite_sheet = pygame.image.load("ss_stairs.png").convert_alpha()

        self.sprites = [
            self.blue_car_sprite_sheet,
            self.green_car_sprite_sheet,
            self.green_truck_sprite_sheet,
            self.barrel_sprite_sheet,
            self.chest_sprite_sheet,
            self.stairs_sprite_sheet,
        ]

        self.sprite_index = 0  # Start with the first sprite sheet
        self.current_sprite = self.sprites[self.sprite_index]  # Use only the selected sprite sheet
        # Modifiable parameters
        self.mod_perspective = 45
        self.mod_scale = 1.0
        self.mod_spacing = 1.0
        self.mod_angle = 0

        # Define locations
        location_topleft = (32, 32)
        location_bottomright = (self.screen_size[0] - 32, self.screen_size[1] - 32)
        location_center = (self.screen_size[0] / 2, self.screen_size[1] / 2)
        location_bottomleft = (32, self.screen_size[1] - 32)
        location_topright = (self.screen_size[0] - 32, 32)
        self.locations = [location_topleft, location_bottomright, location_center, location_bottomleft, location_topright]

    def get_slices(self, sheet):
        slice_length = min(sheet.get_width(), sheet.get_height())
        slices = []
        for i in range(sheet.get_width() // slice_length):
            rect = pygame.Rect(i * slice_length, 0, slice_length, slice_length)
            image = sheet.subsurface(rect).copy()
            slices.append(image)
        return slices

    def draw_stack_with_optional_rotation(self, x, y, sprite_sheet, angle, scale=1.0, height_spacing=1.0, perspective=60, rotate=True):
        """
        Draw the rotated stack or a specific slice for debugging.
        """
        slices = self.get_slices(sprite_sheet)
        perspective_scale = math.cos(math.radians(perspective))
        height_offset = height_spacing * scale

        # If debugging a specific slice, limit to that slice
        if self.debug_enabled is True:
            slices = [slices[self.debug_slice]]

        rotated_slices = []

        for i, layer in enumerate(slices):
            # Rotate the layer
            if rotate:
                rotated_layer = pygame.transform.rotate(layer, angle)  # Create a rotated version of the layer
                rotated_slices.append(rotated_layer)  # Store it in the rotated_slices list
            else:
                rotated_slices.append(layer)  # Keep original layer if no rotation

        # Blit each rotated layer
        for i, layer in enumerate(rotated_slices):
            self.screen.blit(layer, (x - layer.get_width() / 2, (y - layer.get_height() / 2) - i * height_offset))

    def handle_input(self):
        """Handles input with a cooldown."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_input_time < self.input_cooldown:
            return  # Skip input processing if still in cooldown

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.mod_angle += 1  # Rotate counterclockwise
        if keys[pygame.K_RIGHT]:
            self.mod_angle -= 1  # Rotate clockwise
        self.mod_angle %= 360

        # Debug slice controls
        if keys[pygame.K_UP]:
            # Increment the debug slice index
            sprite_slices = len(self.get_slices(self.current_sprite))
            self.debug_slice = (self.debug_slice + 1) % len(self.get_slices(self.sprites[0]))  # Wrap around on increment
        if keys[pygame.K_DOWN]:
            # Decrement (handle negative indices correctly)
            sprite_slices = len(self.get_slices(self.current_sprite))
            self.debug_slice = (self.debug_slice - 1) % sprite_slices
        if keys[pygame.K_d]:
            sprite_slices = len(self.get_slices(self.current_sprite))
            self.sprite_index = (self.sprite_index + 1) % len(self.sprites)
            self.current_sprite = self.sprites[self.sprite_index]
        if keys[pygame.K_a]:  # Cycle through sprites
            sprite_slices = len(self.get_slices(self.current_sprite))
            self.sprite_index = (self.sprite_index - 1) % len(self.sprites)
            self.current_sprite = self.sprites[self.sprite_index]
        if keys[pygame.K_SPACE]:
            self.debug_enabled = not self.debug_enabled  # Reset to full stack display

        # Update the last input time
        self.last_input_time = current_time

    def update(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    exit()

            # Handle input with cooldown
            self.handle_input()

            self.screen.fill((30, 30, 30))

            for location in self.locations:
                pos_x, pos_y = location
                sprite = self.current_sprite  # Use the stairs sprite sheet for all locations
                self.draw_stack_with_optional_rotation(pos_x, pos_y, sprite, self.mod_angle, self.mod_scale, self.mod_spacing, self.mod_perspective, True)
            pygame.display.flip()
            self.clock.tick(60)

# Run the program
if __name__ == "__main__":
    app = SpriteStackTest()
    app.update()