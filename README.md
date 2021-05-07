# Jokbot

Este bot publica imagenes de la página Cyanide and Happiness, las 
imagenes son generadas aleatoriamente.


## Table of Content

* [Development Environment Configuration](#development-environment-configuration)
* [Test the Application](#test-the-application)


## Development Environment Configuration
- Download the files from this repository.

  ```bash
  git clone 
  ```

- Create a virtual environment with Anaconda

  ```bash
  conda create -n jokbot python=3.8 -y
  ```

- Now, let's activate the created virtual environment

  ```bash
  conda activate jokbot
  ```

- With the virtual environment activated we are going to install 
  the requirements used in the project

  ```bash
  pip3 install -r requirements.txt
  ```

- We must export the following environment variable

  ```bash
  export $(cat .env | grep -v ^# | xargs)
  ```

- Finally, run the application server

  ```bash
  python -m flask run
  ```


## Test the Application

### Develop

You can test the endpoint locally with the following curl:

```bash
    curl --location --request GET 'http://127.0.0.1:5000/'
  ```
