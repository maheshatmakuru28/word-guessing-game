from flask import Flask, render_template_string, jsonify, request
import random

app = Flask(__name__)

HTML = """
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
    font-family: Arial, sans-serif;
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
    overflow-x: hidden;
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
    padding: 30px 22px;
    border-radius: 25px;
    text-align: center;
    background: rgba(10, 10, 35, 0.72);
    border: 
