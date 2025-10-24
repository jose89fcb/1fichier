import requests
from datetime import datetime

EMAIL = ""      # Tu email 1fichier
PASSWORD = ""   # Tu contraseña

url = "https://1fichier.com/console/account.pl"

# Diccionario de meses en español
MESES = {
    1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
    5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
    9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
}

def main():
    try:
        response = requests.post(url, data={"user": EMAIL, "pass": PASSWORD}, timeout=10)
        response.raise_for_status()

        timestamp_text = response.text.strip()
        try:
            timestamp = int(timestamp_text)
        except ValueError:
            print("No se pudo interpretar la respuesta:")
            print(response.text)
            return

        if timestamp == 0:
            print("Tu cuenta no tiene suscripción premium activa.")
            return

        # Fecha de expiración exacta
        valid_until = datetime.fromtimestamp(timestamp)

        # Calcular tiempo restante desde ahora
        now = datetime.now()
        remaining = valid_until - now
        if remaining.total_seconds() < 0:
            print("Tu suscripción ya ha expirado.")
            return

        dias = remaining.days
        horas = remaining.seconds // 3600
        minutos = (remaining.seconds % 3600) // 60
        segundos = remaining.seconds % 60

        # Formatear fecha en español
        formatted_date = f"{valid_until.day} {MESES[valid_until.month]} {valid_until.year}, " \
                         f"{valid_until.hour:02d}:{valid_until.minute:02d}:{valid_until.second:02d}"

        print(f"Tu cuenta premium expira el: {formatted_date} "
              f"({dias} días, {horas} horas, {minutos} minutos, {segundos} segundos restantes)")

    except requests.exceptions.RequestException as e:
        print("Error en la conexión:", e)

if __name__ == "__main__":
    main()
