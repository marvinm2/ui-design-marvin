# ui-design

Repository to develop the main HTML-based website as central access point. 

## Requirements 

The user needs to install the from `flask`, `requests`, and `wikidataintegrator` Python modules. You can do so by running

```
pip install -r requirements.txt
```

## Deployment

Deployment can be made in two ways: i) on the local machine with Python; ii) on a container on the local machine with Docker

### Deployment with Python

Run the following command in Bash: 

```
python app.py
```

The page should be available at `http://localhost:5000/`. 


### Deployment with Docker

Run the following codes for building the image and running the container

```
docker build -t cap_demo .
docker run -d -p 5001:5000 cap_demo
``` 

The page should be available at `http://localhost:5001/`. 
