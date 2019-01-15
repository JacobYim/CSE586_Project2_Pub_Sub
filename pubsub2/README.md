# Centralized Publish Subscribe Model Implementation
This is the pub-sub model implementation with Python Classes with Flask and Docker.

## How to Run
To run the application, install docker on your machine.

After Installing Docker and running Docker, type the code belew to build the images file in your Docker.

```shell
docker build -t phase2_junghwanyim_sangwookim .
```

Type the next code to run the container from the image.

```shell
docker run -p 4000:80 phase2_junghwanyim_sangwookim
```

Approach to localhost:4000 with your web browser to access to application container.

To terminate the container, press ctl+'c'.
