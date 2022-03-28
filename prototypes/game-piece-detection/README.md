# Prototype: game-piece-detection

This is a prototype / proof of concept project to detect game pieces. 
It also serves the purpose of training the Haar Cascade classifier, should it be used in the main source. 

Dockerfile: This is used to train the classifier. BuildKit is required
```shell
sudo chmod 666 /var/run/docker.sock
DOCKER_BUILDKIT=1 docker build --build-arg COLOR={PIECE_COLOR} --file Dockerfile --output type=local,dest=training/ .
```

# Color Detection Results:

Threshold: Approximately 200/255 still seems to be good as a binary threshold based on the data for training.

Using dominant color in the image seems to not have much impact over average color. 
Best results come from the average color with black pixels omitted after the threshold filter.

(blue, green, red)

| color    | lower           | average         | higher          |
|----------|-----------------|-----------------|-----------------|
| blue     | (148, 105, 81)  | (163, 128, 110) | (179, 151, 139) |
| green    | (132, 128, 103) | (152, 148, 133) | (173, 169, 164) |
| purple   | (132, 119, 115) | (150, 138, 137) | (168, 158, 160) |
| red      | (117, 106, 153) | (143, 128, 170) | (170, 151, 187) |
