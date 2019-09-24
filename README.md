## Python 3.x Reverse shell Implementation
Python 3.x based **py_prompt>>** multi-client and multi-threaded functionalitiy included reverse shell. I have planned to add some features into it by enabling persistence in the
clientside side script so, whenever the client turn on and off the system. It doesn't really matter when he back to online our command & control will get the reverse connection
like the meterpreter shell. I'm currently working on that. This is my first python project.
I just implemented this project to understand how the things really work.<br />

**Outline** <br />
There must be two scripts running 
1. ```server.py``` for accepting the incoming connections from several clients and also to select a specific client and execute the commands
2. ```client.py``` will be considered as our payload. It must be dropped on our target system by performing some social engineering take a look at the essentials below.

**Usecase** <br />
* In the real world you need static ip to run the ```server.py``` for establishing the connection from multiple remote clients
* Run ```server.py``` in cloud platform like Digitalocean or AWS etc...
* When you are running the ```server.py``` script type __help__ to view the menu

**Essentials** <br />
* Pyinstaller will makes the life easier to pack and run the ```client.py```scripts on the target systems without even the python interpreter installed on it.
* Use Pyinstaller to pack the ```client.py``` script with python applications and also to convert in executable
* Create the favicon by using Pyinstaller to make the script looks like legitimate one.


**disclaimer**<br />
Use it for the testing purposes only. If you are using this program without the consent of appropriate user that you are interacting with means
that's illegal. 

