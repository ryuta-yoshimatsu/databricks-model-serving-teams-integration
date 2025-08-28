Please follow these two blog posts:<br>
[Microsoft Teams Meets Databricks Genie API: A Complete Setup Guide](https://medium.com/@ryan-bates/microsoft-teams-meets-databricks-genie-api-a-complete-setup-guide-81f629ace634)<br>
[Microsoft Teams <-> Databricks Genie API - End to End Integration](https://saiponugoti.medium.com/microsoft-teams-databricks-genie-api-end-to-end-integration-2d22b4767e33)<br>

The first post explains how to integrate the Azure Web App and Azure Bot with the Model Serving endpoint (please download the code from this repository). The second post describes how to connect the Azure Bot to Teams. There has been a small update to one of the configurations in the first article (changing from Multi Tenant to Single Tenant), and this requires a few modifications, which I have listed below. The steps that are not listed below should be unchanged.

# Deployment Guide

## Part 1: Skip

---

## Part 2: Setting up the Required Resources in Azure

### Step 3 — Create a Web App
1. Adjust Web App Configuration Settings  
   - Navigate to **Configuration** under **Settings**.  
   - Add the following in **Startup Command**:  
     ```bash
     python3 -m aiohttp.web -H 0.0.0.0 -P 8000 app:init_func
     ```

### Step 4 — Create your Azure Bot
- **Type of App** should be **Single Tenant**  
  *(as of August 1, 2025 only single tenant apps are supported).*

---

## Part 3: Cloning a Repo and Deploying Your App

1. Use the code in this repository.  
   - Edit the `config.py` file and provide the required information.  

### Step 2 — Install necessary dependencies
- **Skip the first 3 steps**  
- **Do NOT** create a local venv before deploying the app (the app will create its own venv during deployment).  
- Resume from **Step 4: Install the Azure CLI**.  

---

### Step 7 — Deploy your App
Run the following command:

```bash
az webapp up \
  --name <your-app-name> \
  --resource-group <your-resource-group> \
  --plan <your-app-service-plan> \
  --runtime "PYTHON:3.10" \
  --sku B1 \
  --location <your-location>

