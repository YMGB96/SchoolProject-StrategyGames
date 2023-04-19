# **Board Blitz**
This is a collection of 2 boardgames - a variant of **checkers** and **chess** with only pawns

## **Prerequisites**
1. Download or clone this repository and move to it with a terminal

2. Make sure that you have [python 3.10 or newer](https://www.python.org/downloads/) installed

3. If you get an error when running `python -V`, add python to your `PATH` variable

4. You can then install the dependencies using:
    ```bash
    pip install -r requirements.txt
    ```

## **Start the Game**
Once you've met all the prerequisits, you can start the game using:
```bash
python board_blitz
```

## **Rules** (in german)
### **Bauernschach**
ist eine simple Variante des Schachs, die nur mit Bauern gespielt
wird. In der Ausgangsstellung stehen dabei die weißen bzw. schwarzen
Spielfiguren (Bauern) auf der jeweiligen Grundlinie. Die Spieler
machen abwechselnd einen Zug, wobei Weiß beginnt. 

<u>Es gibt zwei erlaubte Arten von Zügen:</u>
1)  Ziehen
    kann ein Bauer, indem er ein Feld in Richtung der gegnerischen
    Grundlinie (das sind die Felder, auf denen anfangs die
    gegnerischen Bauern stehen) geht, aber nur sofern dieses Feld
    frei ist (also nicht von einem eigenen oder gegnerischen Bauern
    besetzt ist). 
2)  Schlagen
    kann ein Bauer in Richtung der gegnerischen Grundlinie durch
    diagonales Ziehen in Richtung der gegnerischen Grundlinie,
    aber nur auf einem Feld, auf dem ein gegnerischer Bauer steht. 

Ziel des Spieles ist es, einen Bauern auf die gegnerische
Grundlinie zu platzieren; wenn das gelingt, ist das Spiel sofort
zu Ende und die Farbe, die das erreicht hat, hat gewonnen. Wenn
ein Spieler nicht mehr ziehen kann, oder überhaupt keine Figuren
mehr hat, ist das Spiel für ihn als verloren zu werten. Ein
Unentschieden ist daher in dieser Variante nicht möglich.

### **Dame**
wird hier mit vereinfachten Regeln auf einem 6x6 Spielfeld
gespielt.

Zu Beginn werden für beide Spieler die Spielsteine auf den
schwarzen Feldern der ersten zwei Reihen des Spielfeldes verteilt.
Gespielt wird nur auf den dunklen Feldern. Die Steine ziehen jeweils
ein Feld vorwärts in diagonaler Richtung.

Es herrscht generell Schlagzwang, gegnerische Steine müssen
entsprechend übersprungen und dadurch geschlagen werden, sofern
das direkt angrenzende dahinter liegende Feld frei ist. Der
schlagende Stein wird auf dieses freie Feld gezogen und wenn das
Zielfeld eines Sprungs auf ein Feld führt, von dem aus ein weiterer
Stein übersprungen werden kann, wird der Sprung fortgesetzt. Alle
übersprungenen Steine werden nach dem Zug vom Brett genommen.
Es darf dabei nicht über eigene Spielsteine gesprungen werden.

Das Spiel ist gewonnen, wenn ein Spieler einen Spielstein auf der
gegnerischen Grundlinie platzieren kann.
Das Spiel ist verloren, wenn ein Spieler nicht mehr ziehen kann,
oder keine Spielsteine mehr hat.
Ein Unentschieden ist somit in dieser Variante ebenfalls nicht möglich.
