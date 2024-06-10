import os
import json
import requests
import os
import time
from dotenv import load_dotenv

class baseModel():

    def __init__(self):
        
        load_dotenv()

        self.DATABRICKS_TOKEN = os.getenv('DATABRICKS_TOKEN')

    
    def respond(self, query):
        url_create = "https://dbc-02b8d70c-8167.cloud.databricks.com/api/2.0/jobs/create"
        url_run_now = "https://dbc-02b8d70c-8167.cloud.databricks.com/api/2.0/jobs/run-now"
        url_get_output = "https://dbc-02b8d70c-8167.cloud.databricks.com/api/2.0/jobs/runs/get-output"

        headers = {
        "Authorization": f"Bearer {self.DATABRICKS_TOKEN}",
        "Content-Type": "application/json"
    }
        payload = { "name": "Marketing Chatbot", "tasks": [ { "task_key": "Test", "run_if": "ALL_SUCCESS", "notebook_task": { "notebook_path": "/Workspace/Users/tschauman@group14.technology/Databricks GenAI Summit Hackathon", "base_parameters": { "prompt": query}, "source": "WORKSPACE" }, "warehouse_id": "182c4cf5a7456dd3" } ] }
        response = requests.post(url_create, headers=headers, data=json.dumps(payload))
        job_id = json.loads(response.content)['job_id']

        payload_2 = { "job_id": job_id}
        response = requests.post(url_run_now, headers=headers, data=json.dumps(payload_2))

        run_id = json.loads(response.content)['run_id']
        number_in_job = json.loads(response.content)['number_in_job']

        
        payload_3 = { "run_id": run_id, "number_in_job": number_in_job }
        response = requests.get(url_get_output, headers=headers, data=json.dumps(payload_3))

        while "result_state" not in json.loads(response.content)["metadata"]["state"]:
            payload_3 = { "run_id": run_id, "number_in_job": number_in_job }
            response = requests.get(url_get_output, headers=headers, data=json.dumps(payload_3))
            print(json.loads(response.content)["metadata"]["state"])
            time.sleep(5)

        return json.loads(response.content)["notebook_output"]["result"]


