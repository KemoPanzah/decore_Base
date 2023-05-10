# Documentation
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

To prepare your application run ``` python.exe app.py prepare ``` in your project root directory. Use Terminal in vscode or any other IDE.

To run your application run ``` python.exe app.py ``` in your project root directory. Use Terminal in vscode or any other IDE.

to develop your application run ``` python.exe app.py dev ``` in your project root directory. Use Terminal in vscode or any other IDE.

or 

use your debugger with profile ``` Decore app dev ``` in vscode.