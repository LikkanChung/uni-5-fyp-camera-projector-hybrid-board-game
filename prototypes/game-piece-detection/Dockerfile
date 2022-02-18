# This container is required as an older version (<4) is needed to run train cascades
FROM python:3.8

RUN apt update && apt install -y \
    wget \
    build-essential \
    cmake

# Install Open CV - this takes a long time
RUN mkdir -p ~/opencv && cd ~/opencv && \
    wget https://github.com/opencv/opencv/archive/refs/tags/3.4.16.zip && \
    unzip 3.4.16.zip && \
    rm 3.4.16.zip && \
    mv opencv-3.4.16 OpenCV && \
    cd OpenCV && \
    mkdir build && \
    cd build && \
    cmake \
    -DWITH_QT=ON \
    -DWITH_OPENGL=ON \
    -DFORCE_VTK=ON \
    -DWITH_TBB=ON \
    -DWITH_GDAL=ON \
    -DWITH_XINE=ON \
    -DBUILD_EXAMPLES=ON .. && \
    make -j4 && \
    make install && \
    ldconfig

RUN mkdir cascade

COPY data data
RUN opencv_traincascade -data cascade -vec data/positive/positive.dat -bg data/negative/negative.txt


