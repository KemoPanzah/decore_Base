Overview
--------
decore Base is an out-of-the-box "Python to Vue.js" data application dashboard that helps you go from idea to view in a few simple steps. It is aimed at those who want to focus on the results of their algorithms , do scientific work, or perform teaching or learning functions.

**decore Base is currently a work in progress, only locally deployable, only available for Windows and not yet ready for production.**

The recommended IDE is Visual Studio Code and all my comments and documentation here will also refer to vscode only.

`Insight into the current progress of the decore project <https://github.com/users/KemoPanzah/projects/1/views/1>`_

.. image:: https://ko-fi.com/img/githubbutton_sm.svg
   :target: https://ko-fi.com/P5P2JCC5B
   :alt: Buy me a coffee
   
Contribution
------------
The biggest help I can get right now is if you take a look at the project and tell me what you think. I am grateful for any criticism.

My current sample project is included directly in the Python package. To install the sample application, please see the documentation under **Sample**. Please read **Installation**, **Usage** and **Preperation** first.

Everything that is found in features, bugs or unclear in the documentation, I ask you to let me know.

`Please use the Issues area in the repository for this. <https://github.com/KemoPanzah/decore_Base/issues>`_

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

Usage and Run 
#############
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

Im hier gezeigten Beispiel importieren wir, aus der **uniform-Bibliothek**, die Conform_model Klasse und erweiteren diese um die Felder firstname und lastname.

.. note::
   Beim Import bitte beachten, dass wir uns alles (*) aus dem conform_model-Namespace importieren um auch die Feld-Klassen zu erhalten.

Base
~~~~
Diese Basisklassen dienen in der decore-Applikation als Trägerelement für die View-Komponente, erhalten das Datenmodell und gelten somit auch als Datenquelle für die Auswertung in der **decore Front** Web-Anwendung.

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

View
~~~~
Views dienen in der decore-Applikation als Präsentation der Datensätze in der **decore Front** Web-Anwendung.

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

Run, Development and Build
##########################
To only start your application, run ``python app.py`` in your project root directory. Use the terminal in vscode.

Open the browser and type ``http://localhost:5555``.

Development
~~~~~~~~~~~
To develop your application, use your debugger with the ``[dev] decore base development`` profile in vscode.

Open the browser and type ``http://localhost:5555``.

Build
~~~~~
To build your application, run ``python app.py --build`` in your project root directory. Use the terminal in vscode.


Sample application
------------------

To better understand how decore base works, it is best to look at the sample application. The application represents my continuous development of decore base.

https://github.com/KemoPanzah/decore_Base/tree/master/decore_base/sample

To sync the sample application to a subfolder of the project root directory, run ``python app.py --sample`` in your project root directory. Use the terminal in vscode.

To run the sample application after synchronization, use your debugger with the profile ``[smp] decore base sample`` in vscode.

Notes
-----

This documentation was translated from German to English with Deepl.

