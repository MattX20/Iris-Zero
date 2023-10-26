import pygame


def draw_button(screen, button_rect, button_color, hover_color, text, text_color, is_clicked=False):
    """This function creates a simple pygame button on the screen."""
    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos) and not is_clicked:
        pygame.draw.rect(screen, hover_color, button_rect)
    elif is_clicked:
        pygame.draw.rect(screen, hover_color, button_rect)
    else:
        pygame.draw.rect(screen, button_color, button_rect)

    font = pygame.font.Font(None, 24)
    text_surface = font.render(text, True, text_color)
    text_x = button_rect.x + (button_rect.width -
                              text_surface.get_width()) // 2
    text_y = button_rect.y + (button_rect.height -
                              text_surface.get_height()) // 2
    screen.blit(text_surface, (text_x, text_y))


def draw_text(screen, text, x, y, color):
    """This functions print texts on the pygame screen."""
    font = pygame.font.Font(None, 32)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_circle_with_number(screen, position, radius, number, circle_color, text_color):
    """Draw a circle and a number just above it on the pygame screen."""
    # Draw the circle
    pygame.draw.circle(screen, circle_color, position, radius)

    # Render the number as text
    font = pygame.font.Font(None, 24)
    text_surface = font.render(str(number), True, text_color)

    # Calculate the position of the text below the circle
    text_x = position[0] - text_surface.get_width() / 2 + radius
    text_y = position[1] - text_surface.get_height() - radius / 2

    # Draw the text on the screen
    screen.blit(text_surface, (text_x, text_y))
