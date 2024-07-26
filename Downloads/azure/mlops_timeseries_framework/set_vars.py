# Databricks notebook source
import os
import yaml
import json
import mlflow 
import time
from datetime import datetime

working_directory = dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath()
working_directory = str(working_directory)
config_file_name = "config.yml"
try:
    root_dir = os.path.abspath(os.path.join(working_directory,'..','..'))
    root_dir = root_dir.replace('/databricks/driver/Some(','/Workspace')
    config_path = os.path.join(root_dir,config_file_name)
    # Read the configuration file
    with open(config_path, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
except:
    root_dir = os.path.abspath(os.path.join(config_file_name,'..','..'))
    root_dir = root_dir.replace('Some(','/Workspace')
    config_path = os.path.join(root_dir,config_file_name)
    # Read the configuration file
    with open(config_path, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)


details = dbutils.notebook.entry_point.getDbutils().notebook().getContext().toJson()
details_json = json.loads(details)
base_config = json.dumps(config)
dbutils.jobs.taskValues.set(key='config', value=base_config)
current_run_id = details_json['tags']['jobRunId' ]
print(current_run_id)


# COMMAND ----------

def create_or_set_experiment(config, experiment_name):
    """
    Creates a new MLflow experiment if it does not already exist.

    Args:
        config : dict
        experiment_name (str): The base name of the experiment.

    Returns:
        str: The full name of the experiment.
    """
    # checking if already exists
    experiment_name += f"/time_series_template_experiment_registry"

    try:
        experiment_id = mlflow.create_experiment(experiment_name)
        print(f"Experiment '{experiment_name}' created with ID: {experiment_id} ")
        config["experiment_id"] = experiment_id
    except:
        print(f"Experiment '{experiment_name}' already exist. Skipping creation.")
        experiment_id = mlflow.MlflowClient().get_experiment_by_name(experiment_name).experiment_id
        print(experiment_id)

    # update_config(key="experiment_id", value=experiment_id)
    dbutils.jobs.taskValues.set(key='experiment_id', value=experiment_id)
        
        
    return experiment_name
     
     
def get_run_id(config):
    """
    Starts an MLflow run and retrieves the run ID.

    Args:
        config (dict): Configuration dictionary containing the experiment name.

    Returns:
        str: The run ID of the MLflow run.
    """
    try:
        experiment_name = create_or_set_experiment(config, config["experiment_name"])
    except:
        experiment_name=config["experiment_name"]
        experiment_name += f"/time_series_template_experiment_registry"
    mlflow.set_experiment(experiment_name)
    with mlflow.start_run() as run:

        time.sleep(15)
        run_id = run.info.run_id
        run_name= current_run_id
        #run_name= "example_run_name"
        mlflow.set_tag("mlflow.runName", run_name)
        print(f"Run ID: {run_id}")
    
    # update_config(key="run_id", value=run_id)

    return run_id 


def mlflow_main(config):
    """
    Main function to execute the MLflow experiment run and store the run ID.

    Args:
        config (dict): Configuration dictionary containing the experiment name.

    Returns:
        str: The run ID of the MLflow run.
    """
    
    run_id = get_run_id(config)
    
    dbutils.jobs.taskValues.set(key='run_id', value=run_id)

# COMMAND ----------

mlflow_main(config)

# COMMAND ----------

file_path = config['output_storage_path'].split('/', 1)[1]

# COMMAND ----------

dbutils.fs.mkdirs(file_path)

# COMMAND ----------

