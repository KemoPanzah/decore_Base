# Documentation

decore Base is a "Python to Vue.js" open source package that helps you go from idea to view in a few simple steps. It is targeted to those who want to focus on the results of their algorithms, do scientific work, perform promotional teaching or learning functions.

decore is for this moment a work in progress and for windows only. It is not yet ready for production.

The recommended IDE is Visual Studio Code.

## Get started
### Installation
To install Decore base package run:

```
pip install decore_base
````

### Usage
Create a new file named ```app.py``` in your project root directory.


To use Decore base package import it in your project:

```
from decore_base import decore
```

To create a new Decore application instance use a ```decore``` decoratorated function in app.py file after the ```if __name__ == '__main__':``` line.	

```
if __name__ == '__main__':
    @decore.app(p_title='My App')
    def main():
        pass
```

### Preperation
The prepare command will create all needed support files in your app root directory. It will also create a sample base and model to get you started.

To prepare your application run ``` python.exe app.py prepare ``` in your project root directory. Use Terminal in vscode or any other IDE.

### Development
to develop your application use your debugger with profile ``` Decore app dev ``` in 
vscode.

#### Base
The base is the carrier for views. it can be carry views from same base or views from other bases. The base is also linked with one model.  

#### Model
The model is the data carrier for the base. It can be a simple data model or a complex data model. Every model is linked with one base and is based on peewee ORM. to find out more about peewee ORM visit [peewee](http://docs.peewee-orm.com/en/latest/).

### Build
to build your application use your debugger with profile ``` Decore app build ``` in vscode.

### Run

## Api reference

## Model reference
to simplify the work with the model the following methods where monkey patched to the origin peewee model class.

## Examples
Um die Funktionsweise von Decore base zu verstehen, ist es am besten, sich ein Beispiel anzusehen. Das folgende Beispiel zeigt, wie Sie eine einfache Anwendung erstellen, die eine Liste von Personen anzeigt. Die Anwendung besteht aus einer Ansicht, die eine Liste von Personen anzeigt, und einer Ansicht, die die Details einer Person anzeigt.

## Component slots

```mermaid 
graph
A[Base]  --> B((Circle))
A --> C(Round Rect)
B --> D{Rhombus}
C --> D

