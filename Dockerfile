#Use an official Python runtime as a parent image
FROM python:3.12

#Add the NVIDIA key for CUDA 12 repositories
RUN curl "https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.0-1_all.deb" -o cuda.deb && dpkg -i cuda.deb && rm cuda.deb

#Install CUDA 12 runtime and development packages along with libcudnn and libcublas
RUN apt-get update -y && apt-get install -y --no-install-recommends cuda-cudart-12-0 cuda-nvcc-12-0 cuda-nvrtc-12-0 libcudnn8 libcublas-12-0 && rm -rf /var/lib/apt/lists/*

#Install python3, pip, and ffmpeg
RUN apt-get update && apt-get install -y python3 python3-pip libsndfile1 ffmpeg

#Set the working directory in the container
WORKDIR /app

#Copy the requirements file and the script to the container
COPY . /app

#Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt
# Run your Python script when the container launches
CMD ["python3", "./server.py"]

