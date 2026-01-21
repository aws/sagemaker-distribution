## Welcome

SageMaker Unified Studio is an integrated development environment that brings together familiar tools from AWS analytics and AI/ML services for data processing, SQL analytics, ML model development, and generative AI application development to help teams collaborate and bring data products to market faster.

A project in SageMaker Unified Studio acts as a logical boundary for all the data, tools, and compute needed for a particular business problem. You can import data from your business data catalog, Amazon Redshift, or other connectors such as Google BigQuery and Snowflake. Tooling includes components such as notebooks, queries, visual ETL, and generative AI playgrounds. With execution abstracted through managed connections that are either serverless or pre-configured by your administrator, you can concentrate on your code and data.

## Discover, Build and Manage

There are three menu options: **Discover**, **Build**, and **Manage**.

### Discover

On the **Discover** menu, you have access to the business data catalog (powered by SageMaker Catalog) and its related resources, as well as generative AI playgrounds, model catalogs, and shared assets.

### Build

The **Build** menu provides tools for data analysis and tools for data analysis and engineering, including our poly-compute JupyterLab Notebooks, a multi-engine SQL editor, AI-powered Visual ETL, and Airflow-based workflow tools. With the Machine Learning secondary menu, you can take your data and apply it to classical machine learning from experimentation to hosting inference endpoints. With the generative AI features, you can customize and build apps with Amazon Bedrock's Generative AI tooling suite. All of our tools are enhanced by Amazon Q for improving productivity and empowering users to focus on their goals.

### Manage

On the **Manage** menu, administrators can manage the SageMaker Unified Studio domains, account associations, and end-user permissions.

## Q assistant

Use Amazon Q, at any time from the top right of SageMaker Unified Studio toolbar, to generate code, tests, and debugs, and implement generated code with multi-step planning and reasoning capabilities.

## Projects

### Project Overview

The **Project Overview** gives you one central place to manage everything in your project. You can see and work with all your project resources - including code, data, and compute - in a single view. Your team can access notebooks, run queries, and manage workflows all in the same place. This unified environment lets you focus on using the tools you need, without worrying about the underlying AWS infrastructure that powers them.

### Members

The **Members** tab provides a view of the users and groups you've invited to collaborate on your project, along with their respective roles. Members can either be owners or contributors in a project.

### Data

The **Data** tab shows all data with which you can operate. You can either upload new datasets or connect to exist databases that you might have access to. For more information on adding data to your project, check the documentation.

### Compute

The **Compute** tab displays the configured clusters (such as Spark), databases (such as Amazon Redshift), Spaces (IDEs like JupyterLab), HyperPods, and MLFlow tracking servers, along with other execution endpoints configured for the project. From any of its tabs, you can add additional compute connections to your project as permitted by your administrators. Please check your project profile details to understand the compute allowed in your project.

## JupyterLab

Under the build menu, you can access JupyterLab. The getting_started.ipynb notebook covers the basics of using SageMaker Unified Studio connections with Python kernel for Spark and ML, and is intended as an introduction to the notebook functionality for those not familiar with SageMaker Unified Studio connections.

## Query Editor

The query editor in SageMaker Unified Studio (available under the Build menu) is where you perform data analysis using SQL, supporting both Amazon Redshift and Amazon Athena query engines. The tool makes it simple to connect to your existing data. You can write and run queries, visualize results, view query history, and generate SQL queries using Amazon Q.  For more detailed information, refer to the Query editor documentation.

## Workflows

Workflows in SageMaker Unified Studio allow you to set up and run a series of tasks using Apache Airflow to model data processing procedures and orchestrate code artifacts. You can create workflows in Python code, test them, and access detailed errors and logs on the Workflows page. The tool provides features to view workflow details, including run results, task completions, and parameters.  You can run workflows with default or custom parameters, and monitor their progress on the Runs tab.  Click create workflow to open a python editor in JupyterLab with a sample workflow script. For more advanced visualizations, you can access the Airflow UI to view charts and graphics about the workflow.

## Machine Learning

Below we mention some of the ML features. Please visit our documentation for details list of all Machine Learning features in Amazon SageMaker Unified Studio.

### JumpStart

Apart from building models in JupyterLab, SageMaker Unified Studio also provides access to more than 150 Machine Learning configurable open-source models that support one click deployment and fine tuning. These include foundation models as well as models for natural language processing, object detection, and image classification models. You can explore models by navigating to the "Serverful Model catalog" under the "Discover" menu. 

### Experiments (MLFlow)

SageMaker Unified Studio offers managed MLflow capabilities for creating, analyzing, and managing machine learning experiments. Users can log metrics, parameters, and model information to view and compare experiments, as well as register MLflow Models for management and deployment. Visit the compute tab to check for existing MLFlow tracking servers for your project or create a new one. To access the list of experiments in a project, users can navigate to the "Build" option in the main menu and select "Experiments" from the drop-down menu. 

### Model Registry

The Model Registry in Amazon SageMaker Unified Studio enables users to catalog models and manage their deployment to production by creating Model Groups that track different versions of models trained for specific problems. Users can register models by navigating to the "Build" menu, selecting "Models," and choosing "Register," with options to select model artifacts from various sources. Registered models can be published to the business data catalog to allow discovery and sharing across the broader organization.

## Generative AI

Amazon Bedrock IDE in SageMaker Unified Studio is your all-in-one workspace for building GenAI applications without complex development setup. The tool provides a comprehensive environment where you can discover foundation models through the Model catalog, experiment with different input types in Playgrounds, and build sophisticated chat applications with custom guardrails and data sources. Using the Flow builder, you can create end-to-end AI workflows by connecting prompts and models, while the Prompt builder helps you create and manage your prompts effectively. The Amazon Bedrock IDE includes built-in model evaluation capabilities to assess performance, and a shared gallery for team collaboration on apps, guardrails, and functions. To get started, simply ensure your administrator has enabled GenAI tools access in the admin console.

## Project Storage

Each project comes with a default storage powered by Amazon S3 or a 3rd party repository such as GitHub as configured by your administrator. 

## Data and Model catalog

We hope you enjoy using SageMaker Unified Studio and we look forward to hearing from you. Please use the Feedback icon in the top right corner of your screen to provide feedback.
