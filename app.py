from flask import Flask, render_template_string, request, session
import random
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")

WORDS = {
    "APPLE": "A fruit that can be red or green",
    "TIGER": "A large wild cat with stripes",
    "PYTHON": "A popular programming language",
    "GITHUB": "A platform for storing code",
    "PLANET": "Earth is one of these",
    "BANANA": "A long yellow fruit",
    "ORANGE": "A citrus fruit",
    "LAPTOP": "A portable computer",
    "SCHOOL": "A place where students learn",
    "GARDEN": "A place where flowers grow",
    "MONKEY": "An animal that can climb trees",
    "ROCKET": "A vehicle used to travel into space",
    "FLOWER": "A colorful part of a plant",
    "DOCTOR": "A person who treats patients",
    "CAMERA": "A device used to take photographs"
}

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
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
            align-items: center;
            justify-content: center;
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea, #764ba2);
        }

        .game {
            background: white;
            padding: 30px 22px;
            border-radius: 20px;
            width: 100%;
            max-width: 450px;
            text-align: center;
            box-shadow: 0 15px 40px #0003;
        }

        h1 {
            color: #6246c7;
        }

        .stats {
            display: flex;
            justify-content: space-around;
            gap: 10px;
            margin: 20px 0;
        }

        .stat {
            background: #f0edff;
            border-radius: 12px;
            padding: 12px;
            flex: 1;
        }

        .stat strong {
            display: block;
            color: #6246c7;
            font-size: 22px;
            margin-top: 5px;
        }

        .word {
            font-size: 30px;
            font-weight: bold;
            letter-spacing: 7px;
            color: #6246c7;
            margin: 28px 0;
            overflow-wrap: anywhere;
        }

        .hint {
            background: #fff8df;
            padding: 14px;
            border-radius: 10px;
            color: #66521a;
            line-height: 1.5;
        }

        input {
            width: 100%;
            padding: 14px;
            margin-top: 15px;
            border: 2px solid #ddd;
            border-radius: 10px;
            font-size: 18px;
            text-align: center;
            text-transform: uppercase;
        }

        input:focus {
            outline: none;
            border-color: #6246c7;
        }

        button {
            width: 100%;
            padding: 14px;
            margin-top: 12px;
            border: none;
            border-radius: 10px;
            background: #6246c7;
            color: white;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
        }

        button:hover {
            background: #4931a5;
        }

        .restart {
            background: #25223b;
        }

        .message {
            font-weight: bold;
            margin: 18px 0;
            line-height: 1.5;
        }

        .footer {
            color: #888;
            font-size: 12px;
            margin-top: 22px;
        }
    </style>
</head>

<body>
<div class="game">
    <h1>🎯 Word Guess</h1>
    <p>Can you guess the hidden word?</p>

    <div class="stats">
        <div class="stat">
            Attempts
            <strong>{{ attempts }}</strong>
        </div>
        <div class="stat">
            Score
            <strong>{{ score }}</strong>
        </div>
    </div>

    <div class="word">{{ display_word }}</div>

    <div class="hint">
        💡 <strong>Hint:</strong> {{ hint }}
    </div>

    {% if message %}
        <div class="message">{{ message }}</div>
    {% endif %}

    {% if not finished %}
        <form method="POST" action="/">
            <input
                type="text"
                name="guess"
                placeholder="Enter your guess"
                maxlength="20"
                autocomplete="off"
                required
                autofocus
            >
            <button type="submit">Check Word 🚀</button>
        </form>
    {% else %}
        <p>The correct word was <strong>{{ answer }}</strong>.</p>
    {% endif %}

    <form method="POST" action="/new">
        <button class="restart" type="submit">
            🔄 New Game
        </button>
    </form>

    <div class="footer">Word Guessing Game • Built with Python</div>
</div>
</body>
</html>
"""


def start_game():
    word, hint = random.choice(list(WORDS.items()))

    session["word"] = word
    session["hint"] = hint
    session["attempts"] = 6
    session["score"] = session.get("score", 0)
    session["finished"] = False
    session["guesses"] = []
    session["message"] = "You have 6 attempts. Good luck!"


@app.route("/", methods=["GET", "POST"])
def home():
    if "word" not in session:
        start_game()

    if request.method == "POST" and not session["finished"]:
        guess = request.form.get("guess", "").strip().upper()
        word = session["word"]

        if not guess.isalpha():
            session["message"] = "Please enter letters only."

        elif len(guess) != len(word):
            session["message"] = (
                f"Enter a word with exactly {len(word)} letters."
            )

        elif guess in session["guesses"]:
            session["message"] = "You already tried that word!"

        else:
            session["guesses"].append(guess)

            if guess == word:
                points = session["attempts"] * 10
                session["score"] += points
                session["finished"] = True
                session["message"] = (
                    f"🎉 Correct! You earned {points} points!"
                )
            else:
                session["attempts"] -= 1

                if session["attempts"] == 0:
                    session["finished"] = True
                    session["message"] = (
                        "Game over! Better luck next time."
                    )
                else:
                    session["message"] = (
                        "❌ Incorrect! Try another word."
                    )

    word = session["word"]
    guesses = session["guesses"]

    # Reveal letters from correctly positioned guesses.
    display_word = " ".join(
        letter if any(
            len(g) == len(word) and g[i] == letter
            for g in guesses
        ) else "_"
        for i, letter in enumerate(word)
    )

    if session["finished"]:
        display_word = " ".join(word)

    return render_template_string(
        HTML,
        display_word=display_word,
        hint=session["hint"],
        attempts=session["attempts"],
        score=session["score"],
        message=session["message"],
        finished=session["finished"],
        answer=word
    )


@app.route("/new", methods=["POST"])
def new_game():
    # Preserve the current score when starting a new round.
    start_game()
    return home()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
