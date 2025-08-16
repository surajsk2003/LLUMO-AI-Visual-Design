"""
Task 2: Explainer Video for Eval360 Engine
Creates a 45-second animation explaining LLUMO AI's Eval360 Engine
"""

from PIL import Image, ImageDraw, ImageFont
import numpy as np
from brand_config import *
from graphics_utils import hex_to_rgb
import cv2
import math

def draw_dashboard(draw, x, y, width, height, alpha=255):
    """Draw a dashboard interface"""
    # Background
    bg_color = (*hex_to_rgb(BRAND_COLORS['light_gray']), alpha)
    draw.rectangle([x, y, x+width, y+height], fill=bg_color, outline=None)
    
    # Header bar
    header_color = (*hex_to_rgb(BRAND_COLORS['primary_purple']), alpha)
    draw.rectangle([x, y, x+width, y+60], fill=header_color)
    
    # Chart areas
    chart_color = (*hex_to_rgb(BRAND_COLORS['dark_gray']), alpha)
    # Chart 1
    draw.rectangle([x+20, y+80, x+width//2-10, y+height//2], fill=chart_color)
    # Chart 2
    draw.rectangle([x+width//2+10, y+80, x+width-20, y+height//2], fill=chart_color)
    # Chart 3
    draw.rectangle([x+20, y+height//2+20, x+width-20, y+height-20], fill=chart_color)

def draw_confused_dashboard(draw, x, y, width, height, frame_num, alpha=255):
    """Draw a confusing, scattered dashboard"""
    # Multiple overlapping windows
    colors = [BRAND_COLORS['error_red'], BRAND_COLORS['warning_orange'], BRAND_COLORS['accent_blue']]
    
    for i in range(3):
        offset_x = int(20 * np.sin(frame_num * 0.1 + i))
        offset_y = int(15 * np.cos(frame_num * 0.15 + i))
        
        window_color = (*hex_to_rgb(colors[i]), alpha//2)
        draw.rectangle([x + offset_x + i*30, y + offset_y + i*25, 
                       x + offset_x + width//2 + i*30, y + offset_y + height//2 + i*25], 
                      fill=window_color, outline=(*hex_to_rgb(colors[i]), alpha), width=2)
        
        # Random lines inside (representing data)
        for j in range(5):
            line_x1 = x + offset_x + i*30 + 20
            line_y1 = y + offset_y + i*25 + 40 + j*15
            line_x2 = line_x1 + 80 + int(20 * np.sin(frame_num * 0.2 + j))
            line_y2 = line_y1
            draw.line([line_x1, line_y1, line_x2, line_y2], 
                     fill=(*hex_to_rgb(colors[i]), alpha), width=2)

def draw_template_library(draw, x, y, width, height, progress, alpha=255):
    """Draw template library animation"""
    # Background
    bg_color = (*hex_to_rgb(BRAND_COLORS['light_gray']), alpha)
    draw.rectangle([x, y, x+width, y+height], fill=bg_color)
    
    # Grid of templates
    template_size = 80
    cols = width // (template_size + 20)
    rows = height // (template_size + 20)
    
    for row in range(rows):
        for col in range(cols):
            template_x = x + 20 + col * (template_size + 20)
            template_y = y + 20 + row * (template_size + 20)
            
            # Animate templates appearing
            template_progress = progress - (row * cols + col) * 0.05
            if template_progress > 0:
                template_alpha = min(alpha, int(template_progress * 500))
                if template_alpha > 0:
                    template_color = (*hex_to_rgb(BRAND_COLORS['primary_purple']), template_alpha)
                    draw.rectangle([template_x, template_y, 
                                  template_x + template_size, template_y + template_size], 
                                  fill=template_color, outline=(*hex_to_rgb(BRAND_COLORS['accent_blue']), template_alpha), width=2)
                    
                    # Add template icon (simple geometric shape)
                    icon_x = template_x + template_size // 2
                    icon_y = template_y + template_size // 2
                    icon_color = (*hex_to_rgb(BRAND_COLORS['text_white']), template_alpha)
                    draw.ellipse([icon_x-15, icon_y-15, icon_x+15, icon_y+15], fill=icon_color)

def draw_feedback_to_metrics(draw, x, y, width, height, progress, alpha=255):
    """Draw feedback transforming into metrics"""
    # Left side: Feedback (text bubbles)
    feedback_texts = ["Good response", "Too slow", "Accurate", "Confusing"]
    
    for i, text in enumerate(feedback_texts):
        bubble_y = y + 50 + i * 80
        bubble_alpha = int(alpha * (1 - progress * 0.7))  # Fade out
        
        if bubble_alpha > 0:
            # Speech bubble
            bubble_color = (*hex_to_rgb(BRAND_COLORS['text_gray']), bubble_alpha)
            draw.ellipse([x + 20, bubble_y, x + 150, bubble_y + 40], fill=bubble_color)
    
    # Arrow
    arrow_alpha = int(alpha * min(1, progress * 2))
    if arrow_alpha > 0:
        arrow_color = (*hex_to_rgb(BRAND_COLORS['primary_purple']), arrow_alpha)
        arrow_x = x + width // 2
        arrow_y = y + height // 2
        # Draw arrow
        draw.polygon([
            (arrow_x - 30, arrow_y - 15),
            (arrow_x + 10, arrow_y),
            (arrow_x - 30, arrow_y + 15),
            (arrow_x - 20, arrow_y)
        ], fill=arrow_color)
    
    # Right side: Metrics (charts and numbers)
    if progress > 0.3:
        metric_alpha = int(alpha * (progress - 0.3) / 0.7)
        
        # Bar chart
        for i in range(4):
            bar_height = int(50 + 30 * np.sin(i + progress * 5))
            bar_y = y + height - bar_height - 50
            bar_color = (*hex_to_rgb(BRAND_COLORS['success_green']), metric_alpha)
            draw.rectangle([x + width - 120 + i * 25, bar_y, 
                          x + width - 100 + i * 25, y + height - 50], fill=bar_color)

def create_explainer_frame(frame_num, total_frames):
    """Create a single frame of the explainer video"""
    width, height = 1920, 1080
    
    # Create base image
    img = Image.new('RGB', (width, height), hex_to_rgb(BRAND_COLORS['dark_bg']))
    draw = ImageDraw.Draw(img)
    
    # Create subtle gradient background
    for y in range(height):
        progress_y = y / height
        r1, g1, b1 = hex_to_rgb(BRAND_COLORS['dark_bg'])
        r2, g2, b2 = hex_to_rgb(BRAND_COLORS['dark_gray'])
        
        r = int(r1 + (r2 - r1) * progress_y * 0.3)  # Subtle gradient
        g = int(g1 + (g2 - g1) * progress_y * 0.3)
        b = int(b1 + (b2 - b1) * progress_y * 0.3)
        
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Calculate animation progress
    progress = frame_num / total_frames
    
    # Load fonts
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 64)
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 42)
        text_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 32)
        small_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Scene timing based on EXPLAINER_SCRIPT
    current_scene = 0
    scene_progress = 0
    
    # Determine current scene
    time_elapsed = progress * 45  # 45 seconds total
    for i, scene in enumerate(EXPLAINER_SCRIPT):
        if time_elapsed >= scene['time'] and time_elapsed < scene['time'] + scene['duration']:
            current_scene = i
            scene_progress = (time_elapsed - scene['time']) / scene['duration']
            break
    
    # Scene 0: "Traditional AI evaluation is complex" (0-5s)
    if current_scene == 0:
        alpha = int(255 * min(1, scene_progress * 2))
        
        # Title text
        title_color = (*hex_to_rgb(BRAND_COLORS['text_white']), alpha)
        draw.text((width//2, 200), "Traditional AI evaluation", 
                 fill=title_color, font=title_font, anchor="mm")
        draw.text((width//2, 280), "is complex and time-consuming", 
                 fill=title_color, font=subtitle_font, anchor="mm")
        
        # Show confused dashboard
        draw_confused_dashboard(draw, width//2 - 300, 400, 600, 400, frame_num, alpha)
    
    # Scene 1: "Scattered evaluation methods" (5-10s)
    elif current_scene == 1:
        alpha = 255
        
        # Title
        title_color = (*hex_to_rgb(BRAND_COLORS['warning_orange']), alpha)
        draw.text((width//2, 150), "Scattered Evaluation Methods", 
                 fill=title_color, font=title_font, anchor="mm")
        
        # Show multiple disconnected tools
        for i in range(4):
            tool_x = 200 + i * 350
            tool_y = 300 + int(30 * np.sin(frame_num * 0.1 + i))  # Floating effect
            
            tool_alpha = int(alpha * min(1, scene_progress + i * 0.1))
            draw_dashboard(draw, tool_x, tool_y, 250, 200, tool_alpha)
            
            # Tool labels
            labels = ["Tool A", "Tool B", "Tool C", "Tool D"]
            label_color = (*hex_to_rgb(BRAND_COLORS['text_gray']), tool_alpha)
            draw.text((tool_x + 125, tool_y + 220), labels[i], 
                     fill=label_color, font=text_font, anchor="mm")
    
    # Scene 2: "Introducing Eval360 Engine" (10-15s)
    elif current_scene == 2:
        alpha = 255
        
        # Clear background for logo reveal
        logo_alpha = int(255 * scene_progress)
        
        # LLUMO AI Logo
        logo_color = (*hex_to_rgb(BRAND_COLORS['primary_purple']), logo_alpha)
        draw.text((width//2, height//2 - 100), "LLUMO AI", 
                 fill=logo_color, font=title_font, anchor="mm")
        
        # Eval360 Engine
        eval_color = (*hex_to_rgb(BRAND_COLORS['accent_blue']), logo_alpha)
        draw.text((width//2, height//2), "Eval360 Engine", 
                 fill=eval_color, font=subtitle_font, anchor="mm")
        
        # Subtitle
        subtitle_color = (*hex_to_rgb(BRAND_COLORS['text_gray']), logo_alpha)
        draw.text((width//2, height//2 + 80), "Unified AI Evaluation Platform", 
                 fill=subtitle_color, font=text_font, anchor="mm")
        
        # Add glow effect
        if scene_progress > 0.5:
            glow_alpha = int(logo_alpha * 0.3)
            glow_color = (*hex_to_rgb(BRAND_COLORS['primary_purple']), glow_alpha)
            draw.ellipse([width//2 - 300, height//2 - 150, width//2 + 300, height//2 + 150], 
                        outline=glow_color, width=5)
    
    # Scene 3: "Build Custom Evals Fast" (15-23s)
    elif current_scene == 3:
        alpha = 255
        
        # Title
        title_color = (*hex_to_rgb(BRAND_COLORS['primary_purple']), alpha)
        draw.text((width//2, 120), "Build Custom Evals Fast", 
                 fill=title_color, font=title_font, anchor="mm")
        
        # Show template library
        draw_template_library(draw, width//2 - 400, 200, 800, 600, scene_progress, alpha)
        
        # Add "Template Library" label
        label_color = (*hex_to_rgb(BRAND_COLORS['text_white']), alpha)
        draw.text((width//2, 850), "Choose from hundreds of pre-built evaluation templates", 
                 fill=label_color, font=text_font, anchor="mm")
    
    # Scene 4: "Turn Feedback into Metrics" (23-31s)
    elif current_scene == 4:
        alpha = 255
        
        # Title
        title_color = (*hex_to_rgb(BRAND_COLORS['success_green']), alpha)
        draw.text((width//2, 120), "Turn Feedback into Metrics", 
                 fill=title_color, font=title_font, anchor="mm")
        
        # Show transformation
        draw_feedback_to_metrics(draw, width//2 - 400, 200, 800, 600, scene_progress, alpha)
        
        # Labels
        label_color = (*hex_to_rgb(BRAND_COLORS['text_white']), alpha)
        draw.text((width//4, 850), "Human Feedback", 
                 fill=label_color, font=text_font, anchor="mm")
        draw.text((3*width//4, 850), "Quantified Metrics", 
                 fill=label_color, font=text_font, anchor="mm")
    
    # Scene 5: "Experience LLUMO AI today" (31-45s)
    else:
        alpha = 255
        
        # Clean dashboard view
        draw_dashboard(draw, width//2 - 400, 200, 800, 500, alpha)
        
        # CTA text
        cta_alpha = int(255 * min(1, scene_progress * 2))
        cta_color = (*hex_to_rgb(BRAND_COLORS['primary_purple']), cta_alpha)
        draw.text((width//2, 800), "Experience LLUMO AI Today", 
                 fill=cta_color, font=title_font, anchor="mm")
        
        # Website/contact info
        contact_color = (*hex_to_rgb(BRAND_COLORS['text_gray']), cta_alpha)
        draw.text((width//2, 900), "Transform your AI evaluation workflow", 
                 fill=contact_color, font=subtitle_font, anchor="mm")
        
        # Final logo
        final_logo_alpha = int(255 * max(0, scene_progress - 0.5) * 2)
        if final_logo_alpha > 0:
            final_logo_color = (*hex_to_rgb(BRAND_COLORS['primary_purple']), final_logo_alpha)
            draw.text((width//2, 980), "LLUMO AI", 
                     fill=final_logo_color, font=subtitle_font, anchor="mm")
    
    return np.array(img)

def create_explainer_video():
    """Create the complete explainer video"""
    print("Creating explainer video...")
    
    fps = ANIMATION_CONFIG['fps']
    duration = ANIMATION_CONFIG['explainer_duration']
    total_frames = fps * duration
    
    # Create frames
    frames = []
    for frame_num in range(total_frames):
        if frame_num % 30 == 0:  # Print progress every second
            print(f"Rendering frame {frame_num + 1}/{total_frames} ({frame_num/total_frames*100:.1f}%)")
        
        frame = create_explainer_frame(frame_num, total_frames)
        frames.append(frame)
    
    # Save as video using OpenCV
    height, width, _ = frames[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('Explainer_Video.mp4', fourcc, fps, (width, height))
    
    print("Writing video file...")
    for i, frame in enumerate(frames):
        if i % 60 == 0:  # Print progress every 2 seconds
            print(f"Writing frame {i + 1}/{len(frames)}")
        # Convert RGB to BGR for OpenCV
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        out.write(frame_bgr)
    
    out.release()
    
    print("Explainer video created successfully: Explainer_Video.mp4")
    print(f"Duration: {duration} seconds, Resolution: {width}x{height}, FPS: {fps}")

if __name__ == "__main__":
    create_explainer_video()