import time
import lora
from config import dev_eui, app_eui, app_key

# Connect to LoRaWAN
n = lora.LORA()
n.connect(dev_eui, app_eui, app_key)

count = 0
while True:
    print("Cycle ", count)
    count = count + 1

    n.send('0022.6000.05240.45')
    time.sleep(10)
