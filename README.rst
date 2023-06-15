decore Base is an out-of-the-box "Python to Vue.js" data application dashboard that helps you go from idea to view in a few simple steps. It is aimed at those who want to focus on the results of their algorithms , do scientific work, or perform teaching or learning functions.

.. image:: https://ko-fi.com/img/githubbutton_sm.svg
   :target: https://ko-fi.com/P5P2JCC5B
   :alt: Buy me a coffee

**decore Base is currently a work in progress, only locally deployable, only available for Windows and not yet ready for production.**

The recommended IDE is Visual Studio Code and all my comments and documentation here will also refer to vscode only.

`Insight into the current progress of the decore project <https://github.com/users/KemoPanzah/projects/1/views/1>`_

Contribution
------------

The biggest help I can get right now is if you take a look at the project and tell me what you think. I am grateful for any criticism.

My current sample project is included directly in the Python package. To install the sample application, please see the documentation under **Sample**. Please read **Installation**, **Usage** and **Preperation** first.

Everything that is found in features, bugs or unclear in the documentation, I ask you to let me know.

`Please use the Issues area in the repository for this. <https://github.com/KemoPanzah/decore_Base/issues>`_

Get started
-----------
Installation
############

Create an empty Python project in your desired directory. I will refer to this directory as **project root directory** in the following course of this documentation.

To install decore Base, run the following command in your project root directory. Use the terminal in vscode.

.. code-block:: python
   pip install decore-Base

This requires an activated Python Interpreter! To learn more about Python Interpreters, visit `Python Interpreter <https://code.visualstudio.com/docs/python/environments>`_.

Preperation
###########
Create a new file named ``app.py`` in your project root directory.

To use decore Base, import it into your project. 

.. code-block:: python
   from decore_base import decore

You then use the prepare command to create all the auxiliary files you need in your project root directory.

To prepare your application, run ``python app.py --prepare`` in your project root directory. Use the terminal in vscode.

Usage
#####
To allow the Python interpreter to process the future base classes, add the following import.

.. code-block:: python
   from bases import *

Typically, a Python main module contains a query that checks whether it is the main module, and then calls the ``main`` function.

We next create a line ``if __name__ == '__main__':`` in the app.py file.

To create a new Decore application instance, use a ``@decore.app`` decorated ``main`` function in the app.py file after the line ``if __name__ == '__main__':``.

.. code-block:: python
   from decore_base import decore
   from bases import *

   if __name__ == '__main__':
       @decore.app(p_title='My App')
       def main():
           pass

You can find an example here:

https://github.com/KemoPanzah/decore_Base/blob/master/decore_base/sample/app.py

Debug and Run
#############

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

To understand how decore base works, it is best to look at the sample application. The application represents my continuous development of decore base.

https://github.com/KemoPanzah/decore_Base/tree/master/decore_base/sample

To sync the sample application to a subfolder of the project root directory, run ``python app.py --sample`` in your project root directory. Use the terminal in vscode.

To run the sample application after synchronization, use your debugger with the profile ``[smp] decore base sample`` in vscode.

Notes
-----

This documentation was translated from German to English by GitHub Copilot.
