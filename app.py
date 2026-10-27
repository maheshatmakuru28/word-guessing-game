from flask import Flask, render_template_string, request, session
import random
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")

WORDS = {
    "APPLE": "🍎 A fruit that can be red or green",
    "TIGER": "🐅 A wild animal with stripes",
    "PYTHON": "🐍 A popular programming language",
    "GITHUB": "💻 A platform for hosting code",
    "PLANET": "🌍 Earth is one of these",
    "BANANA": "🍌 A long yellow fruit",
    "LAPTOP": "💻 A portable computer",
    "SCHOOL": "🏫 A place where students learn",
    "GARDEN": "🌷 A place where flowers grow",
    "ROCKET": "🚀 A vehicle used in space",
    "FLOWER": "🌺 A colorful part of a plant",
    "DOCTOR": "🩺 A person who treats patients",
    "CAMERA": "📸 A device used to take photos",
    "MONKEY": "🐒 An animal that climbs trees",
    "ORANGE": "🍊 A citrus fruit",
    "BRIDGE": "🌉 A structure that crosses a river",
    "POCKET": "👖 A small pouch in clothing",
    "WINDOW": "🪟 An opening in a wall",
    "MOBILE": "📱 A phone you can carry",
    "CASTLE": "🏰 A large fortified building",
}

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>Word Master 3D</title>

<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    min-height: 100vh;
    padding: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: Arial, sans-serif;
    color: white;
    background: linear-gradient(-45deg,
        #090920, #25105c, #071e42, #3b0764);
    background-size: 400% 400%;
