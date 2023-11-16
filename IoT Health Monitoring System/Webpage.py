# <meta http-equiv="refresh" content="10">

class Web_Class():
    def __init__(self):
        pass
    
    def HTML_main(self,room_temp,room_hum, body_temp, pulse_rate, Sp02,Heading_rtemp, Body_rtemp, Heading_hum, Body_hum, Heading_temp,Body_temp, Heading_Sp02, Body_Sp02, Heading_bpm, Body_bpm ):
        html = """
                <!DOCTYPE html>
                <html>

                <head>
                <title>My IOT Project - 22002780</title>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <script src="https://kit.fontawesome.com/2cebbf1e25.js" crossorigin="anonymous"></script>
                

                <!-- Html style -->
                <style>
                /* style for main red card */
                .main-card {
                display: flex;
                justify-content: center;
                background-color: #4CAF50;
                height: 150px;
                align-items: center;
                }

                .main-card p {
                color: #fff;
                font-size: 30px;

                }

                /* style for flip card */
                /* flip card box */
                .flip-card-box {
                margin-top: 20px;
                display: flex;
                flex-direction: column;
                align-items: center;
                }

                /* outer flip card */
                .flip-card {
                padding: 10px;
                width: 300px;
                height: 200px;
                perspective: 1000px;
                margin-bottom: 50px;
                }

                /* inner flip card */
                .flip-card-inner {
                position: relative;
                width: 100%;
                height: 100%;
                transition: transform 0.6s;
                transform-style: preserve-3d;
                box-shadow: rgba(0, 0, 0, 0.08) 0px 4px 100px;
                }

                /* rotate style */
                .flip-card.flip-card-flipped .flip-card-inner {
                transform: rotateY(180deg);
                }

                /* style for both front and back */
                .flip-card-front,
                .flip-card-back {
                position: absolute;
                width: 100%;
                height: 100%;
                backface-visibility: hidden;
                text-align: center;
                }

                /* style for front card */
                .flip-card-front {
                padding: 10px;
                background-color: #fff;
                color: black;
                }

                /* style for back card */
                .flip-card-back {
                padding: 10px;
                background-color: #4CAF50;
                color: white;
                transform: rotateY(180deg);
                }

                .main_card_text {
                justify-items: center;
                font-size: 25px;
                }

                .parameters {
                font-size: 28px;
                justify-items: center;
                font-family: sans-serif;
                margin-top: -50;

                }
                .parameters_temp {
                font-size: 25px;
                justify-items: center;
                font-family: sans-serif;
                margin-top: -50;
                }
                .value {
                font-size: 25px;
                justify-items: center;
                }
                </style>
                </head>

                <!-- Html body -->

                <body>

                <!-- Main card section -->
                <section>
                <div class="main-card">
                <div>
                <p align="center" style="font-family:verdana"><B>Health Monitoring System</B></p>
                <p align="center" style="font-family:Times; font-size: 24px">Internet of Health Things</p>
                </div>
                </div>
                </section>

                <!-- flip card box -->
                <div class="flip-card-box">
                <!-- flip card one -->
                <section>
                <div class="flip-card" onclick="flipCard(event)">
                <div class="flip-card-inner">
                <div class="flip-card-front">

                <h1 class="parameters"> <i class="fas fa-temperature-half fa-beat fa-xl" style="color: #cc0f0f;"></i>
                Room Temperature</h1>

                <p class="value">""" + str(room_temp) +""" &deg;C</p>
                </div>
                <div class="flip-card-back">
                <h1>""" + str(Heading_rtemp) +"""</h1>
                <p>""" + str(Body_rtemp) +"""</p>
                </div>
                </div>
                </div>
                </section>



                <!-- flip card two -->
                <section>
                <div class="flip-card" onclick="flipCard(event)">
                <div class="flip-card-inner">
                <div class="flip-card-front">
                <h1 class="parameters"><i class="fa-solid fa-droplet fa-bounce fa-2xl" style="color: #346fd5;"></i> Humidity</h1>
                <p class="value">""" + str (room_hum)+""" %</p>
                </div>
                <div class="flip-card-back">
                <h1>""" + str(Heading_hum) +"""</h1>
                <p>""" + str(Body_hum) +"""</p>
                </div>
                </div>
                </div>
                </section>

                <!-- flip card three -->
                <section>
                <div class="flip-card" onclick="flipCard(event)">
                <div class="flip-card-inner">
                <div class="flip-card-front">
                <h1 class="parameters_temp"><i class="fas fa-thermometer fa-shake fa-2xl" style="color: #cc0f0f;"></i> Body Temperature</h1>
                <p class="value">"""+ str(body_temp) +""" &deg;C</p>
                </div>
                <div class="flip-card-back">
                <h1>""" + str(Heading_temp) +"""</h1>
                <p>""" + str(Body_temp) +"""</p>
                </div>
                </div>
                </div>
                </section>

                <!-- flip card four -->
                <section>
                <div class="flip-card" onclick="flipCard(event)">
                <div class="flip-card-inner">
                <div class="flip-card-front">
                <h1 class="parameters"><i class="fa-solid fa-heart-pulse fa-beat fa-2xl" style="color: #e63205;"></i> Heart Rate</h1>
                <p class="value">""" + str(pulse_rate) +"""BPM</p>
                </div>
                <div class="flip-card-back">
                <h1>""" + str(Heading_bpm) +"""</h1>
                <p>""" + str(Body_bpm) +"""</p>
                </div>
                </div>
                </div>
                </section>

                <!-- flip card five -->
                <section>
                <div class="flip-card" onclick="flipCard(event)">
                <div class="flip-card-inner">
                <div class="flip-card-front">
                <h1 class="parameters"> <i class="fa-solid fa-mask-ventilator fa-fade fa-2xl" style="color: #03358c;"></i> Sp02</h1>
                <p class="value">""" + str(Sp02)+"""%</p>
                </div>
                <div class="flip-card-back">
                <h1>""" + str(Heading_Sp02) +"""</h1>
                <p>""" + str(Body_Sp02) +"""</p>
                </div>
                </div>
                </div>
                </section>
                </div>


                <!-- script for card flip-->
                <script>
                document.body.appendChild(pElement);
                function flipCard(event) {
                event.currentTarget.classList.toggle('flip-card-flipped');
                }
                </script>
                </body>

                </html>
                """
        return html
    
    def HTML_reg(self):
        html = '''<!DOCTYPE html>
<html>
<head>
    <title>User Registration Form</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>

        * {
            box-sizing: border-box;
        }

        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
        }

        .title {
            background-color: #eaf7ed;
            padding: 10px;
            margin-bottom: 20px;
        }

        h2 {
            text-align: center;
            margin: 0;
        }
        h3 {
            text-align: center;
            margin: 0;
        }

        form {
            max-width: 500px;
            margin: 0 auto;
        }

        label {
            display: inline-block;
            width: 100px;
            font-weight: bold;
            margin-top: 10px;
            vertical-align: top;
        }

        input[type="text"],
        input[type="password"],
        input[type="email"],
        input[type="number"],
        select {
            width: calc(100% - 120px);
            padding: 10px;
            margin-top: 5px;
            border: 1px solid #ccc;
            border-radius: 4px;
            vertical-align: top;
        }

        input[type="submit"] {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            width: 100%;
            margin-top: 10px;
        }

        @media only screen and (max-width: 600px) {
            form {
                max-width: 100%;
            }

            label {
                width: 100%;
                display: block;
            }

            input[type="text"],
            input[type="password"],
            input[type="email"],
            input[type="number"],
            select {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="title">
        <h2>IOT Based Vital Sign Monitoring System</h2>
        
    </div>
        <h3>User Registration</h3>
    <form action="submit.php" method="post">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" required>

        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required>

        <label for="email">Email:</label>
        <input type="email" id="email" name="email" required>

        <label for="age">Age:</label>
        <input type="number" id="age" name="age" required>

        <label for="weight">Weight:</label>
        <input type="number" id="weight" name="weight" required>

        <label for="height">Height:</label>
        <input type="number" id="height" name="height" required>

        <label for="gender">Gender:</label>
        <select id="gender" name="gender" required>
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="other">Other</option>
        </select>

        <input type="submit" value="Submit">
    </form>
</body>
</html>

'''
        return html
    
    def HTML_log(self):
        html = '''
<!DOCTYPE html>
<html>
<head>
    <title>Login Page</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * {
            box-sizing: border-box;
        }

        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
        }

        .container {
            max-width: 400px;
            margin: 0 auto;
            text-align: center;
        }

        .title {
            background-color: #eaf7ed;
            padding: 10px;
            margin-bottom: 20px;
        }

        h2 {
            margin: 0;
        }

        label {
            display: inline-block;
            width: 100px;
            font-weight: bold;
            margin-top: 10px;
            vertical-align: top;
        }

        input[type="text"],
        input[type="password"] {
            width: calc(100% - 120px);
            padding: 10px;
            margin-top: 5px;
            border: 1px solid #ccc;
            border-radius: 4px;
            vertical-align: top;
        }

        input[type="submit"] {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            width: 100%;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="title">
            <h2>IOT Based Vital Sign Monitoring System</h2>
        </div>
        <h3>Login Page</h3>
        <form action="login.php" method="post">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required>

            <br>

            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required>

            <br>

            <input type="submit" value="Login">
        </form>
        <form action="signup.php" method="post">
            <input type="submit" value="Sign up">
        </form>
    </div>
</body>
</html>

'''
        return html

