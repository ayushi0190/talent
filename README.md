# Description #

Talentmatcher application rebuild with FastAPI

### How to setup locally? ###

* Change directory  
	``` cd <project_dir> ```

* Install poetry  
  ``` source setup.sh (Linux)```  
    or  
  ``` pip install poetry (windows globally)```  

* Install related python libraries for the project  
  ``` poetry install ```

* Activate environment   
  ``` poetry shell ```

* Activate autohooks   
  ``` poetry run autohooks activate ```

* Alter settings of settings.yaml file
    *  change ENV to DEVELOPMENT or PRODUCTION as per environment

    * Manage all type of setting variables from settings.yaml

* Start application   
  ``` python -m src.routes.main ```

### How to start with Docker? ###

* Build Docker container   
``` docker build -t talentmatcher . ```

* Run Docker container without log   
``` docker run -d -p 9003:9003 talentmatcher ```

* Run Docker container with log   
``` docker run -t -p 9003:9003 talentmatcher ```

* Access point

	http://localhost:9003