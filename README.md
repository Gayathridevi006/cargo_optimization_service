# cargo_optimization_service
## used storage.py for in memory storage

## for more detailing added models separately in models.py , use can also directly add in main.py

pip install -r requirements.txt 
or pip3 install -r requirements.txt

# run the fastapi using uvicorn
uvicorn main:app --reload or python -m uvicorn main:app --reload
#or with port 
uvicorn main:app --reload --port 8000  


# for apis
use http://127.0.0.1:8000/docs


use sample input json in apis as steps below 
1. /input
2. /optimise
3. /results get


--- deployment in aws ec2 by docker
docker build -t cargo-app .
docker run -d -p 8000:8000 --name cargo-app-container cargo-app
docker ps