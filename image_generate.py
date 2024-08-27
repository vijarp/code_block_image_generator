from PIL import Image, ImageDraw, ImageFont

# Function to draw code block with glow effect
def draw_code_block_with_glow(draw, text, font, keywords_color_mapping, start_x=50, start_y=80, line_height=40):
    lines = text.splitlines()
    y = start_y
    
    # Define shadow color for glow effect
    shadow_color = (50, 50, 50, 100)  # RGBA color (adjust as needed)
    
    for line in lines:
        words = line.split(" ")
        x = start_x
        for word in words:
            color = keywords_color_mapping.get(word.upper(), (255, 255, 255))  # Default to white color
            
            # Draw the shadow (glow) around the text
            for dx, dy in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
                draw.text((x + dx, y + dy), word, font=font, fill=shadow_color)
            
            # Draw the main text
            draw.text((x, y), word, font=font, fill=color)
            
            # Calculate the width of the text
            bbox = draw.textbbox((x, y), word, font=font)
            text_width = bbox[2] - bbox[0]
            x += text_width + draw.textbbox((0, 0), " ", font=font)[2]  # Add space width
        y += line_height

# Define the code text and colors for SQL keywords
code_text = """SELECT 
    c.customer_name, 
    IFNULL(SUM(o.amount), 0) AS total_order_value
FROM 
    customers c
LEFT JOIN 
    orders o ON c.customer_id = o.customer_id 
    AND MONTH(o.order_date) = MONTH(CURDATE()) 
    AND YEAR(o.order_date) = YEAR(CURDATE())
GROUP BY 
    c.customer_id, c.customer_name
ORDER BY 
    total_order_value DESC, 
    c.customer_name ASC
LIMIT 10;"""

#code_text = "SELECT * from customers"

keywords_color_mapping = {
    "SELECT": (230, 219, 116),  # Yellowish color
    "FROM": (230, 219, 116),    # Purple color
    "WHERE": (230, 219, 116),   # Blue color
    "AND": (230, 219, 116),     # Purple color
    "JOIN": (230, 219, 116),    # Purple color
    "ON": (230, 219, 116),      # Purple color
    "GROUP": (230, 219, 116),   # Blue color
    "ORDER": (230, 219, 116),   # Blue color
    "BY": (230, 219, 116),      # Blue color
    "LIMIT": (230, 219, 116),  # Yellowish color
}

# Create the image
border_size = 30  # Size of the border

width, height = 1200, (40+30 + 40 + 40 + len(code_text.splitlines()) * 40)
outer_image = Image.new("RGB", (width + 2 * border_size, height + 2 * border_size), (255, 255, 0))  # Yellow border background
outer_draw = ImageDraw.Draw(outer_image)
image = Image.new("RGB", (width, height), (20, 20, 20))  # Dark background
draw = ImageDraw.Draw(image)

# Load a default font
font = ImageFont.load_default(24)

# Draw the code block with glow effect
draw_code_block_with_glow(draw, code_text, font, keywords_color_mapping)
title_bar_color = "#333333"
dot_color = "#FF5F57"  # Close (Red)
dot_spacing = 30
dot_radius = 8
# Draw VSCode-like elements (toolbox and three dots)
#draw.rectangle([20, 20, 1180, 60], fill=(40, 40, 40))  # Top bar
#draw.ellipse([1150, 10, 1170, 30], fill=(97, 175, 239))  # Simulated dot
dot_x = 30
dot_y = 25

for i in range(3):
    draw.ellipse([dot_x - dot_radius, dot_y - dot_radius, dot_x + dot_radius, dot_y + dot_radius], fill=dot_color)
    dot_color = "#FFBD2E" if i == 0 else "#28C840"  # Minimize (Yellow) and Maximize (Green)
    dot_x += dot_spacing


outer_image.paste(image, (border_size, border_size))

# Save the image
outer_image.save("vscode_simulated_code_block_with_glow.png")
