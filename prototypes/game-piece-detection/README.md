# Prototype: game-piece-detection

This is a prototype / proof of concept project to detect game pieces. 
It also serves the purpose of training the Haar Cascade classifier, should it be used in the main source. 

Dockerfile: This is used to train the classifier. BuildKit is required
```shell
sudo chmod 666 /var/run/docker.sock
DOCKER_BUILDKIT=1 docker build --build-arg COLOR={PIECE_COLOR} --file Dockerfile --output type=local,dest=training/ .
```