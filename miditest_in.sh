#!/bin/bash
# controlla che la porta midi sia connessa
MIDIID=$(amidi -l | grep "Smistarumori" | awk '{print $2}')
if [ -z "$MIDIID" ]; then
    echo "Porta MIDI non connessa. Collegare Smistarumori."
    exit 1
fi
echo "Porta MIDI trovata: $MIDIID"
echo "In ascolto dei messaggi MIDI da Smistarumori. Premere Ctrl+C per uscire."
amidi -p $MIDIID -d
