from flask import Flask, render_template_string, jsonify
import random

app = Flask(__name__)

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Word Guessing Game</title>

<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    min-height: 100vh;
    padding: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-family: Arial, sans-serif;
    color: white;
    background: linear-gradient(-45deg, #090979, #6a11cb, #2575fc, #00c9a7);
    background-size: 400% 400%;
    animation: gradient 12s ease infinite;
}

@keyframes gradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.container {
    width: 100%;
    max-width: 520px;
    padding: 28px 20px;
    border-radius: 24px;
    text-align: center;
    background: rgba(10, 10, 35, 0.82);
    border: 1px solid rgba(255,255,255,0.25);
    box-shadow: 0 0 35px rgba(0,255,255,0.3);
    backdrop-filter: blur(12px);
    animation: appear 0.7s ease;
}

@keyframes appear {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

h1 {
    color: #ffe66d;
    font-size: clamp(27px, 7vw, 38px);
    text-shadow: 0 0 15px rgba(255,230,109,0.6);
    margin-bottom: 8px;
}

.subtitle {
    color: #dbeafe;
    margin-bottom: 20px;
}

.stats {
    display: flex;
    gap: 10px;
    margin: 20px 0;
}

.stat {
    flex: 1;
    padding: 12px 5px;
    border-radius: 14px;
    background: rgba(255,255,255,0.1);
}

.stat strong {
    display: block;
    font-size: 24px;
    color: #ffe66d;
    margin-bottom: 5px;
}

.stat span {
    font-size: 12px;
    color: #dbeafe;
}

.hint-box {
    padding: 15px;
    margin: 18px 0;
    border-radius: 15px;
    background: rgba(0,255,200,0.09);
    border: 1px solid rgba(0,255,200,0.25);
}

.hint-label {
    color: #5eead4;
    font-size: 12px;
    letter-spacing: 2px;
    margin-bottom: 8px;
}

#hint {
    line-height: 1.5;
    font-size: 16px;
}

#word {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 7px;
    margin: 25px 0;
}

.tile {
    width: 39px;
    height: 48px;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 10px;
    background: linear-gradient(145deg, #ffffff, #b8c8ff);
    color: #181848;
    font-size: 22px;
    font-weight: bold;
    box-shadow: 0 5px 0 #7586c4;
    animation: tileIn 0.3s ease both;
}

.tile.revealed {
    background: linear-gradient(145deg, #6dffb3, #00c9a7);
    color: #063b31;
    box-shadow: 0 5px 0 #078f78;
}

@keyframes tileIn {
    from {
        transform: rotateY(90deg) scale(0.7);
        opacity: 0;
    }
    to {
        transform: rotateY(0) scale(1);
        opacity: 1;
    }
}

input {
    width: 100%;
    padding: 15px;
    border: 2px solid rgba(255,255,255,0.3);
    border-radius: 12px;
    outline: none;
    font-size: 17px;
    text-align: center;
    color: white;
    background: rgba(255,255,255,0.08);
    margin-bottom: 12px;
}

input::placeholder {
    color: #cbd5e1;
}

input:focus {
    border-color: #5eead4;
    box-shadow: 0 0 12px rgba(94,234,212,0.3);
}

button {
    width: 100%;
    padding: 14px;
    border: none;
    border-radius: 12px;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    transition: transform 0.2s, box-shadow 0.2s;
}

button:hover {
    transform: translateY(-2px);
}

.guess-btn {
    background: linear-gradient(90deg, #ffe66d, #ffb86c);
    color: #11113b;
    box-shadow: 0 5px 0 #bc783e;
}

.new-btn {
    margin-top: 12px;
    color: white;
    background: linear-gradient(90deg, #7c3aed, #2563eb);
}

button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

#message {
    min-height: 28px;
   
