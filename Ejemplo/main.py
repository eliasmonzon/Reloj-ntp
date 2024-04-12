import utime
import ntptime
from lcd16x2 import LCD_16x2
import wifimgr

# Inicializar el LCD 16x2
lcd = LCD_16x2(rs_pin=16, e_pin=17, d4_pin=10, d5_pin=11, d6_pin=12, d7_pin=13)
lcd.clear()  
lcd.display_string("Fecha 00/00/00", row=1)
lcd.display_string("Hora  00:00:00", row=2)

# Función para conectar a la red WiFi usando wifimgr
def connect_wifi():
    try:
        print("Conectando a la red WiFi...")
        wlan = wifimgr.get_connection()
        if wlan is None:
            raise Exception("¡Error! No se pudo conectar a la red WiFi.")
        print("Conexión WiFi establecida:", wlan.ifconfig())
        return True
    except Exception as e:
        print("Error al conectar a la red WiFi:", e)
        return False

# Función para obtener la hora desde el servidor NTP
def get_ntp_time():
    try:
        print("Obteniendo la hora desde el servidor NTP...")
        ntptime.settime()
        return utime.localtime()
    except Exception as e:
        print("Error al obtener la hora desde NTP:", e)
        return None

# Función para mostrar la fecha y hora en el LCD
def display_datetime_on_lcd(datetime_tuple):
    if datetime_tuple is not None:
        buenos_aires_hour = (datetime_tuple[3] -3) % 24  # Ajuste de hora para Buenos Aires (UTC-3)
        #lcd.clear()
        lcd.display_string("Fecha", row=1)
        lcd.display_string("Hora", row=2)
        lcd.display_string("{:02d}/{:02d}/{:02d}".format(datetime_tuple[2], datetime_tuple[1], (datetime_tuple[0]%100)), row=1, col=6)
        lcd.display_string("{:02d}:{:02d}:{:02d}".format(buenos_aires_hour, datetime_tuple[4], datetime_tuple[5]), row=2, col=6)

# Bucle principal
while True:
    # Intentar conectar a la red WiFi
    if connect_wifi():
        # Si la conexión WiFi es exitosa, obtener la hora desde NTP
        current_time = get_ntp_time()
        
        # Mostrar la hora en el LCD solo si se obtuvo correctamente
        if current_time is not None:
            display_datetime_on_lcd(current_time)
    
    # Esperar un corto tiempo antes de intentar nuevamente (1 segundo)
    utime.sleep(1)

