import supervisor
import board
import storage
import digitalio
import time
import usb_midi

supervisor.set_usb_identification("The XOR", "Smistarumori")
usb_midi.set_names(streaming_interface_name="Smistarumori MIDI", in_jack_name="Smistarumori MIDI In", out_jack_name="Smistarumori MIDI Out"  )

# OCIO: UNA volta messa a False, NON si potrà più accedere al filesystem da PC!
# OCIO: Se si rimane fuori di casa, avviare il coso premendo il pulsante INPUT_C
MODALITA_SVILUPPO = True  # Imposta a True per abilitare la modalità sviluppo (USB mass storage attivo)

input_C = digitalio.DigitalInOut(getattr(board, f'GP26')) #input_C
input_C.direction = digitalio.Direction.INPUT
input_C.pull = digitalio.Pull.UP
time.sleep(0.1)  # Attendi un attimo per stabilizzare lo stato del pin
if not input_C.value:
   MODALITA_SVILUPPO = True
   print("OVERRIDE: rilevato tasto inputC")

if MODALITA_SVILUPPO:
    storage.remount("/", readonly=True)
    m = storage.getmount("/")
    m.label = "SMISTARUMOR"
    storage.enable_usb_drive()
else:
    storage.disable_usb_drive()
    storage.remount("/", readonly=False)
    
