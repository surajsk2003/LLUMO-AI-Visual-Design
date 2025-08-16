"""
Task 1: Hero Section Animation
Creates a 15-second animation showing the transition from weak AI to robust AI
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from graphics_utils import *
from brand_config import *
import cv2
from moviepy.editor import VideoFileClip, AudioFileClip

def create_hero_frame(frame_num, total_frames):
    """Create a single frame of the hero animation"""
    setup_matplotlib_style()
    
    # Create figure with exact pixel dimensions
    fig, ax = plt.subplots(figsize=(16, 9), dpi=120)
    fig.patch.set_facecolor(BRAND_COLORS['dark_bg'])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_aspect('equal')
    
    # Calculate animation progress
    progress = frame_num / total_frames
    
    # Background gradient
    bg_gradient = create_gradient_background(1000, 600, 
                                            BRAND_COLORS['dark_bg'], 
                                            BRAND_COLORS['dark_gray'], 
                                            'horizontal')
    ax.imshow(bg_gradient, extent=[0, 1, 0, 1], aspect='auto')
    
    # Phase 1: Show weak AI (0-3 seconds)
    if progress <= 0.2:
        weak_alpha = 1.0
        robust_alpha = 0.0
        transition_progress = 0
        
    # Phase 2: Transition (3-6 seconds)  
    elif progress <= 0.4:
        transition_progress = (progress - 0.2) / 0.2
        weak_alpha = 1.0 - transition_progress
        robust_alpha = transition_progress
        
    # Phase 3: Show robust AI (6-10 seconds)
    elif progress <= 0.67:
        weak_alpha = 0.0
        robust_alpha = 1.0
        transition_progress = 1.0
        
    # Phase 4: Logo reveal (10-15 seconds)
    else:
        weak_alpha = 0.0
        robust_alpha = 1.0
        transition_progress = 1.0
    
    # Left side - Weak AI (with glitch effects)
    if weak_alpha > 0:
        # Title
        ax.text(0.25, 0.8, "Weak & Broken AI", 
                ha='center', va='center', fontsize=48*weak_alpha, 
                color=BRAND_COLORS['error_red'], weight='bold', alpha=weak_alpha)
        
        # Features list
        for i, feature in enumerate(WEAK_AI_FEATURES):
            y_pos = 0.65 - i * 0.08
            
            # Add glitch effect to text positioning
            glitch_offset = 0
            if progress <= 0.2:
                glitch_offset = np.sin(frame_num * 0.5) * 0.005
            
            ax.text(0.25 + glitch_offset, y_pos, f"❌ {feature}", 
                    ha='center', va='center', fontsize=24*weak_alpha,
                    color=BRAND_COLORS['warning_orange'], alpha=weak_alpha)
        
        # Broken AI icons
        for i in range(3):
            icon_x = 0.15 + i * 0.07
            icon_y = 0.3
            draw_ai_icon(ax, icon_x, icon_y, 0.04, BRAND_COLORS['error_red'], 'broken')
    
    # Transition effects (particles and sweep)
    if 0.2 < progress <= 0.4:
        # Particle system
        particles = create_particle_system(50, 1, 1, transition_progress)
        for particle in particles:
            if 0 <= particle['x'] <= 1 and 0 <= particle['y'] <= 1:
                circle = plt.Circle((particle['x'], particle['y']), 
                                  particle['size']/1000, 
                                  color=BRAND_COLORS['primary_purple'], 
                                  alpha=particle['alpha'])
                ax.add_patch(circle)
        
        # Gradient sweep
        sweep_x = transition_progress
        sweep_width = 0.1
        if sweep_x - sweep_width/2 <= 1:
            sweep_gradient = np.zeros((1080, int(sweep_width * 1920), 3))
            for i in range(int(sweep_width * 1920)):
                alpha = np.sin((i / (sweep_width * 1920)) * np.pi)
                sweep_gradient[:, i] = np.array(hex_to_rgb(BRAND_COLORS['primary_purple'])) / 255.0 * alpha
            
            ax.imshow(sweep_gradient, extent=[sweep_x - sweep_width/2, sweep_x + sweep_width/2, 0, 1], 
                     aspect='equal', alpha=0.7)
    
    # Right side - Robust AI
    if robust_alpha > 0:
        # Title
        ax.text(0.75, 0.8, "Robust AI", 
                ha='center', va='center', fontsize=52*robust_alpha,
                color=BRAND_COLORS['primary_purple'], weight='bold', alpha=robust_alpha)
        
        # Features list
        for i, feature in enumerate(ROBUST_AI_FEATURES):
            y_pos = 0.68 - i * 0.07
            
            # Animate text appearing
            text_alpha = robust_alpha
            if progress <= 0.4:
                delay = i * 0.02
                if transition_progress < delay:
                    text_alpha = 0
                else:
                    text_alpha = min(1, (transition_progress - delay) / 0.1) * robust_alpha
            
            ax.text(0.75, y_pos, f"✅ {feature}", 
                    ha='center', va='center', fontsize=26*text_alpha,
                    color=BRAND_COLORS['success_green'], alpha=text_alpha, weight='bold')
        
        # Robust AI icons (connected network)
        for i in range(3):
            icon_x = 0.65 + i * 0.07
            icon_y = 0.25
            draw_ai_icon(ax, icon_x, icon_y, 0.04, BRAND_COLORS['accent_blue'], 'robust')
    
    # Logo reveal phase
    if progress > 0.67:
        logo_alpha = min(1, (progress - 0.67) / 0.2)
        
        # LLUMO AI Logo (text-based)
        ax.text(0.5, 0.15, "LLUMO AI", 
                ha='center', va='center', fontsize=72*logo_alpha,
                color=BRAND_COLORS['primary_purple'], weight='bold', alpha=logo_alpha)
        
        # Tagline
        ax.text(0.5, 0.08, "Revolutionizing AI Evaluation", 
                ha='center', va='center', fontsize=32*logo_alpha,
                color=BRAND_COLORS['text_gray'], alpha=logo_alpha)
        
        # Add subtle glow effect around logo
        if logo_alpha > 0.5:
            glow_circle = plt.Circle((0.5, 0.11), 0.15, 
                                   color=BRAND_COLORS['primary_purple'], 
                                   alpha=0.1*logo_alpha, linewidth=0)
            ax.add_patch(glow_circle)
    
    plt.tight_layout()
    return fig

def create_hero_animation():
    """Create the complete hero animation"""
    print("Creating hero section animation...")
    
    fps = ANIMATION_CONFIG['fps']
    duration = ANIMATION_CONFIG['hero_duration']
    total_frames = fps * duration
    
    # Create frames
    frames = []
    for frame_num in range(total_frames):
        print(f"Rendering frame {frame_num + 1}/{total_frames}")
        fig = create_hero_frame(frame_num, total_frames)
        
        # Convert matplotlib figure to numpy array
        fig.canvas.draw()
        width, height = fig.canvas.get_width_height()
        buf = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        buf = buf.reshape((height, width, 3))
        frames.append(buf)
        plt.close(fig)
    
    # Save as video using OpenCV
    height, width, _ = frames[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('hero_animation_temp.mp4', fourcc, fps, (width, height))
    
    for frame in frames:
        # Convert RGB to BGR for OpenCV
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        out.write(frame_bgr)
    
    out.release()
    
    # Convert to final format with moviepy (better compression)
    clip = VideoFileClip('hero_animation_temp.mp4')
    clip.write_videofile('Hero_Animation.mp4', codec='libx264', fps=fps)
    clip.close()
    
    # Clean up temp file
    import os
    os.remove('hero_animation_temp.mp4')
    
    print("Hero animation created successfully: Hero_Animation.mp4")

if __name__ == "__main__":
    create_hero_animation()