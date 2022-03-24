# This container is required as an older version (<4) is needed to run train cascades
FROM python:3.8 AS train

RUN apt update && apt install -y \
    wget \
    build-essential \
    cmake

# Install Open CV - this takes a long time, approx 1100s (19m)
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

ARG COLOR

RUN mkdir -p vec vec/$COLOR && \
    mkdir -p cascade/$COLOR

COPY data data
#RUN opencv_createsamples -info data/positive_$COLOR/positive_$COLOR.dat -w 20 -h 20 -num 200 -bgColor 255 -vec vec/$COLOR/positive_$COLOR.vec > vec/$COLOR/create_samples_$COLOR.log
RUN opencv_createsamples -info data/positive_$COLOR.dat -w 20 -h 20 -num 600 -bgColor 255 -vec vec/$COLOR/positive_$COLOR.vec > vec/$COLOR/create_samples_$COLOR.log

RUN opencv_traincascade \
    -data cascade/$COLOR/ \
    -vec vec/$COLOR/positive_$COLOR.vec \
    -bg data/negative/negative.txt \
    -numPos 100 \
    -numNeg 100 \
    -numStages 10 \
    -w 20 -h 20 \
    -maxFalseAlarmRate 0.3 \
    -minHitRate 0.999 \
    > cascade/$COLOR/train_cascade.log

FROM scratch as artifacts
COPY --from=train vec .
COPY --from=train cascade .


