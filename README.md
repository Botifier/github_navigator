A flask based github navigator that uses parallel requests + in memory caching.

### Setup
To setup the backend you need python and pip and then run the following: 
<br/>
``` pip install -r requirements.txt ```
<br/>

### Running the app

``` python server.py ```
<br/>The app will run on http://localhost:9876/ <br/>


## Running Tests
Server tests: 
<br/>
``` python server_tests.py ```
<br/>
Navigator tests: 
<br/>
``` python navigator_tests.py ```
<br/>

## TODO
* Optimize caching
* Add travis
* Improve template design
* Add uWSGI 

