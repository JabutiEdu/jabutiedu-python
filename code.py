import web
import hashlib
from twitter import *
import os
import sys
import RPi.GPIO as GPIO
import time
import random
import string

t = Twitter(auth=OAuth('2208893204-EnDOnXeRjRgesZ9ZpAqjVzG0ABKjaekoZcExU9m', '5YViHIgTiKmTYogJOJ9bedfeMLKHOZPGzwcJI1tDKLRKB', 
                      'Q9BYDAmIYl93w40wSudg', '4HuF5xVvNRWjBufX1HnZK6V2Zia1cn8SkATWH8ZTO0'))

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
        "/cadastro", "cadastro",
        "/", "dashboard"
)

app = web.application(urls, globals())
render = web.template.render('templates/')

class dashboard:
    def GET(self):
        logado = web.cookies(logado = False).logado
        if logado:
            return render.dashboard(web.cookies().usuario)
        else:
            raise web.seeother("/login")
class login:
    def GET(self):
        return render.index()
    def POST(self):
        data = web.input()
        query = 'usuario = \"' + data.username + '\"'
        dados = db.select('usuarios', where=query).list()
        dados = dados[0]
        print dados.senha
        if data.senha == dados.senha:
            web.setcookie("logado", True)
            web.setcookie("usuario", data.username)
            raise web.seeother("/")
        else:
            raise web.seeother("/login")
class executar:
    def GET(self, message):
        code = str(random.randint(10000, 99999999))
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
        return render.modulo1()
if __name__ == "__main__":
    app.run()
