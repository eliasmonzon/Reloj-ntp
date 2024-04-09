import machine
import utime
import network
import ntptime
from lcd16x2 import LCD_16x2
import wifimgr

# Inicializar el LCD 16x2
lcd = LCD_16x2(rs_pin=16, e_pin=17, d4_pin=10, d5_pin=11, d6_pin=12, d7_pin=13)

# Función para conectar a la red WiFi usando wifimgr
def connect_wifi():
    try:
        print("Conectando a la red WiFi...")
        wlan = wifimgr.get_connection()
        if wlan is None:
            raise OSError("No se pudo conectar a la red WiFi.")
        print("Conexión WiFi establecida:", wlan.ifconfig())
        return True
    except OSError as e:
        print("Error al conectar a la red WiFi:", e)
        return False

# Función para obtener la hora desde el servidor NTP
def get_ntp_time():
    try:
        print("Obteniendo la hora desde el servidor NTP...")
        ntptime.settime()
        return utime.localtime()
    except OSError as e:
        print("Error al obtener la hora desde NTP:", e)
        return None

# Función para mostrar la fecha y hora en el LCD
def display_datetime_on_lcd(datetime_tuple):
    if datetime_tuple is not None:
        # Ajustar la hora para Buenos Aires (UTC-3)
        buenos_aires_hour = (datetime_tuple[3] - 3) % 24
        lcd.clear()
        lcd.display_string("Fecha", row=1)
        lcd.display_string("Hora", row=2)
        lcd.display_string("{:02d}/{:02d}/{:04d}".format(datetime_tuple[2], datetime_tuple[1], datetime_tuple[0]), row=1, col=6)
        lcd.display_string("{:02d}:{:02d}:{:02d}".format(buenos_aires_hour, datetime_tuple[4], datetime_tuple[5]), row=2, col=6)
    else:
        lcd.clear()
        lcd.display_string("Error de hora", row=1)

# Bucle principal
while True:
    try:
        # Intentar conectar a la red WiFi
        if not connect_wifi():
            utime.sleep(5)  # Esperar 5 segundos antes de intentar nuevamente
            continue  # Volver al inicio del bucle para intentar reconectar

        # Obtener la hora desde NTP
        current_time = get_ntp_time()

        # Mostrar la fecha y la hora en el LCD
        display_datetime_on_lcd(current_time)

        # Esperar un tiempo antes de actualizar la hora nuevamente
        utime.sleep(1)

    except KeyboardInterrupt:
        print("\nInterrupción de teclado. Saliendo del programa.")
        break  # Salir del bucle en caso de interrupción de teclado

    except Exception as e:
        print("Error en el bucle principal:", e)
        lcd.clear()
        lcd.display_string("Error", row=1)
        utime.sleep(1)  # Esperar antes de reintentar para evitar bucles rápidos
