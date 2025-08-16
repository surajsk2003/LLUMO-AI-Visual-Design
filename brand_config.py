"""
LLUMO AI Brand Configuration
Contains colors, fonts, and styling constants for consistent branding
"""

# LLUMO AI Brand Colors
BRAND_COLORS = {
    'primary_purple': '#6B73FF',
    'secondary_purple': '#9B59B6',
    'dark_bg': '#0D0D0D',
    'dark_gray': '#1A1A1A',
    'light_gray': '#2E2E2E',
    'text_white': '#FFFFFF',
    'text_gray': '#CCCCCC',
    'accent_blue': '#00D4FF',
    'error_red': '#FF4757',
    'warning_orange': '#FF6B35',
    'success_green': '#2ED573'
}

# Animation Settings
ANIMATION_CONFIG = {
    'fps': 30,
    'hero_duration': 15,  # seconds
    'explainer_duration': 45,  # seconds
    'resolution': (1920, 1080),
    'social_resolution': (1080, 1080)
}

# Typography (font sizes relative to image height)
TYPOGRAPHY = {
    'hero_title': 0.08,
    'hero_subtitle': 0.04,
    'body_text': 0.03,
    'small_text': 0.02
}

# Weak AI vs Robust AI Content
WEAK_AI_FEATURES = [
    "Hallucinations",
    "Slow & Time Taking", 
    "Unreliable",
    "Costs are High"
]

ROBUST_AI_FEATURES = [
    "No Hallucinations",
    "Fast",
    "Reliable", 
    "Low Costs",
    "Working Agents"
]

# Explainer Video Script
EXPLAINER_SCRIPT = [
    {"time": 0, "text": "Traditional AI evaluation is complex", "duration": 5},
    {"time": 5, "text": "Scattered evaluation methods", "duration": 5},
    {"time": 10, "text": "Introducing Eval360 Engine", "duration": 5},
    {"time": 15, "text": "Build Custom Evals Fast", "duration": 8},
    {"time": 23, "text": "Turn Feedback into Metrics", "duration": 8},
    {"time": 31, "text": "Experience LLUMO AI today", "duration": 14}
]