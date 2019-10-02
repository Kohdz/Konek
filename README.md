# Konek

[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/Naereen/StrapDown.js/blob/master/LICENSE)

Konek is a Flask web application that mimics the core functionalities of Twitter.

## Live

[Konek](http://konekted.herokuapp.com/)

## Docker Installation (Local/Linux Commands)

### Konek supports Python 3

1. Install Docker `sudo apt install docker`

2. Within the Dockerfile, define the following:
    1. `WORKDIR` (Path of Konek Repository)
    1. `SQLALCHEMY_DATABASE_URI`
    2. `RECAPTCHA_PUBLIC_KEY` 
    3. `RECAPTCHA_PRIVATE_KEY`

3. Build the Docker Image `sudo docker build -t <image name> <path of project>`

4. After the Docker Image has been built, run the image. `sudo docker run -d -p 5000:5000 <image name>`

5. To access Konek, navigate to either http://localhost:5000/ or http://127.0.0.1:5000/

## Preview

<img src="https://imgur.com/yWLLNmy.gif" width="600">

<img src="https://imgur.com/ejro447.gif" width="600">

<img src="https://imgur.com/hoxWN13.gif" width="600">

## Future Implementations

Future implementations can be found in TODO.txt