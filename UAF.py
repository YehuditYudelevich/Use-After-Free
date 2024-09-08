import pygame
import sys
import random

pygame.init()
width, height = 1000, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Animation12")

colors = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "blue": (100, 149, 237),  # Cornflower blue
    "red": (255, 99, 71),  # Tomato red
    "green": (60, 179, 113),  # Medium sea green
    "gray": (169, 169, 169),  # Dark gray
    
    "pink": (255, 255, 224),  # Light yellow
}

def create_object(x, y, color, word):
  
    pygame.draw.rect(screen, color, (x, y, 100, 80), border_radius=30)
    pygame.draw.rect(screen, (0, 0, 0), (x, y, 100, 80), 5, border_radius=30)
    font = pygame.font.Font(None, 40)
    text = font.render(word, True, colors['black'])
    text_rect = text.get_rect(center=(x+50, y+40))
    screen.blit(text, text_rect)

def draw_arrow(x, y):
    pygame.draw.polygon(screen, colors['red'], [(x, y), (x+30, y), (x+15, y-25)])
    pygame.draw.rect(screen, colors['red'], (x+10, y, 10, 20))

def touch_the_box(start_x, start_y, box_x, box_y, word):
    x, y = start_x, start_y
    while y > box_y + 120 or x < box_x + 35:  # Move arrow to touch the box from below
        screen.fill(colors['pink'])
        draw_all_objects()
        if y > box_y + 120:
            y -= 2
        elif x < box_x + 35:
            x += 5
        draw_arrow(x, y)
        pygame.display.flip()
        pygame.time.delay(10)
    
    # Pause to show the arrow touching the box
    pygame.time.delay(100)
    
    if word == 'in use':
        objects[box_x//200]['color'] = colors['gray']
        objects[box_x//200]['word'] = 'Freed'
        objects[box_x//200]['y'] += 100
    if word == 'free':

        broke_the_box(box_x, box_y)
    
    return x, y  # Return the final position of the arrow

    
def broke_the_box(x, y):
    pieces = [(x, y+50), (x+50, y+50), (x, y+90), (x+50, y+90)]
    
    for i in range(4):
        piece_y = y
        while piece_y < height:
            screen.fill(colors['pink'])
            draw_all_objects()
            font = pygame.font.Font(None, 30)
            text = font.render("Trying to Use After Free", True, colors['red'])
            screen.blit(text, (x-20, y-40))

            for j in range(i+1, 4):
                pygame.draw.rect(screen, colors['gray'], (pieces[j][0], pieces[j][1], 50, 40))
        
            if piece_y < height-70:
                pygame.draw.rect(screen, colors['gray'], (pieces[i][0], piece_y, 50, 40))
            
            pygame.display.flip()
            pygame.time.delay(10)
            piece_y += 30          
       
        pygame.time.delay(10)
    
    objects[x//200]['broken'] = True

def draw_all_objects():
    font=pygame.font.Font(None, 40)
    text=font.render("Heap Memory", True, colors['red'])
    screen.blit(text, (20, 20))
    font=pygame.font.Font(None, 30)
    text=font.render("The green rectangles are memory that we allocated and is in use", True, colors['red'])
    screen.blit(text, (20, 400))
    font=pygame.font.Font(None, 30)
    text=font.render("The gray rectangles represent memory that has been freed.", True, colors['red'])
    screen.blit(text, (20, 425))
    for obj in objects:
        if not obj['broken']:
            create_object(obj['x'], obj['y'], obj['color'], obj['word'])

def main_process():
    global objects
    objects = [{'x': 50 + i*200, 'y': 100, 'color': colors['green'], 'word': 'in use', 'broken': False} for i in range(5)]
   
    draw_all_objects()
    pygame.display.flip()
    pygame.time.delay(30)

    arrow_x, arrow_y = 0, 300  # Starting position of the arrow at the bottom

    for i in range(5):
        arrow_x, arrow_y = touch_the_box(arrow_x, arrow_y, 50 + i*200, 50, 'in use')

    pygame.time.delay(70)

    arrow_x, arrow_y = 0, 400 # Reset arrow position for the second phase
    for i in range(5):
        arrow_x, arrow_y = touch_the_box(arrow_x, arrow_y, 50 + i*200, 150, 'free')
    screen.fill(colors['pink'])
    font = pygame.font.Font(None, 80)
    text = font.render("Use After Free", True, colors['red'])
    text_rect = text.get_rect(center=(width//2, height//2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.delay(3000)
    


def main():
    main_process()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()