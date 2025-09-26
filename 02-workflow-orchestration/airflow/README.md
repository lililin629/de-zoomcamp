### Pre-requisites:
This tutorial assumes that the service account credentials JSON file is named `google_credentials.json` and stored in `$HOME/.google/credentials/.` Copy and rename your credentials file to the required path.
docker-compose should be at least version v2.x+ and Docker Engine should have at least 5GB of RAM available, ideally 8GB. On Docker Desktop this can be changed in Preferences > Resources.

### Setup (full version)
1. Create a new airflow subdirectory in your work directory.
2. Download the official Docker-compose YAML file for the latest Airflow version.
```curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.2.3/docker-compose.yaml'``` 
3. generate a .env file with the appropiate UID with the following command:
```echo -e "AIRFLOW_UID=$(id -u)" > .env```
4. The base Airflow Docker image won't work with GCP, so we need to customize it.
    We use the base Apache Airflow image as the base.
    We install the GCP SDK CLI tool so that Airflow can communicate with our GCP project.
    We also need to provide a requirements.txt file to install Python dependencies. The dependencies are:
    apache-airflow-providers-google so that Airflow can use the GCP SDK.
    pyarrow , a library to work with parquet files.
5. Alter the x-airflow-common service definition inside the docker-compose.yaml file as follows:
    - We need to point to our custom Docker image. At the beginning, comment or delete the image field and uncomment the build line, or arternatively, use the following (make sure you respect YAML indentation):
    ```
    build:
        context: .
        dockerfile: ./Dockerfile
    ```
    -  Add a volume and point it to the folder where you stored the credentials json file. Assuming you complied with the pre-requisites and moved and renamed your credentials, add the following line after all the other volumes:
    ```- ~/.google/credentials/:/.google/credentials:ro```
    - Add 2 new environment variables right after the others: GOOGLE_APPLICATION_CREDENTIALS and AIRFLOW_CONN_GOOGLE_CLOUD_DEFAULT:
    ```GOOGLE_APPLICATION_CREDENTIALS: /.google/credentials/google_credentials.json```
    ```AIRFLOW_CONN_GOOGLE_CLOUD_DEFAULT: 'google-cloud-platform://?extra__google_cloud_platform__key_path=/.google/credentials/google_credentials.json'```
    - Add 2 new additional environment variables for your GCP project ID and the GCP bucket that Terraform should have created in the previous lesson. You can find this info in your GCP project's dashboard.
    ```GCP_PROJECT_ID: '<your_gcp_project_id>'```
    ```GCP_GCS_BUCKET: '<your_bucket_id>'```
    - Change the AIRFLOW__CORE__LOAD_EXAMPLES value to 'false'. This will prevent Airflow from populating its interface with DAG examples.
    




