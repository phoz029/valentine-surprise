from flask import Flask, render_template_string, request, jsonify
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return jsonify({"success": True})

    html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Secure Portal</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Playfair+Display:wght@400;600;700;900&family=Crimson+Text:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
  <style>
    * { 
      box-sizing: border-box; 
      margin:0; 
      padding:0; 
    }
    
    body {
      min-height: 100vh;
      font-family: 'Crimson Text', serif;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
      position: relative;
    }
    
    body::before {
      content: '';
      position: absolute;
      inset: 0;
      background: 
        radial-gradient(circle at 20% 50%, rgba(102, 126, 234, 0.3) 0%, transparent 50%),
        radial-gradient(circle at 80% 80%, rgba(118, 75, 162, 0.3) 0%, transparent 50%),
        radial-gradient(circle at 40% 20%, rgba(159, 168, 218, 0.2) 0%, transparent 50%);
      animation: pulse 8s ease-in-out infinite;
      pointer-events: none;
    }
    
    @keyframes pulse {
      0%, 100% { opacity: 0.6; }
      50% { opacity: 0.9; }
    }
    
    body.pink-mode {
      background: linear-gradient(135deg, #ffeef8 0%, #ffe3ec 25%, #ffc1d5 50%, #ffb3c6 75%, #ff9a9e 100%);
    }
    
    #welcome-screen {
      position: fixed;
      inset: 0;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 120;
      animation: fadeIn 1s ease;
    }
    
    .welcome-card {
      background: white;
      padding: 80px 60px;
      border-radius: 30px;
      text-align: center;
      box-shadow: 0 30px 100px rgba(0, 0, 0, 0.3);
      animation: scaleIn 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    
    @keyframes scaleIn {
      from { transform: scale(0.8); opacity: 0; }
      to { transform: scale(1); opacity: 1; }
    }
    
    .welcome-card h2 {
      font-size: 2rem;
      color: #636e72;
      margin-bottom: 20px;
      font-weight: 400;
    }
    
    .welcome-card h1 {
      font-size: 3.2rem;
      color: #667eea;
      font-family: 'Playfair Display', serif;
      font-weight: 700;
      margin-bottom: 0;
    }

    .card {
      width: 90%;
      max-width: 440px;
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(20px);
      padding: 60px 40px;
      border-radius: 30px;
      box-shadow: 
        0 25px 80px rgba(0, 0, 0, 0.15),
        0 0 0 1px rgba(255, 255, 255, 0.5) inset;
      text-align: center;
      transition: opacity 1.2s ease, transform 1.2s ease;
      border: 2px solid rgba(255, 255, 255, 0.8);
    }
    
    .card.fade-out {
      opacity: 0;
      transform: translateY(-60px) scale(0.95);
    }

    h2 { 
      margin-bottom: 35px; 
      color: #2d3436; 
      font-size: 2.4rem;
      font-family: 'Playfair Display', serif;
      font-weight: 600;
      letter-spacing: 0.5px;
    }
    
    input, button {
      width: 100%;
      padding: 18px 24px;
      margin: 16px 0;
      border-radius: 15px;
      font-size: 1.15rem;
      font-family: 'Crimson Text', serif;
      transition: all 0.3s ease;
    }
    
    input { 
      border: 2px solid rgba(102, 126, 234, 0.2); 
      background: rgba(255, 255, 255, 0.9);
      color: #2d3436;
      padding-right: 50px;
    }
    
    input:focus { 
      border-color: #667eea; 
      outline: none;
      background: white;
      transform: translateY(-2px);
      box-shadow: 0 8px 20px rgba(102, 126, 234, 0.15);
    }
    
    .password-wrapper {
      position: relative;
      width: 100%;
    }
    
    .password-toggle {
      position: absolute;
      right: 15px;
      top: 50%;
      transform: translateY(-50%);
      background: none;
      border: none;
      cursor: pointer;
      font-size: 1.2rem;
      padding: 5px;
      color: #636e72;
      width: auto;
      margin: 0;
      transition: color 0.2s ease;
    }
    
    .password-toggle:hover {
      color: #667eea;
    }
    
    button {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      border: none;
      cursor: pointer;
      font-weight: 600;
      letter-spacing: 0.5px;
      box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    }
    
    button:hover { 
      transform: translateY(-3px);
      box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4);
    }
    
    .error-message {
      color: #d63031;
      margin-top: 16px;
      min-height: 1.5em;
      font-size: 1rem;
      font-weight: 500;
    }

    #loader {
      position: fixed;
      inset: 0;
      background: rgba(255, 255, 255, 0.98);
      display: none;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      z-index: 100;
      backdrop-filter: blur(10px);
    }
    
    .spinner {
      width: 64px; 
      height: 64px;
      border: 5px solid rgba(102, 126, 234, 0.1);
      border-top: 5px solid #667eea;
      border-radius: 50%;
      animation: spin 1.2s cubic-bezier(0.4, 0, 0.2, 1) infinite;
    }
    
    @keyframes spin { 
      to { transform: rotate(360deg); } 
    }
    
    #loader p {
      margin-top: 25px;
      color: #667eea;
      font-size: 1.4rem;
      font-weight: 600;
      letter-spacing: 1px;
    }

    #envelope-container {
      width: 90%;
      max-width: 520px;
      margin: 40px auto;
      opacity: 0;
      transform: scale(0.85) translateY(30px);
      transition: opacity 1.5s cubic-bezier(0.4, 0, 0.2, 1), 
                  transform 1.5s cubic-bezier(0.4, 0, 0.2, 1);
      cursor: pointer;
    }
    
    #envelope-container.visible {
      opacity: 1;
      transform: scale(1) translateY(0);
    }
    
    #envelope {
      width: 100%;
      height: 300px;
      background: linear-gradient(135deg, #fff9e6 0%, #fff3d4 100%);
      border-radius: 30px;
      box-shadow: 
        0 20px 60px rgba(214, 48, 49, 0.2),
        0 0 0 2px rgba(255, 255, 255, 0.8) inset;
      position: relative;
      animation: float-envelope 6s ease-in-out infinite;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 6rem;
      border: 3px solid rgba(214, 48, 49, 0.1);
      transition: transform 0.4s ease;
    }
    
    #envelope:hover {
      transform: scale(1.05) rotate(-2deg);
    }
    
    @keyframes float-envelope {
      0%, 100% { transform: translateY(0) rotate(0deg); }
      25% { transform: translateY(-15px) rotate(2deg); }
      50% { transform: translateY(-25px) rotate(0deg); }
      75% { transform: translateY(-15px) rotate(-2deg); }
    }
    
    #envelope-text {
      text-align: center;
      margin-top: 30px;
      font-size: 1.5rem;
      color: #d63031;
      font-family: 'Playfair Display', serif;
      font-weight: 600;
      letter-spacing: 0.5px;
      animation: pulse-text 2s ease-in-out infinite;
    }
    
    @keyframes pulse-text {
      0%, 100% { opacity: 0.7; }
      50% { opacity: 1; }
    }

    #question-container {
      width: 90%;
      max-width: 800px;
      padding: 0;
      background: transparent;
      backdrop-filter: none;
      border-radius: 0;
      box-shadow: none;
      text-align: center;
      opacity: 0;
      transform: translateY(50px);
      transition: opacity 1.2s cubic-bezier(0.4, 0, 0.2, 1), 
                  transform 1.2s cubic-bezier(0.4, 0, 0.2, 1);
      border: none;
    }
    
    #question-container.visible {
      opacity: 1;
      transform: translateY(0);
    }
    
    .question-content {
      background: rgba(255, 255, 255, 0.98);
      backdrop-filter: blur(20px);
      padding: 70px 60px;
      border-radius: 40px;
      box-shadow: 
        0 30px 90px rgba(214, 48, 49, 0.25),
        0 0 0 1px rgba(255, 255, 255, 0.8) inset;
      position: relative;
      overflow: visible;
    }
    
    .question-content::before {
      content: '💕';
      position: absolute;
      top: -40px;
      left: 50%;
      transform: translateX(-50%);
      font-size: 5rem;
      animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
      0%, 100% { transform: translateX(-50%) translateY(0); }
      50% { transform: translateX(-50%) translateY(-15px); }
    }

    h1 { 
      font-size: 4rem; 
      background: linear-gradient(135deg, #d63031 0%, #e84393 50%, #fd79a8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      margin-bottom: 0.3em;
      font-family: 'Playfair Display', serif;
      font-weight: 900;
      line-height: 1.2;
      animation: fadeInScale 1s ease-out 0.3s both;
      letter-spacing: -1px;
    }
    
    @keyframes fadeInScale {
      from { opacity: 0; transform: scale(0.9); }
      to { opacity: 1; transform: scale(1); }
    }
    
    .subtitle { 
      font-size: 1.5rem; 
      margin: 1.2em 0 3em;
      color: #636e72;
      font-weight: 400;
      animation: fadeInScale 1s ease-out 0.5s both;
    }

    .buttons { 
      display: flex; 
      gap: 25px; 
      justify-content: center; 
      margin-top: 3em; 
      flex-wrap: wrap;
    }
    
    .yes-btn, .no-btn {
      padding: 24px 65px;
      font-size: 1.5rem;
      border-radius: 50px;
      min-width: 220px;
      transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
      font-family: 'Playfair Display', serif;
      font-weight: 600;
      letter-spacing: 0.5px;
      animation: fadeInScale 1s ease-out 0.7s both;
      border: none;
      cursor: pointer;
    }
    
    .yes-btn { 
      background: linear-gradient(135deg, #d63031 0%, #e84393 100%);
      color: white;
      box-shadow: 0 15px 40px rgba(214, 48, 49, 0.4);
      position: relative;
      overflow: hidden;
    }
    
    .yes-btn::before {
      content: '';
      position: absolute;
      inset: 0;
      background: linear-gradient(135deg, #e84393 0%, #fd79a8 100%);
      opacity: 0;
      transition: opacity 0.3s ease;
    }
    
    .yes-btn:hover::before {
      opacity: 1;
    }
    
    .yes-btn span {
      position: relative;
      z-index: 1;
    }
    
    .yes-btn:hover { 
      transform: scale(1.08) translateY(-5px); 
      box-shadow: 0 20px 50px rgba(214, 48, 49, 0.6);
    }
    
    .no-btn { 
      background: linear-gradient(135deg, #636e72 0%, #2d3436 100%);
      color: white; 
      position: relative;
      box-shadow: 0 15px 40px rgba(99, 110, 114, 0.3);
    }
    
    .no-btn:hover {
      transform: scale(1.05);
    }

    #popup {
      position: fixed; 
      inset: 0;
      background: rgba(0, 0, 0, 0.75);
      backdrop-filter: blur(8px);
      display: flex;
      align-items: center; 
      justify-content: center;
      z-index: 200;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.4s ease;
    }
    
    #popup.show {
      opacity: 1;
      pointer-events: all;
    }
    
    .popup-box {
      background: white;
      padding: 50px;
      border-radius: 30px;
      text-align: center;
      max-width: 450px;
      box-shadow: 0 25px 80px rgba(0, 0, 0, 0.5);
      transform: scale(0.9);
      transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
      border: 3px solid rgba(214, 48, 49, 0.2);
    }
    
    #popup.show .popup-box {
      transform: scale(1);
    }
    
    .popup-box video {
      max-width: 280px;
      border-radius: 20px;
      margin: 25px 0;
      box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
    }
    
    .popup-box p {
      font-size: 1.6rem;
      margin-top: 25px;
      color: #2d3436;
      font-family: 'Playfair Display', serif;
      font-weight: 600;
    }
    
    .popup-box button {
      margin-top: 25px;
      padding: 14px 45px;
      background: linear-gradient(135deg, #d63031 0%, #e84393 100%);
      color: white;
      border: none;
      border-radius: 25px;
      cursor: pointer;
      font-size: 1.1rem;
      font-family: 'Crimson Text', serif;
      font-weight: 600;
    }

    #sad-cat-overlay {
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.85);
      backdrop-filter: blur(10px);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 300;
      opacity: 0;
      pointer-events: none;
      transition: opacity 1.8s ease;
    }
    
    #sad-cat-overlay.show {
      opacity: 1;
      pointer-events: all;
    }
    
    #sad-cat-overlay img {
      max-width: 90%;
      max-height: 80vh;
      border-radius: 25px;
      box-shadow: 0 20px 80px rgba(0, 0, 0, 0.6);
      animation: sadCatEnter 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    
    @keyframes sadCatEnter {
      from { transform: scale(0.8) translateY(50px); opacity: 0; }
      to { transform: scale(1) translateY(0); opacity: 1; }
    }

    .evil {
      position: fixed;
      top: 20px;
      left: 20px;
      transform: translate(0, 0);
      width: 220px;
      border-radius: 20px;
      box-shadow: 0 15px 50px rgba(0, 0, 0, 0.5);
      z-index: 1;
      border: 2px solid rgba(255, 255, 255, 0.3);
      pointer-events: none;
    }

    #letter-screen {
      position: fixed;
      inset: 0;
      background: linear-gradient(135deg, #ffeef8 0%, #fff5f7 100%);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 150;
      animation: fadeIn 1.5s ease;
      padding: 40px 20px;
      overflow-y: auto;
    }
    
    @keyframes fadeIn {
      from { opacity: 0; }
      to { opacity: 1; }
    }
    
    .letter-container {
      max-width: 700px;
      width: 90%;
      background: white;
      padding: 80px 60px;
      border-radius: 5px;
      box-shadow: 
        0 30px 100px rgba(214, 48, 49, 0.2),
        0 0 0 1px rgba(214, 48, 49, 0.1);
      position: relative;
      animation: letterSlideIn 1.2s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    @keyframes letterSlideIn {
      from { transform: translateY(60px); opacity: 0; }
      to { transform: translateY(0); opacity: 1; }
    }
    
    .letter-container::before {
      content: '';
      position: absolute;
      top: 0;
      left: 50%;
      transform: translateX(-50%);
      width: 100px;
      height: 4px;
      background: linear-gradient(90deg, transparent, #d63031, transparent);
    }
    
    .letter-date {
      text-align: right;
      font-size: 1rem;
      color: #636e72;
      margin-bottom: 40px;
      font-style: italic;
    }
    
    .letter-greeting {
      font-size: 2.2rem;
      color: #d63031;
      margin-bottom: 30px;
      font-family: 'Playfair Display', serif;
      font-weight: 600;
    }
    
    .letter-body {
      font-size: 1.25rem;
      line-height: 2;
      color: #2d3436;
      margin-bottom: 25px;
      text-align: justify;
      font-family: 'Cormorant Garamond', serif;
      font-weight: 400;
    }
    
    .letter-body p {
      margin-bottom: 25px;
    }
    
    .letter-highlight {
      color: #d63031;
      font-weight: 600;
      font-style: italic;
    }
    
    .letter-details {
      background: linear-gradient(135deg, rgba(214, 48, 49, 0.05), rgba(232, 67, 147, 0.05));
      padding: 30px;
      border-radius: 15px;
      margin: 40px 0;
      border-left: 4px solid #d63031;
    }
    
    .letter-details p {
      font-size: 1.2rem;
      margin: 12px 0;
      color: #2d3436;
      font-family: 'Crimson Text', serif;
    }
    
    .letter-details strong {
      color: #d63031;
      font-weight: 600;
    }
    
    .letter-signature {
      text-align: right;
      margin-top: 50px;
      font-size: 1.8rem;
      font-family: 'Playfair Display', serif;
      color: #d63031;
      font-style: italic;
      font-weight: 400;
    }
    
    .letter-hearts {
      text-align: center;
      font-size: 2rem;
      margin-top: 40px;
      opacity: 0.6;
    }

    .hidden { 
      display: none !important; 
    }

    #print-letter-btn {
      display: block;
      margin: 50px auto 30px;
      padding: 16px 50px;
      font-size: 1.2rem;
      font-family: 'Playfair Display', serif;
      background: linear-gradient(135deg, #e63946, #d00000);
      color: white;
      border: none;
      border-radius: 30px;
      cursor: pointer;
      box-shadow: 0 8px 25px rgba(214, 48, 49, 0.4);
      transition: all 0.3s ease;
    }

    #print-letter-btn:hover {
      transform: translateY(-3px);
      box-shadow: 0 12px 35px rgba(214, 48, 49, 0.6);
    }

    @media (max-width: 768px) {
      h1 { font-size: 2.5rem; letter-spacing: -0.5px; }
      .subtitle { font-size: 1.2rem; }
      .yes-btn, .no-btn { min-width: 160px; padding: 18px 35px; font-size: 1.2rem; }
      .letter-container { padding: 50px 30px; }
      .letter-body { font-size: 1.1rem; line-height: 1.8; }
      .question-content { padding: 50px 30px; }
      #envelope { height: 220px; font-size: 4rem; }
      .welcome-card { padding: 60px 40px; }
      .welcome-card h1 { font-size: 2.4rem; }
      .welcome-card h2 { font-size: 1.6rem; }
      .evil { width: 160px; }
    }
    
    @media (max-width: 480px) {
      h1 { font-size: 2rem; }
      .subtitle { font-size: 1.1rem; }
      .yes-btn, .no-btn { 
        min-width: 140px; 
        padding: 16px 30px; 
        font-size: 1.1rem;
      }
      .buttons { gap: 15px; }
      .question-content { padding: 40px 25px; }
      .card { padding: 40px 30px; }
      .letter-container { padding: 40px 25px; }
      .evil { width: 140px; }
    }

    /* ────── PRINT STYLES ────── */
    @media print {
      body {
        background: white !important;
        background-image: none !important;
        color: black !important;
        margin: 0 !important;
        padding: 0 !important;
      }

      body * {
        visibility: hidden;
      }

      #letter-screen,
      #letter-screen * {
        visibility: visible;
      }

      #letter-screen {
        position: static !important;
        display: block !important;
        background: white !important;
        inset: 0 !important;
        z-index: auto !important;
        padding: 0 !important;
        margin: 0 !important;
        overflow-y: visible !important;
        animation: none !important;
        transition: none !important;
      }

      .letter-container {
        box-shadow: none !important;
        border: 1px solid #eee !important;
        background: white !important;
        padding: 2cm 3cm 3cm 3cm !important;           /* ← reduced top padding a lot */
        width: 21cm !important;
        max-width: 21cm !important;
        margin: 0 auto !important;
        border-radius: 0 !important;
        position: relative !important;
        transform: none !important;
        animation: none !important;
        page-break-inside: avoid;
      }

      .letter-container::before {
        display: none !important;
      }

      .letter-date {
        font-size: 11pt !important;
        color: #555 !important;
      }

      .letter-greeting {
        font-size: 19pt !important;
        color: #c1121f !important;
        margin-bottom: 1cm !important;
      }

      .letter-body {
        font-size: 12.5pt !important;
        line-height: 1.7 !important;
        color: #222 !important;
      }

      .letter-highlight {
        color: #b22222 !important;
        font-weight: bold !important;
        background: none !important;
      }

      .letter-details {
        border-left: 5px solid #c1121f !important;
        background: #fff5f5 !important;
        padding: 1cm !important;
        margin: 1.4cm 0 !important;
      }

      .letter-details p {
        font-size: 12pt !important;
        margin: 0.5em 0 !important;
      }

      .letter-signature {
        font-size: 17pt !important;
        color: #c1121f !important;
        margin-top: 2cm !important;
        text-align: right !important;
      }

      .letter-hearts {
        text-align: center !important;
        font-size: 1.8rem !important;
        margin-top: 1.8cm !important;
        color: #e63946 !important;
      }

      #print-letter-btn,
      video, audio, #sad-cat-overlay, #popup, #envelope-container,
      #question-container, .card, #loader, #welcome-screen, .evil,
      #letterBGM {
        display: none !important;
      }

      @page {
        size: A4 portrait;
        margin: 6mm 8mm 12mm 8mm;           /* ← very small top margin */
      }
    }
  </style>
</head>
<body>

<div id="loader">
  <div class="spinner"></div>
  <p>Authenticating…</p>
</div>

<div id="welcome-screen" class="hidden">
  <div class="welcome-card">
    <h2>Welcome back,</h2>
    <h1>Jervine Fajardo</h1>
  </div>
</div>

<div class="card" id="loginCard">
  <h2>Access Portal</h2>
  <form id="loginForm">
    <input id="username" name="username" placeholder="Username" required autocomplete="username">
    <div class="password-wrapper">
      <input id="password" name="password" type="password" placeholder="Password" required autocomplete="current-password">
      <button type="button" class="password-toggle" id="passwordToggle">👁️</button>
    </div>
    <button type="submit" style="margin-top:25px;">Sign In</button>
  </form>
  <p id="error" class="error-message"></p>
</div>

<div id="envelope-container" class="hidden">
  <div id="envelope">💌</div>
  <div id="envelope-text">Click the envelope to open</div>
</div>

<div id="question-container" class="hidden">
  <div class="question-content">
    <h1>Will you be my Valentine? 💖</h1>
    <p class="subtitle">I've been waiting forever to ask you this...</p>
    <div class="buttons">
      <button class="yes-btn" id="yesBtn"><span>Yes! Of course 💘</span></button>
      <button class="no-btn" id="noBtn">No 💔</button>
    </div>
  </div>
</div>

<div id="popup">
  <div class="popup-box">
    <video id="popupVideo" autoplay muted loop playsinline></video>
    <p id="popupText"></p>
    <button onclick="closePopup()">Close</button>
  </div>
</div>

<div id="sad-cat-overlay">
  <img src="/static/assets/sad-cat.jpg" alt="Sad cat">
</div>

<video id="evilVideo" class="evil hidden" loop></video>

<audio id="letterBGM" loop>
  <source src="/static/assets/bgm.mp3" type="audio/mpeg">
</audio>

<div id="letter-screen" class="hidden">
  <div class="letter-container">
    <div class="letter-date">February 2, 2026</div>
    <div class="letter-greeting">My Dearest Love,</div>
    
    <div class="letter-body">
      <p>
        I know myself that I don't have a way with words, and I realize that no amount of poetry or anything I could possibly type here could truly capture what I want to say. But let me try anyway...
      </p>
      <p>
        Every single day that I spend with you, love, uproots any doubts, fears, and every problem I could ever think of. Everything about you makes me feel so alive, so complete, and inspires me to be better.  
        And now, as Valentine's Day approaches, I can't think of anything I want more than to spend it with <span class="letter-highlight">you</span>.
      </p>
      <p>
        So here it is, love — my question and my deepest desire: <span class="letter-highlight">Will you be my Valentine?</span>
      </p>
    </div>
    
    <div class="letter-details">
      <p><strong>When:</strong> February 7, 2026 at 6:00 PM</p>
      <p><strong>Where:</strong> Jiangnan Hotpot & Grill</p>
      <p style="font-size: 1rem; margin-top: 12px; font-style: italic;">(Or anywhere else your heart desires, my queen ♡)</p>
      <p style="margin-top: 20px;"><strong>Attire:</strong> Dress comfortably — or matching outfits if you're feeling extra cute (please? 🥺)</p>
    </div>
    
    <div class="letter-body">
      <p>
        I can't wait to see you there, to share a warm meal, steal glances, make you laugh, and create another beautiful memory together.
      </p>
    </div>
    
    <div class="letter-signature">
      Forever yours,<br>
      <span style="margin-top: 12px; display: inline-block;">Your Love,<br>Jervine ♡</span>
    </div>
    
    <div class="letter-hearts">💕 &nbsp; ✨ &nbsp; 💖 &nbsp; ✨ &nbsp; 💕</div>

    <button id="print-letter-btn" onclick="window.print()">
      🖨️ Print this letter for keeps
    </button>
  </div>
</div>

<script>
// Envelope click
document.getElementById('envelope-container').addEventListener('click', () => {
  const env = document.getElementById('envelope-container');
  env.style.opacity = '0';
  env.style.transform = 'scale(0.8) translateY(60px)';
  setTimeout(() => {
    env.classList.add('hidden');
    document.getElementById('question-container').classList.remove('hidden');
    document.getElementById('question-container').classList.add('visible');
  }, 1000);
});

// Password toggle
const passwordToggle = document.getElementById("passwordToggle");
const passwordInput = document.getElementById("password");

passwordToggle.addEventListener("click", () => {
  if (passwordInput.type === "password") {
    passwordInput.type = "text";
    passwordToggle.textContent = "🙈";
  } else {
    passwordInput.type = "password";
    passwordToggle.textContent = "👁️";
  }
});

// Login flow with validation
const loginForm = document.getElementById("loginForm");
const loginCard = document.getElementById("loginCard");
const loader = document.getElementById("loader");
const error = document.getElementById("error");
const usernameInput = document.getElementById("username");
const welcomeScreen = document.getElementById("welcome-screen");

loginForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  error.textContent = "";
  
  const username = usernameInput.value;
  const password = passwordInput.value;
  
  if (username !== "admin" || password !== "admin242529") {
    error.textContent = "Incorrect username or password";
    passwordInput.value = "";
    passwordInput.focus();
    return;
  }
  
  loader.style.display = "flex";

  await new Promise(r => setTimeout(r, 2500));
  loader.style.display = "none";

  loginCard.classList.add("fade-out");

  setTimeout(() => {
    loginCard.classList.add("hidden");
    welcomeScreen.classList.remove("hidden");
    welcomeScreen.style.display = "flex";
    
    setTimeout(() => {
      document.body.classList.add("pink-mode");
      welcomeScreen.style.opacity = "0";
      welcomeScreen.style.transition = "opacity 1s ease";
      
      setTimeout(() => {
        welcomeScreen.classList.add("hidden");
        welcomeScreen.style.display = "none";
        document.getElementById("envelope-container").classList.remove("hidden");
        document.getElementById("envelope-container").classList.add("visible");
      }, 1000);
    }, 2000);
  }, 1400);
});

// Close popup function
function closePopup() {
  document.getElementById("popup").classList.remove("show");
}

// No button logic
let noCount = 0;
const predefinedPositions = [
  { left: '15%', top: '20%' },
  { left: '70%', top: '15%' },
  { left: '10%', top: '70%' },
  { left: '75%', top: '65%' },
  { left: '40%', top: '15%' },
  { left: '20%', top: '50%' },
  { left: '65%', top: '40%' },
  { left: '30%', top: '75%' }
];

const noBtn = document.getElementById("noBtn");
const popup = document.getElementById("popup");
const popupVideo = document.getElementById("popupVideo");
const popupText = document.getElementById("popupText");
const sadCatOverlay = document.getElementById("sad-cat-overlay");
const evilVideo = document.getElementById("evilVideo");

noBtn.onclick = (e) => {
  if (noCount === 0) {
    noCount++;
    popupVideo.src = "/static/assets/hamster.mp4";
    popupText.textContent = "Wait… really? 🥺";
    popup.classList.add("show");
    setTimeout(() => {
      popupVideo.play().catch(e => console.log("Video play failed:", e));
    }, 100);
  } else if (noCount === 1) {
    noCount++;
    setTimeout(() => sadCatOverlay.classList.add("show"), 50);
    setTimeout(() => {
      sadCatOverlay.classList.remove("show");
    }, 3000);
  } else {
    const posIndex = (noCount - 2) % predefinedPositions.length;
    const pos = predefinedPositions[posIndex];
    
    noBtn.style.position = "fixed";
    noBtn.style.left = pos.left;
    noBtn.style.top = pos.top;
    noBtn.style.transform = "translate(-50%, -50%)";
    noBtn.style.transition = "left 0.4s cubic-bezier(0.4, 0, 0.2, 1), top 0.4s cubic-bezier(0.4, 0, 0.2, 1)";
    
    if (noCount === 2) {
      evilVideo.src = "/static/assets/muhehehe.mp4";
      evilVideo.classList.remove("hidden");
      setTimeout(() => {
        evilVideo.play().catch(e => console.log("Evil play failed:", e));
      }, 300);
    }
    noCount++;
  }
};

// Yes button → show letter
const letterBGM = document.getElementById("letterBGM");

document.getElementById("yesBtn").onclick = () => {
  const questionContainer = document.getElementById("question-container");
  const letterScreen = document.getElementById("letter-screen");
  
  evilVideo.classList.add("hidden");
  evilVideo.pause();
  
  questionContainer.style.opacity = '0';
  questionContainer.style.transform = 'translateY(60px)';
  setTimeout(() => {
    questionContainer.classList.add("hidden");
    letterScreen.classList.remove("hidden");
    letterScreen.style.display = "flex";
    
    letterBGM.play().catch(e => {
      console.log("BGM autoplay blocked:", e);
      const playHint = document.createElement('div');
      playHint.style.cssText = 'position: fixed; top: 20px; right: 20px; background: rgba(214, 48, 49, 0.9); color: white; padding: 12px 20px; border-radius: 25px; font-size: 0.9rem; cursor: pointer; z-index: 200; box-shadow: 0 4px 15px rgba(0,0,0,0.2);';
      playHint.textContent = '🔊 Tap to play music';
      playHint.onclick = () => {
        letterBGM.play();
        playHint.remove();
      };
      document.body.appendChild(playHint);
    });
  }, 1000);
};
</script>
</body>
</html>
    """

    return render_template_string(html)


if __name__ == '__main__':
    os.makedirs("static/assets", exist_ok=True)
    app.run(debug=True)
