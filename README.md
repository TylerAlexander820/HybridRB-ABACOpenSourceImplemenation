# HybridRB-ABACOpenSourceImplemenation
This repository contains the project fiies for an open-source implementation of a IoT Smart Home RBAC/ABAC System using ThingsBoard, Keycloak, and Open Policy Agent.

Performed Using:

Docker Desktop (version 4.52.0) 

ThingsBoard Community Edition (version 4.2.1) 

ThingsBoard Edge (version 4.2) 

Keycloak (version 26.4.5)

Open Policy Agent (OPA) (version 1.10.1)

Python 3.12

PyCharm IDE (version 2025.2.4)

Implementation conducted by Tyler Alexander

HOW TO USE:

Prerequisites:

Docker Desktop

Python 3.12

Note: You may need to add Mosquitto to your environmental variables

Using terminal on Windows, use command "cd *FOLDER_NAME*" to enter the specified folders. Then, run the command "docker compose up -d" to start the container for the specified program.

On your browser, enter:

localhost:8080 for ThingsBoard

localhost:8081 for Keycloak

localhost:18080 for ThingsBoard Edge

For Keycloak, follow the following guide provided by ThingsBoard to properly set it up: https://thingsboard.io/docs/user-guide/oauth-2-support/.

Please note that for the client name, enter "Thingsboard" or you will need to change the URL for the REST API Call within the Smart Home Rule Chain

Create any number of users you would like, set up their email and passwords and create/add in their realm roles.

For ThingsBoard (Cloud/Edge), import the dashboard, rule chains, and widgets using the default "tenant" account. Ensure that the widget logic in the dashboard matches the imported widgets, or you will not be able to get the user's email for authentication.

You can edit the RB/ABAC logic with the OPA/Policies/SmartHomeAuthorization.rego file using Notepad or Notepad++. 
