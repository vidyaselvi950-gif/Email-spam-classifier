from flask import Flask, request, render_template_string
import joblib

app = Flask(__name__)

model = joblib.load("model/spam_classifier.pkl")

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Cosmic Email Spam Classifier</title>

    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
        }

        body {
            min-height: 100vh;
            overflow: hidden;
            display: flex;
            justify-content: center;
            align-items: center;
            background:
                radial-gradient(circle at 20% 20%, #392070 0%, transparent 25%),
                radial-gradient(circle at 80% 30%, #143c72 0%, transparent 25%),
                radial-gradient(circle at 50% 90%, #32145e 0%, transparent 30%),
                #050718;
            position: relative;
            color: white;
        }

        .stars,
        .stars2,
        .stars3 {
            position: absolute;
            inset: 0;
            background-repeat: repeat;
            pointer-events: none;
        }

        .stars {
            background-image:
                radial-gradient(circle, white 1px, transparent 1px);
            background-size: 80px 80px;
            animation: moveStars 18s linear infinite;
            opacity: 0.7;
        }

        .stars2 {
            background-image:
                radial-gradient(circle, #9ee7ff 1px, transparent 1px);
            background-size: 130px 130px;
            animation: moveStars 28s linear infinite reverse;
            opacity: 0.5;
        }

        .stars3 {
            background-image:
                radial-gradient(circle, #dca8ff 1.5px, transparent 1.5px);
            background-size: 180px 180px;
            animation: moveStars 35s linear infinite;
            opacity: 0.5;
        }

        @keyframes moveStars {
            from {
                transform: translateY(0);
            }

            to {
                transform: translateY(80px);
            }
        }

        .planet {
            position: absolute;
            width: 180px;
            height: 180px;
            border-radius: 50%;
            right: -50px;
            top: 60px;
            background:
                radial-gradient(circle at 35% 30%, #ffb6ff, #8c4cff 45%, #29106b 75%);
            box-shadow:
                0 0 40px #884cff,
                0 0 90px rgba(130, 70, 255, 0.5);
            animation: floatPlanet 5s ease-in-out infinite;
        }

        @keyframes floatPlanet {
            0%, 100% {
                transform: translateY(0);
            }

            50% {
                transform: translateY(20px);
            }
        }

        .small-planet {
            position: absolute;
            width: 75px;
            height: 75px;
            border-radius: 50%;
            left: 35px;
            bottom: 70px;
            background:
                radial-gradient(circle at 35% 30%, #77e7ff, #246cff, #111d67);
            box-shadow: 0 0 35px #299fff;
            animation: floatSmall 6s ease-in-out infinite;
        }

        @keyframes floatSmall {
            0%, 100% {
                transform: translateY(0);
            }

            50% {
                transform: translateY(-25px);
            }
        }

        .container {
            position: relative;
            z-index: 5;
            width: 90%;
            max-width: 700px;
            padding: 42px;
            text-align: center;

            background: rgba(10, 15, 45, 0.72);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 30px;

            backdrop-filter: blur(18px);

            box-shadow:
                0 0 30px rgba(120, 80, 255, 0.35),
                0 25px 70px rgba(0, 0, 0, 0.6);

            animation: cardAppear 1s ease;
        }

        @keyframes cardAppear {
            from {
                opacity: 0;
                transform: translateY(30px) scale(0.96);
            }

            to {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
        }

        .icon {
            font-size: 55px;
            margin-bottom: 12px;
            animation: floatIcon 3s ease-in-out infinite;
        }

        @keyframes floatIcon {
            0%, 100% {
                transform: translateY(0);
            }

            50% {
                transform: translateY(-8px);
            }
        }

        h1 {
            font-size: 38px;
            margin-bottom: 15px;
            color: #ffffff;
            text-shadow: 0 0 15px #9b6cff;
        }

        .subtitle {
            color: #b9c7ff;
            font-size: 16px;
            margin-bottom: 28px;
        }

        textarea {
            width: 100%;
            height: 150px;
            resize: none;
            padding: 18px;
            border-radius: 18px;
            border: 1px solid rgba(255,255,255,0.2);
            background: rgba(255,255,255,0.08);
            color: white;
            font-size: 16px;
            outline: none;
            transition: 0.3s;
        }

        textarea:focus {
            border-color: #9b6cff;
            box-shadow: 0 0 20px rgba(155,108,255,0.4);
        }

        textarea::placeholder {
            color: #9ba8d4;
        }

        button {
            margin-top: 20px;
            padding: 14px 35px;
            border: none;
            border-radius: 30px;
            background: linear-gradient(135deg, #7b4dff, #299fff);
            color: white;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 0 25px rgba(100,100,255,0.5);
            transition: 0.3s;
        }

        button:hover {
            transform: scale(1.05);
            box-shadow: 0 0 35px rgba(120,150,255,0.8);
        }

        .result {
            margin-top: 25px;
            padding: 18px;
            border-radius: 18px;
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.15);
            font-size: 20px;
            font-weight: bold;
        }

        .safe {
            color: #63ffb2;
            text-shadow: 0 0 12px rgba(99,255,178,0.6);
        }

        .spam {
            color: #ff6b9d;
            text-shadow: 0 0 12px rgba(255,107,157,0.6);
        }

        .footer {
            margin-top: 22px;
            font-size: 12px;
            color: #7783ad;
        }

        @media (max-width: 600px) {
            .container {
                padding: 28px;
            }

            h1 {
                font-size: 30px;
            }

            .planet {
                width: 120px;
                height: 120px;
            }

            .small-planet {
                width: 55px;
                height: 55px;
            }
        }
    </style>
</head>

<body>

    <div class="stars"></div>
    <div class="stars2"></div>
    <div class="stars3"></div>

    <div class="planet"></div>
    <div class="small-planet"></div>

    <div class="container">

        <div class="icon">🚀</div>

        <h1>Cosmic Email Spam Classifier</h1>

        <div class="subtitle">
            Detect whether an email is safe or spam using Machine Learning
        </div>

        <form method="POST">

            <textarea
                name="email"
                placeholder="Paste your email message here..."
                required
            ></textarea>

            <button type="submit">
                ✨ Analyze Email
            </button>

        </form>

        {% if prediction %}

        <div class="result">

            {% if prediction == "Spam" %}
                <div class="spam">🚨 This email is SPAM</div>
            {% else %}
                <div class="safe">🛡️ This email is SAFE</div>
            {% endif %}

        </div>

        {% endif %}

        <div class="footer">
            AI & Data Science • Machine Learning Project
        </div>

    </div>

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():

    prediction = None

    if request.method == "POST":

        email = request.form["email"]

        result = model.predict([email])[0]

        if result == 1:
            prediction = "Spam"
        else:
            prediction = "Safe"

    return render_template_string(
        HTML,
        prediction=prediction
    )


if __name__ == "__main__":
    app.run(debug=True)