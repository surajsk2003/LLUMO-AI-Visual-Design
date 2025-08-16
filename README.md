# LLUMO AI Visual Design Assignment

A programmatic approach to creating brand-consistent visual content for LLUMO AI, including hero animations, explainer videos, and social media posts.

## 🎯 Project Overview

This project demonstrates advanced visual design capabilities using Python for creating:
- **Hero Animation**: 15-second brand introduction with particle effects
- **Explainer Video**: 45-second product demonstration 
- **Social Media Post**: Instagram-ready brand visualization

## 🛠️ Technical Stack

- **Python 3.8+** - Core programming language
- **PIL/Pillow** - Image processing and generation
- **OpenCV** - Video processing and effects
- **MoviePy** - Video editing and composition
- **NumPy** - Mathematical operations for animations
- **Matplotlib** - Data visualization and graphics
- **SciPy** - Advanced mathematical functions

## 📁 Project Structure

```
├── file/                      # Output deliverables
│   ├── Design_Note.md        # Design philosophy and approach
│   ├── Hero_Animation.mp4    # 15-second hero animation
│   ├── Explainer_Video.mp4   # 45-second explainer video
│   └── Social_Media_Post.png # Instagram post
├── brand_config.py           # Brand colors, fonts, and constants
├── graphics_utils.py         # Reusable graphics functions
├── task1_hero_animation.py   # Hero animation generator
├── task1_hero_simple.py      # Simplified hero version
├── task2_explainer_video.py  # Explainer video generator
├── task3_social_media.py     # Social media post generator
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## 🚀 Quick Start

### Installation

1. **Clone or download** the project files
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Generate Content

**Hero Animation (15 seconds)**:
```bash
python task1_hero_animation.py
```

**Explainer Video (45 seconds)**:
```bash
python task2_explainer_video.py
```

**Social Media Post**:
```bash
python task3_social_media.py
```

## 🎨 Design Features

### Brand Consistency
- **Color Palette**: Purple gradients (#6B73FF to #9B59B6) with dark backgrounds
- **Typography**: Clean, modern sans-serif fonts
- **Animation**: Smooth 30fps transitions with mathematical precision

### Technical Innovation
- **Programmatic Generation**: Pixel-perfect control over all visual elements
- **Mathematical Animations**: Algorithmic particle systems and smooth interpolations
- **Scalable Architecture**: Modular code structure for easy customization

### Visual Storytelling
- **Hero Animation**: Brand introduction with dynamic particle effects
- **Explainer Video**: Problem-solution narrative with timed visual metaphors
- **Social Media**: Circular workflow visualization representing comprehensive AI evaluation

## 📊 Output Specifications

| Content Type | Resolution | Duration | Format |
|--------------|------------|----------|---------|
| Hero Animation | 1920×1080 | 15s | MP4 |
| Explainer Video | 1920×1080 | 45s | MP4 |
| Social Media Post | 1080×1080 | Static | PNG |

## 🔧 Customization

### Brand Colors
Edit `brand_config.py` to modify:
- Primary/secondary colors
- Background themes
- Accent colors

### Animation Settings
Adjust in `brand_config.py`:
- Frame rate (default: 30fps)
- Duration settings
- Resolution preferences

### Content
Modify text content and messaging in the respective task files or `brand_config.py`.

## 📋 Requirements

- **Python**: 3.8 or higher
- **Memory**: 4GB RAM minimum (8GB recommended for video processing)
- **Storage**: 500MB free space for output files
- **OS**: Windows, macOS, or Linux

## 🎯 Design Philosophy

This project emphasizes:
- **Programmatic Precision**: Mathematical control over visual elements
- **Brand Consistency**: Unified visual identity across all deliverables
- **Technical Innovation**: Advanced animation techniques using code
- **Scalability**: Modular architecture for future enhancements

## 📝 Notes

- All animations render at 30fps for smooth playback
- Output files are saved in the `file/` directory
- Processing time varies based on system specifications
- Brand colors and messaging align with LLUMO AI's identity

## 🏆 Assignment Completion

This project fulfills all requirements of the LLUMO AI Graphic Designer assignment:
- ✅ Hero animation with brand elements
- ✅ Explainer video with clear messaging
- ✅ Social media post optimized for Instagram
- ✅ Consistent brand application across all deliverables
- ✅ Technical innovation through programmatic design

---

*Created for LLUMO AI Graphic Designer Assignment*