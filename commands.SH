# Build the Docker image
docker build -t knowledge-base-processor .
docker run -it --env-file .env knowledge-base-processor

chmod +x scripts/build_push.sh                
./scripts/build_push.sh