# Project Setup Guide

This project consists of a backend built with Flask and a frontend built with Vue.js. The backend uses MongoDB for data storage, which is containerized using Docker. The frontend runs locally using Vue.js.

## Prerequisites

Before you start, make sure you have the following installed:

* **Docker**: For containerizing the backend and MongoDB.
* **Node.js**: For running the frontend locally (with Vue.js).
* **Vue CLI**: For managing the Vue.js frontend.

You can download and install Docker from [here](https://www.docker.com/get-started).

To install Node.js and Vue CLI, follow the instructions:

* Install Node.js from [here](https://nodejs.org/).
* Install Vue CLI globally using the following command:
  
  npm install -g @vue/cli

## Backend Setup (Flask + MongoDB)

The backend is containerized using Docker, along with a MongoDB instance. To run the backend, follow these steps:

### Step 1: Clone the repository

Clone the project repository to your local machine:

```bash
git clone <repository-url>
cd <project-directory>
```

### Step 2: Set up the Docker containers

Make sure Docker is installed and running. Inside the project directory, you'll find a `docker-compose.yml` file that defines the backend and MongoDB services.

Run the following command to start the backend and MongoDB containers:

```bash
docker-compose up --build
```

This will:

* Build the Docker images for the backend (Flask) and MongoDB.
* Start the containers for the Flask app and MongoDB.

Once the containers are up and running, the backend will be accessible at `http://localhost:5001`.

### Step 3: Verify the backend and MongoDB

Check the following logs to make sure everything is running smoothly:

* MongoDB container: `mongodb_container`
* Flask backend container: `flask_app_container`

The backend API should be up and running, and MongoDB will be accessible at port `27017`.

## Frontend Setup (Vue.js)

The frontend is a Vue.js application that communicates with the Flask backend. Follow these steps to run it locally:

### Step 1: Install dependencies

First, navigate to the `client` directory (where the Vue app is located) and install the necessary dependencies:

```bash
cd client
npm install
```

### Step 2: Start the Vue app

To run the Vue.js app locally, use the following command:

```bash
npm run serve
```

By default, the Vue app will be available at `http://localhost:8080`.

### Step 3: Access the application

Once the Vue app is running, you can access it in your browser at `http://localhost:8080`. It should communicate with the Flask backend running on `http://localhost:5001`.

## Environment Variables

The project has a env-example in the root, so you need to rename the file to `.env`

```bash
mv .env-example .env
```
