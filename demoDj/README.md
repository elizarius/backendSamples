# Django demo example

## Overview

This project demonstrates Django REST Framework setup with Docker, Python, PostgreSQL. It explores
using VSCode AI agents for development and refactoring.

## How to run
- See django-docker-guide.md 

## Project Status

### Completed
- Setup keycloak in docker
- Create first users / clients with Admin CLI REST API
- Write Django REST sceleton, using REST API, as container
- Setup PostgreSQL as separate container
- Create DB user for web-1 demo


### In Progress
- Write Python library to use  keycloak ADMIN API
- Add postgres custom setup, f.i own postgres.conf 
- Integrate  Django REST container to use with Keycloak
- Add robot tests to demonstrate functionality
- Add pytests to demonstrate functionality


### Planned
- Focus on VSCode AI agents usage and refactoring
- k3s: setup in aelz environment
- k3s: deployment, service configuration
- Add auth policy .f.i RBAC, see Ch 1  of "authorization services"
- Logging manipulation , seems in standalone.xml set extra logger
