decore Base | UI fastly
=======================
Introduction
------------
decore Base ist ein sofort einsatzbereites "Python to Vue.js" Datenanwendungs-Dashboard, das Ihnen hilft, in wenigen einfachen Schritten von der Idee zur Ansicht zu gelangen. Es richtet sich an diejenigen, die sich auf die Ergebnisse ihrer Algorithmen konzentrieren, wissenschaftlich arbeiten oder Lehr- und Lernfunktionen ausführen wollen.

Notes
-----
**decore Base ist derzeit noch in Arbeit, nur lokal einsetzbar, nur für Windows verfügbar und noch nicht produktionsreif**.

Die empfohlene IDE ist Visual Studio Code und alle meine Kommentare und Dokumentationen hier werden sich auch nur auf vscode beziehen.

`Einblicke in den aktuellen Stand des Decore-Projekts <https://github.com/users/KemoPanzah/projects/1/views/1>`_

.. image:: https://ko-fi.com/img/githubbutton_sm.svg
   :target: https://ko-fi.com/P5P2JCC5B
   :alt: Buy me a coffee

Diese Dokumentation wurde mit Deepl vom Deutschen ins Englische übersetzt.

Features and Integrations
-------------------------
- Fertige SPA (Single Page Application) mit Vue.js mittels Quasar Framework (https://github.com/quasarframework/quasar)
- Vordefinierte Webapi für Meta und Aktionen mit Flask (https://github.com/pallets/flask)
- Integriertes ORM für die Datenverwaltung und Datenbankschnittstellen (SQLite) powered by the great Peewee (https://github.com/coleifer/peewee)
- Datenvalidierung mittels Cerberus (https://github.com/pyeve/cerberus)
- Passwortmanagment durch pykeepass (https://github.com/libkeepass/pykeepass)

Bitte unterstützt diese großartigen Projekte!

Contribution
------------
Die größte Hilfe, die ich im Moment bekommen kann, ist, wenn Sie einen Blick auf das Projekt werfen und mir sagen, was Sie davon halten. Ich bin für jede Kritik dankbar.

Mein aktuelles Beispielprojekt ist direkt im Python-Paket enthalten. Um die Beispielanwendung zu installieren, lesen Sie bitte die Dokumentation unter **Beispiel**. Bitte lesen Sie zuerst **Installation**, **Benutzung** und **Vorbereitung**.

Alles, was in der Dokumentation an Funktionen, Fehlern oder Unklarheiten gefunden wird, bitte ich Sie, mir mitzuteilen.

`Bitte benutzen Sie dazu den Problembereich im Repository. <https://github.com/KemoPanzah/decore_Base/issues>`_

Get started
-----------
Um die Anwendungserstellung mit decore Base zu veranschaulichen, erstellen wir nun gemeinsam eine kleine Web-Anwendung.

Die Dekoartoratoren dienen in erster Linie der Erstellung von Meta-Informationen für die spätere Auswertung in der **decore Front** Web-Anwendung und sind nichts vor dem man sich fürchten muss.

*Es ist wirklich simpel, bitte folgt mir!*

Installation
############
Erstellen wir erstmal ein leeres Python-Projekt in Deinem gewünschten Verzeichnis.

Um decore Base zu installieren, führen wir den folgenden Befehl im Projekt-Stammverzeichnis aus. Verwenden wir das Terminal in vscode.

.. code-block:: python
   
   pip install decore-Base

Dies erfordert einen aktiviertes Python-Environment! Um mehr über darüber zu erfahren, besuchen Sie `Python environments in VS Code <https://code.visualstudio.com/docs/python/environments>`_.

Preperation
###########
Erstellen wir nun eine neue Datei mit dem Namen **app.py** in dem Projekt-Stammverzeichnis.

Um decore Base zu verwenden, importieren wir es al aller erstes in das modul **app.py**.

.. code-block:: python
   
   from decore_base import decore

Anschließend erstellen wir mit dem Befehl **prepare** alle benötigten Hilfsdateien im Projektstammverzeichnis.

Um die Anwendung nun tatsächlich vorzubereiten, führen wir nun den Befehl ``python app.py --prepare`` im Terminal aus. Der Pfad muss sich im Projektstammverzeichnis befinden, also da wo die **app.py** liegt.

Usage
#####
Damit der Python-Interpreter die zukünftigen Basisklassen verarbeiten kann, fügen wir noch den folgenden Import hinzu.

.. code-block:: python
   
   from bases import *

Typischerweise enthält ein Python-Hauptmodul eine Abfrage, die überprüft, ob es das Hauptmodul ist, damit wir danach die Funktion ``main`` aufrufen können.

Als nächstes erstellen wir eine Zeile ``if __name__ == '__main__':`` in der Datei **app.py**.

Um eine neue Decore-Anwendungsinstanz zu erstellen, verwenden wir eine ``@decore.app`` dekorierte ``main()`` Funktion in der **app.py** Datei, direkt unter der Zeile: ``if __name__ == '__main__':``.

.. code-block:: python
   
   from decore_base import decore
   from bases import *

   if __name__ == '__main__':
       @decore.app(title='My App')
       def main():
           pass

Model
~~~~~
In einem Model definieren wir die Datenfelder die für, die später zugeodnete, Base benötigt werden. Es dient als Datenbankschnittstelle zu den Datenbanktreibern wie z.B. SQLite, MySQL, PostgreSQL etc.

Wir legen nun die Datei first_model.py im Verzeichnis **models** an und fügen folgenden Code ein:

.. note::
   Um eventuelle zirkuläre Importe zu vermeiden erstellen wir die Modell-Klassen in einem seperaten Verzeichnis **models** in unserem Projektstammverzeichnis. Das Verzeichnis **models** wurde durch den zuvor ausgeführten Befehl ``python app.py --prepare`` mit erstellt.

.. code-block:: python
   
   from decore_base.uniform.conform_model import *

   class First_model(Conform_model):
      firstname = CharField(verbose_name='First Name')
      lastname = CharField(verbose_name='Last Name')


.. note::
   Im hier gezeigten Beispiel importieren wir, aus der **uniform-Bibliothek**, die Conform_model Klasse und erweiteren diese um die Felder firstname und lastname.

   Die Modelle in **decore Base** basieren auf dem großartigen Peewee ORM. Um mehr über Peewee zu erfahren, besuchen Sie `Peewee ORM <http://docs.peewee-orm.com/en/latest/>`_.

.. warning::
   Beim Import bitte beachten, dass wir uns alles (*) aus dem conform_model-Namespace importieren um auch die Feld-Klassen zu erhalten.

Base
~~~~
Diese Basisklassen dienen der decore Applikation als Trägerelement für die View-Komponenten, erhalten das Datenmodell und gelten somit auch als Datenquelle für die Auswertung in der **decore Front** Web-Anwendung.

Nun müssen wir ein neues Python-Modul erstellen, welches eine Basisklasse enthält, zum Beispiel: **first_base.py**, im Verzeichnis **bases** in unserem Projektstammverzeichnis.
Das Verzeichnis **bases** wurde durch den zuvor ausgeführten Befehl ``python app.py --prepare`` mit erstellt.
 
.. code-block:: python

   from decore_base import decore
   from models.first_model import First_model

   @decore.base(title='First Base', icon='mdi-home', model=First_model)
   class First_base:
      pass

.. note::
   Um das zuvor erstellte Model zu verwenden, importieren wir dieses in die Base-Klasse und übergeben es dem Parameter ``model``.

.. warning::
   Damit der Python-Interpreter die Basisklassen auch verarbeiten kann, müssen wir diese in der __init__.py Datei im Verzeichnis **bases** importieren. Die Reihenfolge der einzelnen Importe gibt auch die Reihenfolge in **decore Front** vor.
   
   Wir editiren die Datei **__init__.py** und fügen folgenden Code ein:

   .. code-block:: python

      from .first_base import First_base

View
~~~~
Views dienen der decore Applikation als Präsentation der Datensätze in der **decore Front** Web-Anwendung.

Mit dem View-Dekorator können wir nun eine View-Komponente erzeugen und diese mit der zuvor erstellten Base-Klasse verknüpfen.

Wir editieren nun wieder die Datei **first_base.py** und erweitern den Code wie folgt:

.. code-block:: python
   
   from decore_base import decore
   from models.first_model import First_model

   @decore.base(title='First Base', icon='mdi-home', model=First_model)
   class First_base:
      @decore.view(title='First View', icon='mdi-home', type='table', fields=[First_model.firstname, First_model.lastname])
      def first_view():
         pass

Dialog
~~~~~~
Dialoge sind die Trägerelemente für Widgets in der **decore Front** Web-Anwendung. Sie können nur den Views hinzugefügt werden und steuern die Sichtbarkeit und Darstellungsform der untergeordneten Elemente. Dialoge erhalten auch die Kontrolle über die Submit-Funktionen der Widgets.

In unserem Fall erstellen wir einen Diaolg um eine neue Person mit Vornamen und Nachnamen anzulegen.

Und los gehts ... wieder die Datei **first_base.py** und erweitern den Code wie folgt:

.. code-block:: python
   
   from decore_base import decore
   from models.first_model import First_model

   @decore.base(title='My First Base', icon='mdi-home', model=First_model)
   class First_base:
      @decore.view(title='Person', icon='mdi-account', type='table', fields=[First_model.firstname, First_model.lastname])
      def first_view():
         @decore.dialog(title='Add Person', icon='mdi-plus', type='standard', display='drawer', activator='default-menu')
         def first_dialog():
            pass

Widget
~~~~~~
Widgets sind Komponenten mit denen wir Interaktionen am einzelen Datensatz durchführen können. Sie können nur den Dialogen hinzugefügt werden und sind stapelbar.

Was wir nun brauchen ist noch ein Eingabeformular zu erzeugen, um die Daten für die neue Person einzugeben.

.. code-block:: python
   
   from decore_base import decore
   from models.first_model import First_model

   @decore.base(title='My First Base', icon='mdi-home', model=First_model)
   class First_base:
      @decore.view(title='Person', icon='mdi-account', type='table', fields=[First_model.firstname, First_model.lastname])
      def first_view():
         @decore.dialog(title='Add Person', icon='mdi-plus', type='standard', display='drawer', activator='default-menu')
         def first_dialog():
            @decore.widget(title='Add Person Form', icon='mdi-account', type='form', fields=[First_model.firstname, First_model.lastname])
            def first_widget():
               pass

Action
~~~~~~
Actions sind Methoden mit denen **decore Front** mit **decore Base** kommunizieren kann. Diese können Views und Widgets hinzugefügt werden und sind die einzigen echten Klassen-Methoden im Meta-Bausatz.

Wir benötigen nun eine Action um die Daten der neuen Person zu speichern und erwetern den Code in **first_base.py** wie folgt:

.. code-block:: python
      
      from decore_base import decore
      from models.first_model import First_model
   
      @decore.base(title='My First Base', icon='mdi-home', model=First_model)
      class First_base:
         @decore.view(title='Person', icon='mdi-account', type='table', fields=[First_model.firstname, First_model.lastname])
         def first_view():
            @decore.dialog(title='Add Person', icon='mdi-plus', type='standard', display='drawer', activator='default-menu')
            def first_dialog():
               @decore.widget(title='Add Person Form', icon='mdi-account', type='form', fields=[First_model.firstname, First_model.lastname])
               def first_widget():
                  @decore.action(title='Save Person', icon='mdi-content-save', type='submit')
                  def first_action(self, data):
                     item = First_model(**data['item'])
                     item.title = item.firstname + ' ' + item.lastname
                     if item.save():
                        return True, item.title + ' saved successfully'
                     else:
                        return False, 'Error while saving ' + item.title

.. note::
   Um mit decore Base einen Datensatz zu erzeugen, müssen wir eine Instanz vom Model erzeugen. In unserem Fall **First_model**. Die Instanz wird mit den Daten aus dem Formular befüllt und anschließend gespeichert.

   Die ID in Form einer UUID wird automatisch generiert und muss nicht extra angegeben werden.

.. warning::
   Das Feld **title** wurde aus der Klasse **Deform_model** geerbt und muss bei jeder Datensatzerzeugung belegt werden. Sonst fällt das Item durch die Validierung.

Run, Development and Build
##########################
Um nur Ihre Anwendung zu starten, führen Sie ``python app.py`` in Ihrem Projekt-Stammverzeichnis aus. Verwenden Sie das Terminal in vscode.

Öffnen Sie den Browser und geben Sie ``http://localhost:5555`` ein.

Development
~~~~~~~~~~~
Um Ihre Anwendung zu entwickeln, verwenden Sie Ihren Debugger mit dem Profil ``[dev] decore base development`` in vscode.

Öffnen Sie den Browser und geben Sie ``http://localhost:5555`` ein.

Build
~~~~~
Um Ihre Anwendung zu erstellen, führen Sie ``python app.py --build`` in Ihrem Projekt-Stammverzeichnis aus. Verwenden Sie das Terminal in vscode.

Sample application
------------------
Um besser zu verstehen, wie decore base funktioniert, ist es am besten, sich die Beispielanwendung anzusehen. Die Anwendung repräsentiert meine kontinuierliche Entwicklung von decore base.

https://github.com/KemoPanzah/decore_Sample