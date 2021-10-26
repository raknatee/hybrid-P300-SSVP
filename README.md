# GPU with Docker

## Windows

1. install Docker Desktop with WSL2 based engine
2. follow -> https://docs.docker.com/desktop/windows/wsl/#gpu-support
3. build and run container
```bash
docker-compose up --build -d
```


## Ubuntu

- I havent tried yet.
- But Ubuntu with Docker and GPU are quite very easy (than Windows Version).

## Adding more Dependencies
- go and check Dockerfile.py39

# Project Structure

- root of project is in ./src, for inside of container is in /home/src 
- To make it work perfectly with Python Language Server. The main file is main.py
- Okay, You might see I have a lot of series. Each SERIES is a group of my code which was working on some model maybe? I decided to don't remove any code (to see what I was doing wrong). However, you might see the final version in another branch too because I would integrate it on Programs branch with ML-server.
- It means this branch for my experimentssss.

## You want to run some scripts. How should YOU do?

- exec to my container
  
```bash
docker-compose exec app bash
```

- do something like this. This is an example.

```bash
pipenv run python main.py <python_module> <function> [...args] 
```

- Let say you want to run "./series002/ssvp_chaky/main" file on "main" function.

```bash
pipenv run python main.py series002.ssvp_chaky.main main  
```