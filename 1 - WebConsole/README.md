# WebConsole Demo

First Demo.

With some K5 resources already created & actived:

- KeyPair
- Network
- Router to External network
- Ubuntu image with docker installed

External resources:

- Source code of a web app shared between whole demo steps
- Python script to deploy the Ubuntu image
- Docker image generated from Source Code

Use case:

- With the environment already deployed, create a new VM & select the new Image with docker preinstalled.
- Allocate an external IP to the new VM.
- Access to the VM via SSH.
- Run docker command to deploy a new container with our source code.
- Test the web app.