"""
Graphics Utilities for LLUMO AI Assignment
Common functions for creating graphics elements
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2
from brand_config import BRAND_COLORS, TYPOGRAPHY

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def create_gradient_background(width, height, color1, color2, direction='horizontal'):
    """Create a gradient background"""
    if direction == 'horizontal':
        gradient = np.linspace(0, 1, width)
        gradient = np.tile(gradient, (height, 1))
    else:  # vertical
        gradient = np.linspace(0, 1, height)
        gradient = np.tile(gradient, (width, 1)).T
    
    rgb1 = np.array(hex_to_rgb(color1)) / 255.0
    rgb2 = np.array(hex_to_rgb(color2)) / 255.0
    
    # Create the gradient
    r = rgb1[0] + (rgb2[0] - rgb1[0]) * gradient
    g = rgb1[1] + (rgb2[1] - rgb1[1]) * gradient
    b = rgb1[2] + (rgb2[2] - rgb1[2]) * gradient
    
    return np.stack([r, g, b], axis=2)

def create_glitch_effect(image, intensity=0.3):
    """Create a glitch effect on an image"""
    height, width = image.shape[:2]
    glitched = image.copy()
    
    # Random horizontal shifts
    for _ in range(int(height * intensity / 10)):
        y = np.random.randint(0, height-10)
        shift = np.random.randint(-20, 20)
        if shift > 0:
            glitched[y:y+5, shift:] = glitched[y:y+5, :-shift]
        elif shift < 0:
            glitched[y:y+5, :shift] = glitched[y:y+5, -shift:]
    
    # Color channel shifts
    if len(image.shape) == 3:
        # Red channel shift
        glitched[:, 5:, 0] = image[:, :-5, 0]
        # Blue channel shift  
        glitched[:, :-5, 2] = image[:, 5:, 2]
    
    return glitched

def draw_rounded_rect(fig, ax, x, y, width, height, color, alpha=1.0, corner_radius=0.02):
    """Draw a rounded rectangle"""
    rect = FancyBboxPatch(
        (x, y), width, height,
        boxstyle=f"round,pad=0.01,rounding_size={corner_radius}",
        facecolor=color, alpha=alpha, edgecolor='none'
    )
    ax.add_patch(rect)
    return rect

def create_particle_system(num_particles, width, height, frame_time):
    """Create animated particles for transitions"""
    particles = []
    for _ in range(num_particles):
        x = np.random.uniform(0, width)
        y = np.random.uniform(0, height)
        vx = np.random.uniform(-50, 50)
        vy = np.random.uniform(-50, 50)
        size = np.random.uniform(1, 4)
        particles.append({
            'x': x + vx * frame_time,
            'y': y + vy * frame_time,
            'size': size,
            'alpha': max(0, 1 - frame_time * 2)
        })
    return particles

def draw_ai_icon(ax, x, y, size, color, style='robust'):
    """Draw an AI-themed icon"""
    if style == 'robust':
        # Draw a brain-like network
        # Central node
        circle = plt.Circle((x, y), size*0.3, color=color, alpha=0.8)
        ax.add_patch(circle)
        
        # Connection nodes
        angles = np.linspace(0, 2*np.pi, 6, endpoint=False)
        for angle in angles:
            node_x = x + np.cos(angle) * size * 0.7
            node_y = y + np.sin(angle) * size * 0.7
            
            # Draw connection line
            ax.plot([x, node_x], [y, node_y], color=color, linewidth=2, alpha=0.6)
            
            # Draw node
            node_circle = plt.Circle((node_x, node_y), size*0.15, color=color, alpha=0.7)
            ax.add_patch(node_circle)
    
    else:  # broken style
        # Draw broken/fragmented elements
        fragments_x = [x-size*0.3, x+size*0.2, x-size*0.1, x+size*0.4]
        fragments_y = [y+size*0.2, y-size*0.3, y-size*0.4, y+size*0.1]
        
        for fx, fy in zip(fragments_x, fragments_y):
            fragment = plt.Circle((fx, fy), size*0.15, color=color, alpha=0.5)
            ax.add_patch(fragment)
            
            # Add jagged lines
            ax.plot([x, fx], [y, fy], color=color, linewidth=1, alpha=0.3, linestyle='--')

def setup_matplotlib_style():
    """Setup matplotlib with dark theme and custom fonts"""
    plt.style.use('dark_background')
    plt.rcParams['figure.facecolor'] = BRAND_COLORS['dark_bg']
    plt.rcParams['axes.facecolor'] = BRAND_COLORS['dark_bg']
    plt.rcParams['text.color'] = BRAND_COLORS['text_white']
    plt.rcParams['axes.labelcolor'] = BRAND_COLORS['text_white']
    plt.rcParams['xtick.color'] = BRAND_COLORS['text_white']
    plt.rcParams['ytick.color'] = BRAND_COLORS['text_white']
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']

def create_dashboard_element(ax, x, y, width, height, title, data_points):
    """Create a dashboard visualization element"""
    # Background
    draw_rounded_rect(None, ax, x, y, width, height, BRAND_COLORS['light_gray'], alpha=0.8)
    
    # Title
    ax.text(x + width/2, y + height - 0.05, title, 
            ha='center', va='center', fontsize=12, 
            color=BRAND_COLORS['text_white'], weight='bold')
    
    # Data visualization (simple line chart)
    chart_x = np.linspace(x + 0.05, x + width - 0.05, len(data_points))
    chart_y = y + 0.1 + (np.array(data_points) / 100) * (height - 0.2)
    
    ax.plot(chart_x, chart_y, color=BRAND_COLORS['primary_purple'], linewidth=3)
    ax.scatter(chart_x, chart_y, color=BRAND_COLORS['accent_blue'], s=30, zorder=5)