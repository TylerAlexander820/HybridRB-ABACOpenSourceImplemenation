# HybridRB-ABACOpenSourceImplemenation
This repository contains the project fiies for an open-source implementation of a IoT Smart Home RBAC/ABAC System using ThingsBoard, Keycloak, and Open Policy Agent.

Implementation conducted by Tyler Alexander

HOW TO USE:

Prerequisites:
Docker Desktop
Python 3.12

Note: You may need to add Mosquitto to your environmental variables
Note: If a name is not specified, please enter any name 

Using terminal on Windows, use command "cd *FOLDER_NAME*" to enter the specified folders. Then, run the command "docker compose up -d" to start the container for the specified program.

On your browser, enter:
localhost:8080 for ThingsBoard
localhost:8081 for Keycloak
localhost:18080 for ThingsBoard Edge

For Keycloak, follow the following guide provided by ThingsBoard to properly set it up: https://thingsboard.io/docs/user-guide/oauth-2-support/.
Please note that for the client name, enter "Thingsboard" or you will need to change the URL for the REST API Call within the Smart Home Rule Chain
