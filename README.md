**Scope - was brauchen wir alles**
Datenbank (IN/OUT: Read/Write)
- Bestenliste
- Login
- Spielstände
GUI (Menu)
- IN: User Input
- IN: “Change Scene”
- OUT: Clicked on *BUTTON* :slight_smile:
Menu logic (Menu and “Esc”-Screen)
- IN: Button that was clicked
- IN: Datenbanken
- OUT: Login DB (oder Gast)
- OUT: Spielstand von aktuellem User (oder leerer Spielstand)
GUI (Game)
- IN: User Input
- IN: 2d (6x6) Array
- OUT: Move
Logik der Spiele (Dame, Bauernschach)
- IN: Spielstand
- IN: Move
- OUT: 2d (6x6) Array
- OUT: Valid Moves
- OUT: Spielstand
Grafiken
KI 
- IN: Spielstand
- IN: Difficulty (Depth)
- OUT: Move

**Wie sehen unsere Strukturen aus?**
Datenbanken:
- Login( User ID, Name, Pw Hash, Pw Salt )
- Spielstände( User ID, Board 1, (log?), Board 2, (log?) )
- Bestenliste( User ID, Game, Result, Difficulty, (Time, Moves,, …) )
Spielstand:
- 2d 6x6 Array
Move:
- (team, (from_x, from_y), (to_x, to_y)) or something

**Teilprodukte und Arbeitspakete**
| Arbeit | Zuständiger:in |
Grafiken    Art Director Aileeen
Datenbank    Karin
KI                Bilal
GUI (Menu)    Artem
GUI (Spiel)    Art Director Aileeeeen
Menu logic    The Brain Nils
Spiellogik    Executive Producer Yannick

**Sonstiges**
Wir benutzen folgende Libraries:
  Python
  Sqlite3
  PyGame