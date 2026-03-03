def load_image(path, size, fallback_color=None):
    """Load an image with proper error handling and fallback visualization."""
    try:
        img = pygame.image.load(path)
        img = pygame.transform.scale(img, size)
        return img
    except Exception as e:
        print(f"Failed to load image {path}: {str(e)}")
        
        # Create fallback surface
        surf = pygame.Surface(size)
        if fallback_color:
            surf.fill((50, 50, 50))  # Dark background for contrast
            
            # Determine piece type and color from path
            is_black = 'black' in path.lower()
            piece_color = (200, 0, 0) if is_black else (250, 250, 100)
            
            # Draw different representations for each piece type
            if 'queen' in path.lower():
                # Queen - crown symbol
                center = (size[0]//2, size[1]//2)
                radius = size[0]//3
                pygame.draw.circle(surf, piece_color, center, radius)
                # Crown points
                points = [
                    (center[0], center[1]-radius//2),
                    (center[0]-radius//2, center[1]),
                    (center[0]-radius//4, center[1]-radius//3),
                    (center[0], center[1]-radius//1.5),
                    (center[0]+radius//4, center[1]-radius//3),
                    (center[0]+radius//2, center[1]),
                ]
                pygame.draw.polygon(surf, piece_color, points)
                
            elif 'king' in path.lower():
                # King - cross symbol
                center = (size[0]//2, size[1]//2)
                radius = size[0]//3
                pygame.draw.circle(surf, piece_color, center, radius)
                # Vertical line
                pygame.draw.rect(surf, piece_color, 
                                (center[0]-radius//6, center[1]-radius//1.5, 
                                 radius//3, radius*1.5))
                # Horizontal line
                pygame.draw.rect(surf, piece_color, 
                                (center[0]-radius//1.5, center[1]-radius//6, 
                                 radius*3, radius//3))
                
            else:
                # For other pieces, just draw a circle with letter
                pygame.draw.circle(surf, piece_color, (size[0]//2, size[1]//2), size[0]//3)
                font = pygame.font.SysFont('Arial', size[0]//2)
                text = font.render(path[0].upper(), True, (0, 0, 0))
                surf.blit(text, (size[0]//2-text.get_width()//2, 
                               size[1]//2-text.get_height()//2))
            
            # Add border to make piece visible on any background
            pygame.draw.rect(surf, piece_color, (0, 0, size[0], size[1]), 2)
            
            return surf
        
        # If no fallback color, return transparent surface
        return pygame.Surface(size, pygame.SRCALPHA)

def recolor_image(image, color):
    """Recolor an image while preserving its alpha channel."""
    if image.get_size() == (1, 1):  # Skip if it's a failed load
        return image
        
    colored = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    colored.fill(color)
    
    # Create a mask from the original image's alpha
    mask = pygame.Surface(image.get_size())
    mask.blit(image, (0, 0))
    mask.set_colorkey((0, 0, 0))  # Assuming black is transparent
    
    # Apply the color while preserving the shape
    final = image.copy()
    final.blit(colored, (0, 0), special_flags=pygame.BLEND_MULT)
    final.blit(mask, (0, 0), special_flags=pygame.BLEND_MULT)
    
    return final

# Load pieces with distinct colors and fallbacks
black_queen = load_image('assets/images/black_queen.png', (80, 80), True)
black_king = load_image('assets/images/black_king.png', (80, 80), True)

white_queen = load_image('assets/images/white_queen.png', (80, 80), True)
white_king = load_image('assets/images/white_king.png', (80, 80), True)

# Apply recoloring (optional)
black_queen = recolor_image(black_queen, (200, 50, 50))  # Reddish
black_king = recolor_image(black_king, (50, 50, 200))    # Blueish
white_queen = recolor_image(white_queen, (250, 250, 100)) # Yellowish
white_king = recolor_image(white_king, (100, 250, 100))   # Greenish

# Verify loaded images
def check_image(img, name):
    if img.get_size() == (1, 1):
        print(f"⚠️ {name} failed to load - using fallback")
    else:
        print(f"✓ {name} loaded successfully")

check_image(black_queen, "Black Queen")
check_image(black_king, "Black King")
check_image(white_queen, "White Queen")
check_image(white_king, "White King")