Python networking library perfect for use with pygame!

on server-side you must create a server using the `Server` class
<br>
<br>
follow the example below!
<br>
be sure to replace `192.168.1.52` with a string containing the server IP
and replace `8080` with an integer containing the server port

```
from pygame_networking import Server
server = Server()
server.serve(("192.168.1.52", 8080))

```

To create data that is synced across all clients, You can use the `sync` method


```
from pygame_networking import Server
server = Server()

server.sync("my_variable", "my_data")

server.serve(("192.168.1.52", 8080))

```

replace "my_variable" with a string containing the name you want
<br>
replace "my_data" with a string containing the data the variable is initialized with

NOTE: variable data must always be string, this module does not support any other types

<br>

On client-side you must use the `connect` method to establish a connection with the server

```
from pygame_networking import Server
server = Server()

server.connect(("192.168.1.52", 8080))

```
<br>

You can also use `sync` from client-side to declare new variables

```
from pygame_networking import Server
server = Server()

server.connect(("192.168.1.52", 8080))

server.sync("my_variable", "my_data")

```

<br>

use `get` and `set` to retrieve and modify variables

```
from pygame_networking import Server
server = Server()

server.connect(("192.168.1.52", 8080))

server.set("count", "1")

print(server.get("count"))

```

