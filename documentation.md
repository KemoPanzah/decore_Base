# Dokumentation
## **Allgemeines**
## Datenkontext
Der Datenkontext ist ein Eigenschaftswert der Dialogkomponente im Frontend. Dieser Wert wird bei der Widget-Initialisierung übernommen und bestimmt welcher Item-Typ weiterverarbeitet oder generiert wird. Im Allgemeinen wird dieser generisch durch die Quellcode im Frontend gesetzt.

Es gibt folgende Typen:

#### **default**
Es wird ein neues Default-Item erstellt, also ein neuer Datensatz.
#### **item**
Es wird das derzeit gewählte Item einer View übernommen.
#### **last**
Es wird der letzte Datenbankeintrag vom Backend abgerufen und übernommen.

## **Metabausteine (Funktionsdekoratoren)**
## App
## Metabasis (metabase)
## View (uniform.view)
Die View Funktionen (uniform.view) wird in der Metabasis angewendet.
Der Dekorator ist @uniform.view
### Parameter
<!-- TODO Beispielcode -->
### Ereignisfunktionen
#### **onMounted**
#### **onItemClick**
### Beispiele
#### Dialog (uniform.dialog)
#### Widget (iniform.widget)




activator

Activatoren werden für Aktionen und Dialoge benötigt damit das Backend sie an den  gewünschten positionen oder zu ereignissen darstellen kann und den richtigen Item-Kontext benutzt. 

Activatoren-Hinweise bestehen aus 2 Teilen dem context und dem event Hinweis.

context gibt nur auskunft wie das backend die das item behandelt.

last - das letzte item das der tabelle
default - das standard item aus dem model
item - das zu weiterverarbeitung bereitgestellte item. Zum Beispiel aus einer selection in einer view

z.b last-onload 

```mermaid
graph
A[A Square Rect] -- Link text --> B((Circle))
A --> C(Round Rect)
B --> D{Rhombus}
C --> D