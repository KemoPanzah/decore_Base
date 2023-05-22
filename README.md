# Documentation
decore Base is a "Python to Vue.js" open source package that helps you go from idea to view in a few simple steps. It is aimed at those who want to focus on the results of their algorithms , do scientific work, or perform teaching or learning functions.

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/P5P2JCC5B)

decore is currently a work in progress, available only for Windows and not yet ready for production.

The recommended IDE is Visual Studio Code and all my comments and documentation here will also refer to vscode only.

## Get started
### Installation
Create an empty Python project in your desired directory. I will refer to this directory as the project root directory throughout this documentation.

To install decore base run the following command in your project root directory. Use the terminal in vscode.

```
pip install decore-base
```

This requires an activated Python interpreter! To learn more about Python Interpreter, visit [Python Interpreter](https://code.visualstudio.com/docs/python/environments).

### Usage
Create a new file named ``app.py`` in your project root directory.

To use decore Base, import it into your project:

```
from decore_base import decore
```

Typically, a Python main module contains a query that checks if it is the main module, and then calls the ``main()``` function.

We next create a line ``if __name__ == '__main__':``` in the app.py file.

To create a new Decore application instance, use a ``@decore.app`` decorated function in the app.py file after the line ``if __name__ == '__main__':```.

```
if __name__ == '__main__':
    @decore.app(p_title='My App')
    def main():
        pass
```

An example of this can be found here:

https://github.com/KemoPanzah/decore_Base/blob/master/decore_base/sample/app.py

### Preperation
The preparation command creates all the needed auxiliary files in your app root directory.

To prepare your app, run `` python app.py prepare ``` in your project root directory. Use the terminal in vscode.

### Development
To develop your application, use your debugger with the ``` [dev] decore base development ``` profile in vscode.

### Build
To build your application, use your debugger with the ``` [bld] decore Base build ``` profile in vscode.

### Run
To run your application, run ``` python app.py ``` in your project root directory. Use the terminal in vscode.

## Sample
To understand how Decore base works, it is best to look at the Sample application. The application represents my ongoing development of decore base.

To synchronize the sample application to its root directory run ``python app.py sample`` in your project root directory. Use the terminal in vscode or another IDE.

To run the sample application after synchronization, use your debugger with the profile ``[smp] decore base sample ``` in vscode.

## Explanations

#### Base
The base is basically the carrier element for views. It can get views from the same base or views from other bases. The Base is always linked to a Model.

#### Model
The model defines the data to work with. It can be a simple data model or a complex data model. Each model is linked to a Base and is based on peewee ORM. To learn more about peewee ORM, visit [peewee](http://docs.peewee-orm.com/en/latest/).

## Api reference
To create a GUI with decore Base, one decorates functions in the source code according to the default of the processing process. which must be imported beforehand with ``from decore_base import decore``.

The decore module contains those functions that are needed when creating the metadata for the decore front application.

To understand the general approach, synchronize the sample application with the command ``python app.py sample`` in your project root directory.

### @decor.app()
### @decor.base()
### @decor.view()
### @decor.dialog()
### @decor.widget()
### @decor.action()

## Model reference
To make working with the original Peewee model even easier, some functions have been added to the model.

!DESCRIPTION FOLLOWS!

## Component processing
```mermaid
graph
A[Base] --> B[View]
B --> Z[Action]
B --> C[Dialog]
C --> D[Widget]
D --> F[Sub Dialog]
D --> G[Sub Widget]
F --> G[Sub Widget]
G --> Z[Action]
D --> Z[Action]
```

# Notes
This documentation was translated from German into English using Deepl.
