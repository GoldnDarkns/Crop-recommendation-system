import io
import json
import os
import requests
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ===========================================
# CONFIGURATION
# ===========================================
BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "https://prerna-gade-crop-recommendation-backend.hf.space"
)

SINGLE_PREDICT_ENDPOINT = f"{BACKEND_URL}/predict"
BATCH_PREDICT_ENDPOINT = f"{BACKEND_URL}/batch_predict"

# ===========================================
# PAGE CONFIGURATION
# ===========================================
st.set_page_config(
    page_title="Smart Crop Advisor | AI-Powered Agriculture",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===========================================
# AGRICULTURE-THEMED CSS - LIGHT & NATURAL
# ===========================================
st.markdown("""
<style>
    /* Remove default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Cute Plant Theme - Animated & Adorable - DARKER GREEN, SOOTHING BACKGROUND */
    .main {
        background: linear-gradient(180deg, #c8e6c9 0%, #a5d6a7 30%, #81c784 60%, #66bb6a 100%) !important;
        min-height: 100vh;
        position: relative;
        overflow-x: hidden;
        animation: gentlePulse 8s ease-in-out infinite;
    }
    
    @keyframes gentlePulse {
        0%, 100% {
            background: linear-gradient(180deg, #c8e6c9 0%, #a5d6a7 30%, #81c784 60%, #66bb6a 100%);
        }
        50% {
            background: linear-gradient(180deg, #d4edda 0%, #c3e6cb 30%, #a5d6a7 60%, #81c784 100%);
        }
    }
    
    /* Force all Streamlit containers to have light background */
    .main .block-container, .stApp, [data-testid="stAppViewContainer"], 
    [data-testid="stApp"], .stApp > header, .stApp > div {
        background: transparent !important;
        background-color: transparent !important;
    }
    
    /* Force body and html to darker green, soothing */
    html, body {
        background: linear-gradient(180deg, #c8e6c9 0%, #a5d6a7 30%, #81c784 60%, #66bb6a 100%) !important;
        background-color: #a5d6a7 !important;
    }
    
    /* Override any dark Streamlit defaults - but be selective */
    section[data-testid="stAppViewContainer"] > div,
    .stApp > div > div {
        background: transparent !important;
    }
    
    /* Force Streamlit widgets to have light backgrounds */
    .stNumberInput, .stTextInput, .stSelectbox, .stTextArea {
        background: transparent !important;
    }
    
    /* Force Streamlit columns to be transparent */
    [data-testid="column"] {
        background: transparent !important;
    }
    
    /* CRITICAL: Force all text elements to be visible with high contrast */
    body, .main, .main * {
        color: #1f2937 !important;
    }
    
    /* Override Streamlit's default text colors */
    [class*="st"], [data-testid*="st"] {
        color: #1f2937 !important;
    }
    
    /* Ensure all paragraph and text content is visible */
    p, span, div, a, label, li, td, th, small {
        color: #1f2937 !important;
    }
    
    /* Headings should be darker green but still visible */
    h1, h2, h3, h4, h5, h6 {
        color: #14532d !important;
    }
    
    /* Exception: White text on colored buttons */
    .stButton > button, 
    .stTabs [aria-selected="true"],
    button[class*="primary"] {
        color: white !important;
    }
    
    /* Force Streamlit text widgets to show text */
    .stText, .stMarkdown, .stWrite {
        color: #1f2937 !important;
    }
    
    /* Input labels must be visible */
    label, [class*="label"] {
        color: #1f2937 !important;
        font-weight: 600 !important;
    }
    
    /* All Streamlit markdown content */
    .stMarkdown p, .stMarkdown span, .stMarkdown div,
    .stMarkdown ul, .stMarkdown ol, .stMarkdown li {
        color: #1f2937 !important;
    }
    
    /* Info boxes text - Force light greenish backgrounds and dark text - FIX OVERLAYS */
    [data-baseweb="toast"], .stSuccess, .stError, .stInfo, .stWarning {
        color: #1f2937 !important;
        background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 50%, #c8e6c9 100%) !important;
        background-color: #e8f5e9 !important;
        border: 2px solid rgba(134, 239, 172, 0.6) !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 15px rgba(34, 197, 94, 0.2) !important;
    }
    
    [data-baseweb="toast"] *, .stSuccess *, .stError *, .stInfo *, .stWarning * {
        color: #1f2937 !important;
    }
    
    /* Spinner - Remove dark background */
    .stSpinner > div {
        background: transparent !important;
    }
    
    /* Remove ALL dark backgrounds */
    div[style*="background"], div[style*="background-color"] {
        background: #f0fdf4 !important;
        background-color: #f0fdf4 !important;
    }
    
    /* Force all containers to have light background */
    div, section, article, main, aside {
        background-color: transparent !important;
    }
    
    /* Exception: Only our custom cards should have light greenish backgrounds */
    .modern-card, .stat-card, .feature-card, .crop-info-panel, 
    .result-card, .input-card, .why-crop-box {
        background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 50%, #c8e6c9 100%) !important;
        color: #1f2937 !important;
    }
    
    /* Remove any black or dark backgrounds from Streamlit elements */
    [class*="st"], [data-testid*="st"] {
        background-color: transparent !important;
    }
    
    /* Force all text containers to be visible */
    [class*="element-container"], [data-testid*="element-container"] {
        background: transparent !important;
    }
    
    /* Remove dark backgrounds from any divs */
    div:not(.modern-card):not(.stat-card):not(.feature-card):not(.crop-info-panel):not(.result-card):not(.input-card):not(.why-crop-box) {
        background-color: transparent !important;
    }
    
    /* Animated Plant Background Elements */
    .plant-bg {
        position: fixed;
        pointer-events: none;
        z-index: 0;
        opacity: 0.15;
    }
    
    .floating-plant {
        position: absolute;
        font-size: 3rem;
        animation: floatPlant 6s ease-in-out infinite;
    }
    
    @keyframes floatPlant {
        0%, 100% {
            transform: translateY(0px) rotate(0deg);
        }
        50% {
            transform: translateY(-20px) rotate(5deg);
        }
    }
    
    .growing-plant {
        position: absolute;
        font-size: 2.5rem;
        animation: growPlant 4s ease-in-out infinite;
        transform-origin: bottom center;
    }
    
    @keyframes growPlant {
        0%, 100% {
            transform: scaleY(0.8);
        }
        50% {
            transform: scaleY(1.1);
        }
    }
    
    .bouncing-leaf {
        position: absolute;
        font-size: 2rem;
        animation: bounceLeaf 3s ease-in-out infinite;
    }
    
    @keyframes bounceLeaf {
        0%, 100% {
            transform: translateY(0px) rotate(0deg);
        }
        25% {
            transform: translateY(-15px) rotate(-10deg);
        }
        75% {
            transform: translateY(-10px) rotate(10deg);
        }
    }
    
    html, body, [class*="css"] {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #1f2937 !important;
        background: linear-gradient(180deg, #c8e6c9 0%, #a5d6a7 30%, #81c784 60%, #66bb6a 100%) !important;
    }
    
    /* Force all text to be dark and readable - but be more selective */
    p, span, div, h1, h2, h3, h4, h5, h6, label, li, td, th {
        color: #1f2937 !important;
    }
    
    /* Exception for white text on colored backgrounds */
    .stButton>button, .stTabs [aria-selected="true"] {
        color: white !important;
    }
    
    /* Force Streamlit markdown text to be visible - BIGGER */
    .stMarkdown {
        font-size: 1.15rem !important;
        line-height: 1.7 !important;
    }
    
    .stMarkdown p, .stMarkdown span, .stMarkdown div {
        color: #1f2937 !important;
        font-size: 1.15rem !important;
        line-height: 1.7 !important;
    }
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
        color: #14532d !important;
    }
    
    .stMarkdown h1 { font-size: 3rem !important; }
    .stMarkdown h2 { font-size: 2.5rem !important; }
    .stMarkdown h3 { font-size: 2rem !important; }
    .stMarkdown h4 { font-size: 1.75rem !important; }
    
    .stMarkdown ul, .stMarkdown li {
        color: #1f2937 !important;
        font-size: 1.15rem !important;
        line-height: 1.7 !important;
    }
    
    /* Crop info panel text */
    .crop-info-panel, .crop-info-panel *, .why-crop-box, .why-crop-box * {
        color: #1f2937 !important;
    }
    
    .crop-info-panel h3, .crop-info-panel h4 {
        color: #14532d !important;
    }
    
    /* Main Container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
        background: transparent;
    }
    
    /* Cute Floating Plants Background */
    .plant-bg-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 0;
        overflow: hidden;
    }
    
    .floating-plant-emoji {
        position: absolute;
        font-size: 2.5rem;
        opacity: 0.15;
        animation: floatAround 20s linear infinite;
    }
    
    @keyframes floatAround {
        0% {
            transform: translate(0, 0) rotate(0deg);
        }
        25% {
            transform: translate(100px, -50px) rotate(90deg);
        }
        50% {
            transform: translate(200px, 50px) rotate(180deg);
        }
        75% {
            transform: translate(100px, 150px) rotate(270deg);
        }
        100% {
            transform: translate(0, 0) rotate(360deg);
        }
    }
    
    /* Hero Section - Cute Plant Theme with Animated Plants */
    .hero-section {
        background: linear-gradient(135deg, rgba(134, 239, 172, 0.3) 0%, rgba(74, 222, 128, 0.3) 50%, rgba(34, 197, 94, 0.3) 100%);
        background-size: 200% 200%;
        padding: 80px 40px;
        border-radius: 30px;
        text-align: center;
        color: #1f2937;
        margin-bottom: 60px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 15px 50px rgba(34, 197, 94, 0.2);
        border: 3px solid rgba(34, 197, 94, 0.3);
        animation: fadeInUpHero 0.6s ease-out 0.1s both, gradientShift 15s ease infinite;
        z-index: 1;
    }
    
    .hero-section::before {
        content: '🌱🌿🌾🌻🌷🌺🌼🌸';
        position: absolute;
        top: -20px;
        left: -20px;
        font-size: 4rem;
        opacity: 0.1;
        animation: floatPlant 8s ease-in-out infinite;
    }
    
    .hero-section::after {
        content: '🌾🌿🌱🌷🌻🌺🌼🌸';
        position: absolute;
        bottom: -20px;
        right: -20px;
        font-size: 4rem;
        opacity: 0.1;
        animation: floatPlant 10s ease-in-out infinite reverse;
    }
    
    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    @keyframes fadeInUpHero {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .hero-title {
        font-size: 4.5rem !important;
        font-weight: 900;
        margin-bottom: 20px;
        color: #15803d;
        position: relative;
        z-index: 2;
        text-shadow: 0 2px 8px rgba(34, 197, 94, 0.3), 0 0 20px rgba(74, 222, 128, 0.2);
        animation: titleBounce 2s ease-in-out infinite, titleGlow 3s ease-in-out infinite alternate;
        letter-spacing: 1px;
    }
    
    @keyframes titleBounce {
        0%, 100% {
            transform: scale(1) rotate(0deg);
        }
        25% {
            transform: scale(1.02) rotate(-0.5deg);
        }
        50% {
            transform: scale(1.03) rotate(0deg);
        }
        75% {
            transform: scale(1.02) rotate(0.5deg);
        }
    }
    
    @keyframes titleGlow {
        0% {
            text-shadow: 0 2px 8px rgba(34, 197, 94, 0.3), 0 0 20px rgba(74, 222, 128, 0.2);
        }
        100% {
            text-shadow: 0 4px 15px rgba(34, 197, 94, 0.5), 0 0 30px rgba(74, 222, 128, 0.4);
        }
    }
    
    /* Cute plant decorations around hero title */
    .hero-title::before {
        content: '🌾🌿🌱';
        position: absolute;
        left: -80px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 2.5rem;
        opacity: 0.4;
        animation: floatPlant 4s ease-in-out infinite;
        z-index: -1;
    }
    
    .hero-title::after {
        content: '🌱🌿🌾';
        position: absolute;
        right: -80px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 2.5rem;
        opacity: 0.4;
        animation: floatPlant 5s ease-in-out infinite reverse;
        z-index: -1;
    }
    
    .hero-subtitle {
        font-size: 1.8rem !important;
        margin-bottom: 30px;
        color: #166534;
        position: relative;
        z-index: 2;
        font-weight: 500;
    }
    
    /* Scroll-triggered fade-in animations - now using CSS animations */
    .fade-in-up {
        animation: fadeInUp 0.45s ease-out both;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(28px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Ensure elements are visible by default, then animate */
    .modern-card, .feature-card, .stat-card, .section-header {
        visibility: visible;
    }
    
    /* Modern Card Design - Cute Plant Theme - MORE GREENISH */
    .modern-card {
        background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 50%, #c8e6c9 100%) !important;
        border-radius: 25px;
        padding: 30px;
        box-shadow: 0 4px 20px rgba(34, 197, 94, 0.2);
        transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
        border: 2px solid rgba(134, 239, 172, 0.5);
        margin-bottom: 30px;
        color: #1f2937 !important;
        animation: fadeInUp 0.5s ease-out both;
        position: relative;
        overflow: hidden;
    }
    
    .modern-card * {
        color: #1f2937 !important;
    }
    
    .modern-card::before {
        content: '🌿';
        position: absolute;
        top: 10px;
        right: 15px;
        font-size: 2rem;
        opacity: 0.2;
        animation: floatPlant 4s ease-in-out infinite;
    }
    
    .modern-card:hover {
        transform: translateY(-8px) scale(1.03);
        box-shadow: 0 12px 30px rgba(34, 197, 94, 0.25);
        border-color: rgba(34, 197, 94, 0.6);
        background: linear-gradient(135deg, #ffffff 0%, #dcfce7 100%);
    }
    
    .modern-card h3 {
        color: #14532d;
        font-weight: 700;
        margin-bottom: 15px;
    }
    
    .modern-card p, .modern-card li {
        color: #4b5563;
        line-height: 1.6;
    }
    
    .modern-card ul {
        color: #4b5563;
    }
    
    /* Input Cards - Cute Plant Theme - MORE GREENISH */
    .input-card {
        background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 50%, #c8e6c9 100%) !important;
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        border-left: 6px solid #4ade80;
        border: 2px solid rgba(134, 239, 172, 0.5);
        transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
        color: #1f2937 !important;
        position: relative;
        overflow: hidden;
    }
    
    .input-card * {
        color: #1f2937 !important;
    }
    
    .input-card::before {
        content: '🌿';
        position: absolute;
        top: 10px;
        right: 15px;
        font-size: 1.8rem;
        opacity: 0.2;
        animation: bounceLeaf 4s ease-in-out infinite;
    }
    
    .input-card:hover {
        border-left-color: #22c55e;
        box-shadow: 0 8px 20px rgba(34, 197, 94, 0.25);
        border-color: rgba(34, 197, 94, 0.5);
        transform: translateY(-3px);
    }
    
    /* Result Card - Cute Plant Theme with reveal animation - NO BLACK */
    .result-card {
        background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 50%, #c8e6c9 100%) !important;
        border-radius: 30px;
        padding: 50px;
        text-align: center;
        box-shadow: 0 8px 30px rgba(34, 197, 94, 0.3);
        margin: 40px 0;
        animation: resultReveal 0.6s ease-out;
        position: relative;
        overflow: hidden;
        border: 3px solid rgba(74, 222, 128, 0.6);
        color: #1f2937 !important;
    }
    
    .result-card * {
        color: #1f2937 !important;
    }
    
    .result-card h2 {
        color: #14532d !important;
    }
    
    .result-card::before {
        content: '🌻🌷🌺🌼🌸🌾🌿🌱';
        position: absolute;
        top: -30px;
        left: -30px;
        font-size: 5rem;
        opacity: 0.1;
        animation: floatPlant 12s ease-in-out infinite;
    }
    
    .result-card::after {
        content: '🌱🌿🌾🌸🌼🌺🌷🌻';
        position: absolute;
        bottom: -30px;
        right: -30px;
        font-size: 5rem;
        opacity: 0.1;
        animation: floatPlant 15s ease-in-out infinite reverse;
    }
    
    .result-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.05) 0%, transparent 70%);
        animation: pulse 3s ease-in-out infinite;
    }
    
    @keyframes resultReveal {
        from {
            opacity: 0;
            transform: scale(0.95);
            box-shadow: 0 0 0 rgba(0,0,0,0);
        }
        to {
            opacity: 1;
            transform: scale(1);
            box-shadow: 0 2px 12px rgba(0,0,0,0.25);
        }
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(30px) scale(0.95);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 0.8; }
    }
    
    .crop-name {
        font-size: 5rem;
        font-weight: 900;
        margin: 30px 0;
        text-shadow: 0 0 20px currentColor, 0 0 40px currentColor, 0 0 60px currentColor;
        position: relative;
        z-index: 1;
        animation: cropNameGlow 2s ease-in-out infinite;
        letter-spacing: 2px;
    }
    
    @keyframes cropNameGlow {
        0%, 100% {
            text-shadow: 0 0 20px currentColor, 0 0 40px currentColor, 0 0 60px currentColor;
            transform: scale(1);
        }
        50% {
            text-shadow: 0 0 30px currentColor, 0 0 60px currentColor, 0 0 90px currentColor, 0 0 120px currentColor;
            transform: scale(1.05);
        }
    }
    
    .crop-emoji {
        font-size: 6rem;
        margin-bottom: 20px;
        position: relative;
        z-index: 1;
        animation: cuteBounce 2s ease-in-out infinite;
        filter: drop-shadow(0 4px 8px rgba(34, 197, 94, 0.3));
    }
    
    @keyframes cuteBounce {
        0%, 100% { 
            transform: translateY(0) scale(1) rotate(0deg); 
        }
        25% { 
            transform: translateY(-15px) scale(1.1) rotate(-5deg); 
        }
        50% { 
            transform: translateY(-20px) scale(1.15) rotate(0deg); 
        }
        75% { 
            transform: translateY(-15px) scale(1.1) rotate(5deg); 
        }
    }
    
    /* Modern Buttons - Cute Plant Theme with press feedback */
    .stButton>button {
        background: linear-gradient(135deg, #4ade80 0%, #22c55e 50%, #16a34a 100%);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 15px 40px;
        font-weight: 700;
        font-size: 1.2rem;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 6px 20px rgba(34, 197, 94, 0.4);
        position: relative;
        overflow: hidden;
        animation: buttonGlow 2s ease-in-out infinite;
    }
    
    @keyframes buttonGlow {
        0%, 100% {
            box-shadow: 0 6px 20px rgba(34, 197, 94, 0.4);
        }
        50% {
            box-shadow: 0 8px 25px rgba(34, 197, 94, 0.6);
        }
    }
    
    .stButton>button::after {
        content: '🌱';
        position: absolute;
        right: 20px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 1.3rem;
        animation: bounceLeaf 2s ease-in-out infinite;
    }
    
    .stButton>button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255,255,255,0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton>button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton>button:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow: 0 10px 30px rgba(34, 197, 94, 0.5);
        background: linear-gradient(135deg, #22c55e 0%, #4ade80 50%, #16a34a 100%);
    }
    
    .stButton>button:active {
        transform: scale(0.97);
        transition: transform 0.15s ease;
    }
    
    .stButton>button.pressed {
        animation: buttonBounce 0.3s ease;
    }
    
    @keyframes buttonBounce {
        0% { transform: scale(0.97); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    /* Stats Cards - SUPER CUTE PLANT THEME - ADORABLE & ANIMATED */
    .stat-card {
        background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 50%, #c8e6c9 100%) !important;
        border-radius: 25px;
        padding: 30px 25px;
        text-align: center;
        box-shadow: 0 6px 25px rgba(34, 197, 94, 0.3);
        transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
        border: 3px solid rgba(74, 222, 128, 0.4);
        color: #1f2937 !important;
        animation: fadeInUp 0.6s ease-out 0.2s both, gentleBounce 4s ease-in-out infinite;
        position: relative;
        overflow: visible;
    }
    
    .stat-card * {
        color: #1f2937 !important;
    }
    
    /* Multiple cute plant decorations */
    .stat-card::before {
        content: '🌿';
        position: absolute;
        top: 10px;
        left: 15px;
        font-size: 2rem;
        opacity: 0.4;
        animation: cuteWiggle 3s ease-in-out infinite;
        z-index: 1;
    }
    
    .stat-card::after {
        content: '🌱';
        position: absolute;
        bottom: 10px;
        right: 15px;
        font-size: 2rem;
        opacity: 0.4;
        animation: growPlant 3s ease-in-out infinite;
        z-index: 1;
    }
    
    /* Additional floating plant stickers */
    .stat-card .plant-sticker-1 {
        position: absolute;
        top: 5px;
        right: 20px;
        font-size: 1.8rem;
        opacity: 0.3;
        animation: floatPlant 4s ease-in-out infinite;
        z-index: 1;
    }
    
    .stat-card .plant-sticker-2 {
        position: absolute;
        bottom: 15px;
        left: 20px;
        font-size: 1.5rem;
        opacity: 0.3;
        animation: bounceLeaf 3.5s ease-in-out infinite;
        z-index: 1;
    }
    
    .stat-card:hover {
        transform: translateY(-12px) scale(1.08) rotate(1deg);
        box-shadow: 0 15px 40px rgba(34, 197, 94, 0.4), 0 0 20px rgba(74, 222, 128, 0.3);
        border-color: rgba(34, 197, 94, 0.8);
        background: linear-gradient(135deg, #ffffff 0%, #dcfce7 100%);
        animation: gentleBounce 2s ease-in-out infinite, cardGlow 2s ease-in-out infinite alternate;
    }
    
    @keyframes cardGlow {
        0% {
            box-shadow: 0 15px 40px rgba(34, 197, 94, 0.4), 0 0 20px rgba(74, 222, 128, 0.3);
        }
        100% {
            box-shadow: 0 15px 45px rgba(34, 197, 94, 0.5), 0 0 30px rgba(74, 222, 128, 0.5);
        }
    }
    
    .stat-number {
        font-size: 4rem !important;
        font-weight: 900;
        color: #14532d;
        margin: 15px 0;
        position: relative;
        z-index: 2;
        text-shadow: 0 2px 8px rgba(34, 197, 94, 0.3);
        animation: numberPulse 2s ease-in-out infinite;
    }
    
    @keyframes numberPulse {
        0%, 100% {
            transform: scale(1);
            text-shadow: 0 2px 8px rgba(34, 197, 94, 0.3);
        }
        50% {
            transform: scale(1.05);
            text-shadow: 0 4px 15px rgba(34, 197, 94, 0.5);
        }
    }
    
    .stat-label {
        font-size: 1.4rem !important;
        color: #14532d;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 700;
        position: relative;
        z-index: 2;
        margin-top: 10px;
        animation: labelGlow 3s ease-in-out infinite;
    }
    
    @keyframes labelGlow {
        0%, 100% {
            color: #14532d;
        }
        50% {
            color: #22c55e;
            text-shadow: 0 0 10px rgba(34, 197, 94, 0.4);
        }
    }
    
    /* Feature Cards - Cute Plant Theme - MORE GREENISH */
    .feature-card {
        background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 50%, #c8e6c9 100%) !important;
        border-radius: 25px;
        padding: 30px;
        color: #1f2937 !important;
        text-align: center;
        margin: 20px 0;
        transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
        box-shadow: 0 4px 20px rgba(34, 197, 94, 0.15);
        border: 2px solid rgba(134, 239, 172, 0.4);
        animation: fadeInUp 0.5s ease-out both;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '🌿';
        position: absolute;
        top: 15px;
        left: 15px;
        font-size: 2rem;
        opacity: 0.2;
        animation: bounceLeaf 4s ease-in-out infinite;
    }
    
    .feature-card:hover {
        transform: scale(1.06) rotate(1deg);
        box-shadow: 0 12px 35px rgba(34, 197, 94, 0.3);
        border-color: rgba(34, 197, 94, 0.6);
        background: linear-gradient(135deg, #ffffff 0%, #dcfce7 100%);
    }
    
    .feature-card h3 {
        color: #14532d;
        font-weight: 700;
    }
    
    .feature-card p {
        color: #4b5563;
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 15px;
    }
    
    /* Input Fields Enhancement - Interactive & Cute */
    .stNumberInput>div>div>input {
        border-radius: 12px;
        border: 2px solid rgba(134, 239, 172, 0.4);
        background-color: #FFFFFF !important;
        color: #1f2937 !important;
        transition: all 0.3s ease;
        font-weight: 500;
        padding: 10px 15px;
        font-size: 1rem !important;
        letter-spacing: normal !important;
        text-transform: none !important;
        width: 100% !important;
        box-sizing: border-box !important;
    }
    
    .stNumberInput>div>div>input:hover {
        border-color: #4ade80;
        box-shadow: 0 4px 12px rgba(34, 197, 94, 0.2);
        transform: translateY(-2px);
    }
    
    .stNumberInput>div>div>input:focus {
        border-color: #22c55e;
        box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.2), 0 4px 15px rgba(34, 197, 94, 0.3);
        background-color: #FFFFFF !important;
        transform: scale(1.02);
    }
    
    /* Input container styling */
    .stNumberInput>div {
        background: transparent !important;
    }
    
    /* Add plant emoji to input fields on hover */
    .stNumberInput:hover::before {
        content: '🌿';
        position: absolute;
        right: 10px;
        opacity: 0.3;
    }
    
    /* Labels - High Contrast */
    label {
        color: #1f2937 !important;
        font-weight: 600;
    }
    
    /* All text elements - High Contrast - Force dark colors - BIGGER FONTS */
    p, span, div {
        color: #1f2937 !important;
        font-size: 1.15rem !important;
        line-height: 1.7 !important;
    }
    
    /* Fix text elongation and ensure proper display */
    input, select, textarea {
        font-size: 1rem !important;
        letter-spacing: normal !important;
        text-transform: none !important;
        font-stretch: normal !important;
        width: 100% !important;
        box-sizing: border-box !important;
    }
    
    /* Ensure selectbox displays selected value correctly */
    [data-baseweb="select"] > div {
        color: #1f2937 !important;
        font-size: 1rem !important;
        letter-spacing: normal !important;
    }
    
    [data-baseweb="select"] > div > div {
        color: #1f2937 !important;
        font-size: 1rem !important;
        white-space: nowrap !important;
        overflow: visible !important;
        text-overflow: clip !important;
    }
    
    /* Force selected value text to be visible */
    [data-baseweb="select"] > div > div > div,
    [data-baseweb="select"] > div > div > div > div,
    [data-baseweb="select"] span,
    [data-baseweb="select"] > div > div > div > span {
        color: #1f2937 !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        opacity: 1 !important;
        visibility: visible !important;
        display: block !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #1f2937 !important;
    }
    
    h1 { font-size: 3rem !important; }
    h2 { font-size: 2.5rem !important; }
    h3 { font-size: 2rem !important; }
    h4 { font-size: 1.75rem !important; }
    h5 { font-size: 1.5rem !important; }
    h6 { font-size: 1.25rem !important; }
    
    /* INTERACTIVE TEXT HOVER EFFECTS - SELECTIVE, NO JITTER */
    /* Only apply to specific text elements, not containers */
    h1:hover, h2:hover, h3:hover, h4:hover, h5:hover, h6:hover {
        text-shadow: 0 0 15px rgba(34, 197, 94, 0.6), 
                     0 0 25px rgba(34, 197, 94, 0.4) !important;
        transition: text-shadow 0.3s ease !important;
        color: #14532d !important;
    }
    
    /* Only text content, not containers */
    .stMarkdown p:hover, .stMarkdown li:hover, 
    .modern-card p:hover, .modern-card li:hover,
    .crop-info-panel p:hover, .crop-info-panel li:hover {
        text-shadow: 0 0 8px rgba(34, 197, 94, 0.5) !important;
        transition: text-shadow 0.3s ease !important;
        color: #14532d !important;
    }
    
    /* Exclude interactive elements and containers */
    button:hover, .stButton:hover, input:hover, select:hover,
    .stSelectbox:hover, .stNumberInput:hover, .stTextInput:hover,
    div:hover, section:hover, article:hover, main:hover {
        /* No hover effects on containers */
    }
    
    /* Secondary text */
    .stMarkdown, .stText, .stMarkdown p, .stMarkdown span, .stMarkdown div {
        color: #1f2937 !important;
    }
    
    /* Captions */
    .stCaption {
        color: #6b7280 !important;
    }
    
    /* Force all Streamlit text to be dark */
    [class*="st"], [data-testid] {
        color: #1f2937 !important;
    }
    
    /* Help text and tooltips */
    [data-testid="stTooltip"], .stTooltip {
        color: #1f2937 !important;
        background: #FFFFFF !important;
    }
    
    /* All headings */
    h1, h2, h3, h4, h5, h6, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #14532d !important;
    }
    
    /* Small text and labels */
    small, .small, [class*="label"] {
        color: #4b5563 !important;
    }
    
    /* Remove old tab styling - using new multi-row version below */
    
    /* Tab content animation */
    .stTabs [data-baseweb="tab-panel"] {
        animation: tabFadeIn 0.4s ease-out;
        border: none !important;
        padding: 20px 0 !important;
        margin-top: 10px;
        background: transparent !important;
    }
    
    @keyframes tabFadeIn {
        from {
            opacity: 0;
            transform: translateX(10px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Chart container animations */
    .chart-container {
        animation: chartEntrance 0.5s ease-out both;
    }
    
    @keyframes chartEntrance {
        from {
            opacity: 0;
            transform: scale(0.85);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    /* Ensure all animated elements are visible - CSS animations work immediately */
    .modern-card, .feature-card, .stat-card, .section-header, .input-section {
        visibility: visible !important;
        opacity: 1 !important;
    }
    
    /* Override any opacity: 0 that might be set elsewhere */
    .modern-card, .feature-card, .stat-card {
        animation: fadeInUp 0.5s ease-out both !important;
    }
    
    /* Make sure stat cards are visible */
    .stat-card {
        opacity: 1 !important;
        transform: translateY(0) !important;
    }
    
    /* Make sure feature cards are visible */
    .feature-card {
        opacity: 1 !important;
        transform: translateY(0) !important;
    }
    
    /* Make sure modern cards are visible */
    .modern-card {
        opacity: 1 !important;
        transform: translateY(0) !important;
    }
    
    /* Input form section animation */
    .input-section {
        animation: fadeInUp 0.5s ease-out 0.1s both;
    }
    
    /* Section Headers - Cute Plant Theme with animated underline - BIGGER */
    .section-header {
        font-size: 3rem !important;
        font-weight: 800;
        color: #15803d;
        margin: 40px 0 20px 0;
        text-align: center;
        position: relative;
        padding-bottom: 20px;
        animation: fadeInUp 0.5s ease-out both;
        text-shadow: 0 2px 8px rgba(34, 197, 94, 0.2);
    }
    
    .section-header::before {
        content: '🌿';
        position: absolute;
        left: 10%;
        top: 50%;
        transform: translateY(-50%);
        font-size: 2rem;
        opacity: 0.4;
        animation: bounceLeaf 3s ease-in-out infinite;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 120px;
        height: 5px;
        background: linear-gradient(135deg, #4ade80 0%, #22c55e 100%);
        border-radius: 3px;
        animation: underlineGlow 5s ease-in-out infinite;
        box-shadow: 0 2px 8px rgba(34, 197, 94, 0.4);
    }
    
    @keyframes underlineGlow {
        0%, 100% {
            opacity: 0.7;
            width: 120px;
            box-shadow: 0 2px 8px rgba(34, 197, 94, 0.3);
        }
        50% {
            opacity: 1;
            width: 180px;
            box-shadow: 0 4px 15px rgba(34, 197, 94, 0.6);
        }
    }
    
    /* Crop Info Panel - Cute Plant Theme */
    .crop-info-panel {
        background: linear-gradient(135deg, #ffffff 0%, #f0fdf4 100%);
        border-radius: 25px;
        padding: 40px;
        margin: 30px 0;
        box-shadow: 0 6px 25px rgba(34, 197, 94, 0.2);
        border-left: 6px solid #4ade80;
        border: 2px solid rgba(134, 239, 172, 0.4);
        animation: fadeInUp 0.6s ease-out both;
        position: relative;
        overflow: hidden;
    }
    
    .crop-info-panel::before {
        content: '🌿🌱';
        position: absolute;
        top: 15px;
        right: 20px;
        font-size: 2.5rem;
        opacity: 0.15;
        animation: bounceLeaf 5s ease-in-out infinite;
    }
    
    .crop-info-panel h3 {
        color: #14532d !important;
        font-weight: 700;
        margin-bottom: 20px;
        font-size: 1.8rem;
    }
    
    .crop-info-panel h4 {
        color: #15803d !important;
        font-weight: 600;
        margin-top: 25px;
        margin-bottom: 15px;
        font-size: 1.3rem;
    }
    
    .crop-info-panel p {
        color: #1f2937 !important;
        line-height: 1.7;
        margin-bottom: 15px;
        font-size: 1.1rem;
    }
    
    .crop-info-panel ul {
        color: #1f2937 !important;
        line-height: 1.8;
        margin-left: 20px;
        font-size: 1rem;
    }
    
    .crop-info-panel li {
        color: #1f2937 !important;
        margin-bottom: 12px;
        font-size: 1rem;
    }
    
    .crop-info-panel strong {
        color: #14532d !important;
        font-weight: 700;
    }
    
    .why-crop-box {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border-radius: 20px;
        padding: 25px;
        margin-top: 20px;
        border-left: 5px solid #4ade80;
        border: 2px solid rgba(134, 239, 172, 0.3);
        position: relative;
    }
    
    .why-crop-box::after {
        content: '✨';
        position: absolute;
        top: 10px;
        right: 15px;
        font-size: 1.5rem;
        opacity: 0.3;
        animation: bounceLeaf 3s ease-in-out infinite;
    }
    
    /* Info Boxes - Agriculture Theme */
    .info-box {
        background: #FFFFFF;
        border-left: 5px solid #22c55e;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 2px 12px rgba(20, 83, 45, 0.08);
        border: 1px solid rgba(15, 23, 42, 0.08);
        color: #1f2937;
    }
    
    /* Streamlit default elements - Agriculture Theme */
    .stDataFrame {
        background-color: #FFFFFF;
    }
    
    /* Metrics - High Contrast */
    [data-testid="stMetricValue"] {
        color: #14532d !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #6b7280 !important;
    }
    
    /* Success/Error/Info/Warning boxes - Cute Plant Theme - FORCE LIGHT */
    .stSuccess, .stSuccess > div {
        background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%) !important;
        background-color: #dcfce7 !important;
        border: 2px solid rgba(74, 222, 128, 0.5) !important;
        border-radius: 15px !important;
        color: #1f2937 !important;
        box-shadow: 0 4px 15px rgba(34, 197, 94, 0.15) !important;
        padding: 15px !important;
    }
    
    .stError, .stError > div {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%) !important;
        background-color: #fee2e2 !important;
        border: 2px solid rgba(239, 68, 68, 0.4) !important;
        border-radius: 15px !important;
        color: #991b1b !important;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.15) !important;
        padding: 15px !important;
    }
    
    .stInfo, .stInfo > div {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%) !important;
        background-color: #dbeafe !important;
        border: 2px solid rgba(59, 130, 246, 0.4) !important;
        border-radius: 15px !important;
        color: #1e40af !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.15) !important;
        padding: 15px !important;
    }
    
    .stWarning, .stWarning > div {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%) !important;
        background-color: #fef3c7 !important;
        border: 2px solid rgba(245, 158, 11, 0.4) !important;
        border-radius: 15px !important;
        color: #92400e !important;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.15) !important;
        padding: 15px !important;
    }
    
    /* Force text in all boxes to be visible */
    .stSuccess *, .stError *, .stInfo *, .stWarning * {
        color: inherit !important;
    }
    
    .stSuccess strong, .stError strong, .stInfo strong, .stWarning strong {
        color: #14532d !important;
        font-weight: 700;
    }
    
    /* Tabs - Cute Plant Theme with Breathing Animations - Multi-row Wrapping */
    .stTabs {
        margin-top: 60px !important;
        margin-bottom: 30px !important;
        padding-top: 20px;
        width: 100%;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px !important;
        margin-bottom: 20px;
        padding: 10px 0;
        overflow: visible !important;
        display: flex !important;
        flex-wrap: wrap !important;
        justify-content: flex-start !important;
        align-items: center !important;
        width: 100%;
        border: none !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #4b5563;
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border: 2px solid rgba(134, 239, 172, 0.4);
        border-radius: 15px;
        transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        position: relative;
        padding: 12px 24px !important;
        font-weight: 600;
        font-size: 0.95rem;
        animation: tabBreathe 3s ease-in-out infinite;
        overflow: hidden;
        white-space: nowrap;
        flex: 0 0 auto;
        margin: 4px 0;
        min-width: fit-content;
        box-sizing: border-box;
    }
    
    @keyframes tabBreathe {
        0%, 100% {
            transform: scale(1);
            box-shadow: 0 2px 8px rgba(34, 197, 94, 0.15);
        }
        50% {
            transform: scale(1.02);
            box-shadow: 0 4px 12px rgba(34, 197, 94, 0.25);
        }
    }
    
    .stTabs [data-baseweb="tab"]::before {
        content: '';
        position: absolute;
        left: 8px;
        opacity: 0.4;
        font-size: 1rem;
        transition: all 0.3s ease;
        animation: tabIconBounce 2s ease-in-out infinite;
    }
    
    @keyframes tabIconBounce {
        0%, 100% {
            transform: translateY(0) rotate(0deg);
        }
        50% {
            transform: translateY(-3px) rotate(5deg);
        }
    }
    
    .stTabs [data-baseweb="tab"]::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover::after {
        left: 100%;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
        transform: translateY(-3px) scale(1.03);
        box-shadow: 0 6px 15px rgba(34, 197, 94, 0.3);
        border-color: rgba(34, 197, 94, 0.6);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4ade80 0%, #22c55e 100%) !important;
        color: white !important;
        border-color: rgba(34, 197, 94, 0.8) !important;
        box-shadow: 0 4px 15px rgba(34, 197, 94, 0.4) !important;
        animation: tabActiveGlow 2s ease-in-out infinite !important;
        transform: translateY(-2px) scale(1.05) !important;
        z-index: 10;
    }
    
    /* Remove any borders or lines from tab container */
    .stTabs [data-baseweb="tab-list"]::before,
    .stTabs [data-baseweb="tab-list"]::after {
        display: none !important;
    }
    
    /* Remove borders from tab container wrapper */
    .stTabs > div {
        border: none !important;
        box-shadow: none !important;
    }
    
    /* Remove any divider lines */
    .stTabs [data-baseweb="tab-list"] > * {
        border-bottom: none !important;
        border-top: none !important;
    }
    
    /* Ensure tab panel has no unwanted borders */
    .stTabs [data-baseweb="tab-panel"] {
        border: none !important;
        padding: 20px 0 !important;
        margin-top: 10px;
        box-shadow: none !important;
    }
    
    /* Make tabs uniform width for better symmetry (optional - can be removed if you want natural widths) */
    @media (min-width: 1200px) {
        .stTabs [data-baseweb="tab"] {
            min-width: 180px;
            text-align: center;
        }
    }
    
    @keyframes tabActiveGlow {
        0%, 100% {
            box-shadow: 0 6px 25px rgba(34, 197, 94, 0.4);
        }
        50% {
            box-shadow: 0 8px 35px rgba(34, 197, 94, 0.6), 0 0 20px rgba(34, 197, 94, 0.3);
        }
    }
    
    .stTabs [aria-selected="true"]::before {
        content: '';
        opacity: 1;
        font-size: 1.1rem;
        animation: tabActiveIcon 1.5s ease-in-out infinite;
    }
    
    @keyframes tabActiveIcon {
        0%, 100% {
            transform: translateY(0) rotate(0deg) scale(1);
        }
        50% {
            transform: translateY(-5px) rotate(10deg) scale(1.1);
        }
    }
    
    /* Dataframe styling */
    .dataframe {
        background-color: #FFFFFF;
        color: #1f2937;
    }
    
    /* Expander - Agriculture Theme */
    .streamlit-expanderHeader {
        background-color: #FFFFFF;
        color: #1f2937;
        border: 1px solid rgba(15, 23, 42, 0.08);
    }
    
    .streamlit-expanderContent {
        background-color: #F8FAF4;
        color: #1f2937;
    }
    
    /* File Uploader - Agriculture Theme */
    .stFileUploader {
        background-color: #FFFFFF;
        border: 1px solid rgba(15, 23, 42, 0.08);
    }
    
    /* Selectbox, Multiselect - Agriculture Theme - FIX OVERLAPPING */
    .stSelectbox {
        position: relative;
        z-index: 1;
    }
    
    .stSelectbox>div>div {
        background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 50%, #c8e6c9 100%) !important;
        background-color: #e8f5e9 !important;
        color: #1f2937 !important;
        border: 2px solid rgba(134, 239, 172, 0.5) !important;
        border-radius: 12px !important;
        padding: 8px 12px !important;
        box-shadow: 0 2px 8px rgba(34, 197, 94, 0.2) !important;
        transition: all 0.3s ease !important;
        font-size: 1rem !important;
        letter-spacing: normal !important;
        text-transform: none !important;
        white-space: nowrap !important;
        overflow: visible !important;
        text-overflow: clip !important;
    }
    
    /* Ensure selectbox selected value displays correctly - ALL NESTED ELEMENTS */
    .stSelectbox>div>div>div,
    .stSelectbox>div>div>div>div,
    .stSelectbox>div>div>div>div>div,
    .stSelectbox>div>div>div>div>div>div,
    .stSelectbox span,
    .stSelectbox>div>div span,
    .stSelectbox>div>div>div span,
    .stSelectbox>div>div>div>div span,
    .stSelectbox * {
        color: #1f2937 !important;
        font-size: 1rem !important;
        letter-spacing: normal !important;
        text-transform: none !important;
        opacity: 1 !important;
        visibility: visible !important;
        font-weight: 500 !important;
    }
    
    /* Force BaseWeb select value to be visible */
    [data-baseweb="select"] *,
    [data-baseweb="select"] > div *,
    [data-baseweb="select"] > div > div *,
    [data-baseweb="select"] > div > div > div *,
    [data-baseweb="select"] > div > div > div > div * {
        color: #1f2937 !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    
    /* CRITICAL: Force the value display container to show text */
    [data-baseweb="select"] > div > div:first-child,
    [data-baseweb="select"] > div[role="combobox"],
    [data-baseweb="select"] > div[role="combobox"] > div:first-child {
        color: #1f2937 !important;
        opacity: 1 !important;
        visibility: visible !important;
        min-height: 20px !important;
    }
    
    /* Ensure any span or div with text content is visible */
    [data-baseweb="select"] > div > div > span,
    [data-baseweb="select"] > div > div > div > span,
    [data-baseweb="select"] span:not(:empty) {
        color: #1f2937 !important;
        opacity: 1 !important;
        visibility: visible !important;
        display: inline-block !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
    }
    
    /* Target the specific BaseWeb value display element */
    [data-baseweb="select"] > div[data-baseweb="select"] > div,
    [data-baseweb="select"] > div > div[role="combobox"],
    [data-baseweb="select"] > div > div[role="combobox"] > div,
    [data-baseweb="select"] > div > div[role="combobox"] > div > div {
        color: #1f2937 !important;
        opacity: 1 !important;
        visibility: visible !important;
        display: flex !important;
        align-items: center !important;
    }
    
    /* Fix text input fields */
    .stTextInput>div>div>input {
        font-size: 1rem !important;
        letter-spacing: normal !important;
        text-transform: none !important;
        width: 100% !important;
        box-sizing: border-box !important;
        color: #1f2937 !important;
    }
    
    .stSelectbox>div>div:hover {
        border-color: rgba(34, 197, 94, 0.7) !important;
        box-shadow: 0 4px 12px rgba(34, 197, 94, 0.3) !important;
        transform: translateY(-2px);
    }
    
    .stMultiSelect>div>div {
        background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 50%, #c8e6c9 100%) !important;
        background-color: #e8f5e9 !important;
        color: #1f2937 !important;
        border: 2px solid rgba(134, 239, 172, 0.5) !important;
        border-radius: 12px !important;
    }
    
    /* JSON Display - Agriculture Theme */
    .stJson {
        background-color: #FFFFFF;
        color: #1f2937;
    }
    
    /* Divider - Agriculture Theme */
    hr {
        border-color: rgba(15, 23, 42, 0.1);
    }
    
    /* Streamlit widgets text colors */
    .stNumberInput label, .stSelectbox label, .stTextInput label {
        color: #1f2937 !important;
        font-weight: 600;
    }
    
    /* Streamlit help text */
    [data-testid="stTooltipIcon"] {
        color: #6b7280 !important;
    }
    
    /* Streamlit metric labels and values */
    [data-testid="stMetricValue"] {
        color: #14532d !important;
        font-weight: 700;
        font-size: 1.3rem;
    }
    
    [data-testid="stMetricLabel"] {
        color: #4b5563 !important;
        font-weight: 500;
    }
    
    /* Metric containers - Interactive - MORE GREENISH */
    [data-testid="stMetricContainer"] {
        background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 50%, #c8e6c9 100%) !important;
        padding: 15px;
        border-radius: 15px;
        border: 2px solid rgba(134, 239, 172, 0.5);
        margin: 5px 0;
        transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
        cursor: pointer;
        box-shadow: 0 2px 10px rgba(34, 197, 94, 0.15);
    }
    
    [data-testid="stMetricContainer"]:hover {
        transform: translateY(-8px) scale(1.08);
        box-shadow: 0 12px 30px rgba(34, 197, 94, 0.35);
        border-color: rgba(34, 197, 94, 0.7);
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%) !important;
    }
    
    /* Streamlit success/error/info/warning text */
    .stSuccess, .stError, .stInfo, .stWarning {
        color: #1f2937 !important;
    }
    
    .stSuccess strong, .stError strong, .stInfo strong, .stWarning strong {
        color: #14532d !important;
    }
    
    /* Streamlit dataframe - Interactive - FIX OVERLAYS - MORE GREENISH */
    .stDataFrame, .dataframe, table {
        color: #1f2937 !important;
        background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 50%, #c8e6c9 100%) !important;
        background-color: #e8f5e9 !important;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(34, 197, 94, 0.25);
        border: 2px solid rgba(134, 239, 172, 0.5);
    }
    
    .dataframe th, table th, thead th {
        background: linear-gradient(135deg, #a5d6a7 0%, #81c784 100%) !important;
        background-color: #a5d6a7 !important;
        color: #14532d !important;
        font-weight: 700;
        padding: 15px !important;
        transition: all 0.3s ease;
        border: 1px solid rgba(34, 197, 94, 0.3) !important;
    }
    
    .dataframe th:hover, table th:hover {
        background: linear-gradient(135deg, #81c784 0%, #66bb6a 100%) !important;
        background-color: #81c784 !important;
        transform: scale(1.02);
        box-shadow: 0 2px 8px rgba(34, 197, 94, 0.3);
    }
    
    .dataframe td, table td {
        color: #1f2937 !important;
        background-color: #f1f8f4 !important;
        padding: 12px !important;
        transition: all 0.2s ease;
        border: 1px solid rgba(200, 230, 201, 0.5) !important;
    }
    
    .dataframe tr:hover td, table tr:hover td {
        background: rgba(200, 230, 201, 0.8) !important;
        background-color: rgba(200, 230, 201, 0.8) !important;
        transform: scale(1.01);
    }
    
    /* Fix any dark overlays on dataframes */
    .stDataFrame * {
        color: #1f2937 !important;
    }
    
    /* Remove any dark table backgrounds */
    table, thead, tbody, tr {
        background-color: transparent !important;
    }
    
    /* NUCLEAR OPTION: Force ALL elements to have light or transparent backgrounds */
    * {
        background-image: none !important;
    }
    
    /* Override any inline dark backgrounds */
    [style*="background-color: rgb(0"], [style*="background-color:#000"], 
    [style*="background-color:black"], [style*="background: rgb(0"],
    [style*="background:#000"], [style*="background:black"] {
        background-color: #f0fdf4 !important;
        background: #f0fdf4 !important;
    }
    
    /* Force all Streamlit widget containers to be light greenish */
    [data-baseweb*="base"] {
        background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 50%, #c8e6c9 100%) !important;
        background-color: #e8f5e9 !important;
        color: #1f2937 !important;
    }
    
    [data-baseweb*="tooltip"], [data-baseweb*="modal"] {
        background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 50%, #c8e6c9 100%) !important;
        background-color: #e8f5e9 !important;
        color: #1f2937 !important;
        border: 2px solid rgba(134, 239, 172, 0.5) !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 15px rgba(34, 197, 94, 0.3) !important;
        z-index: 10001 !important;
    }
    
    /* JSON display - force light */
    .stJson, pre, code {
        background-color: #ffffff !important;
        background: #ffffff !important;
        color: #1f2937 !important;
        border: 2px solid rgba(134, 239, 172, 0.3) !important;
        border-radius: 10px !important;
        padding: 15px !important;
    }
    
    /* File uploader - force light */
    .stFileUploader, .stFileUploader > div {
        background-color: #ffffff !important;
        background: #ffffff !important;
        border: 2px dashed rgba(134, 239, 172, 0.4) !important;
        border-radius: 15px !important;
        padding: 20px !important;
    }
    
    /* Selectbox dropdowns - FIX OVERLAPPING - HIGH Z-INDEX */
    [data-baseweb="select"] {
        position: relative;
        z-index: 1000 !important;
    }
    
    [data-baseweb="select"] > div {
        background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 50%, #c8e6c9 100%) !important;
        background-color: #e8f5e9 !important;
        color: #1f2937 !important;
        border: 2px solid rgba(134, 239, 172, 0.5) !important;
        border-radius: 12px !important;
    }
    
    /* CRITICAL: Force ALL text in selectbox to be visible - target every possible element */
    [data-baseweb="select"] *,
    [data-baseweb="select"] > div *,
    [data-baseweb="select"] > div > div *,
    [data-baseweb="select"] > div > div > div *,
    [data-baseweb="select"] > div > div > div > div *,
    [data-baseweb="select"] > div > div > div > div > div * {
        color: #1f2937 !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    
    /* Ensure the selected value text is visible in the selectbox */
    [data-baseweb="select"] > div > div[data-baseweb="select"],
    [data-baseweb="select"] > div > div[role="combobox"],
    [data-baseweb="select"] > div > div[role="combobox"] > div {
        color: #1f2937 !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    
    [data-baseweb="select"] > div > div > div[aria-selected="true"],
    [data-baseweb="select"] > div > div > div[aria-selected="false"],
    [data-baseweb="select"] > div > div > div > div,
    [data-baseweb="select"] > div > div > div > div > div {
        color: #1f2937 !important;
        opacity: 1 !important;
        visibility: visible !important;
        display: flex !important;
        align-items: center !important;
    }
    
    /* Target the actual text content - ALL POSSIBLE NESTED STRUCTURES */
    [data-baseweb="select"] > div > div > div > div > div,
    [data-baseweb="select"] > div > div > div > div > div > span,
    [data-baseweb="select"] > div > div > div > div > span,
    [data-baseweb="select"] > div > div > div > span,
    [data-baseweb="select"] > div > div > span,
    [data-baseweb="select"] > div > span,
    [data-baseweb="select"] span {
        color: #1f2937 !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        opacity: 1 !important;
        visibility: visible !important;
        display: inline-block !important;
    }
    
    /* Force text nodes to be visible */
    [data-baseweb="select"]::before,
    [data-baseweb="select"] > div::before,
    [data-baseweb="select"] > div > div::before {
        color: #1f2937 !important;
    }
    
    /* Dropdown popover - FIX Z-INDEX AND STYLING */
    [data-baseweb="popover"] {
        background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 50%, #c8e6c9 100%) !important;
        background-color: #e8f5e9 !important;
        color: #1f2937 !important;
        border: 2px solid rgba(134, 239, 172, 0.6) !important;
        border-radius: 12px !important;
        box-shadow: 0 8px 25px rgba(34, 197, 94, 0.4) !important;
        z-index: 10000 !important;
        position: fixed !important;
        max-height: 300px !important;
        overflow-y: auto !important;
        padding: 8px 0 !important;
    }
    
    /* Dropdown options */
    [data-baseweb="popover"] [role="option"],
    [data-baseweb="popover"] li,
    [data-baseweb="popover"] div[role="option"] {
        background: transparent !important;
        color: #1f2937 !important;
        padding: 12px 16px !important;
        border-radius: 8px !important;
        margin: 2px 8px !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
    }
    
    [data-baseweb="popover"] [role="option"]:hover,
    [data-baseweb="popover"] li:hover,
    [data-baseweb="popover"] div[role="option"]:hover {
        background: rgba(200, 230, 201, 0.8) !important;
        background-color: rgba(200, 230, 201, 0.8) !important;
        transform: translateX(5px);
    }
    
    [data-baseweb="popover"] [role="option"][aria-selected="true"],
    [data-baseweb="popover"] li[aria-selected="true"] {
        background: linear-gradient(135deg, #a5d6a7 0%, #81c784 100%) !important;
        background-color: #a5d6a7 !important;
        color: #14532d !important;
        font-weight: 600 !important;
    }
    
    /* Ensure dropdown is above everything */
    [data-baseweb="popover"],
    [data-baseweb="select"] > div[data-baseweb="popover"] {
        z-index: 99999 !important;
        position: fixed !important;
    }
    
    /* Any remaining dark containers */
    div[class*="dark"], div[class*="black"], 
    section[class*="dark"], section[class*="black"] {
        background-color: #f0fdf4 !important;
        background: #f0fdf4 !important;
        color: #1f2937 !important;
    }
    
    /* Streamlit expander - Interactive - FORCE LIGHT */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%) !important;
        background-color: #f0fdf4 !important;
        color: #1f2937 !important;
        border: 2px solid rgba(134, 239, 172, 0.4) !important;
        border-radius: 12px !important;
        padding: 15px !important;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%) !important;
        background-color: #dcfce7 !important;
        transform: translateX(5px);
        box-shadow: 0 4px 12px rgba(34, 197, 94, 0.2);
    }
    
    .streamlit-expanderContent {
        background: linear-gradient(135deg, #ffffff 0%, #f0fdf4 100%) !important;
        background-color: #ffffff !important;
        color: #1f2937 !important;
        border: 2px solid rgba(134, 239, 172, 0.3) !important;
        border-top: none !important;
        border-radius: 0 0 12px 12px !important;
        padding: 20px !important;
    }
    
    .streamlit-expanderContent * {
        color: #1f2937 !important;
        background: transparent !important;
    }
    
    /* All markdown text - Force visibility */
    .stMarkdown {
        color: #1f2937 !important;
    }
    
    .stMarkdown p, .stMarkdown span, .stMarkdown div, .stMarkdown li {
        color: #1f2937 !important;
        font-size: 1rem;
    }
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
        color: #14532d !important;
        font-weight: 700;
    }
    
    /* Input section headings */
    .stMarkdown h3 {
        color: #14532d !important;
        font-weight: 700;
        margin-top: 20px;
        margin-bottom: 15px;
        font-size: 1.5rem;
    }
    
    /* Ensure all text in info boxes is visible */
    .stSuccess, .stError, .stInfo, .stWarning {
        color: #1f2937 !important;
    }
    
    .stSuccess *, .stError *, .stInfo *, .stWarning * {
        color: #1f2937 !important;
    }
    
    /* Loading Animation */
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    /* CUTE & PROFESSIONAL ANIMATIONS */
    
    /* Cute floating hearts/flowers on success */
    @keyframes floatUp {
        0% {
            transform: translateY(0) rotate(0deg);
            opacity: 1;
        }
        100% {
            transform: translateY(-100px) rotate(360deg);
            opacity: 0;
        }
    }
    
    .cute-float {
        position: fixed;
        pointer-events: none;
        font-size: 2rem;
        z-index: 10000;
        animation: floatUp 2s ease-out forwards;
    }
    
    /* Cute loading spinner */
    @keyframes cuteSpin {
        0% { transform: rotate(0deg) scale(1); }
        50% { transform: rotate(180deg) scale(1.1); }
        100% { transform: rotate(360deg) scale(1); }
    }
    
    .cute-spinner {
        display: inline-block;
        animation: cuteSpin 1.5s ease-in-out infinite;
    }
    
    /* Gentle bounce for cards */
    @keyframes gentleBounce {
        0%, 100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(-5px);
        }
    }
    
    .modern-card, .stat-card, .feature-card {
        animation: gentleBounce 3s ease-in-out infinite;
        animation-delay: calc(var(--card-index, 0) * 0.1s);
    }
    
    /* Cute emoji wiggle */
    @keyframes cuteWiggle {
        0%, 100% { transform: rotate(0deg); }
        25% { transform: rotate(-5deg) scale(1.1); }
        75% { transform: rotate(5deg) scale(1.1); }
    }
    
    .cute-emoji {
        display: inline-block;
        animation: cuteWiggle 2s ease-in-out infinite;
    }
    
    /* Soft glow pulse */
    @keyframes softGlow {
        0%, 100% {
            box-shadow: 0 4px 20px rgba(34, 197, 94, 0.2);
        }
        50% {
            box-shadow: 0 4px 30px rgba(34, 197, 94, 0.4), 0 0 20px rgba(74, 222, 128, 0.3);
        }
    }
    
    .result-card {
        animation: softGlow 3s ease-in-out infinite;
    }
    
    /* Cute button press */
    @keyframes cutePress {
        0% { transform: scale(1); }
        50% { transform: scale(0.95); }
        100% { transform: scale(1); }
    }
    
    /* Sweet entrance animations */
    @keyframes sweetFadeIn {
        from {
            opacity: 0;
            transform: translateY(20px) scale(0.95);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }
    
    /* Cute success celebration */
    @keyframes celebrate {
        0%, 100% { transform: scale(1) rotate(0deg); }
        25% { transform: scale(1.2) rotate(-10deg); }
        50% { transform: scale(1.3) rotate(10deg); }
        75% { transform: scale(1.2) rotate(-5deg); }
    }
    
    .celebrate-emoji {
        animation: celebrate 0.6s ease-in-out;
    }
    
    /* Cute hover lift */
    .modern-card:hover, .stat-card:hover, .feature-card:hover {
        animation: none !important;
        transform: translateY(-10px) scale(1.02) !important;
        box-shadow: 0 15px 40px rgba(34, 197, 94, 0.35) !important;
    }
    
    /* Cute input focus */
    input:focus, select:focus, textarea:focus {
        animation: softGlow 2s ease-in-out infinite;
        transform: scale(1.02);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2rem;
        }
        .hero-subtitle {
            font-size: 1rem;
        }
    }
</style>

<script>
    // Cute Floating Plants Background
    (function() {
        function createFloatingPlants() {
            const plants = ['🌱', '🌿', '🌾', '🌻', '🌷', '🌺', '🌼', '🌸', '🌹', '🌵'];
            const container = document.body;
            
            // Remove existing plant container if any
            const existing = document.querySelector('.plant-bg-container');
            if (existing) existing.remove();
            
            const plantContainer = document.createElement('div');
            plantContainer.className = 'plant-bg-container';
            container.appendChild(plantContainer);
            
            // Create 15-20 floating plants
            for (let i = 0; i < 18; i++) {
                const plant = document.createElement('div');
                plant.className = 'floating-plant-emoji';
                plant.textContent = plants[Math.floor(Math.random() * plants.length)];
                plant.style.left = Math.random() * 100 + '%';
                plant.style.top = Math.random() * 100 + '%';
                plant.style.animationDelay = Math.random() * 20 + 's';
                plant.style.animationDuration = (15 + Math.random() * 10) + 's';
                plantContainer.appendChild(plant);
            }
        }
        
        // Initialize on load
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', createFloatingPlants);
        } else {
            createFloatingPlants();
        }
        
        // Re-run on Streamlit reruns
        setTimeout(createFloatingPlants, 500);
        setInterval(() => {
            const plants = document.querySelectorAll('.floating-plant-emoji');
            plants.forEach(plant => {
                if (Math.random() > 0.7) {
                    plant.style.animation = 'none';
                    setTimeout(() => {
                        plant.style.animation = `floatAround ${15 + Math.random() * 10}s linear infinite`;
                    }, 10);
                }
            });
        }, 5000);
        
        // PREMIUM MOUSE TRACKING & INTERACTIVE ANIMATIONS
        let mouseX = 0, mouseY = 0;
        let cursorTrail = [];
        const maxTrailLength = 8;
        
        // Track mouse movement
        document.addEventListener('mousemove', (e) => {
            mouseX = e.clientX;
            mouseY = e.clientY;
            
            // Create cursor trail effect
            if (Math.random() > 0.7) {
                const trail = document.createElement('div');
                trail.className = 'cursor-trail';
                trail.style.left = mouseX + 'px';
                trail.style.top = mouseY + 'px';
                trail.style.position = 'fixed';
                trail.style.width = '6px';
                trail.style.height = '6px';
                trail.style.borderRadius = '50%';
                trail.style.background = 'radial-gradient(circle, rgba(34, 197, 94, 0.6), rgba(74, 222, 128, 0.3))';
                trail.style.pointerEvents = 'none';
                trail.style.zIndex = '9999';
                trail.style.animation = 'trailFade 0.8s ease-out forwards';
                document.body.appendChild(trail);
                
                setTimeout(() => trail.remove(), 800);
            }
            
            // REMOVED PARALLAX EFFECT - Was causing jittering
            // Parallax disabled for better performance and stability
        });
        
        // Add CSS for cursor trail animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes trailFade {
                0% {
                    opacity: 1;
                    transform: scale(1);
                }
                100% {
                    opacity: 0;
                    transform: scale(0);
                }
            }
            
            /* Smooth transitions - SELECTIVE, NO JITTER */
            .modern-card, .stat-card, .feature-card, .result-card,
            .stButton > button, .stTabs [data-baseweb="tab"] {
                transition: transform 0.2s cubic-bezier(0.25, 0.8, 0.25, 1),
                            box-shadow 0.2s ease,
                            background 0.3s ease,
                            border-color 0.3s ease !important;
            }
            
            /* Prevent layout shifts */
            * {
                will-change: auto !important;
            }
            
            /* Premium hover effects */
            .modern-card:hover, .stat-card:hover, .feature-card:hover {
                transform: translateY(-10px) scale(1.02) !important;
                box-shadow: 0 15px 40px rgba(34, 197, 94, 0.35) !important;
            }
            
            /* Smooth scroll animations */
            @keyframes smoothFadeIn {
                from {
                    opacity: 0;
                    transform: translateY(30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            /* Add smooth fade-in to all sections */
            .main > div {
                animation: smoothFadeIn 0.6s ease-out both;
            }
            
            /* Premium button ripple effect */
            .stButton > button {
                position: relative;
                overflow: hidden;
            }
            
            .stButton > button::after {
                content: '';
                position: absolute;
                top: 50%;
                left: 50%;
                width: 0;
                height: 0;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.5);
                transform: translate(-50%, -50%);
                transition: width 0.6s, height 0.6s;
            }
            
            .stButton > button:active::after {
                width: 300px;
                height: 300px;
            }
        `;
        document.head.appendChild(style);
        
        // Intersection Observer for scroll animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.animation = 'smoothFadeIn 0.6s ease-out both';
                    entry.target.style.opacity = '1';
                }
            });
        }, observerOptions);
        
        // Observe all cards and sections
        setTimeout(() => {
            document.querySelectorAll('.modern-card, .stat-card, .feature-card, .section-header').forEach(el => {
                observer.observe(el);
            });
        }, 1000);
        
        // Add smooth page transitions
        document.body.style.opacity = '0';
        setTimeout(() => {
            document.body.style.transition = 'opacity 0.5s ease-in';
            document.body.style.opacity = '1';
        }, 100);
        
        // FIX DROPDOWN OVERLAPPING - Ensure proper z-index AND VISIBLE SELECTED VALUES
        function fixDropdownZIndex() {
            // Find all selectboxes and their popovers
            const selectboxes = document.querySelectorAll('[data-baseweb="select"]');
            const popovers = document.querySelectorAll('[data-baseweb="popover"]');
            
            selectboxes.forEach((selectbox, index) => {
                selectbox.style.position = 'relative';
                selectbox.style.zIndex = (1000 + index).toString();
                
                // Ensure selected value is visible
                const selectValue = selectbox.querySelector('div[aria-selected="true"], div[aria-selected="false"]');
                if (selectValue) {
                    selectValue.style.color = '#1f2937';
                    selectValue.style.opacity = '1';
                    selectValue.style.visibility = 'visible';
                }
                
                // Find and style all text elements inside the selectbox
                const textElements = selectbox.querySelectorAll('span, div');
                textElements.forEach(el => {
                    if (el.textContent && el.textContent.trim() !== '') {
                        el.style.color = '#1f2937';
                        el.style.opacity = '1';
                        el.style.visibility = 'visible';
                        el.style.display = 'inline-block';
                    }
                });
            });
            
            popovers.forEach((popover, index) => {
                popover.style.zIndex = '99999';
                popover.style.position = 'fixed';
                popover.style.background = 'linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 50%, #c8e6c9 100%)';
                popover.style.border = '2px solid rgba(134, 239, 172, 0.6)';
                popover.style.borderRadius = '12px';
                popover.style.boxShadow = '0 8px 25px rgba(34, 197, 94, 0.4)';
                popover.style.maxHeight = '300px';
                popover.style.overflowY = 'auto';
                
                // Style dropdown options
                const options = popover.querySelectorAll('[role="option"], li, div[role="option"]');
                options.forEach(option => {
                    option.style.padding = '12px 16px';
                    option.style.borderRadius = '8px';
                    option.style.margin = '2px 8px';
                    option.style.transition = 'all 0.2s ease';
                    option.style.cursor = 'pointer';
                    option.style.color = '#1f2937';
                    option.style.background = 'transparent';
                    
                    option.addEventListener('mouseenter', function() {
                        this.style.background = 'rgba(200, 230, 201, 0.8)';
                        this.style.transform = 'translateX(5px)';
                    });
                    
                    option.addEventListener('mouseleave', function() {
                        this.style.background = 'transparent';
                        this.style.transform = 'translateX(0)';
                    });
                });
            });
        }
        
        // Function to get selected value from Streamlit widget state
        function getStreamlitWidgetValue(widgetId) {
            try {
                // Try to access Streamlit's widget state
                if (window.parent && window.parent.streamlit && window.parent.streamlit.widgetState) {
                    const state = window.parent.streamlit.widgetState;
                    if (state[widgetId]) {
                        return state[widgetId].value;
                    }
                }
                // Try alternative method
                if (window.streamlit && window.streamlit.widgetState) {
                    const state = window.streamlit.widgetState;
                    if (state[widgetId]) {
                        return state[widgetId].value;
                    }
                }
            } catch (e) {
                console.log('Could not access Streamlit state:', e);
            }
            return null;
        }
        
        // Function to get selected option text from dropdown list
        function getSelectedOptionText(selectbox) {
            // Method 1: Check the popover for selected option
            const popover = document.querySelector('[data-baseweb="popover"]');
            if (popover) {
                const selectedOption = popover.querySelector('[aria-selected="true"], [role="option"][aria-selected="true"], li[aria-selected="true"]');
                if (selectedOption) {
                    const optionText = selectedOption.textContent?.trim();
                    if (optionText && optionText !== '') {
                        return optionText;
                    }
                }
            }
            
            // Method 2: Check all option elements in the selectbox
            const allOptions = selectbox.querySelectorAll('[role="option"], li[role="option"], div[role="option"]');
            for (let option of allOptions) {
                if (option.getAttribute('aria-selected') === 'true' || 
                    option.classList.contains('selected') ||
                    option.getAttribute('data-selected') === 'true') {
                    const optionText = option.textContent?.trim();
                    if (optionText && optionText !== '') {
                        return optionText;
                    }
                }
            }
            
            // Method 3: Try to find the selectbox's associated select element
            const stSelectbox = selectbox.closest('.stSelectbox');
            if (stSelectbox) {
                // Look for hidden input or data attribute
                const hiddenInput = stSelectbox.querySelector('input[type="hidden"]');
                if (hiddenInput && hiddenInput.value) {
                    // Try to find the option with this value
                    const optionWithValue = Array.from(allOptions).find(opt => {
                        return opt.getAttribute('data-value') === hiddenInput.value ||
                               opt.textContent?.trim() === hiddenInput.value;
                    });
                    if (optionWithValue) {
                        return optionWithValue.textContent?.trim();
                    }
                    return hiddenInput.value;
                }
            }
            
            return null;
        }
        
        // Function to ensure selected values are always visible - AGGRESSIVE FIX
        function ensureSelectboxValuesVisible() {
            // Find ALL selectboxes
            const selectboxes = document.querySelectorAll('[data-baseweb="select"], .stSelectbox [data-baseweb="select"]');
            
            selectboxes.forEach(selectbox => {
                // First, try to get the selected option text directly from the dropdown
                let selectedValue = getSelectedOptionText(selectbox);
                // If we didn't get it from the dropdown, try other methods
                if (!selectedValue) {
                    // Try to get the widget key/ID from the selectbox
                    const widgetKey = selectbox.closest('.stSelectbox')?.getAttribute('data-widget-key') || 
                                     selectbox.getAttribute('data-widget-key') ||
                                     selectbox.closest('[data-widget-key]')?.getAttribute('data-widget-key');
                    
                    // Try to get value from Streamlit state
                    if (widgetKey) {
                        selectedValue = getStreamlitWidgetValue(widgetKey);
                    }
                    
                    // Also try to find the value in the DOM - check for hidden inputs
                    const valueInput = selectbox.querySelector('input[type="hidden"], input[value], input[name*="selectbox"]');
                    if (valueInput && valueInput.value) {
                        selectedValue = valueInput.value;
                    }
                    
                    // Last resort: check if there's any visible text that's not an arrow
                    const allText = selectbox.textContent || '';
                    const textParts = allText.split(/[▼▲]/).filter(t => t.trim());
                    if (textParts.length > 0 && !selectedValue) {
                        const candidate = textParts[0].trim();
                        if (candidate && candidate.length > 0) {
                            selectedValue = candidate;
                        }
                    }
                }
                // Force ALL elements inside to be visible
                const allElements = selectbox.querySelectorAll('*');
                allElements.forEach(el => {
                    const text = el.textContent?.trim() || '';
                    // Skip arrow icons, but show everything else
                    if (text && text !== '▼' && text !== '▲' && text !== '') {
                        el.style.setProperty('color', '#1f2937', 'important');
                        el.style.setProperty('opacity', '1', 'important');
                        el.style.setProperty('visibility', 'visible', 'important');
                        el.style.setProperty('display', el.tagName === 'SPAN' ? 'inline' : (el.tagName === 'DIV' ? 'flex' : 'block'), 'important');
                    }
                });
                
                // Find the value display area - try multiple selectors
                const valueSelectors = [
                    'div > div',
                    'div[role="combobox"]',
                    'div[data-baseweb="select"] > div',
                    'div > div > div',
                    'div > div > div > div',
                    'div[aria-expanded]',
                    'div[aria-haspopup]'
                ];
                
                valueSelectors.forEach(selector => {
                    const containers = selectbox.querySelectorAll(selector);
                    containers.forEach(container => {
                        container.style.setProperty('color', '#1f2937', 'important');
                        container.style.setProperty('opacity', '1', 'important');
                        container.style.setProperty('visibility', 'visible', 'important');
                        
                        // Force all children to be visible
                        const children = container.querySelectorAll('*');
                        children.forEach(child => {
                            const childText = child.textContent?.trim() || '';
                            if (childText && childText !== '▼' && childText !== '▲') {
                                child.style.setProperty('color', '#1f2937', 'important');
                                child.style.setProperty('opacity', '1', 'important');
                                child.style.setProperty('visibility', 'visible', 'important');
                            }
                        });
                    });
                });
                
                // Handle text nodes directly
                const walker = document.createTreeWalker(
                    selectbox,
                    NodeFilter.SHOW_TEXT,
                    {
                        acceptNode: function(node) {
                            const text = node.textContent?.trim() || '';
                            if (text && text !== '▼' && text !== '▲' && text.length > 0) {
                                return NodeFilter.FILTER_ACCEPT;
                            }
                            return NodeFilter.FILTER_REJECT;
                        }
                    },
                    false
                );
                
                let textNode;
                while (textNode = walker.nextNode()) {
                    const parent = textNode.parentElement;
                    if (parent) {
                        parent.style.setProperty('color', '#1f2937', 'important');
                        parent.style.setProperty('opacity', '1', 'important');
                        parent.style.setProperty('visibility', 'visible', 'important');
                        
                        // If it's a bare text node, wrap it
                        if (textNode.parentNode === selectbox || textNode.parentNode.nodeName === 'DIV') {
                            const span = document.createElement('span');
                            span.textContent = textNode.textContent;
                            span.style.setProperty('color', '#1f2937', 'important');
                            span.style.setProperty('opacity', '1', 'important');
                            span.style.setProperty('visibility', 'visible', 'important');
                            textNode.parentNode.replaceChild(span, textNode);
                        }
                    }
                }
                
                // Find the main display container - try multiple selectors
                let basewebValue = selectbox.querySelector('[data-baseweb="select"] > div > div');
                if (!basewebValue) {
                    // Try alternative selectors
                    basewebValue = selectbox.querySelector('div > div');
                    if (!basewebValue) {
                        basewebValue = selectbox.querySelector('div[role="combobox"]');
                    }
                }
                
                if (basewebValue) {
                    basewebValue.style.setProperty('color', '#1f2937', 'important');
                    basewebValue.style.setProperty('opacity', '1', 'important');
                    basewebValue.style.setProperty('visibility', 'visible', 'important');
                    
                    // Get computed style to check if it's actually visible
                    const computed = window.getComputedStyle(basewebValue);
                    if (computed.color === 'rgb(0, 0, 0)' || computed.opacity === '0' || computed.visibility === 'hidden') {
                        basewebValue.style.setProperty('color', '#1f2937', 'important');
                        basewebValue.style.setProperty('opacity', '1', 'important');
                        basewebValue.style.setProperty('visibility', 'visible', 'important');
                    }
                    
                    // Get current displayed text (excluding arrow)
                    let currentText = basewebValue.textContent?.trim() || '';
                    // Remove arrow characters
                    currentText = currentText.replace(/[▼▲]/g, '').trim();
                    const isEmpty = !currentText || currentText === '';
                    
                    // Always update if we have a selectedValue and it's different or empty
                    if (selectedValue && (isEmpty || currentText !== selectedValue)) {
                        // Find and preserve the arrow icon
                        const arrow = basewebValue.querySelector('svg, [aria-label*="arrow"], [aria-label*="chevron"], path[d*="M"]');
                        let arrowHTML = '';
                        if (arrow) {
                            arrowHTML = arrow.outerHTML;
                        }
                        
                        // Clear and rebuild
                        basewebValue.innerHTML = '';
                        
                        // Add the selected value text FIRST
                        const valueSpan = document.createElement('span');
                        valueSpan.textContent = selectedValue;
                        valueSpan.style.cssText = 'color: #1f2937 !important; opacity: 1 !important; visibility: visible !important; display: inline-block !important; font-size: 1rem !important; font-weight: 500 !important; margin-right: 8px !important; line-height: 1.5 !important; white-space: nowrap !important;';
                        basewebValue.appendChild(valueSpan);
                        
                        // Then add arrow if it exists
                        if (arrowHTML) {
                            basewebValue.insertAdjacentHTML('beforeend', arrowHTML);
                        }
                    } else if (!selectedValue && isEmpty) {
                        // Even if no selectedValue found, try to find it from the selectbox structure
                        const selectElement = selectbox.querySelector('select');
                        if (selectElement && selectElement.selectedIndex >= 0) {
                            const selectedOption = selectElement.options[selectElement.selectedIndex];
                            if (selectedOption && selectedOption.text) {
                                const valueSpan = document.createElement('span');
                                valueSpan.textContent = selectedOption.text;
                                valueSpan.style.cssText = 'color: #1f2937 !important; opacity: 1 !important; visibility: visible !important; display: inline-block !important; font-size: 1rem !important; font-weight: 500 !important; margin-right: 8px !important;';
                                basewebValue.insertBefore(valueSpan, basewebValue.firstChild);
                            }
                        }
                    } else if (selectedValue && currentText !== selectedValue) {
                        // Value exists but doesn't match - update it
                        const arrow = basewebValue.querySelector('svg, [aria-label*="arrow"], [aria-label*="chevron"]');
                        const arrowHTML = arrow ? arrow.outerHTML : '';
                        basewebValue.innerHTML = '';
                        const valueSpan = document.createElement('span');
                        valueSpan.textContent = selectedValue;
                        valueSpan.style.cssText = 'color: #1f2937 !important; opacity: 1 !important; visibility: visible !important; display: inline-block !important; font-size: 1rem !important; font-weight: 500 !important; margin-right: 8px !important;';
                        basewebValue.appendChild(valueSpan);
                        if (arrowHTML) {
                            basewebValue.insertAdjacentHTML('beforeend', arrowHTML);
                        }
                    }
                }
                
                // Also try to find and update the main display container
                const displayContainers = [
                    selectbox.querySelector('div > div'),
                    selectbox.querySelector('div[role="combobox"]'),
                    selectbox.querySelector('div[role="combobox"] > div'),
                    selectbox.closest('.stSelectbox')?.querySelector('div > div > div')
                ].filter(Boolean);
                
                displayContainers.forEach(container => {
                    if (selectedValue && (!container.textContent || container.textContent.trim() === '' || container.textContent.trim() === '▼')) {
                        // Check if there's an arrow/svg to preserve
                        const arrow = container.querySelector('svg, [aria-label*="arrow"], [aria-label*="chevron"]');
                        const existingText = container.textContent?.trim();
                        
                        if (!existingText || existingText === '▼' || existingText === '▲') {
                            // Clear and add value
                            container.innerHTML = '';
                            if (arrow) {
                                container.appendChild(arrow);
                            }
                            
                            const valueSpan = document.createElement('span');
                            valueSpan.textContent = selectedValue;
                            valueSpan.style.cssText = 'color: #1f2937 !important; opacity: 1 !important; visibility: visible !important; display: inline-block !important; font-size: 1rem !important; font-weight: 500 !important; margin-right: 8px !important;';
                            container.insertBefore(valueSpan, arrow || null);
                        }
                    }
                    
                    // Force visibility
                    container.style.setProperty('color', '#1f2937', 'important');
                    container.style.setProperty('opacity', '1', 'important');
                    container.style.setProperty('visibility', 'visible', 'important');
                });
            });
        }
        
        // Run on load and periodically
        fixDropdownZIndex();
        ensureSelectboxValuesVisible();
        setTimeout(() => {
            fixDropdownZIndex();
            ensureSelectboxValuesVisible();
        }, 500);
        setTimeout(() => {
            fixDropdownZIndex();
            ensureSelectboxValuesVisible();
        }, 1000);
        
        // Also run after any DOM changes - VERY frequently to catch all updates
        setInterval(() => {
            ensureSelectboxValuesVisible();
        }, 100);
        
        // Also run when Streamlit components are ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                setTimeout(ensureSelectboxValuesVisible, 100);
                setTimeout(ensureSelectboxValuesVisible, 500);
                setTimeout(ensureSelectboxValuesVisible, 1000);
            });
        } else {
            setTimeout(ensureSelectboxValuesVisible, 100);
            setTimeout(ensureSelectboxValuesVisible, 500);
            setTimeout(ensureSelectboxValuesVisible, 1000);
        }
        
        // Run on focus events (when user interacts with selectbox)
        document.addEventListener('focus', (e) => {
            if (e.target.closest('[data-baseweb="select"]') || e.target.closest('.stSelectbox')) {
                setTimeout(ensureSelectboxValuesVisible, 50);
            }
        }, true);
        
        // Run on blur events (after selection)
        document.addEventListener('blur', (e) => {
            if (e.target.closest('[data-baseweb="select"]') || e.target.closest('.stSelectbox')) {
                setTimeout(ensureSelectboxValuesVisible, 100);
            }
        }, true);
        
        // Run immediately when page becomes visible
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden) {
                ensureSelectboxValuesVisible();
            }
        });
        
        // Run on every Streamlit rerun (when components update)
        const originalRerun = window.parent.postMessage;
        if (window.parent && window.parent.postMessage) {
            const checkRerun = setInterval(() => {
                ensureSelectboxValuesVisible();
            }, 300);
        }
        
        // Watch for new dropdowns being created and value changes
        const observer = new MutationObserver((mutations) => {
            let shouldFix = false;
            mutations.forEach((mutation) => {
                if (mutation.addedNodes.length > 0) {
                    mutation.addedNodes.forEach((node) => {
                        if (node.nodeType === 1) {
                            if (node.hasAttribute && (
                                node.hasAttribute('data-baseweb') ||
                                node.querySelector && node.querySelector('[data-baseweb="popover"]') ||
                                node.querySelector && node.querySelector('[data-baseweb="select"]')
                            )) {
                                shouldFix = true;
                            }
                        }
                    });
                }
                // Also watch for attribute changes (like when selection changes)
                if (mutation.type === 'attributes' && (
                    mutation.attributeName === 'aria-selected' ||
                    mutation.attributeName === 'value'
                )) {
                    shouldFix = true;
                }
            });
            if (shouldFix) {
                setTimeout(() => {
                    fixDropdownZIndex();
                    ensureSelectboxValuesVisible();
                }, 100);
            }
        });
        
        observer.observe(document.body, {
            childList: true,
            subtree: true,
            attributes: true,
            attributeFilter: ['aria-selected', 'value', 'data-baseweb', 'aria-expanded', 'aria-haspopup']
        });
        
        // Additional observer specifically for selectbox value changes
        const valueObserver = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'childList' || mutation.type === 'characterData') {
                    const target = mutation.target;
                    if (target.closest && target.closest('[data-baseweb="select"]')) {
                        setTimeout(ensureSelectboxValuesVisible, 10);
                    }
                }
            });
        });
        
        // Observe text content changes in selectboxes
        setTimeout(() => {
            document.querySelectorAll('[data-baseweb="select"]').forEach(selectbox => {
                valueObserver.observe(selectbox, {
                    childList: true,
                    subtree: true,
                    characterData: true
                });
            });
        }, 500);
        
        // Also fix on click events (when dropdowns open)
        document.addEventListener('click', function(e) {
            setTimeout(() => {
                fixDropdownZIndex();
                ensureSelectboxValuesVisible();
            }, 50);
        }, true);
        
        // Fix on change events (when selections are made)
        document.addEventListener('change', function(e) {
            const selectbox = e.target.closest('[data-baseweb="select"]') || e.target.closest('.stSelectbox');
            if (selectbox) {
                // Immediately get the selected option text
                setTimeout(() => {
                    const selectedText = getSelectedOptionText(selectbox);
                    if (selectedText) {
                        const displayEl = selectbox.querySelector('[data-baseweb="select"] > div > div') ||
                                        selectbox.querySelector('div > div') ||
                                        selectbox.querySelector('div[role="combobox"]');
                        if (displayEl) {
                            const arrow = displayEl.querySelector('svg');
                            const arrowHTML = arrow ? arrow.outerHTML : '';
                            displayEl.innerHTML = '';
                            const valueSpan = document.createElement('span');
                            valueSpan.textContent = selectedText;
                            valueSpan.style.cssText = 'color: #1f2937 !important; opacity: 1 !important; visibility: visible !important; display: inline-block !important; font-size: 1rem !important; font-weight: 500 !important; margin-right: 8px !important;';
                            displayEl.appendChild(valueSpan);
                            if (arrowHTML) {
                                displayEl.insertAdjacentHTML('beforeend', arrowHTML);
                            }
                        }
                    }
                    ensureSelectboxValuesVisible();
                }, 50);
            }
        }, true);
        
        // Also listen for click events on dropdown options
        document.addEventListener('click', function(e) {
            const option = e.target.closest('[role="option"], li[role="option"], div[role="option"]');
            if (option) {
                // User clicked an option, update display after a short delay
                setTimeout(() => {
                    const selectbox = option.closest('[data-baseweb="select"]') || 
                                    document.querySelector('[data-baseweb="select"]');
                    if (selectbox) {
                        const selectedText = option.textContent?.trim();
                        if (selectedText) {
                            const displayEl = selectbox.querySelector('[data-baseweb="select"] > div > div') ||
                                            selectbox.querySelector('div > div');
                            if (displayEl) {
                                const arrow = displayEl.querySelector('svg');
                                const arrowHTML = arrow ? arrow.outerHTML : '';
                                displayEl.innerHTML = '';
                                const valueSpan = document.createElement('span');
                                valueSpan.textContent = selectedText;
                                valueSpan.style.cssText = 'color: #1f2937 !important; opacity: 1 !important; visibility: visible !important; display: inline-block !important; font-size: 1rem !important; font-weight: 500 !important; margin-right: 8px !important;';
                                displayEl.appendChild(valueSpan);
                                if (arrowHTML) {
                                    displayEl.insertAdjacentHTML('beforeend', arrowHTML);
                                }
                            }
                        }
                        ensureSelectboxValuesVisible();
                    }
                }, 100);
            }
        }, true);
        
        // Also listen for Streamlit's custom events
        window.addEventListener('message', (event) => {
            if (event.data && (event.data.type === 'streamlit:rerun' || event.data.type === 'streamlit:render')) {
                setTimeout(ensureSelectboxValuesVisible, 100);
                setTimeout(ensureSelectboxValuesVisible, 300);
                setTimeout(ensureSelectboxValuesVisible, 600);
            }
        });
        
        // Listen for iframe messages (Streamlit communication)
        if (window.parent !== window) {
            window.parent.addEventListener('message', (event) => {
                if (event.data && (event.data.type === 'streamlit:rerun' || event.data.type === 'streamlit:render')) {
                    setTimeout(ensureSelectboxValuesVisible, 100);
                    setTimeout(ensureSelectboxValuesVisible, 300);
                }
            });
        }
        
        // Hook into Streamlit's rerun if possible
        if (window.streamlit && window.streamlit.setComponentValue) {
            const originalSetComponentValue = window.streamlit.setComponentValue;
            window.streamlit.setComponentValue = function(...args) {
                const result = originalSetComponentValue.apply(this, args);
                setTimeout(ensureSelectboxValuesVisible, 50);
                return result;
            };
        }
        
        // Watch for attribute changes on selectboxes (when value changes)
        const selectObserver = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'attributes' || mutation.type === 'childList') {
                    const target = mutation.target;
                    if (target.closest && (target.closest('[data-baseweb="select"]') || target.closest('.stSelectbox'))) {
                        setTimeout(ensureSelectboxValuesVisible, 50);
                    }
                }
            });
        });
        
        // Observe all selectboxes
        setTimeout(() => {
            document.querySelectorAll('[data-baseweb="select"], .stSelectbox').forEach(selectbox => {
                selectObserver.observe(selectbox, {
                    attributes: true,
                    childList: true,
                    subtree: true,
                    attributeFilter: ['aria-selected', 'value', 'data-baseweb', 'aria-expanded']
                });
            });
        }, 1000);
        
        // REMOVED AGGRESSIVE TEXT HOVER - Using CSS-only for better performance
        // No JavaScript hover effects to prevent jittering
        }, 5000);
    })();
    
    // Enhanced animations for Streamlit
    (function() {
        // Button press feedback
        function setupButtonAnimations() {
            document.querySelectorAll('.stButton > button').forEach(button => {
                button.addEventListener('click', function() {
                    this.style.transform = 'scale(0.97)';
                    setTimeout(() => {
                        this.style.transform = '';
                        this.style.transition = 'transform 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55)';
                        setTimeout(() => {
                            this.style.transition = '';
                        }, 300);
                    }, 150);
                });
            });
        }
        
        // Chart entrance animations
        function setupChartAnimations() {
            const chartObserver = new IntersectionObserver(function(entries) {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.style.opacity = '0';
                        entry.target.style.transform = 'scale(0.85)';
                        entry.target.style.transition = 'opacity 0.5s ease-out, transform 0.5s ease-out';
                        setTimeout(() => {
                            entry.target.style.opacity = '1';
                            entry.target.style.transform = 'scale(1)';
                        }, 50);
                        chartObserver.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.1 });
            
            setTimeout(() => {
                document.querySelectorAll('.js-plotly-plot, [class*="plotly"]').forEach(chart => {
                    chartObserver.observe(chart);
                });
            }, 1000);
        }
        
        // Tab switching animation
        function setupTabAnimations() {
            const tabPanels = document.querySelectorAll('[data-baseweb="tab-panel"]');
            if (tabPanels.length > 0) {
                tabPanels.forEach(panel => {
                    const observer = new MutationObserver(function(mutations) {
                        mutations.forEach(mutation => {
                            if (mutation.type === 'attributes' && mutation.attributeName === 'aria-hidden') {
                                const target = mutation.target;
                                if (target.getAttribute('aria-hidden') === 'false') {
                                    target.style.opacity = '0';
                                    target.style.transform = 'translateX(10px)';
                                    target.style.transition = 'opacity 0.4s ease-out, transform 0.4s ease-out';
                                    setTimeout(() => {
                                        target.style.opacity = '1';
                                        target.style.transform = 'translateX(0)';
                                    }, 10);
                                }
                            }
                        });
                    });
                    observer.observe(panel, { attributes: true, attributeFilter: ['aria-hidden'] });
                });
            }
        }
        
        // Initialize on load
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', function() {
                setupButtonAnimations();
                setupChartAnimations();
                setupTabAnimations();
            });
        } else {
            setupButtonAnimations();
            setupChartAnimations();
            setupTabAnimations();
        }
        
        // Re-run on Streamlit reruns
        if (window.parent !== window) {
            setTimeout(() => {
                setupButtonAnimations();
                setupChartAnimations();
                setupTabAnimations();
            }, 500);
        }
    })();
    
    // Additional Interactive Features
    (function() {
        // 1. Real-time Input Value Animations
        function setupInputAnimations() {
            const inputs = document.querySelectorAll('.stNumberInput input, .stTextInput input, .stSelectbox select');
            inputs.forEach(input => {
                input.addEventListener('input', function() {
                    this.style.transform = 'scale(1.05)';
                    this.style.boxShadow = '0 0 0 4px rgba(34, 197, 94, 0.3)';
                    setTimeout(() => {
                        this.style.transform = 'scale(1)';
                        this.style.boxShadow = '';
                    }, 200);
                });
                
                input.addEventListener('focus', function() {
                    const parent = this.closest('.stNumberInput, .stTextInput, .stSelectbox');
                    if (parent) {
                        parent.style.transform = 'translateY(-3px)';
                        parent.style.transition = 'transform 0.3s ease';
                    }
                });
                
                input.addEventListener('blur', function() {
                    const parent = this.closest('.stNumberInput, .stTextInput, .stSelectbox');
                    if (parent) {
                        parent.style.transform = 'translateY(0)';
                    }
                });
            });
        }
        
        // 2. Interactive Card Hover Effects
        function setupCardInteractions() {
            const cards = document.querySelectorAll('.modern-card, .stat-card, .feature-card, .crop-info-panel');
            cards.forEach(card => {
                card.addEventListener('mouseenter', function() {
                    this.style.transform = 'translateY(-8px) scale(1.02)';
                    this.style.transition = 'all 0.3s ease';
                });
                
                card.addEventListener('mouseleave', function() {
                    this.style.transform = 'translateY(0) scale(1)';
                });
                
                // Click ripple effect
                card.addEventListener('click', function(e) {
                    const ripple = document.createElement('span');
                    const rect = this.getBoundingClientRect();
                    const size = Math.max(rect.width, rect.height);
                    const x = e.clientX - rect.left - size / 2;
                    const y = e.clientY - rect.top - size / 2;
                    
                    ripple.style.width = ripple.style.height = size + 'px';
                    ripple.style.left = x + 'px';
                    ripple.style.top = y + 'px';
                    ripple.style.position = 'absolute';
                    ripple.style.borderRadius = '50%';
                    ripple.style.background = 'rgba(34, 197, 94, 0.3)';
                    ripple.style.transform = 'scale(0)';
                    ripple.style.animation = 'ripple 0.6s ease-out';
                    ripple.style.pointerEvents = 'none';
                    
                    this.style.position = 'relative';
                    this.style.overflow = 'hidden';
                    this.appendChild(ripple);
                    
                    setTimeout(() => ripple.remove(), 600);
                });
            });
        }
        
        // 3. Smooth Scroll to Sections
        function setupSmoothScroll() {
            document.querySelectorAll('a[href^="#"], .section-header').forEach(anchor => {
                anchor.addEventListener('click', function(e) {
                    e.preventDefault();
                    const target = document.querySelector(this.getAttribute('href') || '#' + this.id);
                    if (target) {
                        target.scrollIntoView({
                            behavior: 'smooth',
                            block: 'start'
                        });
                    }
                });
            });
        }
        
        // 4. Progress Indicator for Form Completion
        function setupProgressIndicator() {
            const inputs = document.querySelectorAll('.stNumberInput input');
            if (inputs.length > 0) {
                const progressBar = document.createElement('div');
                progressBar.id = 'form-progress';
                progressBar.style.cssText = `
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 0%;
                    height: 4px;
                    background: linear-gradient(90deg, #4ade80, #22c55e);
                    z-index: 9999;
                    transition: width 0.3s ease;
                    box-shadow: 0 2px 8px rgba(34, 197, 94, 0.4);
                `;
                document.body.appendChild(progressBar);
                
                function updateProgress() {
                    let filled = 0;
                    inputs.forEach(input => {
                        if (input.value && input.value !== '0' && input.value !== '') {
                            filled++;
                        }
                    });
                    const progress = (filled / inputs.length) * 100;
                    progressBar.style.width = progress + '%';
                }
                
                inputs.forEach(input => {
                    input.addEventListener('input', updateProgress);
                    input.addEventListener('change', updateProgress);
                });
                updateProgress();
            }
        }
        
        // 5. Interactive Tooltips
        function setupInteractiveTooltips() {
            const tooltipTriggers = document.querySelectorAll('[data-tooltip], .stTooltip');
            tooltipTriggers.forEach(trigger => {
                trigger.addEventListener('mouseenter', function(e) {
                    const tooltip = document.createElement('div');
                    tooltip.className = 'custom-tooltip';
                    tooltip.textContent = this.getAttribute('data-tooltip') || 'Hover for info';
                    tooltip.style.cssText = `
                        position: absolute;
                        background: linear-gradient(135deg, #14532d, #22c55e);
                        color: white;
                        padding: 8px 12px;
                        border-radius: 8px;
                        font-size: 0.9rem;
                        pointer-events: none;
                        z-index: 10000;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
                        white-space: nowrap;
                    `;
                    document.body.appendChild(tooltip);
                    
                    const rect = this.getBoundingClientRect();
                    tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
                    tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + 'px';
                    
                    this._tooltip = tooltip;
                });
                
                trigger.addEventListener('mouseleave', function() {
                    if (this._tooltip) {
                        this._tooltip.remove();
                        this._tooltip = null;
                    }
                });
            });
        }
        
        // 6. Value Change Animations
        function setupValueAnimations() {
            const observer = new MutationObserver(function(mutations) {
                mutations.forEach(mutation => {
                    if (mutation.type === 'childList') {
                        mutation.addedNodes.forEach(node => {
                            if (node.nodeType === 1 && node.classList) {
                                // Animate metric values
                                if (node.querySelector && node.querySelector('[data-testid="stMetricValue"]')) {
                                    const metric = node.querySelector('[data-testid="stMetricValue"]');
                                    metric.style.animation = 'valuePop 0.5s ease-out';
                                }
                            }
                        });
                    }
                });
            });
            
            observer.observe(document.body, {
                childList: true,
                subtree: true
            });
        }
        
        // 7. Parallax Effect on Scroll
        function setupParallax() {
            let ticking = false;
            window.addEventListener('scroll', function() {
                if (!ticking) {
                    window.requestAnimationFrame(function() {
                        const scrolled = window.pageYOffset;
                        const parallaxElements = document.querySelectorAll('.hero-section, .stat-card');
                        parallaxElements.forEach((el, index) => {
                            const speed = 0.5 + (index * 0.1);
                            el.style.transform = `translateY(${scrolled * speed}px)`;
                        });
                        ticking = false;
                    });
                    ticking = true;
                }
            });
        }
        
        // Add CSS animations
        const style = document.createElement('style');
        style.textContent = `
            @keyframes ripple {
                to {
                    transform: scale(4);
                    opacity: 0;
                }
            }
            @keyframes valuePop {
                0% { transform: scale(0.8); opacity: 0; }
                50% { transform: scale(1.1); }
                100% { transform: scale(1); opacity: 1; }
            }
        `;
        document.head.appendChild(style);
        
        // Initialize all features
        function initAll() {
            setupInputAnimations();
            setupCardInteractions();
            setupSmoothScroll();
            setupProgressIndicator();
            setupInteractiveTooltips();
            setupValueAnimations();
            setupParallax();
        }
        
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initAll);
        } else {
            initAll();
        }
        
        // Re-run on Streamlit reruns
        setTimeout(initAll, 1000);
        setInterval(() => {
            setupInputAnimations();
            setupCardInteractions();
        }, 2000);
    })();
</script>
""", unsafe_allow_html=True)

# ===========================================
# COMPREHENSIVE CROP INFORMATION DATABASE
# ===========================================
CROP_INFO = {
    "rice": {
        "emoji": "🌾",
        "displayName": "Rice",
        "description": "Rice is a water-loving cereal crop suited to warm, humid climates with plenty of rainfall or irrigation. It's a staple food for over half the world's population.",
        "idealConditions": {
            "temperature": {"min": 20, "max": 35},
            "rainfall": {"min": 150, "max": 300},
            "ph": {"min": 5.5, "max": 7.0},
            "humidity": {"min": 70, "max": 100},
            "N": {"min": 80, "max": 120},
            "P": {"min": 30, "max": 60},
            "K": {"min": 30, "max": 50}
        },
        "tips": [
            "Ensure fields can retain water or are well irrigated.",
            "Slightly acidic to neutral soils are preferred.",
            "Requires high humidity and consistent water supply."
        ],
        "color": "#22c55e"
    },
    "maize": {
        "emoji": "🌽",
        "displayName": "Maize",
        "description": "Maize (corn) is a versatile cereal crop that grows well in moderate climates. It's one of the most widely grown crops globally.",
        "idealConditions": {
            "temperature": {"min": 18, "max": 32},
            "rainfall": {"min": 50, "max": 150},
            "ph": {"min": 5.8, "max": 7.0},
            "humidity": {"min": 50, "max": 80},
            "N": {"min": 80, "max": 120},
            "P": {"min": 40, "max": 70},
            "K": {"min": 40, "max": 60}
        },
        "tips": [
            "Well-drained soils are essential.",
            "Moderate rainfall or irrigation needed.",
            "Prefers warm temperatures during growing season."
        ],
        "color": "#a3e635"
    },
    "chickpea": {
        "emoji": "🫘",
        "displayName": "Chickpea",
        "description": "Chickpea is a protein-rich legume that's drought-tolerant and suitable for semi-arid regions. It's an important source of plant protein.",
        "idealConditions": {
            "temperature": {"min": 15, "max": 30},
            "rainfall": {"min": 30, "max": 100},
            "ph": {"min": 6.0, "max": 8.0},
            "humidity": {"min": 30, "max": 60},
            "N": {"min": 20, "max": 50},
            "P": {"min": 20, "max": 50},
            "K": {"min": 20, "max": 50}
        },
        "tips": [
            "Drought-resistant, suitable for dry regions.",
            "Well-drained soils preferred.",
            "Cool season crop in warm climates."
        ],
        "color": "#854d0e"
    },
    "kidneybeans": {
        "emoji": "🫘",
        "displayName": "Kidney Beans",
        "description": "Kidney beans are high-protein legumes that need moderate rainfall. They're a staple in many cuisines worldwide.",
        "idealConditions": {
            "temperature": {"min": 18, "max": 28},
            "rainfall": {"min": 50, "max": 120},
            "ph": {"min": 6.0, "max": 7.5},
            "humidity": {"min": 40, "max": 70},
            "N": {"min": 30, "max": 60},
            "P": {"min": 30, "max": 60},
            "K": {"min": 30, "max": 60}
        },
        "tips": [
            "Moderate rainfall or irrigation required.",
            "Neutral to slightly acidic soils work best.",
            "Warm season crop."
        ],
        "color": "#dc2626"
    },
    "pigeonpeas": {
        "emoji": "🫘",
        "displayName": "Pigeon Peas",
        "description": "Pigeon peas are drought-resistant pulse crops that thrive in warm climates. They're highly nutritious and fix nitrogen in soil.",
        "idealConditions": {
            "temperature": {"min": 20, "max": 35},
            "rainfall": {"min": 40, "max": 100},
            "ph": {"min": 5.5, "max": 7.5},
            "humidity": {"min": 40, "max": 70},
            "N": {"min": 20, "max": 50},
            "P": {"min": 20, "max": 50},
            "K": {"min": 20, "max": 50}
        },
        "tips": [
            "Excellent drought tolerance.",
            "Can grow in poor soils.",
            "Warm climate crop."
        ],
        "color": "#ca8a04"
    },
    "mothbeans": {
        "emoji": "🫘",
        "displayName": "Moth Beans",
        "description": "Moth beans are hardy legumes suitable for arid regions. They're drought-tolerant and can grow in poor soil conditions.",
        "idealConditions": {
            "temperature": {"min": 20, "max": 35},
            "rainfall": {"min": 25, "max": 80},
            "ph": {"min": 6.0, "max": 8.0},
            "humidity": {"min": 30, "max": 60},
            "N": {"min": 15, "max": 40},
            "P": {"min": 15, "max": 40},
            "K": {"min": 15, "max": 40}
        },
        "tips": [
            "Highly drought-resistant.",
            "Suitable for arid and semi-arid regions.",
            "Can tolerate poor soil conditions."
        ],
        "color": "#92400e"
    },
    "mungbean": {
        "emoji": "🫘",
        "displayName": "Mung Bean",
        "description": "Mung beans are fast-growing legumes good for short seasons. They're quick to mature and highly nutritious.",
        "idealConditions": {
            "temperature": {"min": 20, "max": 35},
            "rainfall": {"min": 50, "max": 120},
            "ph": {"min": 6.0, "max": 7.5},
            "humidity": {"min": 50, "max": 80},
            "N": {"min": 30, "max": 60},
            "P": {"min": 30, "max": 60},
            "K": {"min": 30, "max": 60}
        },
        "tips": [
            "Fast-growing, short season crop.",
            "Moderate water requirements.",
            "Warm season crop."
        ],
        "color": "#65a30d"
    },
    "blackgram": {
        "emoji": "🫘",
        "displayName": "Black Gram",
        "description": "Black gram is a nutritious pulse that grows well in warm climates. It's rich in protein and essential nutrients.",
        "idealConditions": {
            "temperature": {"min": 20, "max": 35},
            "rainfall": {"min": 60, "max": 140},
            "ph": {"min": 6.0, "max": 7.5},
            "humidity": {"min": 50, "max": 80},
            "N": {"min": 30, "max": 70},
            "P": {"min": 30, "max": 70},
            "K": {"min": 30, "max": 70}
        },
        "tips": [
            "Prefers warm, humid conditions.",
            "Moderate rainfall needed.",
            "Well-drained soils preferred."
        ],
        "color": "#1f2937"
    },
    "lentil": {
        "emoji": "🫘",
        "displayName": "Lentil",
        "description": "Lentils are protein-rich legumes that are cool season crops. They're highly nutritious and easy to grow.",
        "idealConditions": {
            "temperature": {"min": 10, "max": 25},
            "rainfall": {"min": 40, "max": 100},
            "ph": {"min": 6.0, "max": 7.5},
            "humidity": {"min": 40, "max": 70},
            "N": {"min": 20, "max": 50},
            "P": {"min": 20, "max": 50},
            "K": {"min": 20, "max": 50}
        },
        "tips": [
            "Cool season crop.",
            "Moderate water requirements.",
            "Well-drained soils essential."
        ],
        "color": "#f59e0b"
    },
    "pomegranate": {
        "emoji": "🍎",
        "displayName": "Pomegranate",
        "description": "Pomegranate is a fruit tree that requires well-drained soil. It produces antioxidant-rich fruits and is drought-tolerant once established.",
        "idealConditions": {
            "temperature": {"min": 15, "max": 35},
            "rainfall": {"min": 50, "max": 150},
            "ph": {"min": 5.5, "max": 7.5},
            "humidity": {"min": 40, "max": 70},
            "N": {"min": 50, "max": 100},
            "P": {"min": 40, "max": 80},
            "K": {"min": 50, "max": 100}
        },
        "tips": [
            "Requires well-drained soil.",
            "Drought-tolerant once established.",
            "Prefers warm, dry summers."
        ],
        "color": "#dc2626"
    },
    "banana": {
        "emoji": "🍌",
        "displayName": "Banana",
        "description": "Banana is a tropical fruit that needs high humidity and consistent moisture. It's one of the most popular fruits worldwide.",
        "idealConditions": {
            "temperature": {"min": 20, "max": 35},
            "rainfall": {"min": 100, "max": 250},
            "ph": {"min": 5.5, "max": 7.0},
            "humidity": {"min": 75, "max": 100},
            "N": {"min": 80, "max": 150},
            "P": {"min": 40, "max": 80},
            "K": {"min": 100, "max": 200}
        },
        "tips": [
            "Requires high humidity and consistent moisture.",
            "Needs protection from strong winds.",
            "Rich, well-drained soil preferred."
        ],
        "color": "#fbbf24"
    },
    "mango": {
        "emoji": "🥭",
        "displayName": "Mango",
        "description": "Mango is a tropical fruit tree that thrives in warm climates. It produces sweet, juicy fruits and requires well-drained soil.",
        "idealConditions": {
            "temperature": {"min": 20, "max": 35},
            "rainfall": {"min": 80, "max": 200},
            "ph": {"min": 5.5, "max": 7.5},
            "humidity": {"min": 60, "max": 90},
            "N": {"min": 70, "max": 120},
            "P": {"min": 40, "max": 80},
            "K": {"min": 80, "max": 150}
        },
        "tips": [
            "Tropical climate preferred.",
            "Well-drained soil essential.",
            "Requires warm temperatures year-round."
        ],
        "color": "#f97316"
    },
    "grapes": {
        "emoji": "🍇",
        "displayName": "Grapes",
        "description": "Grapes are vine fruits that grow well in moderate climates. They're used for fresh consumption, wine, and raisins.",
        "idealConditions": {
            "temperature": {"min": 15, "max": 30},
            "rainfall": {"min": 50, "max": 120},
            "ph": {"min": 5.5, "max": 7.5},
            "humidity": {"min": 50, "max": 80},
            "N": {"min": 50, "max": 100},
            "P": {"min": 40, "max": 80},
            "K": {"min": 60, "max": 120}
        },
        "tips": [
            "Moderate climate preferred.",
            "Well-drained soils essential.",
            "Requires support structures for vines."
        ],
        "color": "#a855f7"
    },
    "watermelon": {
        "emoji": "🍉",
        "displayName": "Watermelon",
        "description": "Watermelon is a summer fruit that needs warm temperatures and plenty of water. It's refreshing and highly water-content.",
        "idealConditions": {
            "temperature": {"min": 22, "max": 35},
            "rainfall": {"min": 50, "max": 150},
            "ph": {"min": 6.0, "max": 7.0},
            "humidity": {"min": 50, "max": 80},
            "N": {"min": 60, "max": 120},
            "P": {"min": 40, "max": 80},
            "K": {"min": 60, "max": 120}
        },
        "tips": [
            "Warm temperatures essential.",
            "Needs consistent moisture.",
            "Well-drained, sandy soils preferred."
        ],
        "color": "#ef4444"
    },
    "muskmelon": {
        "emoji": "🍈",
        "displayName": "Muskmelon",
        "description": "Muskmelon is a sweet melon that's a warm season crop. It requires moderate water and warm temperatures.",
        "idealConditions": {
            "temperature": {"min": 20, "max": 32},
            "rainfall": {"min": 40, "max": 100},
            "ph": {"min": 6.0, "max": 7.5},
            "humidity": {"min": 50, "max": 75},
            "N": {"min": 50, "max": 100},
            "P": {"min": 30, "max": 70},
            "K": {"min": 50, "max": 100}
        },
        "tips": [
            "Warm season crop.",
            "Moderate water requirements.",
            "Well-drained soils preferred."
        ],
        "color": "#84cc16"
    },
    "apple": {
        "emoji": "🍎",
        "displayName": "Apple",
        "description": "Apple is a temperate fruit that prefers cool climates. It requires well-drained soil and cold winters for proper fruiting.",
        "idealConditions": {
            "temperature": {"min": 8, "max": 25},
            "rainfall": {"min": 60, "max": 150},
            "ph": {"min": 6.0, "max": 7.0},
            "humidity": {"min": 50, "max": 80},
            "N": {"min": 60, "max": 120},
            "P": {"min": 40, "max": 80},
            "K": {"min": 60, "max": 120}
        },
        "tips": [
            "Cool climate preferred.",
            "Requires cold winters for dormancy.",
            "Well-drained, fertile soils needed."
        ],
        "color": "#ef4444"
    },
    "orange": {
        "emoji": "🍊",
        "displayName": "Orange",
        "description": "Orange is a citrus fruit that grows in subtropical climates. It requires well-drained soil and moderate temperatures.",
        "idealConditions": {
            "temperature": {"min": 15, "max": 30},
            "rainfall": {"min": 80, "max": 180},
            "ph": {"min": 5.5, "max": 7.0},
            "humidity": {"min": 60, "max": 85},
            "N": {"min": 70, "max": 130},
            "P": {"min": 40, "max": 80},
            "K": {"min": 80, "max": 150}
        },
        "tips": [
            "Subtropical climate preferred.",
            "Well-drained soils essential.",
            "Moderate to high humidity needed."
        ],
        "color": "#f97316"
    },
    "papaya": {
        "emoji": "🥭",
        "displayName": "Papaya",
        "description": "Papaya is a tropical fruit that requires warm and humid conditions. It grows quickly and produces sweet, nutritious fruits.",
        "idealConditions": {
            "temperature": {"min": 20, "max": 35},
            "rainfall": {"min": 100, "max": 250},
            "ph": {"min": 5.5, "max": 7.0},
            "humidity": {"min": 70, "max": 100},
            "N": {"min": 70, "max": 130},
            "P": {"min": 40, "max": 80},
            "K": {"min": 80, "max": 150}
        },
        "tips": [
            "Tropical, warm and humid climate needed.",
            "High rainfall or irrigation required.",
            "Well-drained, fertile soils preferred."
        ],
        "color": "#fbbf24"
    },
    "coconut": {
        "emoji": "🥥",
        "displayName": "Coconut",
        "description": "Coconut is a tropical palm that grows in coastal regions. It requires high humidity, warm temperatures, and plenty of rainfall.",
        "idealConditions": {
            "temperature": {"min": 22, "max": 35},
            "rainfall": {"min": 150, "max": 300},
            "ph": {"min": 5.5, "max": 8.0},
            "humidity": {"min": 75, "max": 100},
            "N": {"min": 80, "max": 150},
            "P": {"min": 40, "max": 90},
            "K": {"min": 100, "max": 200}
        },
        "tips": [
            "Coastal, tropical regions preferred.",
            "Requires high humidity and rainfall.",
            "Sandy, well-drained soils work best."
        ],
        "color": "#84cc16"
    },
    "cotton": {
        "emoji": "🧵",
        "displayName": "Cotton",
        "description": "Cotton is a fiber crop that prefers warm and dry climates. It requires well-drained soil and moderate rainfall.",
        "idealConditions": {
            "temperature": {"min": 20, "max": 35},
            "rainfall": {"min": 50, "max": 120},
            "ph": {"min": 5.8, "max": 8.0},
            "humidity": {"min": 40, "max": 70},
            "N": {"min": 60, "max": 120},
            "P": {"min": 40, "max": 80},
            "K": {"min": 60, "max": 120}
        },
        "tips": [
            "Warm, dry climate preferred.",
            "Well-drained soils essential.",
            "Moderate water requirements."
        ],
        "color": "#f8fafc"
    },
    "jute": {
        "emoji": "🌿",
        "displayName": "Jute",
        "description": "Jute is a fiber crop that requires high rainfall and humidity. It's used for making ropes, bags, and textiles.",
        "idealConditions": {
            "temperature": {"min": 20, "max": 35},
            "rainfall": {"min": 150, "max": 300},
            "ph": {"min": 6.0, "max": 7.5},
            "humidity": {"min": 70, "max": 100},
            "N": {"min": 80, "max": 150},
            "P": {"min": 40, "max": 90},
            "K": {"min": 100, "max": 200}
        },
        "tips": [
            "High rainfall and humidity required.",
            "Warm, humid climate preferred.",
            "Fertile, alluvial soils work best."
        ],
        "color": "#22c55e"
    },
    "coffee": {
        "emoji": "☕",
        "displayName": "Coffee",
        "description": "Coffee is a beverage crop that prefers high altitude and moderate temperatures. It requires well-drained soil and consistent rainfall.",
        "idealConditions": {
            "temperature": {"min": 15, "max": 28},
            "rainfall": {"min": 100, "max": 200},
            "ph": {"min": 5.5, "max": 6.5},
            "humidity": {"min": 60, "max": 85},
            "N": {"min": 70, "max": 130},
            "P": {"min": 40, "max": 80},
            "K": {"min": 80, "max": 150}
        },
        "tips": [
            "High altitude preferred (1000-2000m).",
            "Moderate temperatures needed.",
            "Well-drained, slightly acidic soils."
        ],
        "color": "#854d0e"
    }
}

# ===========================================
# HELPER FUNCTIONS
# ===========================================
def get_crop_emoji(crop_name):
    crop_lower = crop_name.lower()
    return CROP_INFO.get(crop_lower, {}).get("emoji", "🌱")

def get_crop_info(crop_name):
    """Get full crop information"""
    crop_lower = crop_name.lower()
    return CROP_INFO.get(crop_lower, {})

def get_crop_description(crop_name):
    crop_lower = crop_name.lower()
    info = CROP_INFO.get(crop_lower, {})
    return info.get("description", "Agricultural crop suitable for your conditions.")

def get_crop_color(crop_name):
    crop_lower = crop_name.lower()
    return CROP_INFO.get(crop_lower, {}).get("color", "#22c55e")

def get_crop_display_name(crop_name):
    crop_lower = crop_name.lower()
    info = CROP_INFO.get(crop_lower, {})
    return info.get("displayName", crop_name.title())

def generate_why_crop_explanations(crop_name, user_inputs):
    """Generate explanations for why this crop fits the user's inputs"""
    crop_lower = crop_name.lower()
    crop_info = CROP_INFO.get(crop_lower, {})
    
    if not crop_info or "idealConditions" not in crop_info:
        return ["This crop is suitable based on your soil and climate conditions."]
    
    ideal = crop_info["idealConditions"]
    explanations = []
    
    # Temperature check
    if "temperature" in ideal and "temperature" in user_inputs:
        temp_range = ideal["temperature"]
        user_temp = user_inputs["temperature"]
        if temp_range["min"] <= user_temp <= temp_range["max"]:
            explanations.append(f"🌡️ Your temperature ({user_temp}°C) is within the ideal range for {crop_info.get('displayName', crop_name)} ({temp_range['min']}-{temp_range['max']}°C).")
        elif user_temp < temp_range["min"]:
            explanations.append(f"🌡️ Your temperature ({user_temp}°C) is slightly below ideal, but {crop_info.get('displayName', crop_name)} can still grow with proper care.")
        else:
            explanations.append(f"🌡️ Your temperature ({user_temp}°C) is slightly above ideal, but {crop_info.get('displayName', crop_name)} can adapt to warmer conditions.")
    
    # Rainfall check
    if "rainfall" in ideal and "rainfall" in user_inputs:
        rain_range = ideal["rainfall"]
        user_rain = user_inputs["rainfall"]
        if rain_range["min"] <= user_rain <= rain_range["max"]:
            explanations.append(f"🌧️ Your rainfall ({user_rain}mm) matches the ideal range for {crop_info.get('displayName', crop_name)} ({rain_range['min']}-{rain_range['max']}mm).")
        elif user_rain < rain_range["min"]:
            explanations.append(f"🌧️ Your rainfall ({user_rain}mm) is below ideal, but {crop_info.get('displayName', crop_name)} can grow with irrigation.")
        else:
            explanations.append(f"🌧️ Your rainfall ({user_rain}mm) is above ideal, but {crop_info.get('displayName', crop_name)} can handle higher rainfall with good drainage.")
    
    # pH check
    if "ph" in ideal and "ph" in user_inputs:
        ph_range = ideal["ph"]
        user_ph = user_inputs["ph"]
        if ph_range["min"] <= user_ph <= ph_range["max"]:
            explanations.append(f"🧪 Your soil pH ({user_ph}) is within the preferred range for {crop_info.get('displayName', crop_name)} ({ph_range['min']}-{ph_range['max']}).")
        else:
            explanations.append(f"🧪 Your soil pH ({user_ph}) can be adjusted to better suit {crop_info.get('displayName', crop_name)} if needed.")
    
    # Humidity check
    if "humidity" in ideal and "humidity" in user_inputs:
        hum_range = ideal["humidity"]
        user_hum = user_inputs["humidity"]
        if hum_range["min"] <= user_hum <= hum_range["max"]:
            explanations.append(f"💧 Your humidity ({user_hum}%) is suitable for {crop_info.get('displayName', crop_name)}.")
    
    # Nutrient checks (simplified)
    if "N" in ideal and "N" in user_inputs:
        n_range = ideal["N"]
        user_n = user_inputs["N"]
        if n_range["min"] <= user_n <= n_range["max"]:
            explanations.append(f"🌿 Your nitrogen levels ({user_n}ppm) are appropriate for {crop_info.get('displayName', crop_name)}.")
    
    if not explanations:
        explanations.append(f"Your soil and climate conditions are suitable for growing {crop_info.get('displayName', crop_name)}.")
    
    return explanations

def create_visualization(data, previous_data=None):
    features = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
    feature_labels = ["Nitrogen (N)", "Phosphorus (P)", "Potassium (K)", "Temperature", "Humidity", "pH", "Rainfall"]
    values = [data.get(f, 0) for f in features]
    
    # Normalize values for better radar chart display
    max_val = max(values) if max(values) > 0 else 100
    normalized_values = [v / max_val * 100 for v in values]
    
    # Create figure with animation support
    fig = go.Figure()
    
    # Add previous trace for smooth transition (if available)
    if previous_data:
        prev_values = [previous_data.get(f, 0) for f in features]
        prev_max = max(prev_values) if max(prev_values) > 0 else 100
        prev_normalized = [v / prev_max * 100 for v in prev_values]
        
        fig.add_trace(go.Scatterpolar(
            r=prev_normalized,
            theta=feature_labels,
            fill='toself',
            name='Previous',
            line_color='rgba(34, 197, 94, 0.3)',
            fillcolor='rgba(34, 197, 94, 0.1)',
            line_width=2,
            marker=dict(size=8, color='rgba(20, 83, 45, 0.5)'),
            showlegend=False
        ))
    
    # Add current trace
    fig.add_trace(go.Scatterpolar(
        r=normalized_values,
        theta=feature_labels,
        fill='toself',
        name='Current Parameters',
        line_color='#22c55e',
        fillcolor='rgba(34, 197, 94, 0.35)',
        line_width=4,
        marker=dict(
            size=14, 
            color='#14532d',
            line=dict(width=3, color='#ffffff'),
            symbol='circle'
        ),
        hovertemplate='<b>%{theta}</b><br>Normalized: %{r:.1f}%<br>Actual: %{customdata}<extra></extra>',
        customdata=[f"{values[i]:.1f}" for i in range(len(values))]
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=16, color='#1f2937', family='Arial, sans-serif', weight='bold'),
                gridcolor='rgba(34, 197, 94, 0.3)',
                gridwidth=2,
                linecolor='rgba(34, 197, 94, 0.5)',
                linewidth=2,
                showline=True,
                ticksuffix='%',
                tickmode='linear',
                tick0=0,
                dtick=20,
                showticklabels=True
            ),
            angularaxis=dict(
                tickfont=dict(size=18, color='#14532d', family='Arial, sans-serif', weight='bold'),
                linecolor='rgba(34, 197, 94, 0.5)',
                linewidth=2,
                gridcolor='rgba(34, 197, 94, 0.25)',
                gridwidth=1
            ),
            bgcolor='rgba(241, 248, 244, 0.95)'
        ),
        showlegend=False,
        height=500,
        paper_bgcolor='rgba(241, 248, 244, 0.95)',
        plot_bgcolor='rgba(255, 255, 255, 0.9)',
        font=dict(color='#1f2937', size=14, family='Arial, sans-serif'),
        title=dict(
            text='Parameter Analysis Radar Chart (Live Updates)',
            font=dict(size=24, color='#14532d', family='Arial, sans-serif', weight='bold'),
            x=0.5,
            xanchor='center',
            y=0.95,
            yanchor='top'
        ),
        margin=dict(l=80, r=80, t=80, b=80),
        # Add transition animation
    )
    
    return fig

# ===========================================
# HERO SECTION
# ===========================================
st.markdown("""
<div class="hero-section">
    <div style="position: relative; display: inline-block;">
        <h1 class="hero-title">🌾 Smart Crop Advisor</h1>
        <div style="position: absolute; top: -20px; left: 50%; transform: translateX(-50%); font-size: 2rem; opacity: 0.6; animation: floatPlant 3s ease-in-out infinite;">🌱</div>
        <div style="position: absolute; top: -15px; right: 10%; font-size: 1.5rem; opacity: 0.5; animation: bounceLeaf 2.5s ease-in-out infinite;">🌿</div>
        <div style="position: absolute; top: -15px; left: 10%; font-size: 1.5rem; opacity: 0.5; animation: bounceLeaf 3s ease-in-out infinite;">🌾</div>
        <div style="position: absolute; bottom: -25px; left: 20%; font-size: 1.8rem; opacity: 0.4; animation: cuteWiggle 2.8s ease-in-out infinite;">🌻</div>
        <div style="position: absolute; bottom: -25px; right: 20%; font-size: 1.8rem; opacity: 0.4; animation: cuteWiggle 3.2s ease-in-out infinite;">🌺</div>
    </div>
    <p class="hero-subtitle">Helping farmers choose the right crop for their soil and climate | AI-Powered Agriculture Solutions</p>
    <div style="margin-top: 20px; font-size: 2rem; opacity: 0.6; animation: floatPlant 4s ease-in-out infinite;">
        🌱 🌿 🌾 🌻 🌷 🌺 🌼 🌸 🍀 🌳
    </div>
</div>
""", unsafe_allow_html=True)

# ===========================================
# STATS SECTION
# ===========================================
st.markdown('<div style="margin-bottom: 50px;"></div>', unsafe_allow_html=True)
col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)

with col_stat1:
    st.markdown("""
    <div class="stat-card">
        <div class="plant-sticker-1">✨</div>
        <div class="plant-sticker-2">🌻</div>
        <div style="font-size: 3rem; margin-bottom: 10px; position: relative; z-index: 2; animation: cuteWiggle 2s ease-in-out infinite;">🎯</div>
        <div class="stat-number">99.09%</div>
        <div class="stat-label">Accuracy</div>
        <div style="font-size: 1.2rem; margin-top: 10px; color: #22c55e; font-weight: 600; position: relative; z-index: 2;">AI-Powered Precision</div>
    </div>
    """, unsafe_allow_html=True)

with col_stat2:
    st.markdown("""
    <div class="stat-card">
        <div class="plant-sticker-1">🌺</div>
        <div class="plant-sticker-2">🍀</div>
        <div style="font-size: 3rem; margin-bottom: 10px; position: relative; z-index: 2; animation: cuteWiggle 2.5s ease-in-out infinite;">🌾</div>
        <div class="stat-number">22</div>
        <div class="stat-label">Crop Types</div>
        <div style="font-size: 1.2rem; margin-top: 10px; color: #22c55e; font-weight: 600; position: relative; z-index: 2;">Diverse Options</div>
    </div>
    """, unsafe_allow_html=True)

with col_stat3:
    st.markdown("""
    <div class="stat-card">
        <div class="plant-sticker-1">🌸</div>
        <div class="plant-sticker-2">🌷</div>
        <div style="font-size: 3rem; margin-bottom: 10px; position: relative; z-index: 2; animation: cuteWiggle 3s ease-in-out infinite;">📊</div>
        <div class="stat-number">7</div>
        <div class="stat-label">Parameters</div>
        <div style="font-size: 1.2rem; margin-top: 10px; color: #22c55e; font-weight: 600; position: relative; z-index: 2;">Comprehensive Analysis</div>
    </div>
    """, unsafe_allow_html=True)

with col_stat4:
    st.markdown("""
    <div class="stat-card">
        <div class="plant-sticker-1">🌼</div>
        <div class="plant-sticker-2">🌿</div>
        <div style="font-size: 3rem; margin-bottom: 10px; position: relative; z-index: 2; animation: cuteWiggle 2.2s ease-in-out infinite;">📈</div>
        <div class="stat-number">2,200+</div>
        <div class="stat-label">Data Points</div>
        <div style="font-size: 1.2rem; margin-top: 10px; color: #22c55e; font-weight: 600; position: relative; z-index: 2;">Rich Dataset</div>
    </div>
    """, unsafe_allow_html=True)

# ===========================================
# MAIN TABS - With Spacing
# ===========================================
st.markdown('<div style="margin-top: 60px; margin-bottom: 20px;"></div>', unsafe_allow_html=True)
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12, tab13, tab14, tab15 = st.tabs([
    "🌱 Single Prediction", 
    "📊 Batch Analysis", 
    "🔄 Crop Comparison",
    "📅 Seasonal Planner",
    "💰 Market Prices",
    "🌤️ Weather Insights",
    "📈 Analytics",
    "🌍 Soil Health",
    "🔄 Rotation Planner",
    "💧 Irrigation Calculator",
    "🦠 Disease & Pests",
    "📊 Yield Prediction",
    "🌿 Fertilizer Engine",
    "📜 History & Export",
    "💡 About"
])

# ===========================================
# TAB 1: SINGLE PREDICTION
# ===========================================
with tab1:
    st.markdown('<h2 class="section-header">Enter Your Soil & Climate Parameters</h2>', unsafe_allow_html=True)
    
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.markdown("### 🌍 Soil Nutrients")
        col1, col2, col3 = st.columns(3)

        with col1:
            N = st.number_input(
                "🌿 Nitrogen (N) ppm",
                min_value=0.0,
                max_value=200.0,
                value=90.0,
                step=1.0,
                help="Essential for leaf growth and green color"
            )

        with col2:
            P = st.number_input(
                "🔬 Phosphorus (P) ppm",
                min_value=0.0,
                max_value=200.0,
                value=42.0,
                step=1.0,
                help="Important for root development and flowering"
            )

        with col3:
            K = st.number_input(
                "⚡ Potassium (K) ppm",
                min_value=0.0,
                max_value=250.0,
                value=43.0,
                step=1.0,
                help="Vital for overall plant health and disease resistance"
            )
        
        st.markdown("### 🌡️ Climate Conditions")
        col4, col5 = st.columns(2)
        
        with col4:
            temperature = st.number_input(
                "🌡️ Temperature (°C)",
                min_value=0.0,
                max_value=60.0,
                value=24.0,
                step=0.5,
                help="Average temperature in your region"
            )
            
            humidity = st.number_input(
                "💧 Humidity (%)",
                min_value=0.0,
                max_value=100.0,
                value=82.0,
                step=0.5,
                help="Relative humidity level"
            )
        
        with col5:
            ph = st.number_input(
                "🧪 Soil pH",
                min_value=0.0,
                max_value=14.0,
                value=6.4,
                step=0.1,
                help="Acidity/alkalinity of soil (7 is neutral)"
            )
            
            rainfall = st.number_input(
                "🌧️ Rainfall (mm)",
                min_value=0.0,
                max_value=300.0,
                value=120.0,
                step=1.0,
                help="Annual or seasonal rainfall"
            )
        
        # Climate Conditions Visualization - LIVE UPDATES
        st.markdown("### 📈 Climate Overview (Live Updates)")
        
        # Use actual values for better readability
        climate_data = {
            "Temperature": temperature,
            "Humidity": humidity,
            "Rainfall": rainfall,
            "pH": ph
        }
        
        # Create a more readable chart with better spacing
        fig_climate = go.Figure()
        fig_climate.add_trace(go.Bar(
            x=list(climate_data.keys()),
            y=list(climate_data.values()),
            marker=dict(
                color=['#ef4444', '#3b82f6', '#06b6d4', '#22c55e'],
                line=dict(color='#1f2937', width=2)
            ),
            text=[f"{temperature:.1f}°C", f"{humidity:.0f}%", f"{rainfall:.0f}mm", f"{ph:.1f}"],
            textposition='outside',
            textfont=dict(
                color='#1f2937', 
                size=18,
                family='Arial, sans-serif',
                weight='bold'
            ),
            hovertemplate='<b>%{x}</b><br>Value: %{text}<extra></extra>',
            hoverlabel=dict(
                bgcolor='rgba(34, 197, 94, 0.9)',
                font_size=16,
                font_family='Arial'
            )
        ))
        
        # Calculate max value for y-axis (add 20% padding)
        max_val = max(climate_data.values()) * 1.2 if max(climate_data.values()) > 0 else 100
        
        fig_climate.update_layout(
            height=450,
            showlegend=False,
            paper_bgcolor='rgba(241, 248, 244, 0.95)',
            plot_bgcolor='rgba(255, 255, 255, 0.9)',
            xaxis=dict(
                tickfont=dict(color='#1f2937', size=16, family='Arial', weight='bold'),
                title=dict(
                    text='Climate Parameters',
                    font=dict(size=18, color='#14532d', family='Arial', weight='bold')
                ),
                gridcolor='rgba(34, 197, 94, 0.2)',
                gridwidth=1,
                showgrid=True
            ),
            yaxis=dict(
                tickfont=dict(color='#1f2937', size=14, family='Arial'),
                title=dict(
                    text='Values',
                    font=dict(size=18, color='#14532d', family='Arial', weight='bold')
                ),
                gridcolor='rgba(34, 197, 94, 0.2)',
                gridwidth=1,
                showgrid=True,
                showticklabels=True,
                range=[0, max_val]
            ),
            margin=dict(l=60, r=40, t=40, b=60),
            title=dict(
                text='Climate Conditions Analysis (Live)',
                font=dict(size=22, color='#14532d', family='Arial', weight='bold'),
                x=0.5,
                xanchor='center'
            ),
        )
        
        climate_chart_key = f"climate_{temperature}_{humidity}_{rainfall}_{ph}"
        st.plotly_chart(fig_climate, use_container_width=True, key=climate_chart_key)
        
        # Add live update indicator
        st.markdown("""
        <div style="text-align: center; margin-top: 10px; padding: 10px; 
                    background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%); 
                    border-radius: 10px; border: 2px solid rgba(34, 197, 94, 0.3);">
            <p style="color: #14532d; font-weight: 600; margin: 0;">
                ✨ All charts update automatically as you change values above
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_right:
        st.markdown("### 📊 Advanced Analytics Dashboard")
        
        # Create tabs for different visualizations
        viz_tab1, viz_tab2, viz_tab3, viz_tab4 = st.tabs(["🎯 Radar Chart", "📊 Soil Nutrients", "🌡️ Climate Data", "📈 Summary"])
        
        with viz_tab1:
            st.markdown("#### 🎯 Parameter Analysis Radar Chart (Live Updates)")
            
            # Store previous values for smooth transitions
            if 'prev_input_data' not in st.session_state:
                st.session_state.prev_input_data = None
            
            input_data = {
                "N": N, "P": P, "K": K,
                "temperature": temperature,
                "humidity": humidity,
                "ph": ph,
                "rainfall": rainfall
            }
            
            # Create visualization with previous data for smooth transition
            fig = create_visualization(input_data, st.session_state.prev_input_data)
            
            # Update previous data
            st.session_state.prev_input_data = input_data.copy()
            
            # Display with key to force update
            chart_key = f"radar_{N}_{P}_{K}_{temperature}_{humidity}_{ph}_{rainfall}"
            st.plotly_chart(fig, use_container_width=True, key=chart_key)
            
            # Add live update indicator
            st.markdown("""
            <div style="text-align: center; margin-top: 10px; padding: 10px; 
                        background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%); 
                        border-radius: 10px; border: 2px solid rgba(34, 197, 94, 0.3);">
                <p style="color: #14532d; font-weight: 600; margin: 0;">
                    ✨ Chart updates automatically as you change values above
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with viz_tab2:
            st.markdown("#### 🌿 Soil Nutrient Analysis (Live Updates)")
            
            # Soil nutrients bar chart - updates dynamically
            nutrients_data = {
                "Nutrient": ["Nitrogen (N)", "Phosphorus (P)", "Potassium (K)"],
                "Value (ppm)": [N, P, K],
                "Ideal Min": [50, 30, 50],
                "Ideal Max": [150, 100, 200]
            }
            
            fig_nutrients = go.Figure()
            
            # Add ideal range bars
            fig_nutrients.add_trace(go.Bar(
                name='Ideal Range',
                x=nutrients_data["Nutrient"],
                y=[nutrients_data["Ideal Max"][i] - nutrients_data["Ideal Min"][i] for i in range(3)],
                base=nutrients_data["Ideal Min"],
                marker_color='rgba(200, 230, 201, 0.5)',
                hovertemplate='Ideal Range: %{base:.0f}-%{y:.0f} ppm<extra></extra>'
            ))
            
            # Add actual values with dynamic colors
            colors = []
            for i in range(3):
                if nutrients_data["Ideal Min"][i] <= nutrients_data["Value (ppm)"][i] <= nutrients_data["Ideal Max"][i]:
                    colors.append('#22c55e')
                elif nutrients_data["Value (ppm)"][i] < nutrients_data["Ideal Min"][i]:
                    colors.append('#fbbf24')
                else:
                    colors.append('#ef4444')
            
            fig_nutrients.add_trace(go.Bar(
                name='Your Values',
                x=nutrients_data["Nutrient"],
                y=nutrients_data["Value (ppm)"],
                marker_color=colors,
                text=[f"{v:.0f} ppm" for v in nutrients_data["Value (ppm)"]],
                textposition='outside',
                textfont=dict(size=16, color='#1f2937', weight='bold'),
                hovertemplate='<b>%{x}</b><br>Value: %{y:.0f} ppm<extra></extra>',
                marker_line=dict(width=2, color='#1f2937')
            ))
            
            fig_nutrients.update_layout(
                barmode='overlay',
                height=400,
                title=dict(
                    text='Soil Nutrient Levels vs Ideal Range (Live)',
                    font=dict(size=20, color='#14532d', weight='bold')
                ),
                xaxis=dict(
                    title=dict(text='Nutrients', font=dict(size=18, color='#14532d', weight='bold')),
                    tickfont=dict(size=16, color='#1f2937', weight='bold')
                ),
                yaxis=dict(
                    title=dict(text='Concentration (ppm)', font=dict(size=18, color='#14532d', weight='bold')),
                    tickfont=dict(size=14, color='#1f2937')
                ),
                paper_bgcolor='rgba(241, 248, 244, 0.95)',
                plot_bgcolor='rgba(255, 255, 255, 0.9)',
                showlegend=True,
                legend=dict(font=dict(size=14))
            )
            
            chart_key_nutrients = f"nutrients_{N}_{P}_{K}"
            st.plotly_chart(fig_nutrients, use_container_width=True, key=chart_key_nutrients)
            
            # Nutrient status indicators
            col_n1, col_n2, col_n3 = st.columns(3)
            with col_n1:
                n_status = "✅ Optimal" if 50 <= N <= 150 else "⚠️ Check"
                n_color = "#22c55e" if 50 <= N <= 150 else "#ef4444"
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 100%); 
                            padding: 20px; border-radius: 15px; border: 2px solid {n_color}; 
                            text-align: center;">
                    <h4 style="color: #14532d; margin: 0;">Nitrogen (N)</h4>
                    <p style="font-size: 1.5rem; font-weight: bold; color: {n_color}; margin: 10px 0;">{N:.0f} ppm</p>
                    <p style="color: #6b7280; margin: 0;">{n_status}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col_n2:
                p_status = "✅ Optimal" if 30 <= P <= 100 else "⚠️ Check"
                p_color = "#22c55e" if 30 <= P <= 100 else "#ef4444"
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 100%); 
                            padding: 20px; border-radius: 15px; border: 2px solid {p_color}; 
                            text-align: center;">
                    <h4 style="color: #14532d; margin: 0;">Phosphorus (P)</h4>
                    <p style="font-size: 1.5rem; font-weight: bold; color: {p_color}; margin: 10px 0;">{P:.0f} ppm</p>
                    <p style="color: #6b7280; margin: 0;">{p_status}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col_n3:
                k_status = "✅ Optimal" if 50 <= K <= 200 else "⚠️ Check"
                k_color = "#22c55e" if 50 <= K <= 200 else "#ef4444"
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 100%); 
                            padding: 20px; border-radius: 15px; border: 2px solid {k_color}; 
                            text-align: center;">
                    <h4 style="color: #14532d; margin: 0;">Potassium (K)</h4>
                    <p style="font-size: 1.5rem; font-weight: bold; color: {k_color}; margin: 10px 0;">{K:.0f} ppm</p>
                    <p style="color: #6b7280; margin: 0;">{k_status}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with viz_tab3:
            st.markdown("#### 🌡️ Climate Conditions Analysis (Live Updates)")
            
            # Climate gauge charts - update dynamically
            col_c1, col_c2 = st.columns(2)
            
            with col_c1:
                # Temperature gauge - updates live
                fig_temp = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = temperature,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Temperature (°C) - Live", 'font': {'size': 20, 'color': '#14532d', 'weight': 'bold'}},
                    delta = {'reference': 25, 'font': {'size': 16}},
                    number = {'font': {'size': 30, 'color': '#1f2937', 'weight': 'bold'}},
                    gauge = {
                        'axis': {'range': [None, 50], 'tickfont': {'size': 14, 'color': '#1f2937', 'weight': 'bold'}},
                        'bar': {'color': "#22c55e", 'line': {'width': 2}},
                        'steps': [
                            {'range': [0, 15], 'color': "lightblue"},
                            {'range': [15, 30], 'color': "#86efac"},
                            {'range': [30, 50], 'color': "#fbbf24"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 40
                        }
                    }
                ))
                fig_temp.update_layout(
                    height=300,
                    paper_bgcolor='rgba(241, 248, 244, 0.95)',
                    font=dict(size=16, color='#1f2937'),
                )
                st.plotly_chart(fig_temp, use_container_width=True, key=f"temp_{temperature}")
            
            with col_c2:
                # Humidity gauge - updates live
                fig_hum = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = humidity,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Humidity (%) - Live", 'font': {'size': 20, 'color': '#14532d', 'weight': 'bold'}},
                    number = {'font': {'size': 30, 'color': '#1f2937', 'weight': 'bold'}},
                    gauge = {
                        'axis': {'range': [None, 100], 'tickfont': {'size': 14, 'color': '#1f2937', 'weight': 'bold'}},
                        'bar': {'color': "#3b82f6", 'line': {'width': 2}},
                        'steps': [
                            {'range': [0, 30], 'color': "#fee2e2"},
                            {'range': [30, 70], 'color': "#86efac"},
                            {'range': [70, 100], 'color': "#22c55e"}
                        ]
                    }
                ))
                fig_hum.update_layout(
                    height=300,
                    paper_bgcolor='rgba(241, 248, 244, 0.95)',
                    font=dict(size=16, color='#1f2937'),
                )
                st.plotly_chart(fig_hum, use_container_width=True, key=f"hum_{humidity}")
            
            # Rainfall and pH comparison - update live
            col_c3, col_c4 = st.columns(2)
            
            with col_c3:
                fig_rain = go.Figure(go.Bar(
                    x=['Rainfall'],
                    y=[rainfall],
                    marker_color='#06b6d4',
                    marker_line=dict(width=2, color='#1f2937'),
                    text=[f"{rainfall:.0f} mm"],
                    textposition='outside',
                    textfont=dict(size=20, color='#1f2937', weight='bold'),
                    hovertemplate='Rainfall: %{y:.0f} mm<extra></extra>'
                ))
                fig_rain.update_layout(
                    height=250,
                    title=dict(text='Rainfall (Live)', font=dict(size=18, color='#14532d', weight='bold')),
                    xaxis=dict(tickfont=dict(size=16)),
                    yaxis=dict(
                        title=dict(text='mm', font=dict(size=16, weight='bold')),
                        tickfont=dict(size=14)
                    ),
                    paper_bgcolor='rgba(241, 248, 244, 0.95)',
                    plot_bgcolor='rgba(255, 255, 255, 0.9)',
                    showlegend=False,
                )
                st.plotly_chart(fig_rain, use_container_width=True, key=f"rain_{rainfall}")
            
            with col_c4:
                fig_ph = go.Figure(go.Bar(
                    x=['pH Level'],
                    y=[ph],
                    marker_color='#22c55e' if 6.0 <= ph <= 7.0 else '#ef4444',
                    marker_line=dict(width=2, color='#1f2937'),
                    text=[f"{ph:.1f}"],
                    textposition='outside',
                    textfont=dict(size=20, color='#1f2937', weight='bold'),
                    hovertemplate='pH: %{y:.1f}<extra></extra>'
                ))
                fig_ph.update_layout(
                    height=250,
                    title=dict(text='Soil pH (Live)', font=dict(size=18, color='#14532d', weight='bold')),
                    xaxis=dict(tickfont=dict(size=16)),
                    yaxis=dict(
                        title=dict(text='pH', font=dict(size=16, weight='bold')),
                        tickfont=dict(size=14),
                        range=[0, 14]
                    ),
                    paper_bgcolor='rgba(241, 248, 244, 0.95)',
                    plot_bgcolor='rgba(255, 255, 255, 0.9)',
                    showlegend=False,
                )
                st.plotly_chart(fig_ph, use_container_width=True, key=f"ph_{ph}")
        
        with viz_tab4:
            st.markdown("#### 📈 Comprehensive Data Summary")
            
            # All metrics in a nice grid
            metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
            
            with metrics_col1:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 100%); 
                            padding: 25px; border-radius: 20px; border: 2px solid rgba(34, 197, 94, 0.4); 
                            text-align: center; box-shadow: 0 4px 15px rgba(34, 197, 94, 0.2);">
                    <div style="font-size: 2.5rem; margin-bottom: 10px;">🌿</div>
                    <h4 style="color: #14532d; margin: 10px 0; font-size: 1.2rem;">Nitrogen (N)</h4>
                    <p style="font-size: 2rem; font-weight: bold; color: #22c55e; margin: 0;">{N:.0f}</p>
                    <p style="color: #6b7280; margin: 5px 0 0 0; font-size: 0.9rem;">ppm</p>
                </div>
                """, unsafe_allow_html=True)
            
            with metrics_col2:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 100%); 
                            padding: 25px; border-radius: 20px; border: 2px solid rgba(34, 197, 94, 0.4); 
                            text-align: center; box-shadow: 0 4px 15px rgba(34, 197, 94, 0.2);">
                    <div style="font-size: 2.5rem; margin-bottom: 10px;">🔬</div>
                    <h4 style="color: #14532d; margin: 10px 0; font-size: 1.2rem;">Phosphorus (P)</h4>
                    <p style="font-size: 2rem; font-weight: bold; color: #22c55e; margin: 0;">{P:.0f}</p>
                    <p style="color: #6b7280; margin: 5px 0 0 0; font-size: 0.9rem;">ppm</p>
                </div>
                """, unsafe_allow_html=True)
            
            with metrics_col3:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 100%); 
                            padding: 25px; border-radius: 20px; border: 2px solid rgba(34, 197, 94, 0.4); 
                            text-align: center; box-shadow: 0 4px 15px rgba(34, 197, 94, 0.2);">
                    <div style="font-size: 2.5rem; margin-bottom: 10px;">⚡</div>
                    <h4 style="color: #14532d; margin: 10px 0; font-size: 1.2rem;">Potassium (K)</h4>
                    <p style="font-size: 2rem; font-weight: bold; color: #22c55e; margin: 0;">{K:.0f}</p>
                    <p style="color: #6b7280; margin: 5px 0 0 0; font-size: 0.9rem;">ppm</p>
                </div>
                """, unsafe_allow_html=True)
            
            with metrics_col4:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 100%); 
                            padding: 25px; border-radius: 20px; border: 2px solid rgba(34, 197, 94, 0.4); 
                            text-align: center; box-shadow: 0 4px 15px rgba(34, 197, 94, 0.2);">
                    <div style="font-size: 2.5rem; margin-bottom: 10px;">🌡️</div>
                    <h4 style="color: #14532d; margin: 10px 0; font-size: 1.2rem;">Temperature</h4>
                    <p style="font-size: 2rem; font-weight: bold; color: #22c55e; margin: 0;">{temperature:.1f}</p>
                    <p style="color: #6b7280; margin: 5px 0 0 0; font-size: 0.9rem;">°C</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            metrics_col5, metrics_col6, metrics_col7, metrics_col8 = st.columns(4)
            
            with metrics_col5:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 100%); 
                            padding: 25px; border-radius: 20px; border: 2px solid rgba(34, 197, 94, 0.4); 
                            text-align: center; box-shadow: 0 4px 15px rgba(34, 197, 94, 0.2);">
                    <div style="font-size: 2.5rem; margin-bottom: 10px;">💧</div>
                    <h4 style="color: #14532d; margin: 10px 0; font-size: 1.2rem;">Humidity</h4>
                    <p style="font-size: 2rem; font-weight: bold; color: #22c55e; margin: 0;">{humidity:.0f}</p>
                    <p style="color: #6b7280; margin: 5px 0 0 0; font-size: 0.9rem;">%</p>
                </div>
                """, unsafe_allow_html=True)
            
            with metrics_col6:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 100%); 
                            padding: 25px; border-radius: 20px; border: 2px solid rgba(34, 197, 94, 0.4); 
                            text-align: center; box-shadow: 0 4px 15px rgba(34, 197, 94, 0.2);">
                    <div style="font-size: 2.5rem; margin-bottom: 10px;">🧪</div>
                    <h4 style="color: #14532d; margin: 10px 0; font-size: 1.2rem;">Soil pH</h4>
                    <p style="font-size: 2rem; font-weight: bold; color: #22c55e; margin: 0;">{ph:.1f}</p>
                    <p style="color: #6b7280; margin: 5px 0 0 0; font-size: 0.9rem;">pH level</p>
                </div>
                """, unsafe_allow_html=True)
            
            with metrics_col7:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 100%); 
                            padding: 25px; border-radius: 20px; border: 2px solid rgba(34, 197, 94, 0.4); 
                            text-align: center; box-shadow: 0 4px 15px rgba(34, 197, 94, 0.2);">
                    <div style="font-size: 2.5rem; margin-bottom: 10px;">🌧️</div>
                    <h4 style="color: #14532d; margin: 10px 0; font-size: 1.2rem;">Rainfall</h4>
                    <p style="font-size: 2rem; font-weight: bold; color: #22c55e; margin: 0;">{rainfall:.0f}</p>
                    <p style="color: #6b7280; margin: 5px 0 0 0; font-size: 0.9rem;">mm</p>
                </div>
                """, unsafe_allow_html=True)
            
            with metrics_col8:
                # Calculate overall suitability score
                score = 0
                total = 7
                if 50 <= N <= 150: score += 1
                if 30 <= P <= 100: score += 1
                if 50 <= K <= 200: score += 1
                if 15 <= temperature <= 35: score += 1
                if 40 <= humidity <= 80: score += 1
                if 6.0 <= ph <= 7.5: score += 1
                if 50 <= rainfall <= 200: score += 1
                suitability_pct = (score / total) * 100
                
                suit_color = "#22c55e" if suitability_pct >= 80 else "#fbbf24" if suitability_pct >= 60 else "#ef4444"
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 100%); 
                            padding: 25px; border-radius: 20px; border: 2px solid {suit_color}; 
                            text-align: center; box-shadow: 0 4px 15px rgba(34, 197, 94, 0.2);">
                    <div style="font-size: 2.5rem; margin-bottom: 10px;">⭐</div>
                    <h4 style="color: #14532d; margin: 10px 0; font-size: 1.2rem;">Suitability</h4>
                    <p style="font-size: 2rem; font-weight: bold; color: {suit_color}; margin: 0;">{suitability_pct:.0f}%</p>
                    <p style="color: #6b7280; margin: 5px 0 0 0; font-size: 0.9rem;">Overall Score</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # NEW: Comprehensive Parameter Comparison Chart
            st.markdown("### 📊 Comprehensive Parameter Analysis (Live Updates)")
            
            # Define optimal ranges for each parameter
            optimal_ranges = {
                "Nitrogen (N)": {"current": N, "min": 50, "max": 150, "unit": "ppm"},
                "Phosphorus (P)": {"current": P, "min": 30, "max": 100, "unit": "ppm"},
                "Potassium (K)": {"current": K, "min": 50, "max": 200, "unit": "ppm"},
                "Temperature": {"current": temperature, "min": 15, "max": 35, "unit": "°C"},
                "Humidity": {"current": humidity, "min": 40, "max": 80, "unit": "%"},
                "Soil pH": {"current": ph, "min": 6.0, "max": 7.5, "unit": ""},
                "Rainfall": {"current": rainfall, "min": 50, "max": 200, "unit": "mm"}
            }
            
            # Create comparison chart with error bars
            fig_comparison = go.Figure()
            
            params = list(optimal_ranges.keys())
            current_values = [optimal_ranges[p]["current"] for p in params]
            min_values = [optimal_ranges[p]["min"] for p in params]
            max_values = [optimal_ranges[p]["max"] for p in params]
            
            # Add optimal range bars (background)
            for i, param in enumerate(params):
                fig_comparison.add_trace(go.Bar(
                    name=f'Optimal Range',
                    x=[param],
                    y=[max_values[i] - min_values[i]],
                    base=[min_values[i]],
                    marker_color='rgba(200, 230, 201, 0.4)',
                    marker_line=dict(width=1, color='rgba(34, 197, 94, 0.6)'),
                    hovertemplate=f'<b>{param}</b><br>Optimal Range: {min_values[i]}-{max_values[i]} {optimal_ranges[param]["unit"]}<extra></extra>',
                    showlegend=(i == 0)
                ))
            
            # Add current values with color coding
            colors = []
            for i, param in enumerate(params):
                if min_values[i] <= current_values[i] <= max_values[i]:
                    colors.append('#22c55e')  # Green - optimal
                elif current_values[i] < min_values[i]:
                    colors.append('#fbbf24')  # Yellow - below optimal
                else:
                    colors.append('#ef4444')  # Red - above optimal
            
            fig_comparison.add_trace(go.Bar(
                name='Your Current Value',
                x=params,
                y=current_values,
                marker_color=colors,
                marker_line=dict(width=2, color='#1f2937'),
                text=[f"{v:.1f}{optimal_ranges[p]['unit']}" for v, p in zip(current_values, params)],
                textposition='outside',
                textfont=dict(size=14, color='#1f2937', weight='bold'),
                hovertemplate='<b>%{x}</b><br>Current: %{y:.1f}<extra></extra>',
                showlegend=True
            ))
            
            # Add markers for optimal midpoints
            midpoints = [(min_values[i] + max_values[i]) / 2 for i in range(len(params))]
            fig_comparison.add_trace(go.Scatter(
                name='Optimal Midpoint',
                x=params,
                y=midpoints,
                mode='markers',
                marker=dict(
                    symbol='diamond',
                    size=12,
                    color='#14532d',
                    line=dict(width=2, color='white')
                ),
                hovertemplate='<b>%{x}</b><br>Optimal Midpoint: %{y:.1f}<extra></extra>',
                showlegend=True
            ))
            
            fig_comparison.update_layout(
                barmode='overlay',
                height=500,
                title=dict(
                    text='Current Values vs Optimal Ranges - Comprehensive Analysis (Live)',
                    font=dict(size=22, color='#14532d', weight='bold')
                ),
                xaxis=dict(
                    title=dict(text='Parameters', font=dict(size=18, color='#14532d', weight='bold')),
                    tickfont=dict(size=14, color='#1f2937', weight='bold'),
                    tickangle=-45
                ),
                yaxis=dict(
                    title=dict(text='Values', font=dict(size=18, color='#14532d', weight='bold')),
                    tickfont=dict(size=14, color='#1f2937')
                ),
                paper_bgcolor='rgba(241, 248, 244, 0.95)',
                plot_bgcolor='rgba(255, 255, 255, 0.9)',
                showlegend=True,
                legend=dict(
                    font=dict(size=14, color='#1f2937'),
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                hovermode='closest'
            )
            
            chart_key_comparison = f"comparison_{N}_{P}_{K}_{temperature}_{humidity}_{ph}_{rainfall}"
            st.plotly_chart(fig_comparison, use_container_width=True, key=chart_key_comparison)
            
            # Add status indicators below chart
            st.markdown("### 🎯 Parameter Status Indicators")
            status_cols = st.columns(7)
            
            for idx, (param, data) in enumerate(optimal_ranges.items()):
                with status_cols[idx]:
                    current = data["current"]
                    min_val = data["min"]
                    max_val = data["max"]
                    unit = data["unit"]
                    
                    if min_val <= current <= max_val:
                        status = "✅ Optimal"
                        status_color = "#22c55e"
                        status_bg = "rgba(34, 197, 94, 0.1)"
                    elif current < min_val:
                        status = "⚠️ Low"
                        status_color = "#fbbf24"
                        status_bg = "rgba(251, 191, 36, 0.1)"
                    else:
                        status = "🔴 High"
                        status_color = "#ef4444"
                        status_bg = "rgba(239, 68, 68, 0.1)"
                    
                    st.markdown(f"""
                    <div style="background: {status_bg}; 
                                padding: 15px; border-radius: 12px; border: 2px solid {status_color}; 
                                text-align: center;">
                        <p style="color: #14532d; font-weight: 600; margin: 0 0 5px 0; font-size: 0.9rem;">{param}</p>
                        <p style="font-size: 1.3rem; font-weight: bold; color: {status_color}; margin: 5px 0;">{current:.1f}{unit}</p>
                        <p style="color: {status_color}; font-size: 0.85rem; margin: 0;">{status}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="text-align: center; margin-top: 20px; padding: 15px; 
                        background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%); 
                        border-radius: 12px; border: 2px solid rgba(34, 197, 94, 0.3);">
                <p style="color: #14532d; font-weight: 600; margin: 0;">
                    ✨ All charts and indicators update automatically as you change values above
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    
    with col_btn2:
        predict_button = st.button(
            "🚀 Get AI Recommendation",
            use_container_width=True,
            type="primary"
        )
    
    if predict_button:
        input_payload = {
            "N": N,
            "P": P,
            "K": K,
            "temperature": temperature,
            "humidity": humidity,
            "ph": ph,
            "rainfall": rainfall
        }

        try:
            with st.spinner("🤖 Analyzing soil and climate data with AI..."):
                resp = requests.post(SINGLE_PREDICT_ENDPOINT, json=input_payload, timeout=20)

            if resp.status_code == 200:
                data = resp.json()
                crop = data.get("recommended_crop", "Unknown")
                crop_info = get_crop_info(crop)
                crop_emoji = get_crop_emoji(crop)
                crop_desc = get_crop_description(crop)
                crop_color = get_crop_color(crop)
                crop_display_name = get_crop_display_name(crop)
                
                # Generate why crop explanations
                why_explanations = generate_why_crop_explanations(crop, input_payload)
                
                st.balloons()
                
                # Cute celebration emojis
                st.markdown("""
                <div style="text-align: center; font-size: 3rem; margin: 20px 0; animation: celebrate 0.8s ease-in-out;">
                    <span style="display: inline-block; animation: celebrate 0.6s ease-in-out;">✨</span>
                    <span style="display: inline-block; animation: celebrate 0.6s ease-in-out 0.1s;">🌱</span>
                    <span style="display: inline-block; animation: celebrate 0.6s ease-in-out 0.2s;">🌿</span>
                    <span style="display: inline-block; animation: celebrate 0.6s ease-in-out 0.3s;">🌾</span>
                    <span style="display: inline-block; animation: celebrate 0.6s ease-in-out 0.4s;">✨</span>
                </div>
                """, unsafe_allow_html=True)
                
                # Result Card
                st.markdown(f"""
                <div class="result-card" style="border: 3px solid {crop_color};">
                    <div class="crop-emoji">{crop_emoji}</div>
                    <h2 style='color: #14532d; margin: 20px 0; font-size: 2rem; font-weight: 800;'>Recommended Crop</h2>
                    <div class="crop-name" style="color: {crop_color};">{crop_display_name}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Save to history (Feature 1: Historical Data)
                if 'prediction_history' not in st.session_state:
                    st.session_state.prediction_history = []
                
                history_entry = {
                    'timestamp': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'crop': crop_display_name,
                    'inputs': input_payload.copy(),
                    'crop_color': crop_color,
                    'crop_emoji': crop_emoji
                }
                st.session_state.prediction_history.insert(0, history_entry)
                if len(st.session_state.prediction_history) > 50:  # Keep last 50
                    st.session_state.prediction_history = st.session_state.prediction_history[:50]
                
                # Crop Information Panel - Using Streamlit Components
                if crop_info:
                    ideal_conditions = crop_info.get("idealConditions", {})
                    tips = crop_info.get("tips", [])
                    
                    # Create the info panel using Streamlit components
                    st.markdown('<div class="crop-info-panel">', unsafe_allow_html=True)
                    
                    # About section
                    st.markdown(f"### 🌾 About {crop_display_name}")
                    st.markdown(f"{crop_desc}")
                    
                    # Ideal Growing Conditions
                    st.markdown("#### 📋 Ideal Growing Conditions")
                    conditions_list = []
                    if "temperature" in ideal_conditions:
                        temp_range = ideal_conditions["temperature"]
                        conditions_list.append(f"🌡️ **Temperature:** {temp_range['min']}-{temp_range['max']}°C")
                    
                    if "rainfall" in ideal_conditions:
                        rain_range = ideal_conditions["rainfall"]
                        conditions_list.append(f"🌧️ **Rainfall:** {rain_range['min']}-{rain_range['max']}mm")
                    
                    if "ph" in ideal_conditions:
                        ph_range = ideal_conditions["ph"]
                        conditions_list.append(f"🧪 **Soil pH:** {ph_range['min']}-{ph_range['max']}")
                    
                    if "humidity" in ideal_conditions:
                        hum_range = ideal_conditions["humidity"]
                        conditions_list.append(f"💧 **Humidity:** {hum_range['min']}-{hum_range['max']}%")
                    
                    for condition in conditions_list:
                        st.markdown(f"- {condition}")
                    
                    # Growing Tips
                    if tips:
                        st.markdown("#### 💡 Growing Tips")
                        for tip in tips:
                            st.markdown(f"- {tip}")
                    
                    # Why This Crop Fits
                    st.markdown("#### ✨ Why This Crop Fits Your Field")
                    st.markdown('<div class="why-crop-box">', unsafe_allow_html=True)
                    for explanation in why_explanations:
                        st.markdown(f"- {explanation}")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="crop-info-panel">
                        <p style="color: #1f2937 !important;">This crop is suitable based on your soil and climate conditions. You can explore crop-specific guidance with your local agricultural advisor.</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                info_col1, info_col2 = st.columns(2)
                
                with info_col1:
                    st.success(f"✅ **Crop:** {crop_display_name}")
                    st.info(f"📊 **Model Confidence:** High (99%+ accuracy)")
                
                with info_col2:
                    st.warning("💡 **Next Steps:**")
                    st.markdown("""
                    - Verify local market demand
                    - Check seed availability
                    - Plan planting schedule
                    - Consult local agricultural extension
                    """)
                
                with st.expander("📊 View Input Parameters Used"):
                    st.json(input_payload)
            
            else:
                st.error(f"❌ Error: Backend returned status {resp.status_code}")

        except requests.exceptions.RequestException as e:
            st.error("❌ Connection Error: Could not reach the backend API.")
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")

# ===========================================
# TAB 2: BATCH PREDICTION
# ===========================================
with tab2:
    st.markdown('<h2 class="section-header">Batch Crop Analysis</h2>', unsafe_allow_html=True)
    
    with st.expander("📖 CSV Format Instructions"):
        st.markdown("""
        Your CSV file should contain the following columns:
        - **N** (Nitrogen in ppm)
        - **P** (Phosphorus in ppm)
        - **K** (Potassium in ppm)
        - **temperature** (in °C)
        - **humidity** (in %)
        - **ph** (soil pH value)
        - **rainfall** (in mm)
        """)
    
    uploaded_file = st.file_uploader(
        "📁 Upload CSV File",
        type=["csv"],
        help="Select a CSV file with soil and climate data"
    )

    if uploaded_file is not None:
        try:
            df_preview = pd.read_csv(uploaded_file)
            st.success(f"✅ File loaded successfully! ({len(df_preview)} rows)")
            
            st.markdown("### 📄 Data Preview")
            st.dataframe(df_preview.head(10), use_container_width=True)
            
            required_cols = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
            missing_cols = [col for col in required_cols if col not in df_preview.columns]
            
            if missing_cols:
                st.error(f"❌ Missing required columns: {', '.join(missing_cols)}")
            else:
                st.success("✅ All required columns present!")
                
                uploaded_file.seek(0)
                
                if st.button("🚀 Get Batch Predictions", use_container_width=True, type="primary"):
                    files = {
                        "file": ("batch.csv", uploaded_file.getvalue(), "text/csv")
                    }
                    
                    try:
                        with st.spinner("🤖 Processing batch predictions with AI..."):
                            resp = requests.post(BATCH_PREDICT_ENDPOINT, files=files, timeout=60)
                        
                        if resp.status_code == 200:
                            result = resp.json()
                            
                            if isinstance(result, list):
                                df_result = pd.DataFrame(result)
                                
                                desired_order = [
                                    "N", "P", "K",
                                    "temperature", "humidity", "ph", "rainfall",
                                    "recommended_crop"
                                ]
                                existing_cols = [c for c in desired_order if c in df_result.columns]
                                df_result = df_result[existing_cols]
                                
                                st.success(f"✅ Successfully processed {len(df_result)} predictions!")
                                st.balloons()
                                
                                st.markdown("### 🌾 Prediction Results")
                                st.dataframe(df_result, use_container_width=True, height=400)
                                
                                st.markdown("### 📊 Crop Distribution")
                                crop_counts = df_result['recommended_crop'].value_counts()
                                
                                col_chart1, col_chart2 = st.columns(2)
                                
                                with col_chart1:
                                    fig_bar = px.bar(
                                        x=crop_counts.index,
                                        y=crop_counts.values,
                                        title="Crop Recommendations Count",
                                        labels={"x": "Crop", "y": "Count"},
                                        color=crop_counts.values,
                                        color_continuous_scale="Greens"
                                    )
                                    fig_bar.update_layout(
                                        paper_bgcolor='rgba(0,0,0,0)',
                                        plot_bgcolor='rgba(0,0,0,0)'
                                    )
                                    st.plotly_chart(fig_bar, use_container_width=True)
                                
                                with col_chart2:
                                    fig_pie = px.pie(
                                        values=crop_counts.values,
                                        names=crop_counts.index,
                                        title="Crop Distribution (%)"
                                    )
                                    fig_pie.update_layout(
                                        paper_bgcolor='rgba(0,0,0,0)',
                                        plot_bgcolor='rgba(0,0,0,0)'
                                    )
                                    st.plotly_chart(fig_pie, use_container_width=True)
                                
                                csv_buffer = io.StringIO()
                                df_result.to_csv(csv_buffer, index=False)
                                st.download_button(
                                    label="⬇️ Download Results as CSV",
                                    data=csv_buffer.getvalue(),
                                    file_name="crop_recommendations.csv",
                                    mime="text/csv",
                                    use_container_width=True
                                )
                            else:
                                st.warning("⚠️ Unexpected response format")
                                st.json(result)
                        else:
                            st.error(f"❌ Error: Backend returned status {resp.status_code}")
                            st.text(resp.text)
                    
                    except Exception as e:
                        st.error(f"❌ An error occurred: {str(e)}")

        except Exception as e:
            st.error(f"❌ Could not read CSV file: {str(e)}")
    
    else:
        st.info("👆 Please upload a CSV file to begin batch analysis.")

# ===========================================
# TAB 3: CROP COMPARISON
# ===========================================
with tab3:
    st.markdown('<h2 class="section-header">🔄 Crop Comparison Tool</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="modern-card">
        <p>Compare up to 3 crops side-by-side to see which one best fits your conditions.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_comp1, col_comp2, col_comp3 = st.columns(3)
    
    with col_comp1:
        crop1 = st.selectbox("🌾 Crop 1", options=[""] + list(CROP_INFO.keys()), format_func=lambda x: CROP_INFO.get(x, {}).get("displayName", x) if x else "Select Crop", key="comp_crop1")
    
    with col_comp2:
        crop2 = st.selectbox("🌾 Crop 2", options=[""] + list(CROP_INFO.keys()), format_func=lambda x: CROP_INFO.get(x, {}).get("displayName", x) if x else "Select Crop", key="comp_crop2")
    
    with col_comp3:
        crop3 = st.selectbox("🌾 Crop 3", options=[""] + list(CROP_INFO.keys()), format_func=lambda x: CROP_INFO.get(x, {}).get("displayName", x) if x else "Select Crop", key="comp_crop3")
    
    selected_crops = [c for c in [crop1, crop2, crop3] if c]
    
    if selected_crops:
        st.markdown("### 📊 Detailed Comparison Table")
        
        comparison_data = []
        for crop in selected_crops:
            info = CROP_INFO.get(crop, {})
            ideal = info.get("idealConditions", {})
            temp_range = ideal.get('temperature', {})
            rain_range = ideal.get('rainfall', {})
            ph_range = ideal.get('ph', {})
            hum_range = ideal.get('humidity', {})
            n_range = ideal.get('N', {})
            p_range = ideal.get('P', {})
            k_range = ideal.get('K', {})
            
            comparison_data.append({
                "Crop": info.get("displayName", crop),
                "Emoji": info.get("emoji", "🌱"),
                "Temp Range": f"{temp_range.get('min', 'N/A')}-{temp_range.get('max', 'N/A')}°C" if temp_range else "N/A",
                "Rainfall": f"{rain_range.get('min', 'N/A')}-{rain_range.get('max', 'N/A')}mm" if rain_range else "N/A",
                "pH Range": f"{ph_range.get('min', 'N/A')}-{ph_range.get('max', 'N/A')}" if ph_range else "N/A",
                "Humidity": f"{hum_range.get('min', 'N/A')}-{hum_range.get('max', 'N/A')}%" if hum_range else "N/A",
                "N (ppm)": f"{n_range.get('min', 'N/A')}-{n_range.get('max', 'N/A')}" if n_range else "N/A",
                "P (ppm)": f"{p_range.get('min', 'N/A')}-{p_range.get('max', 'N/A')}" if p_range else "N/A",
                "K (ppm)": f"{k_range.get('min', 'N/A')}-{k_range.get('max', 'N/A')}" if k_range else "N/A"
            })
        
        df_compare = pd.DataFrame(comparison_data)
        
        # Style the dataframe for better readability
        st.markdown("""
        <style>
        .dataframe {
            font-size: 1.1rem !important;
        }
        .dataframe th {
            font-size: 1.2rem !important;
            font-weight: bold !important;
        }
        .dataframe td {
            font-size: 1.1rem !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.dataframe(df_compare, use_container_width=True, height=200)
        
        # Multiple Visual Comparison Charts
        if len(selected_crops) >= 2:
            st.markdown("### 📈 Comprehensive Visual Comparisons")
            
            # Create tabs for different comparison views
            comp_tab1, comp_tab2, comp_tab3, comp_tab4, comp_tab5 = st.tabs([
                "🌡️ Temperature", "🌧️ Rainfall", "🧪 pH & Humidity", "🌿 Nutrients", "📊 Overview"
            ])
            
            with comp_tab1:
                st.markdown("#### 🌡️ Temperature Range Comparison")
                fig_temp = go.Figure()
                
                colors_list = ['#22c55e', '#3b82f6', '#ef4444', '#fbbf24', '#8b5cf6']
                
                for idx, crop in enumerate(selected_crops):
                    info = CROP_INFO.get(crop, {})
                    ideal = info.get("idealConditions", {})
                    temp_range = ideal.get("temperature", {})
                    if temp_range:
                        fig_temp.add_trace(go.Bar(
                            name=info.get("displayName", crop),
                            x=["Min Temp", "Max Temp"],
                            y=[temp_range.get("min", 0), temp_range.get("max", 0)],
                            marker_color=colors_list[idx % len(colors_list)],
                            marker_line=dict(width=2, color='#1f2937'),
                            text=[f"{temp_range.get('min', 0)}°C", f"{temp_range.get('max', 0)}°C"],
                            textposition='outside',
                            textfont=dict(size=18, color='#1f2937', weight='bold'),
                            hovertemplate='<b>%{fullData.name}</b><br>%{x}: %{y}°C<extra></extra>'
                        ))
                
                fig_temp.update_layout(
                    title=dict(
                        text='Temperature Range Comparison',
                        font=dict(size=24, color='#14532d', family='Arial', weight='bold')
                    ),
                    barmode='group',
                    height=450,
                    paper_bgcolor='rgba(241, 248, 244, 0.95)',
                    plot_bgcolor='rgba(255, 255, 255, 0.9)',
                    xaxis=dict(
                        tickfont=dict(size=18, color='#1f2937', weight='bold'),
                        title=dict(text='Temperature Type', font=dict(size=20, color='#14532d', weight='bold'))
                    ),
                    yaxis=dict(
                        tickfont=dict(size=16, color='#1f2937'),
                        title=dict(text='Temperature (°C)', font=dict(size=20, color='#14532d', weight='bold')),
                        gridcolor='rgba(34, 197, 94, 0.2)',
                        gridwidth=1
                    ),
                    legend=dict(
                        font=dict(size=16, color='#1f2937'),
                        bgcolor='rgba(255, 255, 255, 0.8)',
                        bordercolor='rgba(34, 197, 94, 0.3)',
                        borderwidth=2
                    ),
                    margin=dict(l=60, r=40, t=60, b=60)
                )
                st.plotly_chart(fig_temp, use_container_width=True)
            
            with comp_tab2:
                st.markdown("#### 🌧️ Rainfall Requirements Comparison")
                fig_rain = go.Figure()
                
                for idx, crop in enumerate(selected_crops):
                    info = CROP_INFO.get(crop, {})
                    ideal = info.get("idealConditions", {})
                    rain_range = ideal.get("rainfall", {})
                    if rain_range:
                        min_rain = rain_range.get("min", 0)
                        max_rain = rain_range.get("max", 0)
                        avg_rain = (min_rain + max_rain) / 2
                        
                        fig_rain.add_trace(go.Bar(
                            name=info.get("displayName", crop),
                            x=[info.get("displayName", crop)],
                            y=[avg_rain],
                            marker_color=colors_list[idx % len(colors_list)],
                            marker_line=dict(width=2, color='#1f2937'),
                            text=[f"{min_rain}-{max_rain}mm"],
                            textposition='outside',
                            textfont=dict(size=16, color='#1f2937', weight='bold'),
                            hovertemplate='<b>%{fullData.name}</b><br>Range: %{text}<extra></extra>',
                            error_y=dict(
                                type='data',
                                symmetric=False,
                                array=[max_rain - avg_rain],
                                arrayminus=[avg_rain - min_rain],
                                color='#1f2937',
                                width=3
                            )
                        ))
                
                fig_rain.update_layout(
                    title=dict(
                        text='Rainfall Requirements Comparison',
                        font=dict(size=24, color='#14532d', family='Arial', weight='bold')
                    ),
                    barmode='group',
                    height=450,
                    paper_bgcolor='rgba(241, 248, 244, 0.95)',
                    plot_bgcolor='rgba(255, 255, 255, 0.9)',
                    xaxis=dict(
                        tickfont=dict(size=18, color='#1f2937', weight='bold'),
                        title=dict(text='Crop', font=dict(size=20, color='#14532d', weight='bold'))
                    ),
                    yaxis=dict(
                        tickfont=dict(size=16, color='#1f2937'),
                        title=dict(text='Rainfall (mm)', font=dict(size=20, color='#14532d', weight='bold')),
                        gridcolor='rgba(34, 197, 94, 0.2)',
                        gridwidth=1
                    ),
                    showlegend=False,
                    margin=dict(l=60, r=40, t=60, b=60)
                )
                st.plotly_chart(fig_rain, use_container_width=True)
            
            with comp_tab3:
                st.markdown("#### 🧪 pH & Humidity Comparison")
                col_ph, col_hum = st.columns(2)
                
                with col_ph:
                    fig_ph = go.Figure()
                    for idx, crop in enumerate(selected_crops):
                        info = CROP_INFO.get(crop, {})
                        ideal = info.get("idealConditions", {})
                        ph_range = ideal.get("ph", {})
                        if ph_range:
                            min_ph = ph_range.get("min", 0)
                            max_ph = ph_range.get("max", 0)
                            avg_ph = (min_ph + max_ph) / 2
                            
                            fig_ph.add_trace(go.Bar(
                                name=info.get("displayName", crop),
                                x=[info.get("displayName", crop)],
                                y=[avg_ph],
                                marker_color=colors_list[idx % len(colors_list)],
                                marker_line=dict(width=2, color='#1f2937'),
                                text=[f"{min_ph:.1f}-{max_ph:.1f}"],
                                textposition='outside',
                                textfont=dict(size=14, color='#1f2937', weight='bold'),
                                error_y=dict(
                                    type='data',
                                    symmetric=False,
                                    array=[max_ph - avg_ph],
                                    arrayminus=[avg_ph - min_ph],
                                    color='#1f2937',
                                    width=2
                                )
                            ))
                    
                    fig_ph.update_layout(
                        title=dict(text='pH Range', font=dict(size=20, color='#14532d', weight='bold')),
                        height=400,
                        paper_bgcolor='rgba(241, 248, 244, 0.95)',
                        plot_bgcolor='rgba(255, 255, 255, 0.9)',
                        xaxis=dict(tickfont=dict(size=14, weight='bold')),
                        yaxis=dict(
                            title=dict(text='pH', font=dict(size=16, weight='bold')),
                            tickfont=dict(size=14),
                            range=[0, 14]
                        ),
                        showlegend=False
                    )
                    st.plotly_chart(fig_ph, use_container_width=True)
                
                with col_hum:
                    fig_hum = go.Figure()
                    for idx, crop in enumerate(selected_crops):
                        info = CROP_INFO.get(crop, {})
                        ideal = info.get("idealConditions", {})
                        hum_range = ideal.get("humidity", {})
                        if hum_range:
                            min_hum = hum_range.get("min", 0)
                            max_hum = hum_range.get("max", 0)
                            avg_hum = (min_hum + max_hum) / 2
                            
                            fig_hum.add_trace(go.Bar(
                                name=info.get("displayName", crop),
                                x=[info.get("displayName", crop)],
                                y=[avg_hum],
                                marker_color=colors_list[idx % len(colors_list)],
                                marker_line=dict(width=2, color='#1f2937'),
                                text=[f"{min_hum}-{max_hum}%"],
                                textposition='outside',
                                textfont=dict(size=14, color='#1f2937', weight='bold'),
                                error_y=dict(
                                    type='data',
                                    symmetric=False,
                                    array=[max_hum - avg_hum],
                                    arrayminus=[avg_hum - min_hum],
                                    color='#1f2937',
                                    width=2
                                )
                            ))
                    
                    fig_hum.update_layout(
                        title=dict(text='Humidity Range', font=dict(size=20, color='#14532d', weight='bold')),
                        height=400,
                        paper_bgcolor='rgba(241, 248, 244, 0.95)',
                        plot_bgcolor='rgba(255, 255, 255, 0.9)',
                        xaxis=dict(tickfont=dict(size=14, weight='bold')),
                        yaxis=dict(
                            title=dict(text='Humidity (%)', font=dict(size=16, weight='bold')),
                            tickfont=dict(size=14),
                            range=[0, 100]
                        ),
                        showlegend=False
                    )
                    st.plotly_chart(fig_hum, use_container_width=True)
            
            with comp_tab4:
                st.markdown("#### 🌿 Soil Nutrient Requirements Comparison")
                
                # N, P, K comparison
                nutrients_to_compare = ['N', 'P', 'K']
                nutrient_names = ['Nitrogen (N)', 'Phosphorus (P)', 'Potassium (K)']
                
                fig_nutrients = go.Figure()
                
                for idx, nutrient in enumerate(nutrients_to_compare):
                    for crop_idx, crop in enumerate(selected_crops):
                        info = CROP_INFO.get(crop, {})
                        ideal = info.get("idealConditions", {})
                        nut_range = ideal.get(nutrient, {})
                        if nut_range:
                            min_nut = nut_range.get("min", 0)
                            max_nut = nut_range.get("max", 0)
                            avg_nut = (min_nut + max_nut) / 2
                            
                            fig_nutrients.add_trace(go.Bar(
                                name=f"{info.get('displayName', crop)} - {nutrient_names[idx]}",
                                x=[nutrient_names[idx]],
                                y=[avg_nut],
                                marker_color=colors_list[crop_idx % len(colors_list)],
                                marker_line=dict(width=2, color='#1f2937'),
                                text=[f"{min_nut}-{max_nut}"],
                                textposition='outside',
                                textfont=dict(size=12, color='#1f2937', weight='bold'),
                                legendgroup=info.get('displayName', crop),
                                showlegend=(idx == 0)  # Only show legend for first nutrient
                            ))
                
                fig_nutrients.update_layout(
                    title=dict(
                        text='Soil Nutrient Requirements (N, P, K)',
                        font=dict(size=24, color='#14532d', weight='bold')
                    ),
                    barmode='group',
                    height=500,
                    paper_bgcolor='rgba(241, 248, 244, 0.95)',
                    plot_bgcolor='rgba(255, 255, 255, 0.9)',
                    xaxis=dict(
                        tickfont=dict(size=18, color='#1f2937', weight='bold'),
                        title=dict(text='Nutrients', font=dict(size=20, color='#14532d', weight='bold'))
                    ),
                    yaxis=dict(
                        tickfont=dict(size=16, color='#1f2937'),
                        title=dict(text='Concentration (ppm)', font=dict(size=20, color='#14532d', weight='bold')),
                        gridcolor='rgba(34, 197, 94, 0.2)'
                    ),
                    legend=dict(
                        font=dict(size=14, color='#1f2937'),
                        bgcolor='rgba(255, 255, 255, 0.8)',
                        bordercolor='rgba(34, 197, 94, 0.3)',
                        borderwidth=2
                    ),
                    margin=dict(l=60, r=40, t=60, b=60)
                )
                st.plotly_chart(fig_nutrients, use_container_width=True)
            
            with comp_tab5:
                st.markdown("#### 📊 Comprehensive Overview Radar Chart")
                
                # Create radar chart comparing all parameters
                fig_radar = go.Figure()
                
                for idx, crop in enumerate(selected_crops):
                    info = CROP_INFO.get(crop, {})
                    ideal = info.get("idealConditions", {})
                    
                    # Get all parameter ranges
                    params = []
                    values_min = []
                    values_max = []
                    
                    if ideal.get('temperature'):
                        params.append('Temperature')
                        values_min.append(ideal['temperature']['min'])
                        values_max.append(ideal['temperature']['max'])
                    
                    if ideal.get('rainfall'):
                        params.append('Rainfall')
                        values_min.append(ideal['rainfall']['min'])
                        values_max.append(ideal['rainfall']['max'])
                    
                    if ideal.get('ph'):
                        params.append('pH')
                        values_min.append(ideal['ph']['min'])
                        values_max.append(ideal['ph']['max'])
                    
                    if ideal.get('humidity'):
                        params.append('Humidity')
                        values_min.append(ideal['humidity']['min'])
                        values_max.append(ideal['humidity']['max'])
                    
                    if ideal.get('N'):
                        params.append('Nitrogen')
                        values_min.append(ideal['N']['min'])
                        values_max.append(ideal['N']['max'])
                    
                    if ideal.get('P'):
                        params.append('Phosphorus')
                        values_min.append(ideal['P']['min'])
                        values_max.append(ideal['P']['max'])
                    
                    if ideal.get('K'):
                        params.append('Potassium')
                        values_min.append(ideal['K']['min'])
                        values_max.append(ideal['K']['max'])
                    
                    # Normalize values for radar chart (0-100 scale)
                    max_val = max(values_max) if values_max else 100
                    normalized_avg = [((min_v + max_v) / 2) / max_val * 100 for min_v, max_v in zip(values_min, values_max)]
                    
                    # Convert hex color to rgba format
                    hex_color = colors_list[idx % len(colors_list)]
                    # Remove # and convert to RGB values
                    hex_clean = hex_color.lstrip('#')
                    r = int(hex_clean[0:2], 16)
                    g = int(hex_clean[2:4], 16)
                    b = int(hex_clean[4:6], 16)
                    rgba_color = f'rgba({r}, {g}, {b}, 0.3)'
                    
                    fig_radar.add_trace(go.Scatterpolar(
                        r=normalized_avg,
                        theta=params,
                        fill='toself',
                        name=info.get("displayName", crop),
                        line_color=hex_color,
                        fillcolor=rgba_color,
                        line_width=3,
                        marker=dict(size=10, color=hex_color)
                    ))
                
                fig_radar.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 100],
                            tickfont=dict(size=16, color='#1f2937', weight='bold'),
                            gridcolor='rgba(34, 197, 94, 0.3)',
                            gridwidth=2
                        ),
                        angularaxis=dict(
                            tickfont=dict(size=18, color='#14532d', family='Arial', weight='bold'),
                            linecolor='rgba(34, 197, 94, 0.5)',
                            gridcolor='rgba(34, 197, 94, 0.25)'
                        ),
                        bgcolor='rgba(241, 248, 244, 0.95)'
                    ),
                    title=dict(
                        text='Comprehensive Parameter Comparison',
                        font=dict(size=24, color='#14532d', weight='bold')
                    ),
                    height=600,
                    paper_bgcolor='rgba(241, 248, 244, 0.95)',
                    plot_bgcolor='rgba(255, 255, 255, 0.9)',
                    legend=dict(
                        font=dict(size=16, color='#1f2937'),
                        bgcolor='rgba(255, 255, 255, 0.8)',
                        bordercolor='rgba(34, 197, 94, 0.3)',
                        borderwidth=2
                    ),
                    margin=dict(l=80, r=80, t=80, b=80)
                )
                st.plotly_chart(fig_radar, use_container_width=True)
            
            # Additional Information Cards
            st.markdown("### 💡 Detailed Crop Information")
            
            info_cols = st.columns(len(selected_crops))
            for idx, crop in enumerate(selected_crops):
                with info_cols[idx]:
                    info = CROP_INFO.get(crop, {})
                    ideal = info.get("idealConditions", {})
                    tips = info.get("tips", [])
                    
                    st.markdown(f"""
                    <div class="modern-card" style="height: 100%;">
                        <div style="text-align: center; font-size: 4rem; margin-bottom: 15px;">{info.get('emoji', '🌱')}</div>
                        <h3 style="color: #14532d; text-align: center; margin-bottom: 20px; font-size: 1.8rem;">{info.get('displayName', crop)}</h3>
                        <p style="color: #4b5563; line-height: 1.6; margin-bottom: 20px; font-size: 1.1rem;">{info.get('description', 'Agricultural crop.')}</p>
                        <div style="border-top: 2px solid rgba(34, 197, 94, 0.3); padding-top: 15px; margin-top: 15px;">
                            <h4 style="color: #14532d; font-size: 1.3rem; margin-bottom: 10px;">📋 Key Requirements:</h4>
                            <ul style="color: #4b5563; font-size: 1rem; line-height: 1.8;">
                                {f"<li>🌡️ Temp: {ideal.get('temperature', {}).get('min', 'N/A')}-{ideal.get('temperature', {}).get('max', 'N/A')}°C</li>" if ideal.get('temperature') else ""}
                                {f"<li>🌧️ Rainfall: {ideal.get('rainfall', {}).get('min', 'N/A')}-{ideal.get('rainfall', {}).get('max', 'N/A')}mm</li>" if ideal.get('rainfall') else ""}
                                {f"<li>🧪 pH: {ideal.get('ph', {}).get('min', 'N/A')}-{ideal.get('ph', {}).get('max', 'N/A')}</li>" if ideal.get('ph') else ""}
                                {f"<li>💧 Humidity: {ideal.get('humidity', {}).get('min', 'N/A')}-{ideal.get('humidity', {}).get('max', 'N/A')}%</li>" if ideal.get('humidity') else ""}
                            </ul>
                        </div>
                        {f'<div style="margin-top: 15px;"><h4 style="color: #14532d; font-size: 1.2rem; margin-bottom: 8px;">💡 Tips:</h4><ul style="color: #4b5563; font-size: 0.95rem;">' + ''.join([f"<li>{tip}</li>" for tip in tips[:3]]) + '</ul></div>' if tips else ''}
                    </div>
                    """, unsafe_allow_html=True)

# ===========================================
# TAB 4: SEASONAL PLANNER
# ===========================================
with tab4:
    st.markdown('<h2 class="section-header">📅 Seasonal Crop Planner</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="modern-card">
        <p>Get crop recommendations based on the current season and planting calendar.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_season1, col_season2 = st.columns(2)
    
    with col_season1:
        current_month = st.selectbox("📆 Current Month", 
            options=["January", "February", "March", "April", "May", "June",
                    "July", "August", "September", "October", "November", "December"],
            index=pd.Timestamp.now().month - 1)
        
        season = "Spring" if current_month in ["March", "April", "May"] else \
                 "Summer" if current_month in ["June", "July", "August"] else \
                 "Fall" if current_month in ["September", "October", "November"] else "Winter"
        
        st.info(f"🌤️ **Current Season:** {season}")
    
    with col_season2:
        region = st.selectbox("🌍 Region Type", 
            options=["Tropical", "Subtropical", "Temperate", "Cold", "Arid"])
    
    # Seasonal recommendations
    seasonal_crops = {
        "Spring": ["rice", "maize", "chickpea", "kidneybeans", "lentil"],
        "Summer": ["rice", "maize", "watermelon", "muskmelon", "cotton", "jute"],
        "Fall": ["lentil", "chickpea", "apple", "grapes"],
        "Winter": ["lentil", "chickpea", "apple", "orange"]
    }
    
    recommended_seasonal = seasonal_crops.get(season, [])
    
    st.markdown("### 🌾 Recommended Crops for This Season")
    
    cols = st.columns(min(3, len(recommended_seasonal)))
    for idx, crop in enumerate(recommended_seasonal[:6]):
        with cols[idx % 3]:
            info = CROP_INFO.get(crop, {})
            st.markdown(f"""
            <div class="stat-card" style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 10px;">{info.get('emoji', '🌱')}</div>
                <div style="font-size: 1.3rem; font-weight: 700; color: #14532d;">{info.get('displayName', crop)}</div>
                <div style="font-size: 0.9rem; color: #6b7280; margin-top: 5px;">{season} Season</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("### 📅 Planting Calendar")
    calendar_data = {
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        "Best Crops": [
            "Lentil, Chickpea", "Lentil, Chickpea", "Rice, Maize", "Rice, Maize", "Rice, Maize",
            "Rice, Cotton", "Rice, Cotton", "Rice, Cotton", "Lentil, Chickpea", "Lentil, Chickpea",
            "Lentil, Chickpea", "Lentil, Chickpea"
        ]
    }
    df_calendar = pd.DataFrame(calendar_data)
    st.dataframe(df_calendar, use_container_width=True)

# ===========================================
# TAB 5: MARKET PRICES
# ===========================================
with tab5:
    st.markdown('<h2 class="section-header">💰 Market Price Insights</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="modern-card">
        <p>View estimated market prices and profitability analysis for recommended crops.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mock market price data (in real app, this would come from an API)
    market_prices = {
        "rice": {"price_per_kg": 45, "demand": "High", "trend": "↑"},
        "maize": {"price_per_kg": 28, "demand": "Medium", "trend": "→"},
        "wheat": {"price_per_kg": 35, "demand": "High", "trend": "↑"},
        "cotton": {"price_per_kg": 120, "demand": "High", "trend": "↑"},
        "jute": {"price_per_kg": 55, "demand": "Medium", "trend": "→"},
        "mango": {"price_per_kg": 80, "demand": "High", "trend": "↑"},
        "banana": {"price_per_kg": 30, "demand": "High", "trend": "→"}
    }
    
    selected_crop_price = st.selectbox("🌾 Select Crop for Price Analysis", 
        options=list(market_prices.keys()),
        format_func=lambda x: CROP_INFO.get(x, {}).get("displayName", x))
    
    if selected_crop_price:
        price_info = market_prices.get(selected_crop_price, {})
        info = CROP_INFO.get(selected_crop_price, {})
        
        # Market Overview Section
        st.markdown("### 📊 Market Overview")
        col_price1, col_price2, col_price3, col_price4 = st.columns(4)
        
        with col_price1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 100%); 
                        padding: 20px; border-radius: 15px; border: 2px solid rgba(34, 197, 94, 0.4); 
                        text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 10px;">💰</div>
                <h4 style="color: #14532d; margin: 10px 0; font-size: 1.1rem;">Price per kg</h4>
                <p style="font-size: 1.8rem; font-weight: bold; color: #22c55e; margin: 0;">₹{price_info.get('price_per_kg', 0)}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_price2:
            demand_color = "#22c55e" if price_info.get('demand') == "High" else "#fbbf24" if price_info.get('demand') == "Medium" else "#ef4444"
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 100%); 
                        padding: 20px; border-radius: 15px; border: 2px solid {demand_color}; 
                        text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 10px;">📈</div>
                <h4 style="color: #14532d; margin: 10px 0; font-size: 1.1rem;">Market Demand</h4>
                <p style="font-size: 1.8rem; font-weight: bold; color: {demand_color}; margin: 0;">{price_info.get('demand', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_price3:
            trend_emoji = "📈" if price_info.get('trend') == "↑" else "📉" if price_info.get('trend') == "↓" else "➡️"
            trend_color = "#22c55e" if price_info.get('trend') == "↑" else "#ef4444" if price_info.get('trend') == "↓" else "#6b7280"
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 100%); 
                        padding: 20px; border-radius: 15px; border: 2px solid {trend_color}; 
                        text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 10px;">{trend_emoji}</div>
                <h4 style="color: #14532d; margin: 10px 0; font-size: 1.1rem;">Price Trend</h4>
                <p style="font-size: 1.8rem; font-weight: bold; color: {trend_color}; margin: 0;">{price_info.get('trend', '→')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_price4:
            crop_emoji = info.get('emoji', '🌱')
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 100%); 
                        padding: 20px; border-radius: 15px; border: 2px solid rgba(34, 197, 94, 0.4); 
                        text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 10px;">{crop_emoji}</div>
                <h4 style="color: #14532d; margin: 10px 0; font-size: 1.1rem;">Crop Type</h4>
                <p style="font-size: 1.3rem; font-weight: bold; color: #14532d; margin: 0;">{info.get('displayName', selected_crop_price)}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Profitability calculator with live updates
        st.markdown("### 💵 Profitability Calculator (Live Updates)")
        st.markdown("""
        <div style="background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%); 
                    padding: 15px; border-radius: 12px; border: 2px solid rgba(34, 197, 94, 0.3); 
                    margin-bottom: 20px;">
            <p style="color: #14532d; font-weight: 600; margin: 0; font-size: 1.1rem;">
                💡 Adjust the values below to see how profitability changes in real-time!
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col_profit1, col_profit2 = st.columns(2)
        
        with col_profit1:
            st.markdown("#### 📥 Input Parameters")
            expected_yield = st.number_input(
                "🌾 Expected Yield (kg/acre)", 
                min_value=0.0, 
                value=1000.0, 
                step=50.0,
                help="Estimated crop yield per acre based on your field conditions"
            )
            cost_per_acre = st.number_input(
                "💸 Cost per Acre (₹)", 
                min_value=0.0, 
                value=50000.0, 
                step=1000.0,
                help="Total cost including seeds, fertilizers, labor, irrigation, etc."
            )
            
            # Additional cost breakdown
            with st.expander("💰 Cost Breakdown (Optional)"):
                seed_cost = st.number_input("Seeds", min_value=0.0, value=10000.0, step=500.0)
                fertilizer_cost = st.number_input("Fertilizers", min_value=0.0, value=15000.0, step=500.0)
                labor_cost = st.number_input("Labor", min_value=0.0, value=15000.0, step=500.0)
                irrigation_cost = st.number_input("Irrigation", min_value=0.0, value=10000.0, step=500.0)
                total_breakdown = seed_cost + fertilizer_cost + labor_cost + irrigation_cost
                cost_per_acre = total_breakdown if total_breakdown > 0 else cost_per_acre
        
        with col_profit2:
            st.markdown("#### 📊 Financial Results (Live Calculation)")
            
            # Calculate metrics
            price_per_kg = price_info.get('price_per_kg', 0)
            revenue = expected_yield * price_per_kg
            profit = revenue - cost_per_acre
            profit_margin = (profit / revenue * 100) if revenue > 0 else 0
            roi = (profit / cost_per_acre * 100) if cost_per_acre > 0 else 0
            break_even_yield = cost_per_acre / price_per_kg if price_per_kg > 0 else 0
            
            # Display metrics with better styling
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 100%); 
                        padding: 20px; border-radius: 15px; border: 2px solid rgba(34, 197, 94, 0.4); 
                        margin-bottom: 15px;">
                <h4 style="color: #14532d; margin: 0 0 15px 0; font-size: 1.3rem;">💰 Total Revenue</h4>
                <p style="font-size: 2.5rem; font-weight: bold; color: #22c55e; margin: 0;">₹{revenue:,.0f}</p>
                <p style="color: #6b7280; margin: 5px 0 0 0; font-size: 0.9rem;">Yield: {expected_yield:,.0f} kg × Price: ₹{price_per_kg}/kg</p>
            </div>
            """, unsafe_allow_html=True)
            
            profit_color = "#22c55e" if profit > 0 else "#ef4444"
            profit_icon = "✅" if profit > 0 else "❌"
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 100%); 
                        padding: 20px; border-radius: 15px; border: 2px solid {profit_color}; 
                        margin-bottom: 15px;">
                <h4 style="color: #14532d; margin: 0 0 15px 0; font-size: 1.3rem;">💵 Net Profit {profit_icon}</h4>
                <p style="font-size: 2.5rem; font-weight: bold; color: {profit_color}; margin: 0;">₹{profit:,.0f}</p>
                <p style="color: #6b7280; margin: 5px 0 0 0; font-size: 0.9rem;">Profit Margin: {profit_margin:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Additional metrics
            col_metric1, col_metric2 = st.columns(2)
            with col_metric1:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 100%); 
                            padding: 15px; border-radius: 12px; border: 2px solid rgba(34, 197, 94, 0.3); 
                            text-align: center;">
                    <h5 style="color: #14532d; margin: 0 0 10px 0; font-size: 1rem;">📈 ROI</h5>
                    <p style="font-size: 1.8rem; font-weight: bold; color: #22c55e; margin: 0;">{roi:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col_metric2:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 100%); 
                            padding: 15px; border-radius: 12px; border: 2px solid rgba(34, 197, 94, 0.3); 
                            text-align: center;">
                    <h5 style="color: #14532d; margin: 0 0 10px 0; font-size: 1rem;">⚖️ Break-Even</h5>
                    <p style="font-size: 1.5rem; font-weight: bold; color: #fbbf24; margin: 0;">{break_even_yield:.0f} kg</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Visualizations Section
        st.markdown("### 📈 Market Analysis & Trends")
        
        # Create tabs for different visualizations
        market_tab1, market_tab2, market_tab3 = st.tabs(["📊 Price Trend", "💰 Profitability Analysis", "📉 Cost Breakdown"])
        
        with market_tab1:
            st.markdown("#### 📊 Historical Price Trend (Last 6 Months)")
            
            # Price trend chart - updates based on selected crop
            months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
            base_price = price_info.get('price_per_kg', 0)
            
            # Generate realistic price variations
            import random
            random.seed(hash(selected_crop_price) % 1000)  # Consistent seed for same crop
            prices = []
            current_price = base_price
            for i in range(6):
                variation = random.uniform(-0.08, 0.12)  # -8% to +12% variation
                current_price = current_price * (1 + variation)
                prices.append(max(current_price, base_price * 0.7))  # Don't go below 70% of base
            
            fig_price = go.Figure()
            fig_price.add_trace(go.Scatter(
                x=months,
                y=prices,
                mode='lines+markers',
                name='Price Trend',
                line=dict(color='#22c55e', width=4),
                marker=dict(size=12, color='#14532d', line=dict(width=2, color='#ffffff')),
                fill='tonexty',
                fillcolor='rgba(34, 197, 94, 0.2)',
                text=[f"₹{p:.1f}/kg" for p in prices],
                textposition='top center',
                textfont=dict(size=14, color='#1f2937', weight='bold'),
                hovertemplate='<b>%{x}</b><br>Price: ₹%{y:.2f}/kg<extra></extra>'
            ))
            
            # Add average line
            avg_price = sum(prices) / len(prices)
            fig_price.add_hline(
                y=avg_price, 
                line_dash="dash", 
                line_color="#fbbf24",
                annotation_text=f"Average: ₹{avg_price:.2f}/kg",
                annotation_position="right",
                annotation_font_size=14,
                annotation_font_color="#1f2937"
            )
            
            fig_price.update_layout(
                title=dict(
                    text=f'{info.get("displayName", selected_crop_price)} Price Trend (Live)',
                    font=dict(size=24, color='#14532d', weight='bold')
                ),
                xaxis=dict(
                    title=dict(text='Month', font=dict(size=18, color='#14532d', weight='bold')),
                    tickfont=dict(size=16, color='#1f2937', weight='bold'),
                    gridcolor='rgba(34, 197, 94, 0.2)'
                ),
                yaxis=dict(
                    title=dict(text='Price (₹/kg)', font=dict(size=18, color='#14532d', weight='bold')),
                    tickfont=dict(size=16, color='#1f2937'),
                    gridcolor='rgba(34, 197, 94, 0.2)',
                    gridwidth=1
                ),
                paper_bgcolor='rgba(241, 248, 244, 0.95)',
                plot_bgcolor='rgba(255, 255, 255, 0.9)',
                height=450,
                margin=dict(l=60, r=40, t=60, b=60),
                hovermode='x unified'
            )
            
            price_chart_key = f"price_{selected_crop_price}"
            st.plotly_chart(fig_price, use_container_width=True, key=price_chart_key)
            
            # Price statistics
            col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
            with col_stat1:
                st.metric("📊 Current Price", f"₹{prices[-1]:.2f}/kg")
            with col_stat2:
                st.metric("📈 Highest", f"₹{max(prices):.2f}/kg")
            with col_stat3:
                st.metric("📉 Lowest", f"₹{min(prices):.2f}/kg")
            with col_stat4:
                st.metric("📊 Average", f"₹{avg_price:.2f}/kg")
        
        with market_tab2:
            st.markdown("#### 💰 Profitability Analysis (Live Updates)")
            
            # Profitability visualization - updates when yield/cost changes
            fig_profit = go.Figure()
            
            # Revenue bar
            fig_profit.add_trace(go.Bar(
                name='Revenue',
                x=['Financial Breakdown'],
                y=[revenue],
                marker_color='#22c55e',
                marker_line=dict(width=2, color='#1f2937'),
                text=[f"₹{revenue:,.0f}"],
                textposition='outside',
                textfont=dict(size=18, color='#1f2937', weight='bold'),
                hovertemplate='Revenue: ₹%{y:,.0f}<extra></extra>'
            ))
            
            # Cost bar (stacked)
            fig_profit.add_trace(go.Bar(
                name='Cost',
                x=['Financial Breakdown'],
                y=[cost_per_acre],
                marker_color='#ef4444',
                marker_line=dict(width=2, color='#1f2937'),
                text=[f"₹{cost_per_acre:,.0f}"],
                textposition='inside',
                textfont=dict(size=16, color='#ffffff', weight='bold'),
                hovertemplate='Cost: ₹%{y:,.0f}<extra></extra>'
            ))
            
            # Profit line
            if profit > 0:
                fig_profit.add_trace(go.Scatter(
                    x=['Financial Breakdown'],
                    y=[profit],
                    mode='markers+text',
                    name='Profit',
                    marker=dict(size=20, color='#22c55e', symbol='star'),
                    text=[f"Profit: ₹{profit:,.0f}"],
                    textposition='top center',
                    textfont=dict(size=16, color='#22c55e', weight='bold'),
                    hovertemplate='Profit: ₹%{y:,.0f}<extra></extra>'
                ))
            
            fig_profit.update_layout(
                title=dict(
                    text='Revenue vs Cost Analysis (Live)',
                    font=dict(size=24, color='#14532d', weight='bold')
                ),
                barmode='overlay',
                height=400,
                paper_bgcolor='rgba(241, 248, 244, 0.95)',
                plot_bgcolor='rgba(255, 255, 255, 0.9)',
                xaxis=dict(
                    tickfont=dict(size=16, weight='bold'),
                    showticklabels=False
                ),
                yaxis=dict(
                    title=dict(text='Amount (₹)', font=dict(size=18, color='#14532d', weight='bold')),
                    tickfont=dict(size=14, color='#1f2937'),
                    gridcolor='rgba(34, 197, 94, 0.2)'
                ),
                legend=dict(font=dict(size=14)),
                margin=dict(l=60, r=40, t=60, b=60)
            )
            
            profit_chart_key = f"profit_{expected_yield}_{cost_per_acre}_{selected_crop_price}"
            st.plotly_chart(fig_profit, use_container_width=True, key=profit_chart_key)
            
            # Profitability insights
            st.markdown("#### 💡 Profitability Insights")
            
            insights = []
            if profit > 0:
                insights.append(f"✅ **Profitable:** You can expect a profit of ₹{profit:,.0f} per acre")
                insights.append(f"📈 **ROI:** {roi:.1f}% return on investment")
                if profit_margin > 50:
                    insights.append("🌟 **Excellent Margin:** Profit margin above 50% indicates strong profitability")
                elif profit_margin > 30:
                    insights.append("👍 **Good Margin:** Profit margin between 30-50% is healthy")
            else:
                insights.append(f"⚠️ **Not Profitable:** Current setup results in a loss of ₹{abs(profit):,.0f}")
                insights.append(f"💡 **Suggestion:** Increase yield to at least {break_even_yield:.0f} kg/acre to break even")
                insights.append("📊 **Tip:** Consider reducing costs or finding better market prices")
            
            if expected_yield < break_even_yield:
                insights.append(f"⚖️ **Break-Even:** You need {break_even_yield:.0f} kg/acre to cover costs")
            
            for insight in insights:
                st.info(insight)
        
        with market_tab3:
            st.markdown("#### 📉 Cost Breakdown Analysis")
            
            # Cost breakdown pie chart
            if 'seed_cost' in locals():
                cost_breakdown = {
                    'Seeds': seed_cost,
                    'Fertilizers': fertilizer_cost,
                    'Labor': labor_cost,
                    'Irrigation': irrigation_cost
                }
            else:
                # Default breakdown
                cost_breakdown = {
                    'Seeds': cost_per_acre * 0.2,
                    'Fertilizers': cost_per_acre * 0.3,
                    'Labor': cost_per_acre * 0.3,
                    'Irrigation': cost_per_acre * 0.2
                }
            
            fig_cost = go.Figure(data=[go.Pie(
                labels=list(cost_breakdown.keys()),
                values=list(cost_breakdown.values()),
                hole=0.4,
                marker=dict(colors=['#22c55e', '#3b82f6', '#fbbf24', '#ef4444']),
                textinfo='label+percent+value',
                texttemplate='%{label}<br>₹%{value:,.0f}<br>(%{percent})',
                textfont=dict(size=16, color='#1f2937', weight='bold'),
                hovertemplate='<b>%{label}</b><br>Amount: ₹%{value:,.0f}<br>Percentage: %{percent}<extra></extra>'
            )])
            
            fig_cost.update_layout(
                title=dict(
                    text='Cost Breakdown per Acre (Live)',
                    font=dict(size=24, color='#14532d', weight='bold')
                ),
                height=450,
                paper_bgcolor='rgba(241, 248, 244, 0.95)',
                plot_bgcolor='rgba(255, 255, 255, 0.9)',
                legend=dict(
                    font=dict(size=16, color='#1f2937'),
                    bgcolor='rgba(255, 255, 255, 0.8)',
                    bordercolor='rgba(34, 197, 94, 0.3)',
                    borderwidth=2
                ),
                margin=dict(l=40, r=40, t=60, b=40)
            )
            
            cost_chart_key = f"cost_{cost_per_acre}_{selected_crop_price}"
            st.plotly_chart(fig_cost, use_container_width=True, key=cost_chart_key)
            
            # Cost breakdown table
            st.markdown("#### 💰 Detailed Cost Breakdown")
            cost_df = pd.DataFrame({
                'Category': list(cost_breakdown.keys()),
                'Amount (₹)': [f"{v:,.0f}" for v in cost_breakdown.values()],
                'Percentage': [f"{(v/cost_per_acre*100):.1f}%" for v in cost_breakdown.values()]
            })
            st.dataframe(cost_df, use_container_width=True, hide_index=True)
        
        # Market comparison with other crops
        st.markdown("### 🔄 Price Comparison with Other Crops")
        
        # Get prices for all crops
        all_crop_prices = []
        for crop_key, crop_data in market_prices.items():
            crop_info_data = CROP_INFO.get(crop_key, {})
            all_crop_prices.append({
                'Crop': crop_info_data.get('displayName', crop_key),
                'Price (₹/kg)': crop_data.get('price_per_kg', 0),
                'Demand': crop_data.get('demand', 'N/A'),
                'Emoji': crop_info_data.get('emoji', '🌱')
            })
        
        # Sort by price
        all_crop_prices.sort(key=lambda x: x['Price (₹/kg)'], reverse=True)
        
        # Create comparison chart
        fig_compare_prices = go.Figure()
        fig_compare_prices.add_trace(go.Bar(
            x=[item['Crop'] for item in all_crop_prices],
            y=[item['Price (₹/kg)'] for item in all_crop_prices],
            marker=dict(
                color=['#22c55e' if item['Crop'] == info.get('displayName', selected_crop_price) else '#86efac' for item in all_crop_prices],
                line=dict(width=2, color='#1f2937')
            ),
            text=[f"₹{item['Price (₹/kg)']}/kg" for item in all_crop_prices],
            textposition='outside',
            textfont=dict(size=14, color='#1f2937', weight='bold'),
            hovertemplate='<b>%{x}</b><br>Price: ₹%{y}/kg<extra></extra>'
        ))
        
        fig_compare_prices.update_layout(
            title=dict(
                text='Market Price Comparison Across All Crops',
                font=dict(size=24, color='#14532d', weight='bold')
            ),
            height=500,
            paper_bgcolor='rgba(241, 248, 244, 0.95)',
            plot_bgcolor='rgba(255, 255, 255, 0.9)',
            xaxis=dict(
                tickfont=dict(size=14, color='#1f2937', weight='bold'),
                title=dict(text='Crop', font=dict(size=18, color='#14532d', weight='bold'))
            ),
            yaxis=dict(
                tickfont=dict(size=14, color='#1f2937'),
                title=dict(text='Price (₹/kg)', font=dict(size=18, color='#14532d', weight='bold')),
                gridcolor='rgba(34, 197, 94, 0.2)'
            ),
            margin=dict(l=60, r=40, t=60, b=100),
            showlegend=False
        )
        
        st.plotly_chart(fig_compare_prices, use_container_width=True)
        
        # Market insights
        st.markdown("### 💡 Market Insights & Recommendations")
        
        col_insight1, col_insight2 = st.columns(2)
        
        with col_insight1:
            st.markdown("""
            <div class="modern-card">
                <h4 style="color: #14532d; margin-bottom: 15px;">📊 Market Analysis</h4>
                <ul style="color: #4b5563; line-height: 1.8; font-size: 1.05rem;">
                    <li><strong>Current Price:</strong> ₹{:.2f}/kg is {} the market average</li>
                    <li><strong>Demand Level:</strong> {} demand indicates {} market conditions</li>
                    <li><strong>Price Trend:</strong> {} trend suggests {} prices in near future</li>
                    <li><strong>Best Time:</strong> Consider {} season for optimal pricing</li>
                </ul>
            </div>
            """.format(
                price_info.get('price_per_kg', 0),
                "above" if price_info.get('price_per_kg', 0) > avg_price else "below",
                price_info.get('demand', 'N/A'),
                "favorable" if price_info.get('demand') == "High" else "moderate",
                price_info.get('trend', '→'),
                "increasing" if price_info.get('trend') == "↑" else "stable" if price_info.get('trend') == "→" else "decreasing",
                "harvest"
            ), unsafe_allow_html=True)
        
        with col_insight2:
            st.markdown("""
            <div class="modern-card">
                <h4 style="color: #14532d; margin-bottom: 15px;">💡 Profitability Tips</h4>
                <ul style="color: #4b5563; line-height: 1.8; font-size: 1.05rem;">
                    <li><strong>Yield Optimization:</strong> Aim for at least {} kg/acre for profitability</li>
                    <li><strong>Cost Management:</strong> Keep costs below ₹{:.0f}/acre for better margins</li>
                    <li><strong>Market Timing:</strong> {} demand suggests good market conditions</li>
                    <li><strong>Risk Management:</strong> Consider crop insurance for price volatility</li>
                </ul>
            </div>
            """.format(
                int(break_even_yield * 1.2),
                revenue * 0.6 if revenue > 0 else 50000,
                price_info.get('demand', 'N/A')
            ), unsafe_allow_html=True)

# ===========================================
# TAB 6: WEATHER INSIGHTS
# ===========================================
with tab6:
    st.markdown('<h2 class="section-header">🌤️ Weather Insights</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="modern-card">
        <p>Get weather-based recommendations and climate alerts for your region.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_weather1, col_weather2 = st.columns(2)
    
    with col_weather1:
        location = st.text_input("📍 Location", value="Enter your location")
        current_temp = st.number_input("🌡️ Current Temperature (°C)", min_value=-10.0, max_value=50.0, value=25.0)
        current_humidity = st.number_input("💧 Current Humidity (%)", min_value=0.0, max_value=100.0, value=70.0)
        current_rainfall = st.number_input("🌧️ Recent Rainfall (mm)", min_value=0.0, max_value=500.0, value=50.0)
    
    with col_weather2:
        st.markdown("### 🌦️ Weather Alerts")
        
        alerts = []
        if current_temp > 35:
            alerts.append("⚠️ **High Temperature Alert:** Consider heat-tolerant crops")
        if current_humidity < 30:
            alerts.append("⚠️ **Low Humidity Alert:** Drought conditions detected")
        if current_rainfall > 200:
            alerts.append("⚠️ **Heavy Rainfall Alert:** Ensure proper drainage")
        if current_temp < 10:
            alerts.append("⚠️ **Cold Weather Alert:** Consider cold-season crops")
        
        if alerts:
            for alert in alerts:
                st.warning(alert)
        else:
            st.success("✅ Weather conditions are favorable for most crops")
        
        st.markdown("### 📊 Weather Summary")
        weather_summary = {
            "Temperature": f"{current_temp}°C",
            "Humidity": f"{current_humidity}%",
            "Rainfall": f"{current_rainfall}mm"
        }
        for key, value in weather_summary.items():
            st.metric(key, value)
    
    # Weather-based crop recommendations
    st.markdown("### 🌾 Weather-Based Recommendations")
    
    weather_suitable_crops = []
    for crop, info in CROP_INFO.items():
        ideal = info.get("idealConditions", {})
        temp_range = ideal.get("temperature", {})
        if temp_range and temp_range.get("min", 0) <= current_temp <= temp_range.get("max", 100):
            weather_suitable_crops.append(crop)
    
    if weather_suitable_crops:
        cols = st.columns(min(4, len(weather_suitable_crops)))
        for idx, crop in enumerate(weather_suitable_crops[:8]):
            with cols[idx % 4]:
                info = CROP_INFO.get(crop, {})
                st.markdown(f"""
                <div class="stat-card" style="text-align: center;">
                    <div style="font-size: 2.5rem;">{info.get('emoji', '🌱')}</div>
                    <div style="font-weight: 600; color: #14532d;">{info.get('displayName', crop)}</div>
                </div>
                """, unsafe_allow_html=True)

# ===========================================
# TAB 7: ADVANCED ANALYTICS
# ===========================================
with tab7:
    st.markdown('<h2 class="section-header">📈 Advanced Analytics Dashboard</h2>', unsafe_allow_html=True)
    
    # Initialize session state for analytics
    if 'prediction_history' not in st.session_state:
        st.session_state.prediction_history = []
    
    if st.session_state.prediction_history:
        st.markdown("### 📊 Prediction History Analytics")
        
        history_df = pd.DataFrame(st.session_state.prediction_history)
        
        col_anal1, col_anal2, col_anal3 = st.columns(3)
        
        with col_anal1:
            st.metric("Total Predictions", len(history_df))
        
        with col_anal2:
            unique_crops = history_df['crop'].nunique()
            st.metric("Unique Crops", unique_crops)
        
        with col_anal3:
            most_common = history_df['crop'].mode()[0] if not history_df.empty else "N/A"
            st.metric("Most Recommended", most_common)
        
        # Crop frequency chart
        st.markdown("### 📊 Crop Recommendation Frequency")
        crop_counts = history_df['crop'].value_counts()
        
        fig_freq = px.bar(
            x=crop_counts.index,
            y=crop_counts.values,
            title="Crop Recommendations Over Time",
            labels={"x": "Crop", "y": "Count"},
            color=crop_counts.values,
            color_continuous_scale="Greens"
        )
        fig_freq.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=400
        )
        st.plotly_chart(fig_freq, use_container_width=True)
        
        # Input parameter trends
        st.markdown("### 📈 Input Parameter Trends")
        if not history_df.empty:
            avg_n = history_df['inputs'].apply(lambda x: x.get('N', 0)).mean()
            avg_p = history_df['inputs'].apply(lambda x: x.get('P', 0)).mean()
            avg_k = history_df['inputs'].apply(lambda x: x.get('K', 0)).mean()
            avg_temp = history_df['inputs'].apply(lambda x: x.get('temperature', 0)).mean()
            
            col_nut1, col_nut2, col_nut3, col_nut4 = st.columns(4)
            with col_nut1:
                st.metric("Avg Nitrogen", f"{avg_n:.1f} ppm")
            with col_nut2:
                st.metric("Avg Phosphorus", f"{avg_p:.1f} ppm")
            with col_nut3:
                st.metric("Avg Potassium", f"{avg_k:.1f} ppm")
            with col_nut4:
                st.metric("Avg Temperature", f"{avg_temp:.1f}°C")
        
        # History table
        st.markdown("### 📋 Recent Predictions")
        display_history = history_df[['timestamp', 'crop', 'inputs']].head(10).copy()
        display_history['inputs'] = display_history['inputs'].apply(lambda x: f"N:{x.get('N',0)}, P:{x.get('P',0)}, K:{x.get('K',0)}")
        st.dataframe(display_history, use_container_width=True)
    else:
        st.info("📊 No prediction history yet. Make some predictions to see analytics!")

# ===========================================
# TAB 8: SOIL HEALTH DASHBOARD
# ===========================================
with tab8:
    st.markdown('<h2 class="section-header">🌍 Soil Health Dashboard</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="modern-card">
        <p>Analyze your soil health and get recommendations for improvement.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_soil1, col_soil2 = st.columns(2)
    
    with col_soil1:
        st.markdown("### 🌿 Enter Soil Parameters")
        soil_n = st.number_input("Nitrogen (N) ppm", min_value=0.0, max_value=200.0, value=90.0)
        soil_p = st.number_input("Phosphorus (P) ppm", min_value=0.0, max_value=200.0, value=42.0)
        soil_k = st.number_input("Potassium (K) ppm", min_value=0.0, max_value=250.0, value=43.0)
        soil_ph = st.number_input("Soil pH", min_value=0.0, max_value=14.0, value=6.4)
    
    with col_soil2:
        st.markdown("### 📊 Soil Health Score")
        
        # Calculate soil health score
        n_score = min(100, (soil_n / 100) * 100) if soil_n > 0 else 0
        p_score = min(100, (soil_p / 50) * 100) if soil_p > 0 else 0
        k_score = min(100, (soil_k / 50) * 100) if soil_k > 0 else 0
        ph_score = 100 if 6.0 <= soil_ph <= 7.0 else max(0, 100 - abs(soil_ph - 6.5) * 20)
        
        overall_score = (n_score + p_score + k_score + ph_score) / 4
        
        st.metric("Overall Health Score", f"{overall_score:.1f}/100", 
                 delta="Excellent" if overall_score >= 80 else "Good" if overall_score >= 60 else "Needs Improvement")
        
        # Nutrient levels
        st.markdown("#### Nutrient Levels")
        st.progress(n_score / 100, text=f"Nitrogen: {n_score:.0f}%")
        st.progress(p_score / 100, text=f"Phosphorus: {p_score:.0f}%")
        st.progress(k_score / 100, text=f"Potassium: {k_score:.0f}%")
        st.progress(ph_score / 100, text=f"pH Balance: {ph_score:.0f}%")
    
    # Recommendations
    st.markdown("### 💡 Soil Improvement Recommendations")
    recommendations = []
    
    if n_score < 50:
        recommendations.append("🌿 **Nitrogen:** Add organic compost or nitrogen-rich fertilizers")
    if p_score < 50:
        recommendations.append("🔬 **Phosphorus:** Apply bone meal or rock phosphate")
    if k_score < 50:
        recommendations.append("⚡ **Potassium:** Add potash or wood ash")
    if ph_score < 70:
        if soil_ph < 6.0:
            recommendations.append("🧪 **pH:** Add lime to increase pH (reduce acidity)")
        else:
            recommendations.append("🧪 **pH:** Add sulfur to decrease pH (reduce alkalinity)")
    
    if recommendations:
        for rec in recommendations:
            st.info(rec)
    else:
        st.success("✅ Your soil is in excellent condition!")

# ===========================================
# TAB 9: CROP ROTATION PLANNER
# ===========================================
with tab9:
    st.markdown('<h2 class="section-header">🔄 Crop Rotation Planner</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="modern-card">
        <p>Plan a multi-year crop rotation schedule to maintain soil health and maximize yields.</p>
    </div>
    """, unsafe_allow_html=True)
    
    years = st.slider("📅 Rotation Period (Years)", min_value=2, max_value=5, value=3)
    
    # Crop rotation groups
    rotation_groups = {
        "Legumes": ["chickpea", "kidneybeans", "lentil", "mungbean", "blackgram"],
        "Cereals": ["rice", "maize", "wheat"],
        "Fruits": ["mango", "banana", "apple", "orange", "papaya"],
        "Fiber": ["cotton", "jute"]
    }
    
    st.markdown("### 🌾 Select Crops for Rotation")
    
    selected_rotation = []
    for group_name, crops in rotation_groups.items():
        selected = st.multiselect(
            f"{group_name} Crops",
            options=crops,
            format_func=lambda x: CROP_INFO.get(x, {}).get("displayName", x),
            default=crops[:1] if crops else []
        )
        selected_rotation.extend(selected)
    
    if selected_rotation:
        st.markdown("### 📅 Rotation Schedule")
        
        rotation_schedule = []
        for year in range(1, years + 1):
            for season in ["Spring", "Summer", "Fall", "Winter"]:
                # Simple rotation logic
                crop_idx = ((year - 1) * 4 + ["Spring", "Summer", "Fall", "Winter"].index(season)) % len(selected_rotation)
                crop = selected_rotation[crop_idx]
                info = CROP_INFO.get(crop, {})
                rotation_schedule.append({
                    "Year": year,
                    "Season": season,
                    "Crop": info.get("displayName", crop),
                    "Emoji": info.get("emoji", "🌱")
                })
        
        df_rotation = pd.DataFrame(rotation_schedule)
        st.dataframe(df_rotation, use_container_width=True)
        
        # Visual rotation calendar
        st.markdown("### 📊 Rotation Calendar Visualization")
        fig_rotation = go.Figure()
        
        for year in range(1, years + 1):
            year_data = df_rotation[df_rotation['Year'] == year]
            fig_rotation.add_trace(go.Bar(
                name=f"Year {year}",
                x=year_data['Season'],
                y=[1] * len(year_data),
                text=year_data['Crop'],
                textposition='inside',
                marker_color=['#22c55e', '#4ade80', '#86efac', '#bbf7d0'][year % 4]
            ))
        
        fig_rotation.update_layout(
            title="Crop Rotation Schedule",
            barmode='group',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=400
        )
        st.plotly_chart(fig_rotation, use_container_width=True)
        
        st.markdown("### 💡 Rotation Benefits")
        st.info("""
        **Benefits of Crop Rotation:**
        - Prevents soil nutrient depletion
        - Reduces pest and disease buildup
        - Improves soil structure
        - Maintains biodiversity
        - Increases overall yield
        """)

# ===========================================
# TAB 10: SMART IRRIGATION CALCULATOR
# ===========================================
with tab10:
    st.markdown('<h2 class="section-header">💧 Smart Irrigation Calculator</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="modern-card">
        <p>Calculate optimal water requirements, generate irrigation schedules, and analyze water efficiency for your crops.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Input Section
    col_irr1, col_irr2 = st.columns(2)
    
    with col_irr1:
        st.markdown("### 🌾 Crop & Field Information")
        selected_crop_irr = st.selectbox(
            "🌾 Select Crop",
            options=list(CROP_INFO.keys()),
            format_func=lambda x: CROP_INFO.get(x, {}).get("displayName", x),
            key="irr_crop"
        )
        
        field_area = st.number_input(
            "📐 Field Area (acres)",
            min_value=0.1,
            value=1.0,
            step=0.1,
            help="Total area of your field in acres",
            key="irr_area"
        )
        
        soil_type = st.selectbox(
            "🌍 Soil Type",
            options=["Sandy", "Loamy", "Clay", "Sandy Loam", "Clay Loam"],
            key="irr_soil"
        )
        
        current_soil_moisture = st.slider(
            "💧 Current Soil Moisture (%)",
            min_value=0,
            max_value=100,
            value=50,
            help="Current moisture level in your soil",
            key="irr_moisture"
        )
    
    with col_irr2:
        st.markdown("### 🌡️ Climate Conditions")
        avg_temp_irr = st.number_input(
            "🌡️ Average Temperature (°C)",
            min_value=0.0,
            max_value=50.0,
            value=25.0,
            step=0.5,
            key="irr_temp"
        )
        
        avg_humidity_irr = st.number_input(
            "💨 Average Humidity (%)",
            min_value=0.0,
            max_value=100.0,
            value=70.0,
            step=1.0,
            key="irr_humidity"
        )
        
        recent_rainfall_irr = st.number_input(
            "🌧️ Recent Rainfall (mm)",
            min_value=0.0,
            value=0.0,
            step=1.0,
            help="Rainfall in the last 7 days",
            key="irr_rainfall"
        )
        
        evapotranspiration = st.number_input(
            "☀️ Evapotranspiration Rate (mm/day)",
            min_value=0.0,
            value=5.0,
            step=0.1,
            help="Daily water loss through evaporation and transpiration",
            key="irr_et"
        )
    
    if selected_crop_irr:
        crop_info_irr = CROP_INFO.get(selected_crop_irr, {})
        ideal_irr = crop_info_irr.get("idealConditions", {})
        
        # Calculate water requirements
        # Base water requirement varies by crop
        crop_water_needs = {
            "rice": 1200, "maize": 500, "wheat": 450, "cotton": 600,
            "jute": 800, "coconut": 1000, "banana": 1200, "mango": 800,
            "grapes": 600, "watermelon": 400, "muskmelon": 400
        }
        
        base_water_need = crop_water_needs.get(selected_crop_irr, 500)  # mm per season
        
        # Adjust for temperature
        temp_factor = 1 + (avg_temp_irr - 25) * 0.02  # 2% per degree above/below 25°C
        
        # Adjust for humidity
        humidity_factor = 1 - (avg_humidity_irr - 70) * 0.005  # Lower humidity = more water needed
        
        # Adjust for soil type
        soil_factors = {
            "Sandy": 1.3, "Loamy": 1.0, "Clay": 0.8,
            "Sandy Loam": 1.1, "Clay Loam": 0.9
        }
        soil_factor = soil_factors.get(soil_type, 1.0)
        
        # Calculate daily water requirement
        days_in_season = 120  # Average crop season
        daily_water_need = (base_water_need / days_in_season) * temp_factor * humidity_factor * soil_factor
        
        # Account for rainfall
        daily_rainfall = recent_rainfall_irr / 7
        irrigation_needed = max(0, daily_water_need - daily_rainfall)
        
        # Calculate total water needed
        total_water_liters = irrigation_needed * field_area * 4046.86  # Convert acres to sq meters, then to liters
        
        # Water efficiency score
        optimal_moisture = 60  # Optimal soil moisture percentage
        moisture_deviation = abs(current_soil_moisture - optimal_moisture)
        efficiency_score = max(0, 100 - (moisture_deviation * 2))
        
        # Results Section
        st.markdown("### 💧 Irrigation Analysis Results")
        
        col_res1, col_res2, col_res3, col_res4 = st.columns(4)
        
        with col_res1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 100%); 
                        padding: 20px; border-radius: 15px; border: 2px solid rgba(34, 197, 94, 0.4); 
                        text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 10px;">💧</div>
                <h4 style="color: #14532d; margin: 10px 0; font-size: 1.1rem;">Daily Water Need</h4>
                <p style="font-size: 1.8rem; font-weight: bold; color: #22c55e; margin: 0;">{daily_water_need:.1f}</p>
                <p style="color: #6b7280; margin: 5px 0 0 0; font-size: 0.9rem;">mm/day</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_res2:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 100%); 
                        padding: 20px; border-radius: 15px; border: 2px solid rgba(34, 197, 94, 0.4); 
                        text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 10px;">🌧️</div>
                <h4 style="color: #14532d; margin: 10px 0; font-size: 1.1rem;">Irrigation Needed</h4>
                <p style="font-size: 1.8rem; font-weight: bold; color: #3b82f6; margin: 0;">{irrigation_needed:.1f}</p>
                <p style="color: #6b7280; margin: 5px 0 0 0; font-size: 0.9rem;">mm/day</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_res3:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 100%); 
                        padding: 20px; border-radius: 15px; border: 2px solid rgba(34, 197, 94, 0.4); 
                        text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 10px;">📊</div>
                <h4 style="color: #14532d; margin: 10px 0; font-size: 1.1rem;">Total Water</h4>
                <p style="font-size: 1.8rem; font-weight: bold; color: #06b6d4; margin: 0;">{total_water_liters/1000:.1f}</p>
                <p style="color: #6b7280; margin: 5px 0 0 0; font-size: 0.9rem;">Liters/day</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_res4:
            efficiency_color = "#22c55e" if efficiency_score >= 70 else "#fbbf24" if efficiency_score >= 50 else "#ef4444"
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 100%); 
                        padding: 20px; border-radius: 15px; border: 2px solid {efficiency_color}; 
                        text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 10px;">⭐</div>
                <h4 style="color: #14532d; margin: 10px 0; font-size: 1.1rem;">Efficiency Score</h4>
                <p style="font-size: 1.8rem; font-weight: bold; color: {efficiency_color}; margin: 0;">{efficiency_score:.0f}</p>
                <p style="color: #6b7280; margin: 5px 0 0 0; font-size: 0.9rem;">/ 100</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Irrigation Schedule Generator
        st.markdown("### 📅 Irrigation Schedule Generator")
        
        schedule_type = st.radio(
            "Schedule Type",
            options=["Daily", "Weekly", "Custom"],
            horizontal=True,
            key="irr_schedule_type"
        )
        
        if schedule_type == "Daily":
            days = st.slider("Number of Days", 1, 30, 7, key="irr_days")
            schedule_data = []
            for day in range(1, days + 1):
                schedule_data.append({
                    "Day": f"Day {day}",
                    "Water Needed (mm)": round(irrigation_needed, 1),
                    "Water Needed (Liters)": round(total_water_liters, 0),
                    "Time": "Early Morning (6-8 AM)" if day % 2 == 0 else "Evening (6-8 PM)"
                })
            df_schedule = pd.DataFrame(schedule_data)
            st.dataframe(df_schedule, use_container_width=True, hide_index=True)
        
        elif schedule_type == "Weekly":
            weeks = st.slider("Number of Weeks", 1, 12, 4, key="irr_weeks")
            schedule_data = []
            for week in range(1, weeks + 1):
                weekly_water = irrigation_needed * 7
                schedule_data.append({
                    "Week": f"Week {week}",
                    "Total Water (mm)": round(weekly_water, 1),
                    "Total Water (Liters)": round(total_water_liters * 7, 0),
                    "Frequency": "3-4 times per week",
                    "Best Days": "Monday, Wednesday, Friday, Sunday"
                })
            df_schedule = pd.DataFrame(schedule_data)
            st.dataframe(df_schedule, use_container_width=True, hide_index=True)
        
        # Rainfall vs Irrigation Balance
        st.markdown("### ⚖️ Rainfall vs Irrigation Balance")
        
        col_balance1, col_balance2 = st.columns(2)
        
        with col_balance1:
            fig_balance = go.Figure()
            fig_balance.add_trace(go.Bar(
                name='Rainfall',
                x=['Water Sources'],
                y=[daily_rainfall],
                marker_color='#3b82f6',
                marker_line=dict(width=2, color='#1f2937'),
                text=[f"{daily_rainfall:.1f} mm"],
                textposition='outside',
                textfont=dict(size=16, color='#1f2937', weight='bold')
            ))
            fig_balance.add_trace(go.Bar(
                name='Irrigation Needed',
                x=['Water Sources'],
                y=[irrigation_needed],
                marker_color='#22c55e',
                marker_line=dict(width=2, color='#1f2937'),
                text=[f"{irrigation_needed:.1f} mm"],
                textposition='outside',
                textfont=dict(size=16, color='#1f2937', weight='bold')
            ))
            fig_balance.update_layout(
                title=dict(text='Daily Water Balance', font=dict(size=20, color='#14532d', weight='bold')),
                barmode='group',
                height=350,
                paper_bgcolor='rgba(241, 248, 244, 0.95)',
                plot_bgcolor='rgba(255, 255, 255, 0.9)',
                yaxis=dict(title='Water (mm/day)', tickfont=dict(size=14)),
                showlegend=True,
                legend=dict(font=dict(size=14))
            )
            st.plotly_chart(fig_balance, use_container_width=True)
        
        with col_balance2:
            coverage_percent = (daily_rainfall / daily_water_need * 100) if daily_water_need > 0 else 0
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 100%); 
                        padding: 25px; border-radius: 15px; border: 2px solid rgba(34, 197, 94, 0.4);">
                <h4 style="color: #14532d; margin-bottom: 15px;">📊 Water Coverage Analysis</h4>
                <p style="font-size: 1.1rem; color: #4b5563; margin: 10px 0;">
                    <strong>Rainfall Coverage:</strong> {coverage_percent:.1f}%
                </p>
                <p style="font-size: 1.1rem; color: #4b5563; margin: 10px 0;">
                    <strong>Irrigation Required:</strong> {100 - coverage_percent:.1f}%
                </p>
                <div style="margin-top: 20px; padding: 15px; background: rgba(34, 197, 94, 0.1); border-radius: 10px;">
                    <p style="color: #14532d; font-weight: 600; margin: 0;">
                        💡 {'Rainfall is sufficient!' if coverage_percent >= 100 else f'Need {irrigation_needed:.1f}mm/day irrigation'}
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Irrigation System Cost Calculator
        st.markdown("### 💰 Irrigation System Cost Calculator")
        
        col_cost1, col_cost2 = st.columns(2)
        
        with col_cost1:
            irrigation_method = st.selectbox(
                "🚿 Irrigation Method",
                options=["Drip Irrigation", "Sprinkler System", "Flood Irrigation", "Center Pivot"],
                key="irr_method"
            )
            
            system_cost_per_acre = {
                "Drip Irrigation": 50000,
                "Sprinkler System": 40000,
                "Flood Irrigation": 10000,
                "Center Pivot": 80000
            }
            
            initial_cost = system_cost_per_acre.get(irrigation_method, 30000) * field_area
            
            maintenance_cost = st.number_input(
                "🔧 Annual Maintenance Cost (₹)",
                min_value=0.0,
                value=initial_cost * 0.05,
                step=1000.0,
                key="irr_maintenance"
            )
            
            electricity_cost_per_unit = st.number_input(
                "⚡ Electricity Cost (₹/unit)",
                min_value=0.0,
                value=8.0,
                step=0.5,
                key="irr_electricity"
            )
            
            pump_efficiency = st.slider(
                "⚙️ Pump Efficiency (%)",
                min_value=50,
                max_value=100,
                value=75,
                key="irr_pump_eff"
            )
        
        with col_cost2:
            # Calculate operational costs
            # Water pumping cost (assuming 1 kWh per 1000 liters)
            daily_pumping_cost = (total_water_liters / 1000) * electricity_cost_per_unit * (100 / pump_efficiency)
            annual_pumping_cost = daily_pumping_cost * 365
            
            total_annual_cost = maintenance_cost + annual_pumping_cost
            cost_per_liter = total_annual_cost / (total_water_liters * 365) if total_water_liters > 0 else 0
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 100%); 
                        padding: 25px; border-radius: 15px; border: 2px solid rgba(34, 197, 94, 0.4);">
                <h4 style="color: #14532d; margin-bottom: 20px;">💰 Cost Breakdown</h4>
                <div style="margin: 15px 0;">
                    <p style="color: #4b5563; font-size: 1.1rem; margin: 5px 0;">
                        <strong>Initial Setup:</strong> ₹{initial_cost:,.0f}
                    </p>
                    <p style="color: #4b5563; font-size: 1.1rem; margin: 5px 0;">
                        <strong>Annual Maintenance:</strong> ₹{maintenance_cost:,.0f}
                    </p>
                    <p style="color: #4b5563; font-size: 1.1rem; margin: 5px 0;">
                        <strong>Annual Pumping Cost:</strong> ₹{annual_pumping_cost:,.0f}
                    </p>
                    <div style="border-top: 2px solid rgba(34, 197, 94, 0.3); margin: 15px 0; padding-top: 15px;">
                        <p style="color: #14532d; font-size: 1.3rem; font-weight: bold; margin: 0;">
                            <strong>Total Annual Cost:</strong> ₹{total_annual_cost:,.0f}
                        </p>
                        <p style="color: #6b7280; font-size: 1rem; margin: 5px 0 0 0;">
                            Cost per Liter: ₹{cost_per_liter:.4f}
                        </p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Water Efficiency Recommendations
        st.markdown("### 💡 Water Efficiency Recommendations")
        
        recommendations = []
        if efficiency_score < 70:
            recommendations.append("⚠️ **Soil Moisture:** Current moisture is not optimal. Aim for 60-70% for best results.")
        if irrigation_needed > daily_water_need * 0.5:
            recommendations.append("💧 **High Water Need:** Consider mulching to reduce evaporation and water loss.")
        if soil_type == "Sandy":
            recommendations.append("🌍 **Sandy Soil:** Sandy soil requires more frequent, smaller irrigation sessions.")
        if avg_temp_irr > 30:
            recommendations.append("🌡️ **High Temperature:** Increase irrigation frequency during hot weather.")
        if coverage_percent < 50:
            recommendations.append("🌧️ **Low Rainfall:** Rainfall is insufficient. Regular irrigation is essential.")
        
        if not recommendations:
            recommendations.append("✅ **Optimal Conditions:** Your irrigation setup looks good! Maintain current practices.")
        
        for rec in recommendations:
            st.info(rec)

# ===========================================
# TAB 11: DISEASE & PEST DETECTION
# ===========================================
with tab11:
    st.markdown('<h2 class="section-header">🦠 Disease & Pest Detection</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="modern-card">
        <p>Identify crop diseases and pests, assess risks, and get prevention and treatment recommendations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Disease Detection Section
    st.markdown("### 🔍 Disease Identification")
    
    col_disease1, col_disease2 = st.columns(2)
    
    with col_disease1:
        crop_for_disease = st.selectbox(
            "🌾 Select Crop",
            options=list(CROP_INFO.keys()),
            format_func=lambda x: CROP_INFO.get(x, {}).get("displayName", x),
            key="disease_crop"
        )
        
        symptoms = st.multiselect(
            "🩺 Select Symptoms (Select all that apply)",
            options=[
                "Yellowing Leaves", "Brown Spots", "Wilting", "Stunted Growth",
                "Leaf Curling", "White Powdery Coating", "Black Spots", "Root Rot",
                "Fruit Rot", "Leaf Blight", "Mosaic Patterns", "Necrosis"
            ],
            key="disease_symptoms"
        )
        
        affected_area = st.selectbox(
            "📍 Affected Area",
            options=["Leaves", "Stems", "Roots", "Fruits", "Flowers", "Entire Plant"],
            key="disease_area"
        )
    
    with col_disease2:
        region_disease = st.selectbox(
            "🌍 Region",
            options=["Tropical", "Subtropical", "Temperate", "Cold", "Arid"],
            key="disease_region"
        )
        
        season_disease = st.selectbox(
            "📅 Current Season",
            options=["Spring", "Summer", "Fall", "Winter", "Monsoon"],
            key="disease_season"
        )
        
        severity = st.slider(
            "⚠️ Severity Level",
            min_value=1,
            max_value=5,
            value=3,
            help="1 = Mild, 5 = Severe",
            key="disease_severity"
        )
    
    # Disease Database
    disease_database = {
        "rice": {
            "Blast": {"symptoms": ["Brown Spots", "Leaf Blight"], "area": "Leaves", "season": "Monsoon"},
            "Bacterial Blight": {"symptoms": ["Yellowing Leaves", "Wilting"], "area": "Leaves", "season": "Monsoon"},
            "Sheath Blight": {"symptoms": ["Brown Spots", "Stunted Growth"], "area": "Stems", "season": "Summer"}
        },
        "maize": {
            "Corn Smut": {"symptoms": ["Black Spots", "Fruit Rot"], "area": "Fruits", "season": "Summer"},
            "Northern Leaf Blight": {"symptoms": ["Brown Spots", "Leaf Blight"], "area": "Leaves", "season": "Summer"},
            "Root Rot": {"symptoms": ["Root Rot", "Wilting"], "area": "Roots", "season": "Monsoon"}
        },
        "wheat": {
            "Rust": {"symptoms": ["Brown Spots", "Yellowing Leaves"], "area": "Leaves", "season": "Spring"},
            "Powdery Mildew": {"symptoms": ["White Powdery Coating", "Leaf Curling"], "area": "Leaves", "season": "Spring"},
            "Fusarium": {"symptoms": ["Root Rot", "Wilting"], "area": "Roots", "season": "Fall"}
        }
    }
    
    # Initialize possible_diseases to avoid NameError
    possible_diseases = []
    
    if symptoms and crop_for_disease:
        # Match diseases
        crop_diseases = disease_database.get(crop_for_disease, {})
        
        for disease_name, disease_info in crop_diseases.items():
            match_score = 0
            if any(symptom in disease_info.get("symptoms", []) for symptom in symptoms):
                match_score += 2
            if disease_info.get("area") == affected_area:
                match_score += 1
            if disease_info.get("season") == season_disease:
                match_score += 1
            
            if match_score > 0:
                possible_diseases.append((disease_name, match_score))
        
        possible_diseases.sort(key=lambda x: x[1], reverse=True)
        
        if possible_diseases:
            st.markdown("### 🎯 Possible Disease Matches")
            
            for idx, (disease, score) in enumerate(possible_diseases[:3]):
                confidence = min(100, (score / 4) * 100)
                confidence_color = "#22c55e" if confidence >= 70 else "#fbbf24" if confidence >= 50 else "#ef4444"
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 100%); 
                            padding: 20px; border-radius: 15px; border: 2px solid {confidence_color}; 
                            margin-bottom: 15px;">
                    <h4 style="color: #14532d; margin: 0 0 10px 0;">{disease}</h4>
                    <p style="color: #4b5563; margin: 5px 0;">
                        <strong>Confidence:</strong> <span style="color: {confidence_color}; font-weight: bold;">{confidence:.0f}%</span>
                    </p>
                    <p style="color: #4b5563; margin: 5px 0;">
                        <strong>Common Symptoms:</strong> {', '.join(disease_database.get(crop_for_disease, {}).get(disease, {}).get('symptoms', []))}
                    </p>
                </div>
                """, unsafe_allow_html=True)
    
    # Pest Risk Assessment
    st.markdown("### 🐛 Pest Risk Assessment")
    
    col_pest1, col_pest2 = st.columns(2)
    
    with col_pest1:
        pest_crop = st.selectbox(
            "🌾 Crop for Pest Assessment",
            options=list(CROP_INFO.keys()),
            format_func=lambda x: CROP_INFO.get(x, {}).get("displayName", x),
            key="pest_crop"
        )
        
        pest_region = st.selectbox(
            "🌍 Region",
            options=["Tropical", "Subtropical", "Temperate", "Cold", "Arid"],
            key="pest_region"
        )
        
        pest_season = st.selectbox(
            "📅 Season",
            options=["Spring", "Summer", "Fall", "Winter", "Monsoon"],
            key="pest_season"
        )
    
    with col_pest2:
        # Pest database
        pest_risks = {
            "rice": {"Aphids": 0.7, "Stem Borer": 0.8, "Leaf Folder": 0.6},
            "maize": {"Corn Earworm": 0.7, "Fall Armyworm": 0.8, "Aphids": 0.5},
            "wheat": {"Aphids": 0.6, "Rust Mite": 0.5, "Armyworm": 0.4}
        }
        
        crop_pests = pest_risks.get(pest_crop, {})
        
        # Adjust risk based on season
        season_factors = {
            "Spring": 1.2, "Summer": 1.5, "Fall": 1.0, "Winter": 0.7, "Monsoon": 1.3
        }
        season_factor = season_factors.get(pest_season, 1.0)
        
        st.markdown("### 📊 Pest Risk Levels")
        
        for pest_name, base_risk in crop_pests.items():
            adjusted_risk = min(1.0, base_risk * season_factor)
            risk_percent = adjusted_risk * 100
            risk_color = "#ef4444" if risk_percent >= 70 else "#fbbf24" if risk_percent >= 40 else "#22c55e"
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 100%); 
                        padding: 15px; border-radius: 12px; border: 2px solid {risk_color}; 
                        margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: #14532d; font-weight: 600; font-size: 1.1rem;">🐛 {pest_name}</span>
                    <span style="color: {risk_color}; font-weight: bold; font-size: 1.2rem;">{risk_percent:.0f}%</span>
                </div>
                <div style="margin-top: 8px; height: 8px; background: rgba(34, 197, 94, 0.2); border-radius: 4px; overflow: hidden;">
                    <div style="height: 100%; width: {risk_percent}%; background: {risk_color}; transition: width 0.5s;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Prevention & Treatment Recommendations
    st.markdown("### 💡 Prevention & Treatment Recommendations")
    
    prevention_tips = {
        "rice": [
            "Use disease-resistant varieties",
            "Maintain proper water management",
            "Apply fungicides during monsoon",
            "Practice crop rotation",
            "Remove infected plant parts immediately"
        ],
        "maize": [
            "Plant early to avoid peak pest season",
            "Use Bt maize varieties for pest resistance",
            "Apply neem-based pesticides",
            "Maintain field hygiene",
            "Monitor regularly for early detection"
        ],
        "wheat": [
            "Use certified disease-free seeds",
            "Apply preventive fungicides",
            "Maintain proper spacing",
            "Avoid excessive nitrogen",
            "Practice crop rotation with legumes"
        ]
    }
    
    treatment_options = {
        "Blast": "Apply Tricyclazole or Propiconazole fungicides",
        "Bacterial Blight": "Use Copper-based bactericides",
        "Powdery Mildew": "Apply Sulfur or Potassium bicarbonate",
        "Aphids": "Use Neem oil or Insecticidal soap",
        "Stem Borer": "Apply Chlorantraniliprole or Emamectin benzoate"
    }
    
    col_prev1, col_prev2 = st.columns(2)
    
    with col_prev1:
        st.markdown("#### 🛡️ Prevention Tips")
        tips = prevention_tips.get(crop_for_disease if crop_for_disease else pest_crop, prevention_tips.get("rice", []))
        for tip in tips:
            st.markdown(f"✅ {tip}")
    
    with col_prev2:
        st.markdown("#### 💊 Treatment Options")
        if possible_diseases:
            top_disease = possible_diseases[0][0]
            treatment = treatment_options.get(top_disease, "Consult local agricultural extension officer for specific treatment")
            st.info(f"**For {top_disease}:** {treatment}")
        else:
            st.info("Select symptoms above to get specific treatment recommendations")
    
    # IPM Suggestions
    st.markdown("### 🌿 Integrated Pest Management (IPM) Suggestions")
    
    ipm_strategies = [
        "**Biological Control:** Introduce beneficial insects like ladybugs and lacewings",
        "**Cultural Practices:** Practice crop rotation and intercropping",
        "**Mechanical Control:** Use traps and barriers",
        "**Chemical Control:** Use pesticides as last resort, prefer organic options",
        "**Monitoring:** Regular field inspections and early detection"
    ]
    
    for strategy in ipm_strategies:
        st.markdown(f"- {strategy}")

# ===========================================
# TAB 12: YIELD PREDICTION & OPTIMIZATION
# ===========================================
with tab12:
    st.markdown('<h2 class="section-header">📊 Yield Prediction & Optimization</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="modern-card">
        <p>Get AI-powered yield predictions, compare crops, and receive optimization suggestions to maximize your harvest.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Input Section
    col_yield1, col_yield2 = st.columns(2)
    
    with col_yield1:
        st.markdown("### 🌾 Crop & Field Setup")
        yield_crop = st.selectbox(
            "🌾 Select Crop",
            options=list(CROP_INFO.keys()),
            format_func=lambda x: CROP_INFO.get(x, {}).get("displayName", x),
            key="yield_crop"
        )
        
        yield_area = st.number_input(
            "📐 Field Area (acres)",
            min_value=0.1,
            value=1.0,
            step=0.1,
            key="yield_area"
        )
        
        # Get current soil/climate from session or use defaults
        yield_N = st.number_input("🌿 Nitrogen (N) ppm", min_value=0.0, max_value=200.0, value=90.0, step=1.0, key="yield_N")
        yield_P = st.number_input("🔬 Phosphorus (P) ppm", min_value=0.0, max_value=200.0, value=42.0, step=1.0, key="yield_P")
        yield_K = st.number_input("⚡ Potassium (K) ppm", min_value=0.0, max_value=250.0, value=43.0, step=1.0, key="yield_K")
    
    with col_yield2:
        st.markdown("### 🌡️ Climate Conditions")
        yield_temp = st.number_input("🌡️ Temperature (°C)", min_value=0.0, max_value=60.0, value=24.0, step=0.5, key="yield_temp")
        yield_humidity = st.number_input("💧 Humidity (%)", min_value=0.0, max_value=100.0, value=82.0, step=1.0, key="yield_humidity")
        yield_ph = st.number_input("🧪 Soil pH", min_value=0.0, max_value=14.0, value=6.4, step=0.1, key="yield_ph")
        yield_rainfall = st.number_input("🌧️ Rainfall (mm)", min_value=0.0, max_value=300.0, value=120.0, step=1.0, key="yield_rainfall")
    
    if yield_crop:
        # Yield prediction based on crop and conditions
        # Base yields (kg/acre) for optimal conditions
        base_yields = {
            "rice": 4000, "maize": 3500, "wheat": 3000, "cotton": 800,
            "jute": 2000, "coconut": 12000, "banana": 20000, "mango": 8000,
            "grapes": 5000, "watermelon": 15000, "muskmelon": 12000
        }
        
        base_yield = base_yields.get(yield_crop, 2000)
        
        # Calculate yield factors
        # Nutrient factor (optimal NPK = 1.0)
        optimal_N = 100
        optimal_P = 50
        optimal_K = 100
        
        N_factor = 1.0 - abs(yield_N - optimal_N) / optimal_N * 0.3
        P_factor = 1.0 - abs(yield_P - optimal_P) / optimal_P * 0.3
        K_factor = 1.0 - abs(yield_K - optimal_K) / optimal_K * 0.3
        nutrient_factor = (N_factor + P_factor + K_factor) / 3
        
        # Climate factors
        crop_info_yield = CROP_INFO.get(yield_crop, {})
        ideal_yield = crop_info_yield.get("idealConditions", {})
        temp_range = ideal_yield.get("temperature", {})
        
        if temp_range:
            optimal_temp = (temp_range.get("min", 20) + temp_range.get("max", 30)) / 2
            temp_factor = 1.0 - abs(yield_temp - optimal_temp) / optimal_temp * 0.2
        
        ph_range = ideal_yield.get("ph", {})
        if ph_range:
            optimal_ph = (ph_range.get("min", 6) + ph_range.get("max", 7)) / 2
            ph_factor = 1.0 - abs(yield_ph - optimal_ph) / optimal_ph * 0.15
        
        # Rainfall factor
        rain_range = ideal_yield.get("rainfall", {})
        if rain_range:
            optimal_rain = (rain_range.get("min", 100) + rain_range.get("max", 200)) / 2
            rain_factor = 1.0 - abs(yield_rainfall - optimal_rain) / optimal_rain * 0.2
        
        # Calculate predicted yield
        predicted_yield = base_yield * nutrient_factor * temp_factor * ph_factor * rain_factor
        total_yield = predicted_yield * yield_area
        
        # Results
        st.markdown("### 📊 Yield Prediction Results")
        
        col_yres1, col_yres2, col_yres3 = st.columns(3)
        
        with col_yres1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 100%); 
                        padding: 25px; border-radius: 15px; border: 2px solid rgba(34, 197, 94, 0.4); 
                        text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 10px;">📈</div>
                <h4 style="color: #14532d; margin: 10px 0; font-size: 1.2rem;">Predicted Yield</h4>
                <p style="font-size: 2.5rem; font-weight: bold; color: #22c55e; margin: 0;">{predicted_yield:,.0f}</p>
                <p style="color: #6b7280; margin: 5px 0 0 0; font-size: 1rem;">kg/acre</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_yres2:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 100%); 
                        padding: 25px; border-radius: 15px; border: 2px solid rgba(34, 197, 94, 0.4); 
                        text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 10px;">🌾</div>
                <h4 style="color: #14532d; margin: 10px 0; font-size: 1.2rem;">Total Yield</h4>
                <p style="font-size: 2.5rem; font-weight: bold; color: #22c55e; margin: 0;">{total_yield:,.0f}</p>
                <p style="color: #6b7280; margin: 5px 0 0 0; font-size: 1rem;">kg ({yield_area} acres)</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_yres3:
            yield_score = (nutrient_factor + temp_factor + ph_factor + rain_factor) / 4 * 100
            score_color = "#22c55e" if yield_score >= 80 else "#fbbf24" if yield_score >= 60 else "#ef4444"
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 100%); 
                        padding: 25px; border-radius: 15px; border: 2px solid {score_color}; 
                        text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 10px;">⭐</div>
                <h4 style="color: #14532d; margin: 10px 0; font-size: 1.2rem;">Yield Potential</h4>
                <p style="font-size: 2.5rem; font-weight: bold; color: {score_color}; margin: 0;">{yield_score:.0f}%</p>
                <p style="color: #6b7280; margin: 5px 0 0 0; font-size: 1rem;">of optimal</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Yield Comparison
        st.markdown("### 🔄 Yield Comparison Across Crops")
        
        comparison_crops = st.multiselect(
            "🌾 Select Crops to Compare",
            options=list(CROP_INFO.keys()),
            default=[yield_crop] if yield_crop else [],
            format_func=lambda x: CROP_INFO.get(x, {}).get("displayName", x),
            key="yield_compare"
        )
        
        if comparison_crops:
            comparison_data = []
            for comp_crop in comparison_crops:
                comp_base = base_yields.get(comp_crop, 2000)
                comp_yield = comp_base * nutrient_factor * temp_factor * ph_factor * rain_factor
                comparison_data.append({
                    "Crop": CROP_INFO.get(comp_crop, {}).get("displayName", comp_crop),
                    "Predicted Yield (kg/acre)": round(comp_yield, 0),
                    "Total Yield (kg)": round(comp_yield * yield_area, 0)
                })
            
            df_yield_compare = pd.DataFrame(comparison_data)
            st.dataframe(df_yield_compare, use_container_width=True, hide_index=True)
            
            # Visual comparison
            fig_yield_compare = go.Figure()
            fig_yield_compare.add_trace(go.Bar(
                x=[CROP_INFO.get(c, {}).get("displayName", c) for c in comparison_crops],
                y=[comp_yield for comp_yield in [base_yields.get(c, 2000) * nutrient_factor * temp_factor * ph_factor * rain_factor for c in comparison_crops]],
                marker_color='#22c55e',
                marker_line=dict(width=2, color='#1f2937'),
                text=[f"{y:.0f} kg/acre" for y in [base_yields.get(c, 2000) * nutrient_factor * temp_factor * ph_factor * rain_factor for c in comparison_crops]],
                textposition='outside',
                textfont=dict(size=16, color='#1f2937', weight='bold')
            ))
            fig_yield_compare.update_layout(
                title=dict(text='Yield Comparison', font=dict(size=22, color='#14532d', weight='bold')),
                height=400,
                paper_bgcolor='rgba(241, 248, 244, 0.95)',
                plot_bgcolor='rgba(255, 255, 255, 0.9)',
                xaxis=dict(tickfont=dict(size=14, weight='bold')),
                yaxis=dict(title='Yield (kg/acre)', tickfont=dict(size=14))
            )
            st.plotly_chart(fig_yield_compare, use_container_width=True)
        
        # Optimization Suggestions
        st.markdown("### 💡 Yield Optimization Suggestions")
        
        optimizations = []
        if N_factor < 0.9:
            optimizations.append(f"🌿 **Nitrogen:** Current {yield_N:.0f} ppm. Optimal range: 80-120 ppm. Add nitrogen fertilizer to improve yield by ~{(1-N_factor)*100:.0f}%")
        if P_factor < 0.9:
            optimizations.append(f"🔬 **Phosphorus:** Current {yield_P:.0f} ppm. Optimal range: 40-60 ppm. Add phosphorus fertilizer to improve yield by ~{(1-P_factor)*100:.0f}%")
        if K_factor < 0.9:
            optimizations.append(f"⚡ **Potassium:** Current {yield_K:.0f} ppm. Optimal range: 80-120 ppm. Add potassium fertilizer to improve yield by ~{(1-K_factor)*100:.0f}%")
        if temp_factor < 0.9:
            optimizations.append(f"🌡️ **Temperature:** Current {yield_temp:.1f}°C. Optimal: {optimal_temp:.1f}°C. Consider adjusting planting time or using shade/cover.")
        if ph_factor < 0.9:
            optimizations.append(f"🧪 **pH:** Current {yield_ph:.1f}. Optimal: {optimal_ph:.1f}. Add lime (raise pH) or sulfur (lower pH) to optimize.")
        if rain_factor < 0.9:
            optimizations.append(f"🌧️ **Rainfall:** Current {yield_rainfall:.0f}mm. Optimal: {optimal_rain:.0f}mm. Adjust irrigation accordingly.")
        
        if not optimizations:
            optimizations.append("✅ **Excellent Conditions:** Your field conditions are optimal! Maintain current practices for maximum yield.")
        
        for opt in optimizations:
            st.info(opt)
        
        # Profitability vs Yield Analysis
        if yield_crop in market_prices:
            crop_price = market_prices[yield_crop].get("price_per_kg", 0)
            revenue = total_yield * crop_price
            estimated_cost = yield_area * 50000  # Estimated cost per acre
            profit = revenue - estimated_cost
            
            st.markdown("### 💰 Profitability vs Yield Analysis")
            
            col_prof1, col_prof2 = st.columns(2)
            
            with col_prof1:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 100%); 
                            padding: 20px; border-radius: 15px; border: 2px solid rgba(34, 197, 94, 0.4);">
                    <h4 style="color: #14532d; margin-bottom: 15px;">📊 Financial Projection</h4>
                    <p style="color: #4b5563; font-size: 1.1rem; margin: 10px 0;">
                        <strong>Expected Revenue:</strong> ₹{revenue:,.0f}
                    </p>
                    <p style="color: #4b5563; font-size: 1.1rem; margin: 10px 0;">
                        <strong>Estimated Cost:</strong> ₹{estimated_cost:,.0f}
                    </p>
                    <p style="color: #4b5563; font-size: 1.1rem; margin: 10px 0;">
                        <strong>Expected Profit:</strong> <span style="color: {'#22c55e' if profit > 0 else '#ef4444'}; font-weight: bold;">₹{profit:,.0f}</span>
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            with col_prof2:
                # Yield vs Profit chart
                yield_scenarios = [predicted_yield * 0.7, predicted_yield * 0.85, predicted_yield, predicted_yield * 1.15, predicted_yield * 1.3]
                profit_scenarios = [(y * yield_area * crop_price - estimated_cost) for y in yield_scenarios]
                
                fig_profit_yield = go.Figure()
                fig_profit_yield.add_trace(go.Scatter(
                    x=yield_scenarios,
                    y=profit_scenarios,
                    mode='lines+markers',
                    name='Profit vs Yield',
                    line=dict(color='#22c55e', width=3),
                    marker=dict(size=10, color='#14532d'),
                    hovertemplate='Yield: %{x:.0f} kg/acre<br>Profit: ₹%{y:,.0f}<extra></extra>'
                ))
                fig_profit_yield.add_hline(y=0, line_dash="dash", line_color="#ef4444", annotation_text="Break-even")
                fig_profit_yield.update_layout(
                    title=dict(text='Profitability vs Yield Relationship', font=dict(size=20, color='#14532d', weight='bold')),
                    xaxis=dict(title='Yield (kg/acre)', tickfont=dict(size=14)),
                    yaxis=dict(title='Profit (₹)', tickfont=dict(size=14)),
                    height=350,
                    paper_bgcolor='rgba(241, 248, 244, 0.95)',
                    plot_bgcolor='rgba(255, 255, 255, 0.9)'
                )
                st.plotly_chart(fig_profit_yield, use_container_width=True)

# ===========================================
# TAB 13: FERTILIZER RECOMMENDATION ENGINE
# ===========================================
with tab13:
    st.markdown('<h2 class="section-header">🌿 Fertilizer Recommendation Engine</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="modern-card">
        <p>Get custom NPK blend recommendations, compare organic vs synthetic fertilizers, and optimize application timing.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Input Section
    col_fert1, col_fert2 = st.columns(2)
    
    with col_fert1:
        st.markdown("### 🌾 Crop & Current Soil Status")
        fert_crop = st.selectbox(
            "🌾 Select Crop",
            options=list(CROP_INFO.keys()),
            format_func=lambda x: CROP_INFO.get(x, {}).get("displayName", x),
            key="fert_crop"
        )
        
        fert_N = st.number_input("🌿 Current Nitrogen (N) ppm", min_value=0.0, max_value=200.0, value=90.0, step=1.0, key="fert_N")
        fert_P = st.number_input("🔬 Current Phosphorus (P) ppm", min_value=0.0, max_value=200.0, value=42.0, step=1.0, key="fert_P")
        fert_K = st.number_input("⚡ Current Potassium (K) ppm", min_value=0.0, max_value=250.0, value=43.0, step=1.0, key="fert_K")
        
        fert_area = st.number_input("📐 Field Area (acres)", min_value=0.1, value=1.0, step=0.1, key="fert_area")
    
    with col_fert2:
        st.markdown("### 🎯 Target & Preferences")
        target_yield_boost = st.slider(
            "📈 Target Yield Increase (%)",
            min_value=0,
            max_value=50,
            value=20,
            help="How much yield increase are you targeting?",
            key="fert_yield_boost"
        )
        
        fert_preference = st.radio(
            "🌿 Fertilizer Preference",
            options=["Balanced (NPK)", "Organic Only", "Synthetic Only", "Compare Both"],
            key="fert_preference"
        )
        
        application_timing = st.selectbox(
            "📅 Application Timing",
            options=["Pre-planting", "At Planting", "Early Growth", "Mid-season", "Late Season"],
            key="fert_timing"
        )
    
    if fert_crop:
        crop_info_fert = CROP_INFO.get(fert_crop, {})
        ideal_fert = crop_info_fert.get("idealConditions", {})
        
        # Calculate nutrient requirements
        N_range = ideal_fert.get("N", {})
        P_range = ideal_fert.get("P", {})
        K_range = ideal_fert.get("K", {})
        
        target_N = (N_range.get("min", 80) + N_range.get("max", 120)) / 2 if N_range else 100
        target_P = (P_range.get("min", 40) + P_range.get("max", 60)) / 2 if P_range else 50
        target_K = (K_range.get("min", 80) + K_range.get("max", 120)) / 2 if K_range else 100
        
        # Calculate deficits (accounting for yield boost)
        N_deficit = max(0, (target_N * (1 + target_yield_boost/100)) - fert_N)
        P_deficit = max(0, (target_P * (1 + target_yield_boost/100)) - fert_P)
        K_deficit = max(0, (target_K * (1 + target_yield_boost/100)) - fert_K)
        
        # Convert to kg per acre (assuming 1 ppm ≈ 2 kg/acre for top 6 inches)
        N_kg_needed = N_deficit * 2 * fert_area
        P_kg_needed = P_deficit * 2 * fert_area
        K_kg_needed = K_deficit * 2 * fert_area
        
        # Results
        st.markdown("### 📊 Custom NPK Blend Recommendation")
        
        col_npk1, col_npk2, col_npk3 = st.columns(3)
        
        with col_npk1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 100%); 
                        padding: 20px; border-radius: 15px; border: 2px solid rgba(34, 197, 94, 0.4); 
                        text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 10px;">🌿</div>
                <h4 style="color: #14532d; margin: 10px 0;">Nitrogen (N)</h4>
                <p style="font-size: 2rem; font-weight: bold; color: #22c55e; margin: 0;">{N_kg_needed:.1f}</p>
                <p style="color: #6b7280; margin: 5px 0 0 0;">kg needed</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_npk2:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 100%); 
                        padding: 20px; border-radius: 15px; border: 2px solid rgba(34, 197, 94, 0.4); 
                        text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 10px;">🔬</div>
                <h4 style="color: #14532d; margin: 10px 0;">Phosphorus (P)</h4>
                <p style="font-size: 2rem; font-weight: bold; color: #3b82f6; margin: 0;">{P_kg_needed:.1f}</p>
                <p style="color: #6b7280; margin: 5px 0 0 0;">kg needed</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_npk3:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 100%); 
                        padding: 20px; border-radius: 15px; border: 2px solid rgba(34, 197, 94, 0.4); 
                        text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 10px;">⚡</div>
                <h4 style="color: #14532d; margin: 10px 0;">Potassium (K)</h4>
                <p style="font-size: 2rem; font-weight: bold; color: #fbbf24; margin: 0;">{K_kg_needed:.1f}</p>
                <p style="color: #6b7280; margin: 5px 0 0 0;">kg needed</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Fertilizer Product Recommendations
        st.markdown("### 💊 Recommended Fertilizer Products")
        
        # Common fertilizer compositions
        fertilizers = {
            "Urea (46-0-0)": {"N": 46, "P": 0, "K": 0, "type": "synthetic", "cost_per_kg": 30},
            "DAP (18-46-0)": {"N": 18, "P": 46, "K": 0, "type": "synthetic", "cost_per_kg": 35},
            "MOP (0-0-60)": {"N": 0, "P": 0, "K": 60, "type": "synthetic", "cost_per_kg": 25},
            "NPK 19-19-19": {"N": 19, "P": 19, "K": 19, "type": "synthetic", "cost_per_kg": 40},
            "Compost": {"N": 2, "P": 1, "K": 1, "type": "organic", "cost_per_kg": 5},
            "Farmyard Manure": {"N": 0.5, "P": 0.2, "K": 0.5, "type": "organic", "cost_per_kg": 3},
            "Vermicompost": {"N": 1.5, "P": 1, "K": 1, "type": "organic", "cost_per_kg": 8},
            "Neem Cake": {"N": 5, "P": 1, "K": 1.5, "type": "organic", "cost_per_kg": 15}
        }
        
        # Calculate required amounts for each fertilizer
        recommendations = []
        
        if fert_preference in ["Balanced (NPK)", "Synthetic Only", "Compare Both"]:
            # Synthetic recommendations
            if N_kg_needed > 0:
                urea_needed = N_kg_needed / 0.46
                recommendations.append({
                    "Fertilizer": "Urea (46-0-0)",
                    "Amount (kg)": round(urea_needed, 1),
                    "Type": "Synthetic",
                    "Cost (₹)": round(urea_needed * 30, 0)
                })
            
            if P_kg_needed > 0:
                dap_needed = P_kg_needed / 0.46
                recommendations.append({
                    "Fertilizer": "DAP (18-46-0)",
                    "Amount (kg)": round(dap_needed, 1),
                    "Type": "Synthetic",
                    "Cost (₹)": round(dap_needed * 35, 0)
                })
            
            if K_kg_needed > 0:
                mop_needed = K_kg_needed / 0.60
                recommendations.append({
                    "Fertilizer": "MOP (0-0-60)",
                    "Amount (kg)": round(mop_needed, 1),
                    "Type": "Synthetic",
                    "Cost (₹)": round(mop_needed * 25, 0)
                })
        
        if fert_preference in ["Organic Only", "Compare Both"]:
            # Organic recommendations
            if N_kg_needed > 0:
                compost_needed = N_kg_needed / 0.02
                recommendations.append({
                    "Fertilizer": "Compost",
                    "Amount (kg)": round(compost_needed, 1),
                    "Type": "Organic",
                    "Cost (₹)": round(compost_needed * 5, 0)
                })
        
        if recommendations:
            df_fert_rec = pd.DataFrame(recommendations)
            st.dataframe(df_fert_rec, use_container_width=True, hide_index=True)
            
            total_synthetic_cost = sum([r["Cost (₹)"] for r in recommendations if r["Type"] == "Synthetic"])
            total_organic_cost = sum([r["Cost (₹)"] for r in recommendations if r["Type"] == "Organic"])
        
        # Organic vs Synthetic Comparison
        if fert_preference == "Compare Both":
            st.markdown("### ⚖️ Organic vs Synthetic Comparison")
            
            col_comp1, col_comp2 = st.columns(2)
            
            with col_comp1:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 100%); 
                            padding: 25px; border-radius: 15px; border: 2px solid #3b82f6;">
                    <h4 style="color: #14532d; margin-bottom: 15px;">🔬 Synthetic Fertilizers</h4>
                    <p style="color: #4b5563; margin: 10px 0;">
                        <strong>Total Cost:</strong> ₹{total_synthetic_cost:,.0f}
                    </p>
                    <p style="color: #4b5563; margin: 10px 0;">
                        <strong>Pros:</strong> Fast-acting, precise NPK ratios, cost-effective
                    </p>
                    <p style="color: #4b5563; margin: 10px 0;">
                        <strong>Cons:</strong> Can harm soil health long-term, environmental impact
                    </p>
                    <p style="color: #4b5563; margin: 10px 0;">
                        <strong>Application:</strong> {application_timing}, split into 2-3 applications
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            with col_comp2:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 100%); 
                            padding: 25px; border-radius: 15px; border: 2px solid #22c55e;">
                    <h4 style="color: #14532d; margin-bottom: 15px;">🌿 Organic Fertilizers</h4>
                    <p style="color: #4b5563; margin: 10px 0;">
                        <strong>Total Cost:</strong> ₹{total_organic_cost:,.0f}
                    </p>
                    <p style="color: #4b5563; margin: 10px 0;">
                        <strong>Pros:</strong> Improves soil health, sustainable, long-term benefits
                    </p>
                    <p style="color: #4b5563; margin: 10px 0;">
                        <strong>Cons:</strong> Slower release, larger quantities needed, higher cost
                    </p>
                    <p style="color: #4b5563; margin: 10px 0;">
                        <strong>Application:</strong> {application_timing}, apply 2-3 weeks before planting
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            # Cost-benefit chart
            fig_fert_compare = go.Figure()
            fig_fert_compare.add_trace(go.Bar(
                name='Synthetic',
                x=['Cost', 'Speed', 'Soil Health', 'Environmental'],
                y=[100 - (total_synthetic_cost / max(total_synthetic_cost, total_organic_cost) * 100), 90, 40, 30],
                marker_color='#3b82f6'
            ))
            fig_fert_compare.add_trace(go.Bar(
                name='Organic',
                x=['Cost', 'Speed', 'Soil Health', 'Environmental'],
                y=[100 - (total_organic_cost / max(total_synthetic_cost, total_organic_cost) * 100), 50, 90, 95],
                marker_color='#22c55e'
            ))
            fig_fert_compare.update_layout(
                title=dict(text='Fertilizer Comparison', font=dict(size=20, color='#14532d', weight='bold')),
                barmode='group',
                height=400,
                paper_bgcolor='rgba(241, 248, 244, 0.95)',
                plot_bgcolor='rgba(255, 255, 255, 0.9)',
                yaxis=dict(title='Score (0-100)', tickfont=dict(size=14)),
                legend=dict(font=dict(size=14))
            )
            st.plotly_chart(fig_fert_compare, use_container_width=True)
        
        # Application Timing & Methods
        st.markdown("### 📅 Application Timing & Methods")
        
        timing_guidance = {
            "Pre-planting": "Apply 2-3 weeks before planting. Mix well with soil. Best for organic fertilizers.",
            "At Planting": "Apply during seed sowing. Place 2-3 inches away from seeds. Use balanced NPK.",
            "Early Growth": "Apply 2-3 weeks after germination. Side-dress near plant base. Focus on nitrogen.",
            "Mid-season": "Apply during active growth phase. Top-dress or foliar spray. Balanced nutrients.",
            "Late Season": "Apply before flowering/fruiting. Focus on phosphorus and potassium."
        }
        
        st.info(f"**{application_timing}:** {timing_guidance.get(application_timing, 'Apply as recommended.')}")
        
        # Environmental Impact Assessment
        st.markdown("### 🌍 Environmental Impact Assessment")
        
        if fert_preference in ["Synthetic Only", "Balanced (NPK)"]:
            # Calculate environmental impact
            synthetic_impact = {
                "Carbon Footprint": "High",
                "Water Pollution Risk": "Medium-High",
                "Soil Health Impact": "Negative (long-term)",
                "Biodiversity Impact": "Negative"
            }
            
            col_env1, col_env2 = st.columns(2)
            
            with col_env1:
                st.markdown("#### ⚠️ Synthetic Fertilizer Impact")
                for key, value in synthetic_impact.items():
                    color = "#ef4444" if "Negative" in value or "High" in value else "#fbbf24"
                    st.markdown(f"- **{key}:** <span style='color: {color};'>{value}</span>", unsafe_allow_html=True)
            
            with col_env2:
                st.markdown("#### ✅ Mitigation Strategies")
                st.markdown("""
                - Use slow-release fertilizers
                - Apply in split doses
                - Avoid over-application
                - Test soil regularly
                - Combine with organic matter
                """)
        
        if fert_preference in ["Organic Only", "Compare Both"]:
            organic_impact = {
                "Carbon Footprint": "Low",
                "Water Pollution Risk": "Low",
                "Soil Health Impact": "Positive",
                "Biodiversity Impact": "Positive"
            }
            
            if fert_preference == "Organic Only":
                st.markdown("#### ✅ Organic Fertilizer Impact")
                for key, value in organic_impact.items():
                    color = "#22c55e" if "Positive" in value or "Low" in value else "#fbbf24"
                    st.markdown(f"- **{key}:** <span style='color: {color};'>{value}</span>", unsafe_allow_html=True)

# ===========================================
# TAB 14: HISTORY & EXPORT
# ===========================================
with tab14:
    st.markdown('<h2 class="section-header">📜 Prediction History & Export</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="modern-card">
        <p>View your prediction history, search past recommendations, and export data for analysis.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state if needed
    if 'prediction_history' not in st.session_state:
        st.session_state.prediction_history = []
    
    if st.session_state.prediction_history and len(st.session_state.prediction_history) > 0:
        history_df = pd.DataFrame(st.session_state.prediction_history)
        
        # Search and filter
        col_search1, col_search2 = st.columns([3, 1])
        with col_search1:
            search_term = st.text_input("🔍 Search History", key="history_search", placeholder="Search by crop name...")
        with col_search2:
            if st.button("🗑️ Clear All", key="clear_history"):
                st.session_state.prediction_history = []
                st.success("History cleared!")
                st.rerun()
        
        if search_term:
            history_df = history_df[history_df['crop'].str.contains(search_term, case=False, na=False)]
        
        if not history_df.empty:
            # Display metrics
            col_hist1, col_hist2, col_hist3, col_hist4 = st.columns(4)
            with col_hist1:
                st.metric("Total Predictions", len(history_df))
            with col_hist2:
                st.metric("Unique Crops", history_df['crop'].nunique())
            with col_hist3:
                most_common = history_df['crop'].mode()[0] if not history_df['crop'].mode().empty else "N/A"
                st.metric("Most Recommended", most_common)
            with col_hist4:
                st.metric("Date Range", f"{len(history_df)} entries")
            
            # Display history table
            st.markdown("### 📋 Prediction History")
            display_df = history_df[['timestamp', 'crop']].copy()
            if 'inputs' in history_df.columns:
                display_df['Inputs'] = history_df['inputs'].apply(lambda x: str(x)[:50] + "..." if len(str(x)) > 50 else str(x))
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            # Export options
            st.markdown("### 📥 Export Options")
            col_exp1, col_exp2, col_exp3 = st.columns(3)
            with col_exp1:
                csv = history_df.to_csv(index=False)
                st.download_button(
                    "📄 Download CSV",
                    csv,
                    "crop_prediction_history.csv",
                    "text/csv",
                    key="download_csv",
                    use_container_width=True
                )
            with col_exp2:
                json_str = history_df.to_json(orient='records', indent=2)
                st.download_button(
                    "📄 Download JSON",
                    json_str,
                    "crop_prediction_history.json",
                    "application/json",
                    key="download_json",
                    use_container_width=True
                )
            with col_exp3:
                try:
                    import io
                    excel_buffer = io.BytesIO()
                    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                        history_df.to_excel(writer, index=False)
                    excel_data = excel_buffer.getvalue()
                    st.download_button(
                        "📊 Download Excel",
                        excel_data,
                        "crop_prediction_history.xlsx",
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key="download_excel",
                        use_container_width=True
                    )
                except ImportError:
                    st.info("💡 Excel export requires 'openpyxl'. Install with: pip install openpyxl")
            
            # Visualization
            st.markdown("### 📊 History Visualization")
            crop_counts = history_df['crop'].value_counts()
            
            fig_hist = go.Figure()
            fig_hist.add_trace(go.Bar(
                x=crop_counts.index,
                y=crop_counts.values,
                marker_color='#22c55e',
                marker_line=dict(width=2, color='#1f2937'),
                text=crop_counts.values,
                textposition='outside',
                textfont=dict(size=16, color='#1f2937', weight='bold')
            ))
            fig_hist.update_layout(
                title=dict(text='Crop Recommendation Frequency', font=dict(size=22, color='#14532d', weight='bold')),
                xaxis=dict(tickfont=dict(size=14), title="Crop"),
                yaxis=dict(tickfont=dict(size=14), title="Count"),
                height=400,
                paper_bgcolor='rgba(241, 248, 244, 0.95)',
                plot_bgcolor='rgba(255, 255, 255, 0.9)'
            )
            st.plotly_chart(fig_hist, use_container_width=True)
        else:
            st.info("No predictions match your search criteria.")
    else:
        st.info("📝 No prediction history yet. Make some predictions to see them here!")
        st.markdown("""
        <div class="modern-card">
            <h4>💡 How to use History & Export:</h4>
            <ul>
                <li>Make predictions in the <strong>Single Prediction</strong> tab</li>
                <li>All predictions are automatically saved to your history</li>
                <li>Search and filter your past recommendations</li>
                <li>Export data in CSV, JSON, or Excel format</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ===========================================
# TAB 15: ABOUT
# ===========================================
with tab15:
    st.markdown('<h2 class="section-header">About Smart Crop Advisor</h2>', unsafe_allow_html=True)
    
    col_about1, col_about2 = st.columns(2)
    
    with col_about1:
        st.markdown("""
        <div class="modern-card">
            <h3>🎯 Our Mission</h3>
            <p>Smart Crop Advisor uses advanced machine learning (XGBoost) 
            to analyze soil nutrients and climate conditions, providing 
            data-driven crop recommendations with 99%+ accuracy.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="modern-card">
            <h3>🌱 Supported Crops</h3>
            <p>We support <strong>22 different crop types</strong> including:</p>
            <ul>
                <li>Cereals: Rice, Maize</li>
                <li>Legumes: Chickpea, Kidney Beans, Lentils</li>
                <li>Fruits: Mango, Banana, Apple, Orange</li>
                <li>Fiber Crops: Cotton, Jute</li>
                <li>And many more!</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col_about2:
        st.markdown("""
        <div class="modern-card">
            <h3>📊 Model Performance</h3>
            <ul>
                <li><strong>Accuracy:</strong> 99.09%</li>
                <li><strong>Precision:</strong> 99.19%</li>
                <li><strong>Recall:</strong> 99.09%</li>
                <li><strong>F1-Score:</strong> 99.10%</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="modern-card">
            <h3>💡 Key Features</h3>
            <ul>
                <li>🌍 Comprehensive Analysis (7 parameters)</li>
                <li>🤖 AI-Powered Predictions</li>
                <li>📊 Batch Processing</li>
                <li>📈 Interactive Visualizations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col_feat1, col_feat2, col_feat3 = st.columns(3)
    
    with col_feat1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🌍</div>
            <h3>Comprehensive</h3>
            <p>Analyzes 7 key parameters for accurate recommendations</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_feat2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <h3>AI-Powered</h3>
            <p>Advanced XGBoost algorithm with 99%+ accuracy</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_feat3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <h3>Batch Processing</h3>
            <p>Process multiple records simultaneously</p>
        </div>
        """, unsafe_allow_html=True)

# ===========================================
# FOOTER
# ===========================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #cdd1d6; padding: 40px;'>
    <h3 style='color: #e6e6e6;'>🌾 Smart Crop Advisor</h3>
    <p style='color: #cdd1d6;'>Powered by AI & Machine Learning | Helping farmers make data-driven decisions for better yields</p>
    <p style='margin-top: 20px; font-size: 0.9rem; color: #cdd1d6;'>© 2024 Smart Crop Advisor. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)

