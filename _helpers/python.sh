folder=python/3.10

echo "BUILDING AND PUSHING IMAGES..."
cd $folder
docker compose up --build
docker tag alemna/python:latest alemna/python:3.10.4 
docker push --all-tags alemna/python
