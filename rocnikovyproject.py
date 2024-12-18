import network
import socket
from machine import Pin
import time

# Настройки для точки доступа
ssid = 'PIPICo1'  # Название вашей Wi-Fi сети
password = '12345678'  # Пароль для Wi-Fi точки доступа

# Инициализация LED на пине GPIO 15 (или другом пине по необходимости)
led = Pin("LED", Pin.OUT)

# Настройка точки доступа (Access Point)
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, password=password)

# Отображение IP-адреса точки доступа
print('Точка доступа создана. IP-адрес точки доступа:', ap.ifconfig()[0])

# Создание веб-сервера
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print('Сервер работает на:', addr)

# Основной цикл для сервера
while True:
    cl, addr = s.accept()
    print('Подключен клиент:', addr)
    request = cl.recv(1024)
    request = str(request)
    print('Запрос:', request)

    if '/ledon' in request:
        led.value(1)  # Включить LED
    elif '/ledoff' in request:
        led.value(0)  # Выключить LED

    # Создание HTML ответа с новогодним стилем и красно-белым фоном
    response = """HTTP/1.1 200 OK
Content-Type: text/html
Connection: close

<!DOCTYPE HTML>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0"> <!-- Обеспечение адаптивности -->
<style>
    body {
        font-family: 'Arial', sans-serif;
        text-align: center;
        margin: 0;
        padding: 0;
        background: linear-gradient(45deg, #ff0000 25%, #ffffff 25%, #ffffff 50%, #ff0000 50%, #ff0000 75%, #ffffff 75%, #ffffff); /* Красно-белый фон */
        background-size: 56.57px 56.57px; /* Размер полос */
        animation: snowflakes 10s linear infinite;
    }

    h1 {
        font-size: 3em; 
        color: #ff6347;
        text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5);
        margin-top: 50px;
    }

    button {
        background-color: #4CAF50;
        color: white;
        padding: 20px 40px;
        margin: 20px;
        font-size: 1.5em;
        border: none;
        border-radius: 10px;
        cursor: pointer;
        transition: background-color 0.3s ease;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
    }

    button:hover {
        background-color: #45a049;
    }

    /* Анимация снежинок */
    @keyframes snowflakes {
        0% {
            transform: translateY(-100px);
        }
        100% {
            transform: translateY(100vh);
        }
    }

    /* Эффект плавающих снежинок */
    .snowflake {
        position: absolute;
        color: white;
        font-size: 2em;
        animation: fall 10s linear infinite;
    }

    @keyframes fall {
        0% { transform: translateY(-10px); opacity: 1; }
        100% { transform: translateY(100vh); opacity: 0; }
    }
</style>
</head>
<body>
    <h1>Happy New Year</h1>
    <p><a href="/ledon"><button>ON LED</button></a></p>
    <p><a href="/ledoff"><button>OFF LED</button></a></p>
    
    <!-- Снежинки -->
    <div class="snowflake" style="left: 20%; animation-duration: 8s; animation-delay: 0s;">XOXOXO</div>
    <div class="snowflake" style="left: 40%; animation-duration: 12s; animation-delay: 1s;">Merry Christmas</div>
    <div class="snowflake" style="left: 60%; animation-duration: 10s; animation-delay: 2s;">WOOOOOOW</div>
    <div class="snowflake" style="left: 80%; animation-duration: 15s; animation-delay: 3s;">XOXOXO</div>
</body>
</html>
"""
    cl.send(response)
    cl.close()
