decore Base | UI fastly
=======================
Introduction
------------
decore Base is an out-of-the-box "Python to Vue.js" data application dashboard that helps you go from idea to view in a few simple steps. It is aimed at those who want to focus on the results of their algorithms, do scientific work or perform teaching and learning functions.

Notes
-----
**decore Base is currently a work in progress, only locally deployable, only available for Windows and not yet production ready**.

The recommended IDE is Visual Studio Code and all my comments and documentation here will also refer to vscode only.

`Insights into the current status of the Decore project. <https://github.com/users/KemoPanzah/projects/1/views/1>`_

.. image:: https://ko-fi.com/img/githubbutton_sm.svg
   :target: https://ko-fi.com/P5P2JCC5B
   :alt: Buy me a coffee

This documentation was translated from German into English with Deepl.

Features and Integrations
-------------------------
- Ready-made SPA (Single Page Application) with Vue.js using Quasar Framework (https://github.com/quasarframework/quasar)
- Predefined Webapi for meta and actions with Flask (https://github.com/pallets/flask)
- Integrated ORM for data management and database interfaces (SQLite) powered by the great Peewee (https://github.com/coleifer/peewee)
- Data validation using Cerberus (https://github.com/pyeve/cerberus)
- Password management using pykeepass (https://github.com/libkeepass/pykeepass)

Please support these great projects!

Contribution
------------
The biggest help I can get right now is if you take a look at the project and tell me what you think. I am grateful for any criticism.

My current sample project is included directly in the Python package. To install the example application, please read the documentation in **Example**. Please read **Installation**, **Use** and **Preparation** first.

Anything found in the documentation in terms of features, bugs or ambiguities, please let me know.

`Please use the problem area in the repository for this purpose. <https://github.com/KemoPanzah/decore_Base/issues>`_

Get started
-----------
To illustrate application creation with decore Base, we will now create a small web application together.

The decoartorators are primarily used to create meta-information for later evaluation in the **decore Front** web application and are nothing to be afraid of.

*It's really simple, please follow me!*

Installation
############
Let's first create an empty Python project in your desired directory.

To install decore Base, we run the following command in the project root directory. Let's use the terminal in vscode.

.. code-block:: python
   
   pip install decore-Base

This requires an enabled Python environment! To learn more about this, visit `Python environments in VS Code <https://code.visualstudio.com/docs/python/environments>`_.

Preperation
###########
Now let's create a new file named **app.py** in the project root directory.

To use decore Base, we first import it into the module **app.py**.

.. code-block:: python
   
   from decore_base import decore

Then we use the **prepare** command to create all the necessary auxiliary files in the project root directory.

Now, to actually prepare the application, we run the command ``python app.py --prepare`` in the terminal. The path must be in the project root directory, i.e. where the **app.py** is located.

Usage
#####
To allow the Python interpreter to process the future base classes, we add the following import.

.. code-block:: python
   
   from bases import *

Typically, a Python main module contains a query that checks if it is the main module so that we can call the ``main`` function afterwards.

Next, we create a line ``if __name__ == '__main__':`` in the **app.py** file.

To create a new Decore application instance, we use a ``@decore.app`` decorated ``main()`` function in the **app.py** file, just below the line: ``if __name__ == '__main__':``.

.. code-block:: python
   
   from decore_base import decore
   from bases import *

   if __name__ == '__main__':
       @decore.app(title='My App')
       def main():
           pass

Model
~~~~~
In a model we define the data fields that are needed for the later assigned base. It serves as a database interface to the database drivers such as SQLite, MySQL, PostgreSQL, etc.

We now create the file first_model.py in the directory **models** and insert the following code:

.. note::
   To avoid possible circular imports we create the model classes in a separate directory **models** in our project root directory. The directory **models** was created by the previously executed command ``python app.py --prepare``.

.. code-block:: python
   
   from decore_base.uniform.conform_model import *

   class First_model(Conform_model):
      firstname = CharField(verbose_name='First Name')
      lastname = CharField(verbose_name='Last Name')


.. note::
   In the example shown here, we import, from the **uniform library**, the Conform_model class and extend it with the firstname and lastname fields.

   The models in **decore Base** are based on the great Peewee ORM. To learn more about Peewee, visit `Peewee ORM <http://docs.peewee-orm.com/en/latest/>`_.

.. warning::
   When importing please note that we import everything (*) from the conform_model namespace to get the field classes as well.

Base
~~~~
These base classes serve the decore application as a carrier element for the view components, maintain the data model and are thus also considered the data source for evaluation in the **decore Front** web application.

Now we need to create a new Python module containing a base class, for example: **first_base.py**, in the **bases** directory in our project root directory.
The **bases** directory was co-created by the ``python app.py --prepare`` command executed earlier.
 
.. code-block:: python

   from decore_base import decore
   from models.first_model import First_model

   @decore.base(title='First Base', icon='mdi-home', model=First_model)
   class First_base:
      pass

.. note::
   To use the previously created model, we import it into the Base class and pass it to the ``model`` parameter.

.. warning::
   In order for the Python interpreter to be able to process the base classes, we have to import them into the __init__.py file in the **bases** directory. The order of the individual imports also determines the order in **decore Front**.
   
   We edit the **__init__.py** file and insert the following code:

   .. code-block:: python

      from .first_base import First_base

View
~~~~
Views are used by the decore application to present the data sets in the **decore Front** web application.

With the view decorator we can now create a view component and link it to the previously created base class.

We now edit the **first_base.py** file again and extend the code as follows:

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
Dialogs are the supporting elements for widgets in the **decore Front** web application. They can only be added to views and control the visibility and display style of child elements. Dialogs also get control over the submit functions of the widgets.

In our case, we create a diaolg to create a new person with first name and last name.

Here we go ... again the file **first_base.py** and extend the code as follows:

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
Widgets are components with which we can perform interactions on the single record. They can only be added to dialogs and are stackable.

What we need now is to create an input form to enter the data for the new person.

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
Actions are methods with which **decore Front** can communicate with **decore Base**. They can be added to views and widgets and are the only real class methods in the meta kit.

We now need an action to store the data of the new person and extend the code in **first_base.py** as follows:

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
   To create a record with decore Base, we need to create an instance of the model. In our case **First_model**. The instance is filled with the data from the form and then saved.

   The ID in the form of a UUID is generated automatically and does not have to be specified separately.

.. warning::
   The field **title** was inherited from the class **Deform_model** and must be used for each record creation. Otherwise the item will fail the validation.

Run, Development and Build
##########################
To start only your application, run ``python app.py`` in your project root directory. Use the terminal in vscode.

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