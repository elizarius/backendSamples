# Django demo example

## Overview

This project demonstrates Django REST Framework setup with Docker, Python, PostgreSQL. It explores using VSCode AI agents for development and refactoring.

## How to run
- See django-docker-guide.md 

## Project Status

### Completed
- Setup keycloak in docker
- Create first users / clients with Admin CLI REST API
- Write Django REST sceleton, using REST API, as container
- Setup PostgreSQL as separate container
- Create DB user for web-1


### In Progress
- Copilot AI cli try to use IP
- VSCode Copilot AI try

- Add postgres custom setup, f.i own postgres.conf
- Script to run start up web app (in claude thread is example)
- Investigate own Django user management and policies, how they
  can be mapped to request 
- Write Python library to use keycloak ADMIN API
- Integrate Django REST container to use with Keycloak
- Add robot tests to demonstrate functionality
- Add pytests to demonstrate functionality


### Planned
- k3s: setup in aelz environment
- k3s: deployment, service configuration
- Logging manipulation , seems in standalone.xml set extra logger
