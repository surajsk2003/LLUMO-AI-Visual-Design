"""
Task 1: Hero Section Animation (Simplified Version)
Creates a 15-second animation showing the transition from weak AI to robust AI using PIL
"""

from PIL import Image, ImageDraw, ImageFont
import numpy as np
from brand_config import *
from graphics_utils import hex_to_rgb
import cv2
import os

def create_hero_frame_pil(frame_num, total_frames):
    """Create a single frame using PIL"""
    width, height = 1920, 1080
    
    # Create base image with gradient background
    img = Image.new('RGB', (width, height), hex_to_rgb(BRAND_COLORS['dark_bg']))
    draw = ImageDraw.Draw(img)
    
    # Create gradient background
    for y in range(height):
        progress_y = y / height
        r1, g1, b1 = hex_to_rgb(BRAND_COLORS['dark_bg'])
        r2, g2, b2 = hex_to_rgb(BRAND_COLORS['dark_gray'])
        
        r = int(r1 + (r2 - r1) * progress_y)
        g = int(g1 + (g2 - g1) * progress_y)
        b = int(b1 + (b2 - b1) * progress_y)
        
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Calculate animation progress
    progress = frame_num / total_frames
    
    # Load font (try to get a nice font, fallback to default)
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 72)
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 36)
        text_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 28)
        logo_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 96)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        logo_font = ImageFont.load_default()
    
    # Phase calculations
    if progress <= 0.2:  # Phase 1: Show weak AI (0-3 seconds)
        weak_alpha = 255
        robust_alpha = 0
        transition_progress = 0
        
    elif progress <= 0.4:  # Phase 2: Transition (3-6 seconds)
        transition_progress = (progress - 0.2) / 0.2
        weak_alpha = int(255 * (1.0 - transition_progress))
        robust_alpha = int(255 * transition_progress)
        
    elif progress <= 0.67:  # Phase 3: Show robust AI (6-10 seconds)
        weak_alpha = 0
        robust_alpha = 255
        transition_progress = 1.0
        
    else:  # Phase 4: Logo reveal (10-15 seconds)
        weak_alpha = 0
        robust_alpha = 255
        transition_progress = 1.0
    
    # Left side - Weak AI
    if weak_alpha > 0:
        # Title
        weak_color = (*hex_to_rgb(BRAND_COLORS['error_red']), weak_alpha)
        
        # Add glitch effect to position
        glitch_offset = 0
        if progress <= 0.2:
            glitch_offset = int(np.sin(frame_num * 0.5) * 10)
        
        draw.text((480 + glitch_offset, 200), "Weak & Broken AI", 
                 fill=weak_color, font=title_font, anchor="mm")
        
        # Features list
        feature_color = (*hex_to_rgb(BRAND_COLORS['warning_orange']), weak_alpha)
        for i, feature in enumerate(WEAK_AI_FEATURES):
            y_pos = 350 + i * 80
            draw.text((480, y_pos), f"❌ {feature}", 
                     fill=feature_color, font=text_font, anchor="mm")
        
        # Draw broken icons (simple circles with breaks)
        for i in range(3):
            icon_x = 300 + i * 120
            icon_y = 750
            # Broken circle
            draw.ellipse([icon_x-30, icon_y-30, icon_x+30, icon_y+30], 
                        outline=weak_color, width=3)
            # Break lines
            draw.line([icon_x-20, icon_y-10, icon_x+20, icon_y+10], 
                     fill=weak_color, width=2)
    
    # Transition effects
    if 0.2 < progress <= 0.4:
        # Draw transition sweep
        sweep_x = int(transition_progress * width)
        for i in range(100):  # Gradient sweep width
            alpha = int(255 * np.sin((i / 100) * np.pi))
            sweep_color = (*hex_to_rgb(BRAND_COLORS['primary_purple']), alpha)
            if sweep_x + i < width:
                draw.line([(sweep_x + i, 0), (sweep_x + i, height)], 
                         fill=sweep_color, width=1)
        
        # Draw particles
        for _ in range(30):
            px = int(np.random.uniform(sweep_x - 100, sweep_x + 100))
            py = int(np.random.uniform(0, height))
            if 0 <= px < width:
                particle_alpha = int(255 * transition_progress)
                particle_color = (*hex_to_rgb(BRAND_COLORS['primary_purple']), particle_alpha)
                draw.ellipse([px-3, py-3, px+3, py+3], fill=particle_color)
    
    # Right side - Robust AI
    if robust_alpha > 0:
        # Title
        robust_color = (*hex_to_rgb(BRAND_COLORS['primary_purple']), robust_alpha)
        draw.text((1440, 200), "Robust AI", 
                 fill=robust_color, font=title_font, anchor="mm")
        
        # Features list
        feature_color = (*hex_to_rgb(BRAND_COLORS['success_green']), robust_alpha)
        for i, feature in enumerate(ROBUST_AI_FEATURES):
            y_pos = 320 + i * 70
            
            # Animate text appearing with delay
            text_alpha = robust_alpha
            if progress <= 0.4:
                delay = i * 0.02
                if transition_progress < delay:
                    text_alpha = 0
                else:
                    text_alpha = int(min(255, (transition_progress - delay) / 0.1 * 255))
            
            if text_alpha > 0:
                text_color = (*hex_to_rgb(BRAND_COLORS['success_green']), text_alpha)
                draw.text((1440, y_pos), f"✅ {feature}", 
                         fill=text_color, font=text_font, anchor="mm")
        
        # Draw robust icons (connected network)
        for i in range(3):
            icon_x = 1260 + i * 120
            icon_y = 750
            # Main circle
            draw.ellipse([icon_x-25, icon_y-25, icon_x+25, icon_y+25], 
                        outline=robust_color, fill=robust_color, width=2)
            
            # Connection lines to center
            center_x, center_y = 1380, 700
            draw.line([icon_x, icon_y, center_x, center_y], 
                     fill=robust_color, width=2)
            
            # Small connected nodes
            for angle in [0, 120, 240]:
                node_x = icon_x + int(40 * np.cos(np.radians(angle)))
                node_y = icon_y + int(40 * np.sin(np.radians(angle)))
                draw.ellipse([node_x-8, node_y-8, node_x+8, node_y+8], 
                            outline=robust_color, width=1)
                draw.line([icon_x, icon_y, node_x, node_y], 
                         fill=robust_color, width=1)
    
    # Logo reveal phase
    if progress > 0.67:
        logo_alpha = min(255, int((progress - 0.67) / 0.2 * 255))
        
        # LLUMO AI Logo
        logo_color = (*hex_to_rgb(BRAND_COLORS['primary_purple']), logo_alpha)
        draw.text((960, 900), "LLUMO AI", 
                 fill=logo_color, font=logo_font, anchor="mm")
        
        # Tagline
        tagline_color = (*hex_to_rgb(BRAND_COLORS['text_gray']), logo_alpha)
        draw.text((960, 980), "Revolutionizing AI Evaluation", 
                 fill=tagline_color, font=subtitle_font, anchor="mm")
        
        # Add glow effect
        if logo_alpha > 127:
            glow_alpha = logo_alpha // 4
            glow_color = (*hex_to_rgb(BRAND_COLORS['primary_purple']), glow_alpha)
            draw.ellipse([760, 800, 1160, 1000], outline=glow_color, width=3)
    
    return np.array(img)

def create_hero_animation():
    """Create the complete hero animation"""
    print("Creating hero section animation...")
    
    fps = ANIMATION_CONFIG['fps']
    duration = ANIMATION_CONFIG['hero_duration']
    total_frames = fps * duration
    
    # Create frames
    frames = []
    for frame_num in range(total_frames):
        if frame_num % 30 == 0:  # Print progress every second
            print(f"Rendering frame {frame_num + 1}/{total_frames} ({frame_num/total_frames*100:.1f}%)")
        
        frame = create_hero_frame_pil(frame_num, total_frames)
        frames.append(frame)
    
    # Save as video using OpenCV
    height, width, _ = frames[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('Hero_Animation.mp4', fourcc, fps, (width, height))
    
    print("Writing video file...")
    for i, frame in enumerate(frames):
        if i % 60 == 0:  # Print progress every 2 seconds
            print(f"Writing frame {i + 1}/{len(frames)}")
        # Convert RGB to BGR for OpenCV
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        out.write(frame_bgr)
    
    out.release()
    
    print("Hero animation created successfully: Hero_Animation.mp4")
    print(f"Duration: {duration} seconds, Resolution: {width}x{height}, FPS: {fps}")

if __name__ == "__main__":
    create_hero_animation()