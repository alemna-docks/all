folder=write

echo "BUILDING AND PUSHING IMAGES..."
cd $folder
docker compose up --build
docker push --all-tags alemna/write
