#!/bin/bash
# controlla che la porta midi sia connessa
echo "Nota: questo script richiede 'sendmidi', reperibile su https://github.com/gbevin/SendMIDI"
A=$(sendmidi list | grep "Smistarumori")
if [ -z "$A" ]; then
  echo "Porta Smistarumori non trovata"
  exit 1
fi

echo "Smistarumori Device: $A"
while true; do
  read -p "Seleziona input (da 1 a 3): " INPUT
  if ! [[ "$INPUT" =~ ^[1-3]$ ]]; then
    echo "Input non valido. Inserisci un numero da 1 a 3."
  else
    nota=$((65+$INPUT))
    echo "Impostazione input a $INPUT  -> $nota"
    sendmidi dev $A on $nota 100
  fi

  read -p "Seleziona output (da 1 a 6): " OUTPUT
  if ! [[ "$OUTPUT" =~ ^[1-6]$ ]]; then
    echo "Input non valido. Inserisci un numero da 1 a 6."
  else
    nota=$((60+$OUTPUT))
    echo "Impostazione output a $OUTPUT  -> $nota"
    sendmidi dev $A on $nota 100
  fi
done


