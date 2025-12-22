# Preparasiun:
Collegare l RP2040-Zero al PC, premere il pulsante BOOT e collegarlo. 
Se CircuitPython ancora non fu installato, scaricarlo da 
https://downloads.circuitpython.org/bin/waveshare_rp2040_zero/en_US/adafruit-circuitpython-waveshare_rp2040_zero-en_US-10.0.3.uf2
e copiarlo sul RP2040-Zero.
Il devais si riavviera' ed ora siamo pronti
Nel caso, scollegare e ricollegare RP2040 finche' non appare il devais nomati CIRCUITPY.

# Librerie:
su https://circuitpython.org/libraries scaricare il bundle di librerie compatibile con la versione CircuitPython utilizzata (la 10 al momento della scrittura di questo romanzo).
Le librerie da copiare, estratte da questo file zip, sono:
- adafruit_bus_device
- adafruit_midi

Serve inoltre la libreria lcd, disponibile su: https://github.com/dhalbert/CircuitPython_LCD
Copiare questa libreria 

# Preparazione RP2040
A questo punto, copiare sul fatto apposta i file:
```
  <CIRCUITPY>/
  ├── boot.py
  ├── code.py
  ├── config.json
  └── lib/
         ├── adafruit_bus_device
         ├── adafruit_midi
         └── lcd
```
### IMPORTANTE: usare la rimozione sicura prima di avviare RP2040 ###

Se qualcosa dovesse andare storto, si puo' resettare tutto avviando l RP2040 in boot mode e scopiazzandovi sopra il file flash_nuke.uf2 disponibile su https://github.com/dwelch67/raspberrypi-pico/blob/main/flash_nuke.uf2

