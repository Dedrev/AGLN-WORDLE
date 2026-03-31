# AGLN-WORDL
School project

Arbeitsauftrag: Projekt "Progressives Wordle" – Alternativer Leistungsnachweis
🎯 Ziel des Projekts

In diesem Projekt programmieren Sie in Kleingruppen eine erweiterte Version des beliebten Spiels "Wordle". Ziel ist es nicht nur, ein funktionierendes Spiel zu entwickeln, sondern vor allem den geschriebenen Code im Detail zu verstehen und erklären zu können.
👥 Rahmenbedingungen

    Gruppengröße: 2 bis 3 Personen.

    Eigenständigkeit: Der Code muss von Ihnen selbst geschrieben werden. Die Nutzung von Hilfsmitteln (Internet, KI, Foren) ist zur Recherche erlaubt, aber: Jeder kopierte oder generierte Code muss von jedem Gruppenmitglied im Schlaf verstanden und erklärt werden können.

    Programmiersprache: pro Gruppe frei wählbar

    Art der Anwendung: Die technische Plattform ist Ihnen freigestellt. Sie können das Spiel als Konsolenanwendung, als Desktop-Anwendung (Fenster/GUI) oder als Web-Anwendung umsetzen.

🎮 Spielmechanik & Funktionsumfang

Ihre Version von Wordle soll dynamischer sein als das Original und folgende Funktionen beinhalten:

    Sprachauswahl: Zu Beginn des Spiels muss der Spieler aus mindestens zwei verschiedenen Sprachen (z. B. Deutsch und Englisch) wählen können. Entsprechend müssen für die gewählten Sprachen passende Wörterbücher im Programm hinterlegt oder eingebunden sein.

    Start: Das erste zu erratende Wort besteht immer aus 3 Buchstaben.

    Progression: Errät der Spieler das Wort korrekt, steigt er ein Level auf. Das nächste Wort besteht dann aus 4 Buchstaben, danach aus 5 Buchstaben usw.

    Feedback: Nach jedem Versuch muss das System dem Spieler eine klare Rückmeldung geben (z. B. durch farbliche Markierungen):

        Buchstabe ist im Wort und an der richtigen Stelle.
****
        Buchstabe ist im Wort, aber an der falschen Stelle.

        Buchstabe kommt im Wort nicht vor.

    Ende: Das Spiel endet, wenn der Spieler die maximale Anzahl an Versuchen für das aktuelle Wort überschritten hat.

🏆 Das Highscore-System

Das Spiel muss über ein sinnvolles Highscore-System verfügen, das am Ende einer Runde (oder dauerhaft gespeichert) ausgegeben wird.

Berechnungslogik (Vorgabe):

Um sowohl die Wortlänge als auch die Effizienz des Spielers zu belohnen, wird folgende Logik angewandt:

    Für jedes erratene Wort gibt es eine Basis-Punktzahl: Wortlänge * 10 Punkte.

    Für jeden nicht benötigten Versuch gibt es Bonuspunkte: Übrige Versuche * 5 Punkte.

Was der Highscore anzeigen muss:

Am Ende des Spiels (Game Over) muss folgende Statistik ausgegeben werden:

    Gesamtpunktzahl: Die Summe der Punkte aller erratenen Wörter.

    Längstes erratenes Wort: (z. B. "Das längste gelöste Wort hatte 7 Buchstaben").

    Gesamte Anzahl der Versuche: Wie viele Versuche wurden für den gesamten Durchlauf (über alle Level hinweg) benötigt.

💻 Technische Umsetzung & "Clean Code"

    Nutzen Sie sinnvolle Variablen- und Methodenbezeichner.

    Kommentieren Sie Ihren Code dort, wo komplexe Logik (z. B. die Überprüfung der Buchstaben) stattfindet.

    Lagern Sie wiederkehrende Aufgaben in eigene Funktionen/Methoden aus.

    Achten Sie auf eine saubere Strukturierung bei der Einbindung der verschiedenen Sprach-Wörterbücher (z. B. über separate Textdateien, JSON oder gut strukturierte Arrays).

🗣️ Die Bewertung: Das Fachgespräch

Die Bewertung dieses Leistungsnachweises basiert nicht auf der reinen Abgabe des Codes, sondern auf einem anschließenden Fachgespräch zwischen der Lehrkraft und der Gruppe.

    Dauer: ca. 15-20 Minuten pro Gruppe.

    Ablauf: Ich werde Sie bitten, das Programm zu starten und vorzuführen. Danach gehen wir gemeinsam durch Ihren Quellcode.

    Anforderung: Ich werde gezielt einzelne Gruppenmitglieder aufrufen, um bestimmte Code-Zeilen, Schleifen oder Methoden zu erklären.

    Inhalt: Sie müssen sowohl die Syntax (Warum steht da dieser Befehl? Wie ist er aufgebaut?) als auch die Semantik (Was bewirkt dieser Code-Block im Kontext des Spiels? Wie ist die logische Abfolge?) erklären können.

    Wichtiger Hinweis: Wenn Ihr Spiel perfekt funktioniert, Sie aber im Fachgespräch den Code nicht erklären können, gilt die Leistung als nicht erbracht. Das Code-Verständnis ist die oberste Priorität dieses Projekts!

📅 Zeitplan & Abgabe

    Projektstart: [Datum einfügen]

    Abgabe des Quellcodes: [Datum einfügen] (z. B. als ZIP-Datei oder via GitHub-Link)

    Fachgespräche: Finden am [Datum/Zeitraum einfügen] statt.
