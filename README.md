# Lo Smistarumori

Questo progetto, che non ci vergognamo di definire micidiale, è tipo fai conto un patchbay a 3 ingressi e 6 uscite. La libidine scatta col fatto che è comandabile via MIDI, e come se non bastasse genera un codice di nota a seconda dell'entrata/uscita selezionata. In questo modo, se si utilizzano software di correzione si puo' cambiare preset di in base alla cuffia selezionata. In effetti, tutto questo delirio di progetto nasce proprio dalla mia pigrizia nel cambiare preset a mano.
Il circuito utilizza dei relè, quindi non ci dovrebbe essere degrado del segnale. La logica di controllo è completamente isolata dalla parte audio, non c'è nessun punto di contatto. Tranquillizzato l'audiofilo di turno, procediamo con la narriazione di quella che è stata una lunga gestazione.
I nomi delle entrate/uscite mostrati sul display sono configurati nel file **config.json**; per i nomi si hanno a disposizione fino a 14 caratteri. Per finire,, viene memorizzata l'ultima configurazione utilizzata, in modo che alla riaccensione ritroveremo gli stessi collegamenti. Orco can!

### I Collegamenti
Così come nasce dalla mente malata dello scrivente, e principalmente poiché questa è la mia esatta configurazione, i collegamenti sono:
- Ingresso 1 va diretto all'uscita selezionata
- Gli ingressi 2 e 3 invece sono collegati con l'uscita SEND, e alle cuffie andrà il segnale in ritorno dall'entrata incredibilmente chiamata RETURN. Tra send e return c'è un amplificatore per cuffie esterno, mentre l'entrata 1 puo' essere utilizzata per un segnale gia' amplificato.

Questo percorso di segnali è ampiamente modificabile a piacere, visto che sono solo relè che si muovono. 

### Preparasiun:
Collegare l RP2040-Zero al PC, premere il pulsante BOOT e collegarlo. 
Se CircuitPython non fu installato, scaricarlo da https://downloads.circuitpython.org/bin/waveshare_rp2040_zero/en_US/adafruit-circuitpython-waveshare_rp2040_zero-en_US-10.0.3.uf2
e copiarlo sul microcontrollore: si riavviera' ed ora saremo pronti a programmare il cippo. Alla bisogna, scollegare e ricollegare RP2040 finche' non appare il devais nomato CIRCUITPY.

### Librerie:
Su https://circuitpython.org/libraries scaricare il bundle di librerie compatibile con la versione CircuitPython utilizzata (la 10 al momento della scrittura di questo romanzo).
Le librerie da copiare, estratte da questo file zip, sono:
- adafruit_bus_device
- adafruit_midi

Serve inoltre la libreria lcd, disponibile su: https://github.com/dhalbert/CircuitPython_LCD
La struttura finale deve essere questa:
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
## IMPORTANTE: usare la rimozione sicura una volta copiati i file! ##

Se qualcosa dovesse andare storto, si puo' resettare tutto avviando  RP2040 in boot mode e scopiazzandovi sopra il file **flash_nuke.uf2** disponibile su https://github.com/dwelch67/raspberrypi-pico/blob/main/flash_nuke.uf2

### Circuito elettronico
Se si hanno braccia a somiglianza T-Rex e si vuole risparmiare qualche soldino (oppure semplicemente ci si vuo semplificare la vita), è possibile eliminare dal circuito gli integrati 7400 e praticamente tutti i componeti (transistor, resistenze, ecc.): andranno rimossi in questo caso tutti i diodi LED, ma il circuito funzionera' lo stesso. I componenti utilizzati sono tutti desumibili dallo schema elettrificato e dalle varie illustrazioni presenti in questa repository, il transistor è un comune PNP e può (credo) essere rimpiazzato da un altro PNP qualsiasi.

### Scatolame
La scatola (per lo iutiuber itagliota, "Lo Scatolo") è progettata secondo il materiale elencato qui sotto. Se si cambiano i tipi di tasti, il display o altro è oltremodo ovvio che la progettazione andra' rivista. I file di progettazione in formato originale sono Freecad, e questa è abbastanza parametrica: tutte le misure sono nel file **Dimensioni.FCStd**.
Per tenere i LED alla giusta altezza, con riferimento ai pulsanti utilizzati, ci sono da stampare in 3D degli appositi distanziali (file **Rialzo led.FCStd**).

### Il materiale di partenza
Tutta roba rigorosamente cinese e a basso costo, così come le finanze imponevano. Tutto comprato da Aliexpress, ma si possono trovare componenti equivalenti ovunque.

- Pulsante:
![Pulsante](https://github.com/The-XOR/Smistarumori/blob/main/immagini/pulsante.png)
![Dimensioni pulsante](https://github.com/The-XOR/Smistarumori/blob/main/immagini/pulsante2.png)

- Copricoso:
![Copripulsante](https://github.com/The-XOR/Smistarumori/blob/main/immagini/copripulsante.png)

- LCD (2x16 caratteri), controller I2C tipo PCF8574:
![LCD](https://github.com/The-XOR/Smistarumori/blob/main/immagini/lcd.png)

- Scheda relais: 8 relay a 5 voltaggi
![Relais](https://github.com/The-XOR/Smistarumori/blob/main/immagini/relay.png)

- RP2040 Zero
![Microcontrollore](https://github.com/The-XOR/Smistarumori/blob/main/immagini/rp2040.png)

Elenco componenti:
- n.1 RP2040-Zero (quello piccolino con 23 pin)
- n.10 diodi led (6 di un colore per le uscite, 3 di un altro colore per le entrate, 1 per attività MIDI)
- n.1 LCD 2x16 caratteri (di base è un display 1602 con sopra un controller PCF8574 che lo trasforma da parallelo a I2C)
- n.2 moduli relè da 8, alimentati a 5V. Ce ne vogliono due perchè in genere si usa un canale per ciascheduna orecchia.
- n.1	2N3906	va bene qualsiasi transistore PNP
- n.4 resistenze 470 ohm 1/4W
- n.1 resistenza da 1800-2200 ohm 1/4W
- n.1 resistenza 10000 ohm 1/4W
- n.2 SN7404
- n.9 pulsanti

Connettori utilizzati:
- n.8 prese jack stereo da 6,3
- n.4 prese jack mono da 6,3
- n.1 presa jack stereo da 3,5

## La scheda così come mi è venuta, saldata alla meno peggio. Faccio un altro mestiere, io.
![Scheda fronte](https://github.com/The-XOR/Smistarumori/blob/main/immagini/scheda%20fronte.jpg)

![Scheda retro](https://github.com/The-XOR/Smistarumori/blob/main/immagini/scheda%20de%20retro.jpg)

## Il prodotto finito, così come esposto al MOMA di NY:
![Foto fronte](https://github.com/The-XOR/Smistarumori/blob/main/immagini/fronte.jpg)

![Foto retro](https://github.com/The-XOR/Smistarumori/blob/main/immagini/retro.jpg)


## Test finale
Una volta collegate le schede rele alla scheda principale, verificare che premendo i vari testi entrate/uscite si illuminino i rispettivi led sulle schede rele (le due schede sono collegate in parallelo, una gestisce il canale destro, una il sinistro). Una volta che si è sicuri che tutto funzioni, aprire (direttamente sulla cartella del microcontrollore) il file **boot.py** e modificare la linea:

```
MODALITA_SVILUPPO = False  # Imposta a False per abilitare la persistenza dell'ultima configurazione

```
Disabilitata la modalita' di sviluppo, il microcontrollore non sara' piu' visibile (come disco) dal sistema operativo. Per eventuali modifiche a qualsivoglia file, si puo':
- Resettare completamente il cippo, come narrato innanzi (flash_nuke.uf2 etc). Questa è la via secca.
- La via umida: collegare lo Smistarumori al PC tenendo premuto il tasto **Input C**. In questo modo, il disco dovrebbe riapparire, ma non funzionera' la persistenza.

