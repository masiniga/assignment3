

## Running my Code: Docker Commands 
In order to run my code, you need docker. 
On my computer, in the code subdirectory,
I ran the following command to run all 3 elements.

```bash
$ docker-compose up -d
```
After running this, the same links and commands from assignment 1 should work.

In order to remove the containers, you can run the following.

```bash
$ docker-compose down
```

## Accessing the different elements
Once the containers are running, the elements can be accessed using the following.

### 1. FastAPI

There are three URLs. 
The first displays a short description, 
the second displays the named entities,
and the third displays the dependencies.
(They only take a filetype of .json, and you must
be in a directory that contains such a file.) 
These are given below. 

```bash
$ curl http://127.0.0.1:8000
$ curl http://127.0.0.1:8000/ner -H "Content-Type: application/json" -d@input.json
$ curl http://127.0.0.1:8000/dep -H "Content-Type: application/json" -d@input.json
```

The URLs below do the same thing but take a
pretty parameter, and display the information
in a nicer format. 

```bash
$ curl http://127.0.0.1:8000?pretty=true
$ curl http://127.0.0.1:8000/ner?pretty=true -H "Content-Type: application/json" -d@input.json
$ curl http://127.0.0.1:8000/dep?pretty=true -H "Content-Type: application/json" -d@input.json
```


### 2. Flask
 

The Flask site can be accessed at http://127.0.0.1:5000.


### 3. Streamlit

The Streamlit site can be accessed at  http://localhost:8501/.
