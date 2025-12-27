import board
import busio
import digitalio
import json
import os
import time
import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from lcd.lcd import LCD
from lcd.i2c_pcf8574_interface import I2CPCF8574Interface

FW_VERSION = "1.0"
RELE_ACCESO = False # il modulo rele funiona a logica inversa
MIDI_ACTIVITY_ON = False
PERSISTENZA = False

# Configurazione pin rele (GP0-GP7)
rele_pins = []
for i in range(8):
    pin = digitalio.DigitalInOut(getattr(board, f'GP{i}'))
    pin.direction = digitalio.Direction.OUTPUT
    pin.value = not RELE_ACCESO 
    rele_pins.append(pin)

# I/O
midi_activity = digitalio.DigitalInOut(getattr(board, f'GP27'))
midi_activity.direction = digitalio.Direction.OUTPUT
midi_activity.value = not MIDI_ACTIVITY_ON

# Configurazione pulsanti (GP8-GP16) con pull-up
# GP8-GP13 i primi 6 pulsanti selezionano l'uscita da utilizzare
# GP14-GP16 selezionano l'ingresso da utilizzare
button_pins = [0] * 9
for i in range(len(button_pins)):
    index = i+8
    if index == 16:
        index = 26
    button_pins[i] = digitalio.DigitalInOut(getattr(board, f'GP{index}'))
    button_pins[i].direction = digitalio.Direction.INPUT
    button_pins[i].pull = digitalio.Pull.UP

# IL DISPLAY VA ALIMENTATO A 5V
# I 2 PIN DELLA RETROILLUMINAZIONE VANNO PONTICELLATI TRA LORO
i2c = busio.I2C(board.GP29, board.GP28)  # SCL=GP29, SDA=GP28
# Attendi che I2C sia pronto
while not i2c.try_lock():
    pass
i2c.unlock()
lcd = LCD(I2CPCF8574Interface(i2c, 0x27), num_rows=2, num_cols=16) 

# Configurazione MIDI USB
midi = adafruit_midi.MIDI(midi_in=usb_midi.ports[0], midi_out=usb_midi.ports[1], in_channel=0, out_channel=0)

# Stato dei pulsanti (per debouncing)
last_button_states = [True] * len(button_pins)  # True = non premuto (pull-up)

def init():
    global uscitaSelezionata, ingressoSelezionato, MIDI_NOTE_BASE, nomiIngressi, nomiUscite
    global PERSISTENZA
    try:    
        f = open("ciec", "w")
        PERSISTENZA = True
        f.close()
    except Exception as e:
        print(f"Persitenza disabilitata: {e}")
        PERSISTENZA = False
        
    print(f"Modalità persistenza: {'ON' if PERSISTENZA else 'OFF'}")
   
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
            ingressoSelezionato = config.get("defaultInput", 0)
            uscitaSelezionata = config.get("defaultOutput", 0)
            MIDI_NOTE_BASE = config.get("midiBaseNote", 60)
            nomiIngressi = config.get("inputNames", [])
            nomiUscite = config.get("outputNames", [])    
            f.close()   

        if PERSISTENZA:
            # Carica stato ultimo ingresso/uscita selezionati
            if file_exists("state.json"):
                with open("state.json", "r") as f:
                    state = json.load(f)
                    ingressoSelezionato = state.get("lastInput", ingressoSelezionato)
                    uscitaSelezionata = state.get("lastOutput", uscitaSelezionata)
                    print(f"Ultimo stato caricato: Ingresso {ingressoSelezionato}, Uscita {uscitaSelezionata}")
                    f.close()

        return True
    except Exception as e:
        print(f"Errore lettura configurazione: {e}")
        return False

def file_exists(filename):
    try:
        os.stat(filename)
        return True
    except OSError:
        return False
    
def lcdprint(riga1, riga2=""):
    global lcd
    lcd.clear()
    lcd.set_cursor_pos(0, 0)
    lcd.print(riga1)
    if len(riga2) > 0:
        lcd.set_cursor_pos(1, 0)
        lcd.print(riga2)

def seleziona_ingresso(num):
    global ingressoSelezionato
    print(f"Selezione ingresso {num}")
    if 0 <= num <=2:
        ingressoSelezionato = num
        if num == 0:
            rele_pins[6].value = RELE_ACCESO # (1,0) -> selezione ingresso 1
            rele_pins[7].value = not RELE_ACCESO 
        elif num == 1:
            rele_pins[6].value = not RELE_ACCESO # (0,0) -> selezione ingresso 2
            rele_pins[7].value = not RELE_ACCESO 
        elif num == 2:    
            rele_pins[6].value = not RELE_ACCESO 
            rele_pins[7].value = RELE_ACCESO # (0,1) -> selezione ingresso 3
        sendMidi_in()
        aggiorna_display()

def seleziona_uscita(num):
    global uscitaSelezionata
    if 0 <= num <= 5:
        for i in range(6):
            if i == num:
                rele_pins[i].value = RELE_ACCESO
            else:
                rele_pins[i].value = not RELE_ACCESO
        uscitaSelezionata = num
        sendMidi_Out()
        aggiorna_display()

def sendMidi_in():
    global ingressoSelezionato, nomiIngressi
    nota = MIDI_NOTE_BASE + len(rele_pins) - 2 + ingressoSelezionato
    midi.send(NoteOn(nota, 127))
    print(f"MIDI IN: Note On {nota} ingresso {nomiIngressi[ingressoSelezionato]}")

def sendMidi_Out():
    global uscitaSelezionata, nomiUscite
    nota = MIDI_NOTE_BASE + uscitaSelezionata
    midi.send(NoteOn(nota, 127))
    print(f"MIDI OUT: Note On {nota} uscita {nomiUscite[uscitaSelezionata]}")

def aggiorna_display():
    global ingressoSelezionato, nomiIngressi, uscitaSelezionata, nomiUscite
    print(f"In: {nomiIngressi[ingressoSelezionato]} Out: {nomiUscite[uscitaSelezionata]}")
    ingr = chr(65 + ingressoSelezionato)  # A, B, C
    lcdprint(f"{ingr}:{nomiIngressi[ingressoSelezionato]}", f"{uscitaSelezionata+1}:{nomiUscite[uscitaSelezionata]}")
   
def key_pressed(i):
    print(f"Premuto tasto {i}")
    if 0 <= i <= 5:
        if i != uscitaSelezionata:
            seleziona_uscita(i)
            serialize_state()
            
    elif 6 <= i <= 8:
        ingresso_num = i - 6
        if ingresso_num != ingressoSelezionato:
            seleziona_ingresso(ingresso_num)
            serialize_state()
            
def serialize_state():
    global PERSISTENZA, ingressoSelezionato, uscitaSelezionata
    if PERSISTENZA:
        try:
            with open("state.json", "w") as f:
                state = {
                    "lastInput": ingressoSelezionato,
                    "lastOutput": uscitaSelezionata
                }
                json.dump(state, f)
                f.flush()
                f.close()
                print("Stato salvato")
        except Exception as e:
            print(f"Errore salvataggio stato: {e}")            

def leggi_pulsanti():
    global last_button_states, button_pins    
    tasto_rilevato = False
    for i in range(len(button_pins)):
        current_state = button_pins[i].value      
        # Rileva pressione (transizione da HIGH a LOW con pull-up)
        if last_button_states[i] and not current_state:
            if not tasto_rilevato:
                tasto_rilevato = True   
                key_pressed(i)
                time.sleep(0.3)  # Debouncing        
        last_button_states[i] = current_state      

def elabora_midi():
    msg = midi.receive()    
    if msg is not None:
        if isinstance(msg, NoteOn):
            nota = msg.note
            if msg.velocity > 0 and (MIDI_NOTE_BASE <= nota < MIDI_NOTE_BASE + len(button_pins)):
                key_pressed(nota - MIDI_NOTE_BASE)
                midiActivity()

def midiActivity():
    global midi_activity
    for i in range(3):
        midi_activity.value = MIDI_ACTIVITY_ON
        time.sleep(0.01)
        midi_activity.value = not MIDI_ACTIVITY_ON
        time.sleep(0.01)

def panico(error_msg):
    global midi_activity, rele_pins
    midi_activity.value = not MIDI_ACTIVITY_ON
    # Spegnimento rele
    for pin in rele_pins:
        pin.value = not RELE_ACCESO
    print(f"FUORI SERVIZIO: {error_msg}")
    lcdprint("FUORI SERVIZIO", error_msg)        
    while True:
        time.sleep(1)

if not init():
    panico("ERRORE CONFIG")

if PERSISTENZA:
    lcdprint("Smistarumori", f"v{FW_VERSION} (C) The XOR")
else:
    lcdprint(f"Fw ver. {FW_VERSION}", "NO PERSISTENZA")
time.sleep(1)  # Pausa per lettura versione firmware
seleziona_uscita(uscitaSelezionata)
seleziona_ingresso(ingressoSelezionato)

try:
    # Loop principale
    while True:
        leggi_pulsanti()
        elabora_midi()
        time.sleep(0.01)  # lasciamo un po' di tempo alla CPU x ricezione midi
        
except Exception as e:
    panico(str(e))
