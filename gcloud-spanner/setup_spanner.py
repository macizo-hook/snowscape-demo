import logging
import argparse
from google.cloud import spanner
from google.cloud.spanner_admin_instance_v1.types import spanner_instance_admin
from google.cloud.spanner_v1 import param_types

logging.basicConfig(level=logging.INFO)

def setup_spanner(instance_id, database_id):
    try:
        spanner_client = spanner.Client()

        # Check if instance and db already exist, otherwise create what is missing and populate the newly create db with our desired schema.
        if instance_id in [i.name.split('/')[-1] for i in spanner_client.list_instances()]:
            logging.info(f"Instance {instance_id} already exists.")
            instance = spanner_client.instance(instance_id)
        else:
            logging.info(f"Creating instance {instance_id}...")
            config_name = f"projects/{spanner_client.project}/instanceConfigs/regional-us-central1"
            instance = spanner_client.instance(instance_id, config_name)
            instance.create()

        
        if database_id in [db.name.split("/")[-1] for db in instance.list_databases()]:
            logging.info(f"Database {database_id} already exists.")
            database = instance.database(database_id)
        else:
            logging.info(f"Creating database {database_id}...")
            database = instance.database(database_id, ddl_statements=[
                """CREATE TABLE Orders (
                    OrderID INT64,
                    Timestamp TIMESTAMP,
                    ProductName STRING(1024),
                    Quantity INT64,
                    AvalancheTxID STRING(1024)
                ) PRIMARY KEY (OrderID)
                """
            ])
            database.create()

        logging.info("Spanner setup completed.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Setup Google Cloud Spanner")
    parser.add_argument("--instance_id", required=True, help="Spanner instance ID")
    parser.add_argument("--database_id", required=True, help="Spanner database ID")

    args = parser.parse_args()
    setup_spanner(args.instance_id, args.database_id)
