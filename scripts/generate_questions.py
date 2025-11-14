import json
import random
import unicodedata
import re
from pathlib import Path

random.seed(42)

QUESTIONS_PER_CATEGORY = 30

TEMPLATES = {
    "default": "Welche Option passt zur Beschreibung: {prompt}",
    "Fortnite": "Welches Fortnite-Element passt zur Beschreibung: {prompt}",
    "Marvel": "Welche Marvel-Person oder -Technologie passt zur Beschreibung: {prompt}",
    "Star Wars": "Was aus dem Star-Wars-Universum wird hier beschrieben: {prompt}",
    "Minecraft": "Welches Minecraft-Element passt: {prompt}",
    "Woodwalkers": "Welches Woodwalkers-Element gehört zur Beschreibung: {prompt}",
    "Sheldon": "Welche Aussage über Sheldon Cooper trifft hier zu: {prompt}",
    "Rettungssanitäter für Schüler": "Welcher Rettungstipp passt: {prompt}",
    "Physik 8. Klasse": "Welcher physikalische Begriff passt: {prompt}",
    "Survival-Fragen": "Welche Survival-Idee passt: {prompt}",
    "Mode": "Welcher Modebegriff passt: {prompt}",
    "Haute Couture": "Welches Haute-Couture-Haus oder -Detail passt: {prompt}",
    "Berühmte Designer": "Welcher Designer passt: {prompt}",
    "Englische Ausdrücke (C2-Niveau, auf Englisch formuliert)": "Which expression matches the description: {prompt}",
    "Chemie 10. Klasse": "Welcher Chemiebegriff passt: {prompt}",
    "Serie \"Emily in Paris\"": "Welche Info zu 'Emily in Paris' passt: {prompt}",
    "Beauty & Styling": "Welcher Beauty-Begriff passt: {prompt}",
    "Handtaschen": "Welche Handtaschen-Info passt: {prompt}",
    "Kardiologie": "Welcher kardiologische Begriff passt: {prompt}",
    "Hypertensiologie": "Welcher Hypertonie-Begriff passt: {prompt}",
    "Rhythmologie": "Welcher Rhythmusbegriff passt: {prompt}",
    "Diabetologie": "Welcher Diabetologie-Begriff passt: {prompt}",
    "Lipidmanagement": "Welcher Lipid- oder Stoffwechselbegriff passt: {prompt}",
    "Gesunde Ernährung": "Welches Ernährungsprinzip passt: {prompt}",
    "Frauengesundheit": "Welcher Frauengesundheitsbegriff passt: {prompt}",
    "Spanisch Niveau 11. Klasse": "¿Qué expresión corresponde a la descripción: {prompt}?",
    "Hamburg": "Welcher Hamburg-Fakt passt: {prompt}",
}

def parse_entries(block: str) -> list[dict]:
    entries: list[dict] = []
    for raw_line in block.strip().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            answer, prompt = line.split("|", 1)
        except ValueError as exc:  # pragma: no cover - Entwicklungshelfer
            raise ValueError(f"Ungültige Zeile: {raw_line!r}") from exc
        entries.append({"answer": answer.strip(), "prompt": prompt.strip()})
    if len(entries) != QUESTIONS_PER_CATEGORY:
        raise ValueError(
            f"Jede Kategorie benötigt genau {QUESTIONS_PER_CATEGORY} Einträge, gefunden: {len(entries)}"
        )
    return entries


DATA = {
    "noah": {
        "Fortnite": parse_entries("""
Battle Bus|bringt alle Spieler zu Beginn des Matches hoch über die Insel und lässt sie abspringen
Loot Llama|explodiert in einem Regen aus Ressourcen, Munition und Heilung, wenn du ihn öffnest
Sturmkreis|verkleinert sich fortlaufend und zwingt alle Spieler in ein kleineres Gebiet
Riss-To-Go|teleportiert dich sofort nach oben und lässt dich erneut gleiten
Null Bauen|ist der Modus ohne Baumaterialien, in dem Deckung nur über Gelände und Gadgets entsteht
Reboot-Van|reanimiert ausgeschiedene Teammitglieder mit ihrer Karte
Chug Jug|füllt Lebenspunkte und Schild vollständig auf, benötigt aber eine lange Trinkzeit
Shockwave Hammer|schleudert dich weit durch die Luft und kann Gegner wegstoßen
ODM-Ausrüstung|ermöglicht wendige Greifhaken-Schwünge inspiriert von Attack on Titan
Reality Augments|passive Perks, die zufällig angeboten werden und Boni wie Schnellladen liefern
Kinetic Blade|eine Nahkampfwaffe, die Kombos schlägt und Dashs vergibt
Herald Sanctum Chrom|ermöglicht durch Chrom-Spray das Phasen durch Wände und schnellere Rotation
Launchpad|katapultiert dich und dein Team nach oben für einen freien Gleiterstart
Midas Touch|verwandelt Waffen beim Aufheben in goldene Seltenheit
Heisted Breacher Shotgun|zerstört mit jedem Schuss sofort Mauern
Capture Point|markiert nahe Gegner und Truhen nach erobern eines Ortes im neuen Kapitel
Holo-Chest Schlüssel|öffnen Tresore mit vorbestimmten Waffen, wenn du Schlüssel sammelst
Slap Juice|gibt vorübergehende Ausdauer, sodass du ohne Sprintlimit laufen kannst
Kamehameha Angriff|feuert einen massiven Energiebeam mit großem Schaden ab
Nimbus-Cloud|funktioniert als wiederaufladbarer Schwebe-Sprung für hohe Mobilität
Grind Rails|lassen dich mit vollem Tempo über Mega City gleiten
Muddy Mounds|ermöglichen lautloses Fortbewegen, wenn du dich eingräbst
Jelly Angler|fischt unendlich viele heilende Quallen
Bush Bomb|erschafft ein temporäres Laubversteck auf offener Fläche
Snowball Launcher|verschießt explosive Schneebälle während Winterevents
Mythic Boss Medaillon|gewährt passive Schildregeneration, solange du ihn trägst
Train Heist Tresor|enthält mythische Beute im fahrenden Zug von Kapitel 5
Soccer NPC Aufgaben|fordern dich zu Dribblings oder Torschüssen für EP und Gold
Weapon Mods|lassen dich Läufe, Magazine und Zieloptiken frei kombinieren
Storm Surge|fügt Teams Schaden zu, die zu wenig Schaden gemacht haben, um Campen zu verhindern
"""),
        "Marvel": parse_entries("""
Iron Man Mark 85|ist der finale Nanoanzug, den Tony Stark in Endgame trägt
Arc Reactor|liefert Tony Stark die Energiequelle in seiner Brust
Mjölnir|ist Thors Hammer, der nur von Würdigen gehoben werden kann
Vibranium|ist das seltene Metall aus Wakanda, aus dem Captain Americas Schild besteht
Tesserakt|beherbergt den Raumstein und ermöglicht Teleportation
Infinity Gauntlet|Handschuh, der alle sechs Infinity-Steine aufnehmen kann
Black Widow|Avenger-Spionin Natasha Romanoff mit rotem Haar und Kampfstöcken
Hawkeye|Bogenschütze Clint Barton, der trickreiche Pfeile nutzt
Doctor Strange|Schutz der Zeitlinie mit dem Auge von Agamotto
Scarlet Witch|Wanda Maximoff, die Chaosmagie und Hexfelder kontrolliert
Ant-Man|Scott Lang, der mit Pym-Partikeln Größe verändert
Wasp|Hope van Dyne, die gemeinsam mit Ant-Man fliegt und sticht
Black Panther|König T’Challa, der den Pantheranzug und Kräuterkräfte nutzt
Okoye|Generälin der Dora Milaje mit Vibranium-Speer
Shuri|geniale Erfinderin, die Panther-Anzüge und Gadgets baut
Winter Soldier|Bucky Barnes mit Vibranium-Arm aus Wakanda
Falcon|Sam Wilson, der Flügel und Redwing-Drohne steuert
Captain Marvel|Carol Danvers mit Photonenstrahlen und kosmischer Power
Nick Fury|Direktor von S.H.I.E.L.D. mit Augenklappe
Loki|Asgardischer Gott der Streiche mit Zepter
Heimdall|Wächter der Bifröst-Brücke, der alles sieht
Korg|Steinwesenfreund von Thor mit trockenem Humor
Rocket Raccoon|Genmanipulierter Waschbär und Waffenexperte der Guardians
Groot|baumähnliches Wesen, das sich regenerieren kann
Gamora|Assassinin und adoptierte Tochter von Thanos
Nebula|Zyklopische Schwester, die kybernetische Verbesserungen trägt
Yondu|Ravager-Anführer mit pfeifgesteuertem Pfeil
Eternals|Unsterbliche Gruppe, die Deviants bekämpft
Shang-Chi|meistert die Zehn Ringe seines Vaters
Moon Knight|Söldner Marc Spector mit Identitäten, die für Khonshu kämpfen
"""),
        "Star Wars": parse_entries("""
Millennium Falcon|Schiff von Han Solo und Chewbacca, berühmt für den Kessel-Flug
X-Flügler|Standardjäger der Rebellenallianz mit S-Flügeln
TIE Fighter|imperiales Abfangschiff ohne Schilde
Lightsaber|ikonische Waffe der Jedi und Sith aus Kyberkristallen
Death Star|Monumentale Raumstation mit Superlaser
Holocron|Speicherkristalle für Jedi- oder Sith-Wissen
The Force|mystische Energie, die alles verbindet
Order 66|geheimer Befehl, der die Klone gegen die Jedi wendet
Clone Trooper|Soldatenarmee, die auf Jango Fetts DNA basiert
Stormtrooper|weiße Infanterie des Imperiums
AT-AT|vierbeiniger Kampfläufer auf Hoth
Speeder Bike|schnelles Luftfahrzeug in den Wäldern von Endor
Jedi Council|Rat der weisen Meister auf Coruscant
Sith|Orden, der die dunkle Seite der Macht nutzt
Holonet|Galaxisweites Kommunikationsnetz
Coruscant|Metropole und politisches Zentrum
Tatooine|Wüstenplanet, Heimat von Anakin und Luke
Hoth|Eisplanet mit Echo-Basis der Rebellen
Bespin|Wolkenstadt, in der Lando regiert
Dagobah|Sumpfplanet, auf dem Yoda Luke trainiert
Kylo Ren|Anführer der Ritter von Ren mit Kreuz-Lichtschwert
Rey|Schrottsammlerin, die zur Jedi-Schülerin wird
The Mandalorian|Din Djarin, Kopfgeldjäger mit Beskar-Rüstung
Grogu|machtbegabtes Kind, das Mando begleitet
Dark Saber|schwarzes Lichtschwert der Mandalorianer
Inquisitoren|Machtnutzer, die überlebende Jedi jagen
Hyperspace|Überlichtgeschwindigkeitssystem
Holoprojector|Gerät, das 3D-Nachrichten darstellt
Blaster|Standard-Fernkampfwaffe in der Galaxis
Gonk-Droid|kastenförmiger Energieträger-Droide
"""),
        "Minecraft": parse_entries("""
Creeper|grünes Monster, das explodiert, wenn es sich dir nähert
Enderman|hohes Wesen, das Blöcke trägt und sich teleportiert
Ghast|fliegendes Netherwesen, das Feuerbälle spuckt
Wither|Boss mit drei Schädeln, der Nethersterne droppt
Enderdrache|finaler Boss in der End-Dimension
Netherportal|Tor aus Obsidian, das dich in den Nether bringt
Redstone|Material zum Bau elektrischer Schaltungen
Beacon|Strahlenturm, der Buffs gibt, wenn du ihn aktivierst
Enchanting Table|Block zum Verzaubern von Werkzeugen
Anvil|erlaubt Reparaturen und das Kombinieren von Verzauberungen
Totem der Unsterblichkeit|rettet dich einmalig vor dem Tod
Elytra|Flügel, mit denen du durch die Luft gleiten kannst
Trident|Waffe aus Drowned-Drops, die mit Loyalität zurückkehrt
Shulker-Box|tragbare Kiste, deren Inhalt beim Abbau erhalten bleibt
Village|Dorf mit Händlern und Arbeitsplätzen
Pillager Outpost|Turm der Plünderer mit Bannern und Käfigen
Ocean Monument|Wasserstruktur mit Guardians und Prismarin
Stronghold|unterirdische Festung mit Portalrahmen ins End
Axolotl|freundliche Wasserbegleiter, die dich gegen Drowns unterstützen
Beehive|Block, der Honig und Bienen beherbergt
Honey Block|blockiert Fallgeschwindigkeit und dient als Redstone-Komponente
Snow Golem|Schneekreatur, die Schneebälle auf Gegner wirft
Iron Golem|beschützt Dörfer mit starken Nahkampfangriffen
Bastion Remnant|Nether-Struktur voller Piglins und Loot
Warped Forest|Nether-Biom, das Endermen beherbergt
Moss Block|neuer Block aus Lush Caves mit Knochenmehlverbreitung
Dripstone|Spitzen, aus denen Lava oder Wasser tropfen kann
Goat Horn|Musikinstrument, das beim Rammen gedroppt wird
Cartography Table|Block zum Kopieren und Sperren von Karten
Fletching Table|Arbeitsplatz für Bogner-Dorfbewohner
"""),
        "Woodwalkers": parse_entries("""
Carag|Protagonist, der sich in einen Puma verwandeln kann
Tikaani|Carags beste Freundin mit Wolfs-Gestalt
Holly|freche Rotfuchs-Wandlerin, die Streiche liebt
Brandon|Bison-Wandler mit ruhigem Gemüt
Shari|Leopardin, die Carag im Training unterstützt
Jeffrey|Ehemaliger Feind, der sich in einen Koyoten verwandelt
Mr. Bridger|Direktor der Clearwater High
Mrs. Calloway|Lehrerin für Wandlerkunde an der Schule
Clearwater High|Wandler-Schule in den Rocky Mountains
Winglet-Klub|Geheime Gruppe für waghalsige Schüleraktionen
Lysander|Adler-Wandler mit strenger Haltung
Ella|Schildkröten-Wandlerin mit einem Faible für Kunst
Maya|Kolibri-Wandlerin, die schnelle Flüge beherrscht
King|Grizzly-Wandler, der Carag trainiert
Nanuq|Eisbären-Wandler aus Kanada
Lightning|Kater, der Carag als Haustier begleitet
Spirit Talk|Technik, bei der Wandler mit ihrer Tierseite sprechen
Gestaltwechsel-Schmerz|kurzer Moment, in dem Knochen sich anpassen
Pfadfinder-Team|Schulgruppe, die Waldmissionen übernimmt
Meisterprüfung|Test, der beweist, dass du deine Tierform kontrollieren kannst
Kyrill|Luchs-Wandler, der sich Carag anschließt
Blaue Lagune|Versteckter Ort auf dem Schulgelände mit Thermalwasser
Rat der Ältesten|Gremium, das über Wandler-Gesetze wacht
Geheime Karte|zeigt Pfade zu sicheren Unterschlüpfen für Woodwalker
Rivalenrudel|Gegenspieler, die Carag in Fallen locken wollen
Funkenregen|Trainingsübung, bei der Schüler Funken von Fackeln ausweichen
Seidenpfad|heimlicher Tunnel zwischen den Schlafsälen
Jäger-Club|Organisation von Menschen, die Woodwalker verfolgen
Herbstball|Fest, bei dem Schüler im Menschenkörper tanzen
Bärenmedizin|Heilkräuter-Mix, den Carag als Puma bevorzugt
"""),
        "Sheldon": parse_entries("""
Spot auf dem Sofa|Platz im Wohnzimmer, den Sheldon als seinen Anspruch markiert
Mitbewohnervereinbarung|detaillierter Vertrag zwischen Sheldon und Leonard
Soft Kitty|Kinderlied, das Sheldon beim Kranksein beruhigt
Bazinga|Sheldons Ausruf nach einem gelungenen Streich
Zug-Enthusiasmus|Sheldons Liebe für Fahrpläne, Modelle und reale Lokomotiven
Comicbuch-Mittwoch|fester Tag, an dem die Clique den Laden besucht
Fun with Flags|YouTube-Serie, in der Sheldon Flaggenkunde erklärt
String-Theorie|physikalisches Feld, an dem Sheldon arbeitet
Knock-Ritual|dreimaliges Klopfen plus Namensruf, bevor er einen Raum betritt
MeeMaw|Spitzname für Sheldons Großmutter, die ihn verwöhnt
Tiara|Geschenk für Amy, wenn sie eine wissenschaftliche Errungenschaft feiert
Roommate-Moratorium|Klausel, die Leonard zeitweise aus dem Vertrag entlässt
Cooper-Hofstadter-Polarisation|Veröffentlichung, die beide verbindet
Roboter Shelbot|Telepräsenz, mit der Sheldon krank von zu Hause unterrichtet
ComicCon-Cosplay|Sheldon tritt gern als Spock oder Data verkleidet auf
Frühstücksroutine|Oatmeal-Montag, French Toast Dienstag usw.
Raj-Ehevertrag|Sheldon verhandelt juristische Details für Freunde
Bowling-Rivalität|Konflikt mit dem Comicladenbesitzer Stuart
Roommate-Agreement-Klausel 37B|regelt das Öffnen gemeinsamer Geschenke
Adhäsionsvertrag|Sheldons Lieblingsbeispiel für asymmetrische Machtverteilung
Treppenhaus-Defekt|Fahrstuhl ist jahrelang kaputt, was Sheldons Fitness erhält
Professor Proton|TV-Wissenschaftler, den Sheldon als Kind verehrte
Kohabitationsexperiment|Sheldon zieht vorübergehend bei Amy ein
Spaghetti-Dienstag|wöchentlicher Menüplan in der WG
Comicbuchinventar|Sheldon katalogisiert jede Ausgabe mit Plastikhüllen
Laserharfe|Instrument, das Sheldon im Musikladen spielt
Nobelpreis|Sheldon gewinnt ihn schließlich gemeinsam mit Amy für Superasymmetrie
Emergency-Kit|Go-Bag mit Pässen, Snacks und Videospielen
Sheldonbot|Computerprogramm, das Sheldons Persönlichkeit testen soll
Couch-Fort|Kissenburg, die Sheldon bei Erkältungsangst baut
"""),
        "Rettungssanitäter für Schüler": parse_entries("""
Notruf 112|europäische Nummer für Rettungsdienst und Feuerwehr
ABCDE-Schema|Struktur zur Erstuntersuchung von Patienten
Stabile Seitenlage|Position, um Atemwege freizuhalten
Druckverband|Technik, um starke Blutungen zu stoppen
Rautek-Rettungsgriff|Methode, um Verletzte schnell aus Gefahrenzonen zu ziehen
Helmabnahme|Teamtechnik bei bewusstlosen Motorradfahrern
SAM-Splint|Formbare Schiene zur Schienung von Knochenbrüchen
Tourniquet|Abbindesystem bei lebensbedrohlichen Blutungen an Extremitäten
Defibrillator AED|Gerät zur Abgabe elektrischer Schocks bei Kammerflimmern
Herzdruckmassage|30 Kompressionen gefolgt von 2 Beatmungen
Beatmungsbeutel|Hilfsmittel, um Luft kontrolliert zu verabreichen
Pulsoxymeter|Misst Sauerstoffsättigung am Finger
Bodycheck|Schnelles Abtasten nach versteckten Verletzungen
Sauerstoffmaske|Zubehör, das 6–10 Liter O2 pro Minute liefert
Schocklage|Beinhochlagerung, um Kreislauf zu stabilisieren
HWS-Stütze|Kragen, der die Halswirbelsäule immobilisiert
Rippenprellung|verursacht Druckschmerz, sollte aber stabilisiert werden
Eis-Schema|Entzündete Gelenke: Eis, Kompression, Hochlagern
Sichtungsalgorithmus|START- oder mSTaRT-Triage bei Massenanfall
Glasgow Coma Scale|Bewertung von Bewusstseinslage 3–15 Punkte
Hypoglykämie-Erkennung|Zittern, Schwitzen, Verwirrtheit bei Diabetikern
Anaphylaxie-Management|Adrenalin-Autoinjektor in den Oberschenkel geben
Asthma-Spray|Dosieraerosol, das mit Spacer effektiver wirkt
Hitzeerschöpfung|führt zu Schwindel, braucht Kühlung und Flüssigkeit
Verbrennung 2. Grades|blasenbildend, steril abdecken, nicht aufstechen
PECH-Regel|Pause, Eis, Compression, Hochlagern bei Sportverletzung
Rettungsdecke|silberne Seite nach innen, um Wärme zu halten
SAMU-Schema|Situation, Airway, Maßnahmen, Übergabe für Funkmeldungen
RR-Messung|Blutdruck mit Manschette auf Herzhöhe messen
Handschuhe anziehen|erster Schritt zum Eigenschutz
"""),
        "Physik 8. Klasse": parse_entries("""
Geschwindigkeit|Berechnet sich als Strecke durch Zeit
Beschleunigung|Änderung der Geschwindigkeit pro Zeitintervall
Kraft|wird in Newton gemessen und verursacht Beschleunigung
Masse|Eigenschaft eines Körpers, angegeben in Kilogramm
Gewichtskraft|Produkt aus Masse und Ortsfaktor g
Hebelgesetz|Kraft mal Kraftarm gleich Last mal Lastarm
Dichte|Verhältnis von Masse zu Volumen
Pascal|Einheit für Druck
Archimedisches Prinzip|Auftrieb entspricht verdrängtem Flüssigkeitsgewicht
Schwerpunkt|Punkt, an dem alle Gewichtskräfte angreifen
Impuls|Produkt aus Masse und Geschwindigkeit
Trägheit|Widerstand gegen Bewegungsänderungen
Reibung|Kraft, die Bewegungen hemmt
Federkonstante|Beschreibt Steifigkeit einer Feder
Energieerhaltung|Gesamtenergie in einem abgeschlossenen System bleibt gleich
Potentielle Energie|Energie eines gehobenen Körpers
Kinetische Energie|Energie eines bewegten Körpers
Mechanische Arbeit|Kraft mal Weg
Leistung|Arbeit pro Zeit, Einheit Watt
Ohmsches Gesetz|Spannung gleich Strom mal Widerstand
Reihenschaltung|Ströme gleich, Spannungen addieren sich
Parallelschaltung|Spannungen gleich, Ströme addieren sich
Transformator|verändert Spannungsniveaus durch Spulenwicklungen
Elektromagnet|Spule mit Eisenkern, die ein Magnetfeld erzeugt
Induktion|Entstehung einer Spannung durch Bewegungen im Magnetfeld
Lichtbrechung|Richtungsänderung von Licht beim Übergang in anderes Medium
Reflexion|Zurückwerfen von Licht an spiegelnden Flächen
Elektrostatische Aufladung|Trennung von Ladungen z. B. durch Reibung
Schallgeschwindigkeit|ca. 343 m/s in Luft
Dezibel|Maß für Lautstärke
"""),
        "Survival-Fragen": parse_entries("""
Rule of Three|Du überlebst 3 Minuten ohne Luft, 3 Stunden ohne Schutz, 3 Tage ohne Wasser
Signalfeuer-Dreieck|Drei Feuer in Dreiecksform signalisieren Hilfe
Notfallspiegel|Reflektiert Sonne, um Suchteams auf sich aufmerksam zu machen
Sonnenstandsuhr|Nutze Schatten eines Stocks, um grobe Himmelsrichtungen zu ermitteln
Trinkwasser abkochen|mindestens 5 Minuten kochen, um Keime abzutöten
Wasserfilter aus Sand und Kohle|Improvisierter Filter aus geschichteten Materialien
Biwaksack|Ultraleichte Hülle, die Wärme reflektiert
Tarpknoten|Schnelleckknoten und Spannschnüre für Unterstände
Feuerstahl|Erzeugt Funken selbst bei Nässe
Birkenrinde|brennt schnell und dient als Zunder
Fatwood|Harzreiches Holz, das lange Flammen liefert
Dakota Fire Hole|zwei Gruben für raucharmes, effizientes Feuer
Bow Drill|Reibungsfeuertechnik mit Bogen, Spindel und Brett
Snare|Schlinge zum Fangen kleiner Tiere
Paracord|leichtes, starkes Seil mit sieben Innensträngen
Improvisierter Kompass|Nadel magnetisieren, auf Wasser schwimmen lassen
Bergungssignal|Drei Pfiffe oder Schüsse gelten als Notruf
Mylar-Decke|reflektiert bis zu 90 % Körperwärme
Layering|Mehrere Kleidungsschichten gegen Kälte
Leave No Trace|Sieben Regeln, um Natur zu schützen
Bärenregel|Essenslager mindestens 100 Meter vom Schlafplatz entfernt
Buddy-Check|Partner kontrollieren sich gegenseitig vor Aufbruch
Trotzrichtung bestimmen|Moos wächst nicht nur im Norden, kombiniere Hinweise
SOS am Boden|Große Buchstaben mit Steinen oder Stöcken legen
Trinkwasserpflanzen|Schilf und Bambus speichern sauberes Wasser
Morsecode|SOS ist •••---•••
Signalrauch|Grünes Material sorgt für auffälligen Rauch
Notunterkunft|Lean-to, Debris Hut oder A-Frame je nach Material
Himmelsnavigation|Polarstern im Norden, Kreuz des Südens im Süden
Survival-Kit|enthält Messer, Feuerstarter, Erste-Hilfe, Kompass
"""),
    },
    "johanna": {
        "Mode": parse_entries("""
Capsule Wardrobe|Kleiderschrank mit wenigen, kombinierbaren Lieblingsteilen
Monochrome Look|Outfit komplett in einer Farbfamilie
Color Blocking|Kombination kräftiger, kontrastierender Farben in großen Flächen
Layering|Mehrere Lagen unterschiedlicher Längen übereinander tragen
Statement Piece|auffälliges Einzelteil, das den Rest des Looks bestimmt
Tailoring|maßgeschneiderte Details wie Abnäher und scharfe Kanten
Streetwear|Casual-Looks mit Hoodies, Sneakern und Caps
Athleisure|Sportliche Teile wie Leggings werden alltagstauglich kombiniert
Normcore|unauffälliger Minimalstil mit Jeans und Basic-Shirts
Quiet Luxury|Understatement mit hochwertigen Materialien ohne Logos
Dopamine Dressing|bunte, fröhliche Farben zur Stimmungsaufhellung
Cottagecore|romantische, ländlich inspirierte Kleider und Stickereien
Utility Trend|Overalls, Cargo-Taschen und funktionale Materialien
Sheer Fabrics|Durchscheinende Stoffe wie Organza oder Mesh
Balletcore|Body, Wickelcardigan und Tüll inspiriert vom Ballett
Preppy Style|College-Look mit Blazer, Faltenrock und Loafern
Y2K|Retrotrend mit Crop Tops, Low-Rise-Jeans und Glitzerelementen
Boho|Ethno-Prints, Fransen und fließende Silhouetten
Minimalismus|reduzierte Formen, neutrale Farben, klare Linien
Maximalismus|Mix aus Prints, Farben und Accessoires ohne Zurückhaltung
Androgyn|Verschmelzung maskuliner und femininer Schnitte
Power Suit|markant geschneiderter Anzug für Business-Auftritte
Slip Dress|Seidiges Kleid mit Spaghettiträgern im Lingerie-Stil
Paperbag-Taille|Hosenbund mit gerafftem, paperbag-ähnlichem Abschluss
Wide-Leg Pants|weite Hosen, die locker über den Schuhen fallen
Mock Neck|hoher, aber nicht umgeschlagener Kragen
Cut-Outs|gezielt platzierte Aussparungen an Kleidern oder Tops
Matching Set|Ober- und Unterteil aus demselben Stoff und Print
Statement Sleeve|voluminöse Ärmel wie Puff oder Trompete
Sustainable Fashion|Mode aus recycelten oder zertifizierten Materialien
"""),
        "Haute Couture": parse_entries("""
Maison Chanel|legendäres Pariser Haus mit tweedigen Kostümen
Christian Dior Bar Jacket|ikonischer Silhouettenstart des New Look 1947
Givenchy Atelier|bekannt für klare Linien und Audrey Hepburn Looks
Atelier Versace|dramatische Schnitte, Kristalle und Slits
Balenciaga Cristóbal|Architekt der Couture mit Skulpturformen
Schiaparelli Surrealismus|Augen- und Ohrenschmuck, inspiriert von Dalí
Elie Saab Perlenstickerei|romantische Roben voller Perlen und Spitze
Zuhair Murad Cape-Dresses|orientalisch inspirierte Capes und Cut-outs
Iris van Herpen 3D|technologische Couture aus gedruckten Strukturen
Maison Margiela Artisanal|Upcycling, Dekonstruktion und Handarbeit
Giambattista Valli Tüllwolken|aufwendige Volumen in Bonbonfarben
Alexandre Vauthier Power Couture|Schulterbetonte Silhouetten mit Pailletten
Ralph & Russo|britische Couture mit Pastelltönen und Blumenapplikationen
Valentino Haute Couture|Pierpaolo Picciolis Farbflächen und Schleppen
Fendi Couture|Pelz- und Stickkunst in Rom
Jean Paul Gaultier Corsets|ikonische Korsetts und maritime Details
Chambre Syndicale|Gremium, das Couture-Häuser in Paris zulässt
Flou vs. Tailleur|zwei Departments für fließende Roben und strukturierte Anzüge
Lesage Stickerei|historisches Atelier für Perlen und Pailletten
Lemarié Federn|Federkunstwerkstatt für Couture
Première|Chef-Schneiderin, die Atelierteams leitet
Toile|Probekleid aus Baumwolle vor dem finalen Stoff
Bastidor|metallener Körper für Millinery und Kopfschmuck
HouteFourrure|Pelzdivision innerhalb eines Hauses
Client Fitting|mehrere Anproben, oft drei Termine
Savoir-Faire|Wissen und Handwerk, das Generationen weitergeben
Lookbook Shooting|inszeniert Kollektionen, bevor Kundinnen bestellen
Couture Calendar|zwei offizielle Wochen pro Jahr in Paris
Made-to-Measure|jedes Kleidungsstück auf individuelle Maße gefertigt
Atelier Délai|Herstellung dauert oft 600 Arbeitsstunden
"""),
        "Berühmte Designer": parse_entries("""
Coco Chanel|schuf das kleine Schwarze und Kostüme mit Ketten
Christian Dior|initiierte den New Look 1947
Yves Saint Laurent|brachte den Smoking für Frauen auf den Laufsteg
Karl Lagerfeld|prägte Chanel und Fendi jahrzehntelang
Alexander McQueen|berühmt für dramatische, avantgardistische Shows
Donatella Versace|leitet das Haus Versace mit glamourösen Prints
Giorgio Armani|Meister der cleanen Anzüge und Red-Carpet-Roben
Ralph Lauren|präsentierte den American Preppy Lifestyle
Vivienne Westwood|Punk-Ikone mit Tartans und Korsetts
Tom Ford|relaunchte Gucci und gründete eigenes Label mit Sexappeal
Phoebe Philo|minimalistische Designs bei Céline
Stella McCartney|setzt auf nachhaltige, vegane Materialien
Maria Grazia Chiuri|erste weibliche Kreativdirektorin bei Dior
Pierpaolo Piccioli|verantwortlich für farbintensive Valentino-Couture
Riccardo Tisci|mischte Streetwear in Givenchy und Burberry
Demna|experimenteller Kreativchef bei Balenciaga
Jonathan Anderson|LOEWE und JW Anderson mit Kunstreferenzen
Olivier Rousteing|Balmain Designer mit strukturierten Schultern
Rei Kawakubo|Comme des Garçons Gründerin, die Dekonstruktion liebt
Miuccia Prada|intellektuelle Minimalistin und Miu Miu Designerin
Tory Burch|amerikanische Designerin mit Boho-Preppy Look
Michael Kors|bekannt für Jetset-Looks und Accessoires
Hedi Slimane|brachte Skinny-Silhouetten zu Dior Homme und Celine
Issey Miyake|Pleats Please und technologische Stoffe
Zac Posen|Hollywood-Glamour mit dramatischen Röcken
Carolina Herrera|klassische Eleganz für First Ladies
Alber Elbaz|Lanvin Designer mit verspielten Details
Nicolas Ghesquière|Louis Vuitton Designer mit Sci-Fi-Anklängen
Virgil Abloh|Off-White Gründer und LV Herrenkreativdirektor
Sarah Burton|führte Alexander McQueen nach seinem Tod weiter
"""),
        "Englische Ausdrücke (C2-Niveau, auf Englisch formuliert)": parse_entries("""
to take something with a grain of salt|means to treat a statement with cautious skepticism
silver lining|the hopeful aspect of an otherwise negative situation
cut to the chase|skip preliminaries and go straight to the essential point
sweeping generalization|an overbroad conclusion lacking nuance
serendipitous encounter|a fortunate meeting that occurs by chance
ubiquitous presence|something that seems to appear everywhere
nuanced argument|a line of reasoning with subtle distinctions
quintessential example|the purest embodiment of a category
jump on the bandwagon|join a trend once it has become popular
think on your feet|respond quickly and effectively without preparation
a double-edged sword|something that has both positive and negative consequences
play devil's advocate|argue the opposite side to test its strength
meticulous attention to detail|obsessing over every small component
beyond the scope|outside the defined remit of a discussion
cast a wide net|seek many possibilities at once
bite the bullet|face a difficult situation with resolve
call the shots|be the person who makes the key decisions
broach the subject|introduce a sensitive topic
by the same token|for the same reason; likewise
in the nick of time|at the very last possible moment
put something on the back burner|delay dealing with it for later
reinvent the wheel|waste effort creating something that already exists
rule of thumb|a broadly accurate practical principle
up in the air|undecided or unresolved
on the same wavelength|sharing identical thoughts or feelings
play it by ear|improvise rather than sticking to a plan
read between the lines|understand implied or hidden meanings
raise the bar|increase standards or expectations
word of mouth|information spread by spoken recommendations
to walk a fine line|balance between two opposing demands
"""),
        "Chemie 10. Klasse": parse_entries("""
Atom|Grundbaustein der Materie mit Protonen, Neutronen, Elektronen
Periodensystem|ordnet Elemente nach Ordnungszahl und Eigenschaften
Valenzelektronen|Elektronen der äußersten Schale, bestimmen Bindungen
Ionenbindung|Bindung zwischen positiv und negativ geladenen Teilchen
Kovalente Bindung|Atome teilen Elektronenpaare
Metallbindung|delokalisierte Elektronen bewegen sich in einem Metallgitter
Oxidation|Abgabe von Elektronen
Reduktion|Aufnahme von Elektronen
Redoxreaktion|Gleichzeitige Oxidation und Reduktion
Oxidationszahl|gedachter Ladungszustand eines Atoms
Säuren|geben Protonen (H+) ab
Basen|nehmen Protonen auf oder geben OH- Ionen ab
pH-Wert|Maß für die Konzentration von H+-Ionen
Neutralisation|Reaktion von Säure mit Base zu Salz und Wasser
Titration|Verfahren zur Konzentrationsbestimmung einer Lösung
Massenwirkungsgesetz|beschreibt Gleichgewichtskonstanten chemischer Reaktionen
Katalysator|senkt Aktivierungsenergie, ohne verbraucht zu werden
Endotherm|Reaktion, die Wärme aufnimmt
Exotherm|Reaktion, die Wärme freisetzt
Stöchiometrie|Berechnung von Stoffmengenverhältnissen
Mol|Basiseinheit für Stoffmenge, 6,022 · 10^23 Teilchen
Avogadro-Konstante|Zahl der Teilchen pro Mol
Isotope|Atome desselben Elements mit unterschiedlicher Neutronenzahl
Elektrolyse|Zerlegung einer Verbindung durch elektrischen Strom
Galvanische Zelle|wandelt chemische Energie in elektrische um
Elektronegativität|Maß für die Fähigkeit, Elektronen anzuziehen
Salzlösung|Ionen sind frei beweglich und leiten Strom
Präzipitation|Entstehung eines unlöslichen Niederschlags
Destillation|Trennung von Flüssigkeiten anhand unterschiedlicher Siedepunkte
Chromatografie|Trennverfahren anhand unterschiedlicher Laufgeschwindigkeiten
"""),
        'Serie "Emily in Paris"': parse_entries("""
Emily Cooper|US-Marketingexpertin, die nach Paris versetzt wird
Sylvie Grateau|strenge Chefin von Savoir mit perfektem Stil
Gabriel|Chefkoch im Restaurant Les Deux Compères
Mindy Chen|Emilys beste Freundin und Sängerin
Camille|Künstlerin und Gabriels Partnerin
Savoir|Pariser Agentur, die Emily beschäftigt
Pierre Cadault|exzentrischer Designer, den Emily betreut
Maison Lavaux|Champagnerhaus von Camille's Familie
Antoine Lambert|Parfümmogul und Savoir-Kunde
Julien|Social-Media-Spezialist bei Savoir
Luc|älterer Kollege mit Liebe zu französischem Kino
Emilygram|Emilys wachsender Instagram-Account
Maison Lavaux Spritz|Kampagne mit dem Champagner-Sprayer
La Liste|exklusive Restaurantliste, auf die Emily hinarbeitet
Fashion Week Rooftop|Event, das Emily spontan organisiert
Chicago Office|Emilys vorherige Arbeitsstelle
BnF Bibliothek|Ort eines geheimen Mode-Shootings
STC (Save the Champ)|Hashtag gegen das Übernehmen von Antoine
Madeline Wheeler|Amerikanische Chefin, die später in Paris auftaucht
Château Lalisse|Ort eines Luxus-Retreats
Emily in Paris Season 2 Cliffhanger|Emily soll wählen zwischen USA und Paris
Grey Space Agency|neuer Arbeitgeber, den Emily kurz ausprobiert
Alfie|britischer Banker, der Emilys Liebe wird
Bateau Mouche Event|Launch auf einem Seine-Boot
Patrice|Sylvies Ehemann, mit dem sie in offenem Arrangement lebt
Petra|Mitstudentin im Sprachkurs, die Emily zum Shoplifting verleitet
McDonald's Pitch|Emily verkauft Burger mit Haute-Couture-Twist
Maison Lavaux Garden Party|Ort des Dramas zwischen Emily, Gabriel und Camille
Rue des Fossés Saint-Jacques|Straße von Emilys Wohnung
La Perla Restaurant|Gabriels neues Lokalprojekt
"""),
        "Beauty & Styling": parse_entries("""
Double Cleansing|erst Öl-, dann Schaumreiniger für porentiefe Sauberkeit
Chemical Peeling|AHA oder BHA lösen abgestorbene Hautzellen
Retinol|Vitamin-A-Derivat zur Kollagenbildung
Niacinamide|beruhigt Rötungen und reguliert Talgproduktion
SPF 50|täglicher Sonnenschutz, auch bei Bewölkung
Glass Skin|koreanischer Trend für spiegelglatte Haut
Brow Lamination|Augenbrauen werden gebürstet und fixiert
Tightlining|Eyeliner zwischen den Wimpern für unsichtbare Definition
Cat Eye|Winged Liner, der das Auge optisch anhebt
Soap Brows|Brow-Styling mit transparentem Seifenfilm
Color Correcting|Pfirsich gegen Blau, Grün gegen Rötungen
Underpainting|Bronzer und Concealer vor der Foundation auftragen
Cream Blush|sorgt für natürlichen Glow
Baking|Fixieren von Concealer mit viel losem Puder
Lip Stain|leichte Farbe, die lange hält ohne zu kleben
Glossy Eye|Lidschatten plus Balm für glänzende Lider
Slick Bun|streng zurückgekämmter Dutt
Beach Waves|lässige Locken mit Salzspray
Diffuser|Aufsatz für Locken ohne Frizz
Keratin Treatment|glättet Haare semi-permanent
Balayage|freihändig gemalte Strähnen mit weichem Übergang
Olaplex|Bonding-Produkt zur Haarstärkung
Scalp Scrub|Peeling für die Kopfhaut
Gua Sha|Massage-Stein für Lymphdrainage
LED-Maske|Lichttherapie gegen Akne oder Falten
Gel Maniküre|UV-härtender Nagellack für langen Halt
French Fade|weicher Ombre-French-Look
Microblading|semi-permanente Brauenhärchenzeichnung
Lash Lift|Wimpern werden nach oben gebogen und gefärbt
Setting Spray|fixiert Make-up und nimmt Pudrigkeit
"""),
        "Handtaschen": parse_entries("""
Hermès Birkin|ikonische Tasche mit Wartezeiten und Sattlerhandwerk
Hermès Kelly|Tasche mit Trapezform und H-Schnalle
Chanel 2.55|Steppleder mit Kettenriemen und Mademoiselle-Schloss
Dior Lady Dior|Kulttasche mit Cannage-Steppung und Charms
Louis Vuitton Speedy|klassische Duffel aus Monogram Canvas
Louis Vuitton Capucines|Tasche mit LV-Bügel und strukturierter Form
Gucci Jackie 1961|Hobo-Bag mit Kolbenverschluss
Gucci Marmont|Matelassé-Leder und GG-Schnalle
Prada Galleria|Saffianoleder mit Struktur und Dreifachfach
Prada Re-Edition|Nylon-Satteltasche aus den 2000ern
Fendi Baguette|schmale Schultertasche, gefeiert in Sex and the City
Fendi Peekaboo|Tasche mit zwei Fächern und Mittelseparator
Bottega Veneta Jodie|geflochtene Hobo mit Knoten
Bottega Cassette|gepolsterte Intrecciato-Quadrate
Balenciaga City|abgewetzter Motorradtaschen-Look
Celine Luggage|charakteristische Flügel und Smiley-Front
Celine Triomphe|Logo-verschlossene Schultertasche
Loewe Puzzle|geometrische Panels, die sich falten lassen
Loewe Basket|Strohtasche mit Ledergriffen
Saint Laurent Sac de Jour|strukturierter Tote mit Hängeschloss
Saint Laurent Kate|Abendtasche mit YSL-Kette und Quaste
Givenchy Antigona|kantige Boston Bag mit Dreieckslogo
Mulberry Bayswater|britischer Klassiker mit Postman’s Lock
Chloé Marcie|Hufeisen-Stitching und Tassel
Chloé Drew|runde Tasche mit Metallbügel
Cuyana Tote|Minimalistische Ledertasche zum Personalisieren
Mansur Gavriel Bucket Bag|minimaler Lederbeutel mit Kordelzug
Polène Numéro Un|Pariser Label mit geschwungenen Linien
JW Pei Gabbi|veganer Stoff mit ruched Handle
Telfar Shopping Bag|Unisex-Tasche mit demokratischem Drop
"""),
    },
    "sibylle": {
        "Kardiologie": parse_entries("""
STEMI|ST-Strecken-Hebungsinfarkt mit sofortiger Reperfusion
NSTEMI|Infarkt ohne ST-Hebung, Diagnose via Troponin
Troponin T|hoch-sensitiver Biomarker für Myokardschaden
TIMI-Score|Risikostratifizierung beim akuten Koronarsyndrom
Killip-Klassifikation|Einteilung der Herzinsuffizienz beim Infarkt
PCI|perkutane Koronarintervention mit Stentimplantation
CABG|Koronararterien-Bypass-Operation
Dual Antiplatelet Therapy|Kombination aus ASS und P2Y12-Hemmer
DES-Stent|medikamentenbeschichteter Stent mit geringerer Restenose
Fractional Flow Reserve|Druckmessung zur Beurteilung koronarer Stenosen
IMPELLA|perkutane linksventrikuläre Unterstützungspumpe
IABP|intraaortale Ballonpumpe bei kardiogenem Schock
HFpEF|Herzinsuffizienz mit erhaltener Ejektionsfraktion
HFrEF|Herzinsuffizienz mit reduzierter Ejektionsfraktion
NYHA-Klassen|Belastungsabhängige Einteilung der Herzinsuffizienzsymptome
NT-proBNP|Biomarker zur Differenzierung von Dyspnoe-Ursachen
ACE-Hemmer|Basistherapie der systolischen Herzinsuffizienz
ARNI|Angiotensin-Rezeptor-Neprilysin-Inhibitor, z. B. Sacubitril/Valsartan
SGLT2-Inhibitor|dapagliflozin zur Prognoseverbesserung bei Herzinsuffizienz
CRT-D|kardiale Resynchronisation mit Defibrillatorfunktion
Mitral-Clip|kathetergestützte Mitralklappenrekonstruktion
TAVI|Transkatheter-Aortenklappenimplantation
Left Bundle Branch Block|typische Indikation für CRT
Heart-Team|interdisziplinäre Fallkonferenz bei komplexen Klappenerkrankungen
Coronary Calcium Score|CT-basierter Marker für Atherosklerose
Cardiac MRI|Goldstandard für Myokarditisdiagnostik
Late Gadolinium Enhancement|zeigt fibrotische Myokardareale
Cardio-Onkologie|Überwachung kardiotoxischer Chemotherapien
ESC-Guidelines|europäische Leitlinien für Herztherapien
Cardiac Rehab Phase II|ambulantes Training nach Herzereignis
"""),
        "Hypertensiologie": parse_entries("""
Praxisblutdruck|Messung beim Arzt, kann Weißkitteleffekt zeigen
24h-RR|Langzeitmessung zur Erfassung nächtlicher Werte
Weißkittelhypertonie|erhöhte Werte nur in medizinischer Umgebung
Masked Hypertension|normale Praxiswerte, aber erhöhte ambulant
Arterieller Hypertonus Grad 1|140-159/90-99 mmHg
Arterieller Hypertonus Grad 2|160-179/100-109 mmHg
Arterieller Hypertonus Grad 3|≥180/110 mmHg
Hypertensive Krise|RR > 180/120 ohne Organschaden
Hypertensiver Notfall|RR > 180/120 mit Organschaden
Primärer Hyperaldosteronismus|führt zu therapieresistenter Hypertonie
Renale Denervation|katheterbasierte Therapie bei Resistenz
Salzrestriktion|unter 5 g Kochsalz täglich empfohlen
DASH-Diät|reich an Gemüse, Obst, wenig Fett zur Blutdrucksenkung
ACE-Hemmer|First-Line Medikation bei Hypertonie
ARB|Alternative zu ACE-Hemmern ohne Husten
Kalziumantagonisten|verringern Gefäßtonus
Thiazid-Diuretikum|senkt Blutdruck über Natriurese
Betablocker|indiziert bei Hypertonie plus Herzinsuffizienz
Spironolacton|wirkt bei therapieresistenter Hypertonie
Orthostatische Hypotonie|RR-Abfall beim Aufstehen, relevant bei Therapie
Morning Surge|morgendlicher Blutdruckanstieg
Nocturnal Dipping|physiologischer nächtlicher RR-Abfall
Non-Dipper|fehlender nächtlicher RR-Abfall, höheres Risiko
Central Blood Pressure|aortaler Druck, messbar via Pulswellenanalyse
Pulsdruck|Differenz zwischen systolischem und diastolischem RR
Arteriosteife|Pulse Wave Velocity als Surrogatmarker
Hypertonie bei Schwangerschaft|Gestationshypertonie vs. Präeklampsie
HELLP-Syndrom|hämolytische Komplikation mit Hypertonie
Renovaskuläre Hypertonie|Nierenarterienstenose verursacht hohen RR
Ambulantes Blutdrucktagebuch|Selbstmessungen zur Therapieanpassung
"""),
        "Rhythmologie": parse_entries("""
Vorhofflimmern|häufigste supraventrikuläre Arrhythmie
CHA2DS2-VASc|Score zur Schlaganfallrisikoabschätzung
HAS-BLED|Score zur Blutungsrisikoeinschätzung
Katheterablation|Veröden arrhythmogener Herde mittels Radiofrequenz
Kryoballon|Kältebasierte Pulmonalvenenisolation
Pulmonalvenenisolation|Standardprozedur bei paroxysmalem Vorhofflimmern
AV-Knoten-Reentry|typische Ursache für paroxysmale Supraventrikuläre Tachykardie
Wolff-Parkinson-White|angeborene akzessorische Leitungsbahn
His-Bündel-Ablation|Therapie bei therapierefraktärem Vorhofflimmern
ICD|Implantierbarer Cardioverter-Defibrillator
Subkutaner ICD|Defi ohne transvenöse Elektroden
CRT-P|kardiale Resynchronisation ohne Defibrillatorfunktion
Brugada-Syndrom|genetische Kanalopathie mit Risiko für Kammerflimmern
Long-QT-Syndrom|verzögerte Repolarisation, erhöht Torsade-de-pointes-Risiko
Ajmalin-Test|Provokationstest zur Brugada-Diagnostik
ZIO Patch|Langzeit-EKG-Monitoring als Patch
Holter-EKG|24h-EKG zur Arrhythmieerkennung
Loop-Recorder|implantierter Monitor für seltene Synkopen
Sinusknoten-Dysfunktion|führt zu bradykarden Episoden
Sick-Sinus-Syndrom|Kombination aus Bradykardie und Tachykardie
Pacemaker-DDD|Zweistimulationssystem für Vorhof und Ventrikel
Leadless Pacemaker|kabelloser VVI-Schrittmacher
Vagus-Manöver|z. B. Valsalva zur Terminierung supraventrikulärer Tachykardie
Adenosin|Kurz wirksames Medikament zur AV-Knoten-Blockade
Torsade de pointes|polymorphe VT mit QT-Verlängerung
Elektrokonversion|Synchroner Schock zur Rhythmusnormalisierung
Amiodaron|Breitband-Antiarrhythmikum mit vielen Nebenwirkungen
Flecainid|Klasse-IC-Medikament für Rhythmuskontrolle
His-Bundle-Pacing|physiologisches Schrittmacherverfahren
EHRA-Score|symptomatische Einteilung bei Vorhofflimmern
"""),
        "Diabetologie": parse_entries("""
HbA1c|langfristiger Parameter zur Glukosekontrolle
CGM|kontinuierliches Glukosemonitoring über Sensoren
Time in Range|Prozentsatz der Zeit im Zielbereich 70–180 mg/dl
Basal-Bolus-Therapie|Langzeitinsulin plus Mahlzeiteninsulin
Insulinpumpe|kontinuierliche subkutane Infusionspumpe
Closed-Loop-System|Kombination aus CGM und Automatikpumpe
Metformin|First-Line-Medikament bei Typ-2-Diabetes
SGLT2-Hemmer|fördern Glukoseausscheidung über die Niere
GLP-1-Rezeptoragonist|wirkt appetitzügelnd und gewichtsreduzierend
DPP-4-Hemmer|verlängern Wirkung endogener Incretine
Sulfonylharnstoffe|erhöhen Insulinsekretion, Hypoglykämie-Risiko
Hypoglykämie|unter 70 mg/dl mit Symptomen wie Schwitzen
Hyperglykämie|erhöhte Blutzuckerwerte, führen zu Polyurie
DKA|diabetische Ketoazidose mit Ketonkörpern und Azidose
HHS|hyperosmolares hyperglykämisches Syndrom ohne Ketose
Fuß-Check|jährliche Untersuchung auf Neuropathie
Augen-Hintergrund|Screening auf diabetische Retinopathie
Albuminurie|Frühes Zeichen diabetischer Nephropathie
Neuropathie|schädigt sensible und autonome Nerven
Carb Counting|berechnet Kohlenhydrateinheiten für Insulindosis
Bolus-Rechner|Hilft, Mahlzeiteninsulin einzustellen
Somogyi-Effekt|morgendliche Hyperglykämie nach nächtlicher Hypo
Dawn-Phänomen|morgendlicher Glukoseanstieg durch Hormone
Inselzelltransplantation|Therapieoption bei Typ-1-Diabetes
Hybrid Closed Loop|automatisiert Basalrate, Bolus bleibt manuell
Libre Sensor|Flash-Glukosemonitor ohne Kalibrierung
AGP-Profil|standardisierte CGM-Auswertung
Glyx-Index|gibt Geschwindigkeit des Blutzuckeranstiegs an
Low-Carb-Ernährung|reduziert Kohlenhydrate zur BZ-Kontrolle
Sick-Day-Regeln|angepasste Insulin- und Flüssigkeitszufuhr bei Krankheit
"""),
        "Lipidmanagement": parse_entries("""
LDL-Cholesterin|primäres Zielparameter laut Leitlinien
non-HDL-Cholesterin|Ersatzmarker bei Hypertriglyzeridämie
Triglyzeride|Fette, die bei Werten > 500 mg/dl Pankreatitis riskieren
Lp(a)|genetisch bestimmtes Lipoprotein mit Atheroskleroserisiko
ApoB|Marker für Anzahl atherogener Partikel
Familial Hypercholesterolemia|erblich bedingt hohe LDL-Werte
Statine|HMG-CoA-Reduktasehemmer zur LDL-Senkung
Ezetimib|hemmt Cholesterinaufnahme im Darm
PCSK9-Inhibitor|monoklonale Antikörper, die LDL-Rezeptoren erhalten
Inclisiran|siRNA, die PCSK9-Expression reduziert
Bempedoinsäure|ATP-Citrat-Lyase-Hemmer zur LDL-Senkung
Fibrate|senken vor allem Triglyzeride und erhöhen HDL
Omega-3-Fettsäuren|senken hohe Triglyzeride
Nikotinsäure|älteres Mittel zur Lipidtherapie mit Flush
LDL-Apherese|extrakorporal bei homozygoter FH
Sekundärprävention|intensivere LDL-Ziele nach Ereignissen
ESC Ziel <55 mg/dl|empfohlen für sehr hohes Risiko
Statinintoleranz|Myalgien oder CK-Erhöhung unter Therapie
Coenzym Q10|Supplements, die Myalgien lindern sollen
Lifestyle|Gewichtsreduktion, mediterrane Kost, Sport
Plant Sterols|senken Cholesterinabsorption
Bempedoic Acid|wird nur in der Leber aktiviert, weniger Muskelsymptome
Coronary Artery Calcium|entscheidet bei intermediärem Risiko
Lipidprofil nüchtern|notwendig bei extremen Triglyzeriden
Remnant-Cholesterin|Atherogener Anteil aus VLDL/IDL
Familienanamnese|erhöhtes Risiko bei frühem Infarkt der Eltern
Xanthome|cholesterinhaltige Hautablagerungen
ARC-Studien|belegen Nutzen intensiver LDL-Senkung
Monotherapie vs. Kombination|Mehrere Wirkstoffe erreichen strenge Ziele
Lipidambulanz|spezialisierte Einrichtung für schwere Dyslipidämien
"""),
        "Gesunde Ernährung": parse_entries("""
Mediterrane Diät|betont Olivenöl, Gemüse, Fisch
Ballaststoffe|fördern Sättigung und Darmgesundheit
Vollkorn|liefert komplexe Kohlenhydrate und Mineralstoffe
Omega-3-Fettsäuren|entzündungshemmend, etwa aus Lachs und Leinsamen
Pflanzenproteine|Hülsenfrüchte, Tofu und Tempeh
Fermentierte Lebensmittel|Kimchi, Kefir und Sauerkraut für Mikrobiom
Meal Prep|Vorbereiten gesunder Mahlzeiten im Voraus
Portionskontrolle|bewusstes Abmessen vermeidet Überessen
Saisonal essen|Lebensmittel nach Erntezeiten auswählen
Regional einkaufen|kurze Transportwege und frische Ware
Mindful Eating|achtsames Essen ohne Ablenkung
Hydration|mindestens 1,5–2 Liter Wasser pro Tag
Zuckerreduktion|versteckte Zucker in Getränken meiden
Salzlimit|unter 5 g pro Tag laut WHO
Healthy Fats|Avocado, Nüsse, Samen
Flexitarisch|überwiegend pflanzlich, gelegentlich Fleisch
Intervallfasten|Essensfenster wie 16:8 zur Stoffwechselregulation
Glyx-Kurve|Blutzuckerschwankungen durch Low-GI-Lebensmittel minimieren
Superfoods|Beeren, Chia oder Matcha mit hoher Nährstoffdichte
Meal Timing|Proteine nach dem Training fördern Regeneration
Antioxidantien|Vitamin C, E und Polyphenole schützen Zellen
Phytonährstoffe|Farbstoffe wie Carotinoide, Flavonoide
Makronährstoffverteilung|ausgewogenes Verhältnis von KH, Fett, Protein
Sprossen|vitaminreiche Keimlinge auf Sandwiches und Bowls
Smoothie Bowls|Mix aus Obst, Gemüse und Toppings
Meal Planning|Wochengerichte planen spart Zeit und Geld
Food Waste vermeiden|Reste kreativ verwerten
Nussbutter|gesunde Fette und Eiweiß aus Mandeln oder Erdnüssen
B12 Supplement|wichtig bei veganer Ernährung
Calciumquellen|Brokkoli, Mandeln und angereicherte Drinks
"""),
        "Frauengesundheit": parse_entries("""
Pap-Abstrich|Screening auf Zervixdysplasien
HPV-Impfung|Schützt vor Hochrisiko-Typen, die Krebs verursachen können
BRCA-Testung|genetisches Screening bei familiärem Brustkrebs
Mammographie|Bildgebung ab 50 zum Brustkrebsscreening
Selbstabtastung|monatliche Brustkontrolle
Knochendichte-Messung|erkennt Osteoporoserisiko nach der Menopause
Folsäure|Supplement vor und während Frühschwangerschaft
Gestationsdiabetes|Glukosetest zwischen 24. und 28. SSW
Präeklampsie-Screening|Überwachung von Blutdruck und Proteinurie
Hebammenbetreuung|begleitet Schwangerschaft und Wochenbett
Endometriose|chronische Erkrankung mit ektopischem Endometriumgewebe
PCOS|Polyzystisches Ovarialsyndrom mit Zyklusstörungen
HRT|Hormonersatztherapie zur Linderung menopausaler Symptome
Beckenboden-Training|beugt Inkontinenz und Prolaps vor
Stillberatung|unterstützt beim erfolgreichen Stillen
IUD|Intrauterinspange zur Langzeitverhütung
Kupferkette|hormonfreie Alternative zum Kupfer IUP
Langzyklus-Pille|Verhindert monatliche Entzugsblutungen
Fertilitätsmonitoring|Basaltemperatur und LH-Tests zur Zyklusbestimmung
Pränataldiagnostik|NIPT, Chorionzotten, Amniozentese
Doula|nicht-medizinische Geburtsbegleitung
Stillhütchen|Hilfsmittel bei wunden Brustwarzen
Postpartale Depression|psychische Erkrankung nach Geburt
Babyblues|kurzfristige Stimmungsschwankung nach Entbindung
Muttermilchbanken|Spenden für Frühgeborene
Stillfreundliche Medikamente|Kompatibilität via Embryotox prüfen
Intimpflege|pH-neutrale Produkte, keine Duftstoffe
Vulvodynie|chronische Schmerzen im Vulvabereich
Lichen sclerosus|entzündliche Hauterkrankung im Genitalbereich
Menstruationstracker|Apps zur Zyklusauswertung
"""),
        "Spanisch Niveau 11. Klasse": parse_entries("""
Subjuntivo|modo verbal para expresar deseos, dudas o emociones
Pluscuamperfecto|tiempo que describe acciones anteriores a otra acción pasada
Condicional compuesto|expresa posibilidades no cumplidas en el pasado
Pretérito indefinido|tiempo para acciones puntuales terminadas
Pretérito imperfecto|acciones habituales o descripciones en el pasado
Perífrasis ir a + infinitivo|expresa futuro inmediato
Se impersonal|estructura para hablar sin sujeto específico
Ser vs. estar|ser para cualidades permanentes, estar para estados temporales
Por vs. para|por indica causa, para objetivo o destino
Pronombres de objeto indirecto|le, les para indicar a quién se dirige la acción
Cláusulas con si|si + presente conduce a futuro, si + imperfecto de subjuntivo a condicional
Estilo indirecto|transforma citas directas usando cambios de tiempo
Conectores discursivos|por lo tanto, sin embargo, a pesar de que
Voz pasiva perifrástica|ser + participio
Voz pasiva refleja|se + verbo en tercera persona
Concordancia de adjetivos|género y número coinciden con el sustantivo
Oraciones de relativo|que, quien, cuyo para unir ideas
Futuro perfecto|hablar de acciones completadas antes de otro momento futuro
Mandatos negativos|no + subjuntivo (no hables)
Mandatos formales|subjuntivo presente (hable, hablen)
Expresiones idiomáticas|estar en las nubes, tener ganas de
Falsos amigos|actual significa real, no actual
Campos léxicos|palabras relacionadas con un tema específico
Conectores temporales|antes de que, mientras, después de
Perífrasis estar + gerundio|acción en progreso
Perífrasis llevar + gerundio|indica duración (llevo estudiando dos horas)
Verbos de cambio|ponerse, hacerse, volverse
Discurso persuasivo|tesis, argumentos y contraargumentos
Resumen académico|síntesis con ideas principales sin opinión personal
Comentario cultural|analiza costumbres, música o literatura
"""),
        "Hamburg": parse_entries("""
Elbphilharmonie|Konzerthaus mit Plaza und gläserner Welle
Speicherstadt|UNESCO-Weltkulturerbe mit Lagerhäusern auf Eichenpfählen
HafenCity|modernes Stadtviertel an der Elbe
Reeperbahn|Vergnügungsmeile im Stadtteil St. Pauli
Landungsbrücken|Anleger für Hafenfähren und Hafenrundfahrten
Miniatur Wunderland|größte Modelleisenbahn der Welt
Alster|Binnen- und Außenalster für Segelboote und Jogger
Planten un Blomen|Park mit Wasserspielen und Tropengewächshaus
Michel|St. Michaelis Kirche mit Aussichtsplattform
Fischmarkt|Sonntagmorgenmarkt mit Marktschreiern
Övelgönne|Museumshafen mit historischen Schiffen
Elbtunnel|Alter Tunnel von 1911 für Fußgänger und Radfahrer
Blankenese Treppenviertel|villengeprägtes Elbviertel mit Hanglage
Altonaer Balkon|Aussichtspunkt mit Blick über den Hafen
Schanzenviertel|Hipsterquartier mit Street Art und Cafés
Hagenbecks Tierpark|traditioneller Zoo mit Freigehegen
Köhlbrandbrücke|markante Brücke über den Elbhafen
Binnenalster Fontäne|Wasserfontäne als Wahrzeichen im Sommer
Hamburger Rathaus|Neorenaissancebau mit 647 Räumen
Jungfernstieg|Boulevard zwischen Binnenalster und Einkaufspassagen
Europa Passage|Shoppingcenter mit Glasdach
Elberadweg|beliebte Radroute entlang der Elbe
Hafengeburtstag|jährliches Fest mit Schiffsparaden
Cruise Center|Terminals für Kreuzfahrtschiffe
Süllberg|Aussichtsrestaurant im Westen der Stadt
S-Bahn Linie S1|verbindet Flughafen und Innenstadt
U4 HafenCity|U-Bahn-Linie zum Überseequartier
Gängeviertel|historisches Künstlerquartier
Stadtpark|große Grünanlage mit Planetarium
Bürgerhaus Barmbek|Kulturzentrum im Norden
"""),
    },
}

def slugify(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = normalized.encode("ascii", "ignore").decode()
    ascii_text = re.sub(r"[^a-z0-9]+", "_", ascii_text.lower())
    return ascii_text.strip("_")


def build_questions(person: str, category: str, facts: list[dict]) -> list[dict]:
    questions = []
    slug = slugify(category)
    template = TEMPLATES.get(category, TEMPLATES["default"])
    answers = [fact["answer"] for fact in facts]
    total = len(facts)
    for idx, fact in enumerate(facts, start=1):
        options = [fact["answer"]]
        for offset in range(1, 4):
            options.append(answers[(idx - 1 + offset) % total])
        rng = random.Random(hash((person, category, idx)) & 0xFFFFFFFF)
        rng.shuffle(options)
        question_text = fact.get("question") or template.format(prompt=fact["prompt"])
        entry = {
            "id": f"{person}_{slug}_{idx:03d}",
            "category": category,
            "question": question_text,
            "answers": options,
            "correctIndex": options.index(fact["answer"]),
            "difficulty": "hard" if idx > 25 else "normal",
        }
        questions.append(entry)
    return questions


def main() -> None:
    output_dir = Path("questions")
    for person, categories in DATA.items():
        person_questions: list[dict] = []
        for category, facts in categories.items():
            if len(facts) < 4:
                raise ValueError(f"Kategorie {category} für {person} benötigt mindestens 4 Fakten, hat aber {len(facts)}")
            person_questions.extend(build_questions(person, category, facts))
        path = output_dir / f"{person}_questions.json"
        path.write_text(json.dumps(person_questions, ensure_ascii=False, indent=2))
        print(f"geschrieben: {path}")


if __name__ == "__main__":
    main()
