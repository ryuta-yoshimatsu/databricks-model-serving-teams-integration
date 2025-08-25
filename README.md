Please follow these two blog posts:
[Microsoft Teams Meets Databricks Genie API: A Complete Setup Guide](https://medium.com/@ryan-bates/microsoft-teams-meets-databricks-genie-api-a-complete-setup-guide-81f629ace634)

[Microsoft Teams <-> Databricks Genie API - End to End Integration](https://saiponugoti.medium.com/microsoft-teams-databricks-genie-api-end-to-end-integration-2d22b4767e33)

The first post explains how to integrate the Azure Web App and Azure Bot with the Model Serving endpoint (please download the code from this repository). The second post describes how to connect the Azure Bot to Teams. There has been a small update to one of the configurations in the first article (changing from Multi Tenant to Single Tenant), and this requires a few modifications, which I have listed below. The steps that are not listed below should be unchanged.

Part 1: Skip
Part 2: Setting up the Required Resources in Azure
Step 3 — Create a Web App
Adjust Web App Configuration Settings
Navigate to Configuration under Settings

Add the following in Startup Command: python3 -m aiohttp.web -H 0.0.0.0 -P 8000 app:init_func

Step 4 — Create your Azure Bot
Type of App should be Multi Tenant (as of August 1 2025 only multi tenant are supported)

Part 3: Cloning a Repo and Deploying Your App
Use the code (Databricks_Model_Serving_Endpoint_Teams.zip) shared. Edit the config.py file and provide necessary information.

Step 2 — Install necessary dependencies to deploy your app
Skip the first 3 steps - Do NOT create a venv locally before deploying the app as the app will create its own venv when you deploy.
Resume from 4. Install the Azure CLI

7. Deploy your App
Run the command: az webapp up --name <your-app-name> --resource-group <your-resource-group> --plan <your-app-service-plan> --runtime "PYTHON:3.10" --sku B1 —location <your-location>
After the deployment succeeds, go to the Web App’s overview and click on Start.
