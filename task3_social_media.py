"""
Task 3: Social Media Graphic (1080x1080)
Creates a square social media graphic showcasing 360° workflow visualization
"""

from PIL import Image, ImageDraw, ImageFont
import numpy as np
from brand_config import *
from graphics_utils import hex_to_rgb
import math

def draw_workflow_node(draw, x, y, size, label, color, alpha=255):
    """Draw a workflow node with label"""
    node_color = (*hex_to_rgb(color), alpha)
    outline_color = (*hex_to_rgb(BRAND_COLORS['accent_blue']), alpha)
    text_color = (*hex_to_rgb(BRAND_COLORS['text_white']), alpha)
    
    # Draw circle
    draw.ellipse([x - size//2, y - size//2, x + size//2, y + size//2], 
                fill=node_color, outline=outline_color, width=3)
    
    # Draw label
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 16)
    except:
        font = ImageFont.load_default()
    
    draw.text((x, y), label, fill=text_color, font=font, anchor="mm")

def draw_connection_line(draw, x1, y1, x2, y2, color, alpha=255, width=3):
    """Draw a connection line between nodes"""
    line_color = (*hex_to_rgb(color), alpha)
    draw.line([x1, y1, x2, y2], fill=line_color, width=width)
    
    # Add arrow at the end
    angle = math.atan2(y2 - y1, x2 - x1)
    arrow_length = 15
    arrow_angle = 0.5
    
    arrow_x1 = x2 - arrow_length * math.cos(angle - arrow_angle)
    arrow_y1 = y2 - arrow_length * math.sin(angle - arrow_angle)
    arrow_x2 = x2 - arrow_length * math.cos(angle + arrow_angle)
    arrow_y2 = y2 - arrow_length * math.sin(angle + arrow_angle)
    
    draw.polygon([x2, y2, arrow_x1, arrow_y1, arrow_x2, arrow_y2], fill=line_color)

def draw_circular_dashboard(draw, center_x, center_y, radius, alpha=255):
    """Draw a circular dashboard with workflow visualization"""
    # Outer circle (dashboard background)
    dashboard_color = (*hex_to_rgb(BRAND_COLORS['light_gray']), int(alpha * 0.8))
    outline_color = (*hex_to_rgb(BRAND_COLORS['primary_purple']), alpha)
    
    draw.ellipse([center_x - radius, center_y - radius, 
                 center_x + radius, center_y + radius], 
                fill=dashboard_color, outline=outline_color, width=4)
    
    # Inner circles for data sections
    inner_radius = radius * 0.7
    for i in range(4):
        angle = i * math.pi / 2
        section_x = center_x + inner_radius * 0.6 * math.cos(angle)
        section_y = center_y + inner_radius * 0.6 * math.sin(angle)
        
        section_color = (*hex_to_rgb(BRAND_COLORS['dark_gray']), alpha)
        draw.ellipse([section_x - 40, section_y - 40, section_x + 40, section_y + 40], 
                    fill=section_color, outline=outline_color, width=2)
        
        # Add mini charts inside sections
        for j in range(3):
            chart_x = section_x - 20 + j * 15
            chart_y = section_y - 10 + j * 8
            chart_height = 5 + j * 3
            chart_color = (*hex_to_rgb(BRAND_COLORS['success_green']), alpha)
            draw.rectangle([chart_x, chart_y, chart_x + 8, chart_y + chart_height], 
                          fill=chart_color)

def create_social_media_graphic():
    """Create the social media graphic"""
    print("Creating social media graphic...")
    
    size = 1080
    
    # Create base image
    img = Image.new('RGB', (size, size), hex_to_rgb(BRAND_COLORS['dark_bg']))
    draw = ImageDraw.Draw(img)
    
    # Create radial gradient background
    center = size // 2
    for y in range(size):
        for x in range(size):
            distance = math.sqrt((x - center)**2 + (y - center)**2)
            max_distance = math.sqrt(2) * center
            gradient_factor = 1 - (distance / max_distance)
            
            # Only apply gradient to certain pixels for performance
            if x % 4 == 0 and y % 4 == 0:
                r1, g1, b1 = hex_to_rgb(BRAND_COLORS['dark_bg'])
                r2, g2, b2 = hex_to_rgb(BRAND_COLORS['primary_purple'])
                
                r = int(r1 + (r2 - r1) * gradient_factor * 0.2)
                g = int(g1 + (g2 - g1) * gradient_factor * 0.2)
                b = int(b1 + (b2 - b1) * gradient_factor * 0.2)
                
                # Fill a small square for performance
                draw.rectangle([x, y, x+3, y+3], fill=(r, g, b))
    
    # Load fonts
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 64)
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 32)
        body_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
        logo_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 48)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
        logo_font = ImageFont.load_default()
    
    # Header text
    header_color = hex_to_rgb(BRAND_COLORS['primary_purple'])
    draw.text((size//2, 120), "360° Workflow", 
             fill=header_color, font=title_font, anchor="mm")
    draw.text((size//2, 170), "Visualization", 
             fill=header_color, font=title_font, anchor="mm")
    
    # Central circular dashboard
    dashboard_center_x = size // 2
    dashboard_center_y = size // 2 + 50
    dashboard_radius = 200
    
    draw_circular_dashboard(draw, dashboard_center_x, dashboard_center_y, dashboard_radius)
    
    # Workflow nodes around the dashboard
    workflow_steps = [
        {"label": "Data\nIngestion", "angle": 0, "color": BRAND_COLORS['accent_blue']},
        {"label": "AI\nProcessing", "angle": math.pi/3, "color": BRAND_COLORS['primary_purple']},
        {"label": "Evaluation", "angle": 2*math.pi/3, "color": BRAND_COLORS['success_green']},
        {"label": "Feedback\nLoop", "angle": math.pi, "color": BRAND_COLORS['warning_orange']},
        {"label": "Metrics\nAnalysis", "angle": 4*math.pi/3, "color": BRAND_COLORS['error_red']},
        {"label": "Optimization", "angle": 5*math.pi/3, "color": BRAND_COLORS['accent_blue']}
    ]
    
    node_radius = 300
    node_size = 80
    
    # Draw workflow nodes and connections
    for i, step in enumerate(workflow_steps):
        # Calculate node position
        node_x = dashboard_center_x + node_radius * math.cos(step['angle'])
        node_y = dashboard_center_y + node_radius * math.sin(step['angle'])
        
        # Draw connection to center
        draw_connection_line(draw, 
                           dashboard_center_x + dashboard_radius * 0.8 * math.cos(step['angle']),
                           dashboard_center_y + dashboard_radius * 0.8 * math.sin(step['angle']),
                           node_x - node_size//3 * math.cos(step['angle']),
                           node_y - node_size//3 * math.sin(step['angle']),
                           BRAND_COLORS['primary_purple'], alpha=200, width=2)
        
        # Draw node
        draw_workflow_node(draw, int(node_x), int(node_y), node_size, 
                          step['label'], step['color'])
        
        # Draw connection to next node
        next_step = workflow_steps[(i + 1) % len(workflow_steps)]
        next_node_x = dashboard_center_x + node_radius * math.cos(next_step['angle'])
        next_node_y = dashboard_center_y + node_radius * math.sin(next_step['angle'])
        
        # Calculate connection points on circle edge
        conn_start_x = node_x + node_size//3 * math.cos(next_step['angle'] - step['angle'])
        conn_start_y = node_y + node_size//3 * math.sin(next_step['angle'] - step['angle'])
        conn_end_x = next_node_x - node_size//3 * math.cos(next_step['angle'] - step['angle'])
        conn_end_y = next_node_y - node_size//3 * math.sin(next_step['angle'] - step['angle'])
        
        draw_connection_line(draw, int(conn_start_x), int(conn_start_y),
                           int(conn_end_x), int(conn_end_y),
                           BRAND_COLORS['accent_blue'], alpha=150, width=2)
    
    # Central label
    center_text_color = hex_to_rgb(BRAND_COLORS['text_white'])
    draw.text((dashboard_center_x, dashboard_center_y - 20), "AI Workflow", 
             fill=center_text_color, font=subtitle_font, anchor="mm")
    draw.text((dashboard_center_x, dashboard_center_y + 10), "Dashboard", 
             fill=center_text_color, font=subtitle_font, anchor="mm")
    
    # Bottom text
    bottom_text_color = hex_to_rgb(BRAND_COLORS['text_gray'])
    draw.text((size//2, size - 200), "View AI workflow on a single dashboard", 
             fill=bottom_text_color, font=subtitle_font, anchor="mm")
    
    # Add some data visualization elements
    # Performance metrics in corners
    metrics = [
        {"label": "Accuracy\n95%", "pos": (150, 250), "color": BRAND_COLORS['success_green']},
        {"label": "Speed\n2.3s", "pos": (930, 250), "color": BRAND_COLORS['accent_blue']},
        {"label": "Cost\n-40%", "pos": (150, 830), "color": BRAND_COLORS['warning_orange']},
        {"label": "Reliability\n99.9%", "pos": (930, 830), "color": BRAND_COLORS['primary_purple']}
    ]
    
    for metric in metrics:
        # Background circle
        metric_bg_color = (*hex_to_rgb(BRAND_COLORS['light_gray']), 200)
        draw.ellipse([metric['pos'][0] - 60, metric['pos'][1] - 40,
                     metric['pos'][0] + 60, metric['pos'][1] + 40], 
                    fill=metric_bg_color, 
                    outline=hex_to_rgb(metric['color']), width=2)
        
        # Metric text
        metric_color = hex_to_rgb(metric['color'])
        draw.text(metric['pos'], metric['label'], 
                 fill=metric_color, font=body_font, anchor="mm")
    
    # LLUMO AI logo at bottom
    logo_color = hex_to_rgb(BRAND_COLORS['primary_purple'])
    draw.text((size//2, size - 100), "LLUMO AI", 
             fill=logo_color, font=logo_font, anchor="mm")
    
    # Tagline
    tagline_color = hex_to_rgb(BRAND_COLORS['text_gray'])
    draw.text((size//2, size - 50), "Revolutionizing AI Evaluation", 
             fill=tagline_color, font=body_font, anchor="mm")
    
    # Add subtle decorative elements
    # Geometric patterns in corners
    for corner in [(100, 100), (980, 100), (100, 980), (980, 980)]:
        pattern_color = (*hex_to_rgb(BRAND_COLORS['primary_purple']), 50)
        # Draw hexagon pattern
        for i in range(3):
            hex_size = 20 + i * 10
            hex_x = corner[0] + i * 15
            hex_y = corner[1] + i * 15
            
            # Simple hexagon approximation with circle
            draw.ellipse([hex_x - hex_size//2, hex_y - hex_size//2,
                         hex_x + hex_size//2, hex_y + hex_size//2],
                        outline=pattern_color, width=1)
    
    # Save the image
    img.save('Social_Media_Post.png', 'PNG', quality=95)
    print("Social media graphic created successfully: Social_Media_Post.png")
    print(f"Dimensions: {size}x{size}px, Format: PNG")

if __name__ == "__main__":
    create_social_media_graphic()