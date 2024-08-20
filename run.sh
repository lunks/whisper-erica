docker build -t whisper-erica:latest .
docker run --rm -p 5000:5000 --gpus all -v ./cache:/root/.cache whisper-erica:latest
