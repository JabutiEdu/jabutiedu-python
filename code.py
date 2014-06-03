import web
import hashlib
import os
import sys
import RPi.GPIO as GPIO
import time

db = web.database(dbn='mysql', user='root', pw='jabutiedu', db='jabuti')
def parar():
  GPIO.output(23, GPIO.LOW)
  GPIO.output(24, GPIO.LOW)
  GPIO.output(17, GPIO.LOW)
  GPIO.output(22, GPIO.LOW)
  GPIO.cleanup()

def desligar():
  GPIO.output(9, GPIO.LOW)
  GPIO.output(11, GPIO.LOW)
  GPIO.cleanup()

urls = ("/login", "login",
        "/exec/(.+)", "executar",
        "/modulo1", "modulo1",
        "/cadastro", "signup",
        "/", "dashboard"
)

app = web.application(urls, globals())
render = web.template.render('templates/')
if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DBStore(db, 'sessions'), initializer={'logged': 0, 'username': 0, 'permission': 0})
    web.config._session = session
else:
    session = web.config._session

class dashboard:        
    def GET(self):
        if session.logged:
            return render.dashboard(session.username)
        else:
            raise web.redirect('/login')
class login:
    def GET(self):
        return render.login()
    def POST(self):
        data = web.input()
        username = data.username
        db_data = db.select('users', where='username=$username', vars=locals())[0]
        digest = ""
        digest = hashlib.sha1("raspio" + data.password).hexdigest()
        print data.password
        print digest
        print db_data['password']
        if digest == db_data['password']:
            session.logged = 1
            session.username = data.username
            session.permission = db_data['permission']
            print session.logged
            return web.seeother('/')
        else:
            return "Login Failed"
class signup:
    def GET(self):
        return render.signup()
    def POST(self):
        data = web.input()
        password = ""
        password = hashlib.sha1("raspio" + data.password).hexdigest()
        db.insert('users', username = data.username, password = password, permission = '0')
        return web.seeother("/login")
class executar:
    def GET(self, message):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(23, GPIO.OUT)
        GPIO.setup(24, GPIO.OUT)
        GPIO.setup(17, GPIO.OUT)
        GPIO.setup(22, GPIO.OUT)
        GPIO.setup(9, GPIO.OUT)
        GPIO.setup(11, GPIO.OUT)
        GPIO.output(23, GPIO.LOW)
        GPIO.output(24, GPIO.LOW)
        GPIO.output(17, GPIO.LOW)
        GPIO.output(22, GPIO.LOW)
        if message == 'pf':
            GPIO.output(24, GPIO.HIGH)
            GPIO.output(23, GPIO.LOW)
            GPIO.output(17, GPIO.HIGH)
            GPIO.output(22, GPIO.LOW)
            time.sleep(1)
            parar()
        elif message == 'pt':
            GPIO.output(24, GPIO.LOW)
            GPIO.output(23, GPIO.HIGH)
            GPIO.output(22, GPIO.HIGH)
            GPIO.output(17, GPIO.LOW)
            time.sleep(1)
            parar()
        elif message == 'pe':
            GPIO.output(23, GPIO.LOW)
            GPIO.output(24, GPIO.HIGH)
            GPIO.output(22, GPIO.HIGH)
            GPIO.output(17, GPIO.LOW)
            time.sleep(0.3)
            parar()
        elif message == 'lde':
            GPIO.output(9, GPIO.HIGH)
            GPIO.output(11, GPIO.HIGH)
            time.sleep(2)
            desligar()
        elif message == 'ld':
            GPIO.output(9, GPIO.HIGH)
            time.sleep(2)
            desligar()
        elif message == 'le':
            GPIO.output(11, GPIO.HIGH)
            time.sleep(2)
            desligar()
        elif message == 'pd':
            GPIO.output(24, GPIO.LOW)
            GPIO.output(23, GPIO.HIGH)
            GPIO.output(17, GPIO.HIGH)
            GPIO.output(22, GPIO.LOW)
            time.sleep(0.3)
            parar()
        elif message == 'som':
            os.system("espeak \"oi, eu sou a jabuti edu\" -v portugal -s140 -p60 -g2 -a100")
        elif message == 'musica':
            os.system("mpg321 /home/pi/musica.mp3")
        return "OK"
class modulo1:
    def GET(self):
        if session.logged:
             return render.modulo1()
        else:
             return web.redirect('/login')
if __name__ == "__main__":
    app.run()
