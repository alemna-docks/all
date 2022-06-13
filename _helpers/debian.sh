folder=debian

echo "BUILDING AND PUSHING IMAGES..."
cd $folder
docker compose up --build
docker tag alemna/debian:11 alemna/debian:bullseye
docker tag alemna/debian:stable alemna/debian:bullseye 
docker tag alemna/debian:latest alemna/debian:bullseye 
docker tag alemna/debian:11-slim alemna/debian:bullseye-slim
docker tag alemna/debian:stable-slim alemna/debian:bullseye-slim
docker push --all-tags alemna/debian
