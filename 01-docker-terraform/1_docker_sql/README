✅ commands to setup Postgres and pgAdmin
docker-compose build
docker-compose up -d

✅ command to load data into Postgres # change table_name and url each time
python ingest_data.py \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=ny_taxi \
  --table_name=yellow_taxi_data \ 
  --url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

✅ steps in pgAdmin (http://localhost:8080)
Log in with:
Email: admin@admin.com
Password: root
In the left panel → Servers → right click → Register → Server
Fill it in:
General → Name: ny_taxi_postgres (or anything you like)
Connection tab:
Host name/address: pgdatabase (that’s the service name in docker-compose)
Port: 5432
Username: root
Password: root
Save → Now you can see the ny_taxi database, schemas, and tables.

✅ summary
	• docker-compose.yaml = recipe that lists all services (Postgres, pgAdmin, etc.), so instead of running many docker run commands, you just do docker-compose up. ✔️
	• Containers = little computers (isolated environments) you can run anywhere Docker is available. ✔️
	• Persistence with volumes = data is mounted outside the container, so it survives container shutdown. ✔️

1. Volumes
volumes:
  - "./ny_taxi_postgres_data:/var/lib/postgresql/data:rw"
	• The left side (./ny_taxi_postgres_data) = a folder on your local machine (host).
		○ ./ means “in the current directory where I ran docker-compose”.
	• The right side (/var/lib/postgresql/data) = the folder inside the Postgres container where Postgres normally stores its data.
	• :rw means read/write.
👉 So yes, the database files are saved on your local machine’s filesystem. That’s why your database survives even if the container is deleted — because the data lives outside the container in that local folder.
If you ran this on a Google Cloud VM, the ./ny_taxi_postgres_data folder would live on that VM’s disk, not your laptop.

2. Why local machine and Google Cloud VM?
Think of it in layers:
	• Docker = little computers (containers), but they need a real machine to run on.
		○ Docker doesn’t replace the machine — it sits on top of it.
	• Local machine: Good for development, testing, experimenting quickly.
	• Cloud VM:
		○ Acts like a “remote host computer” where Docker runs.
		○ Useful when you need more compute, or when you want others (teammates, dashboards, clients) to access your services (Postgres/pgAdmin) without relying on your laptop being on.
		○ In practice, this mimics deploying to staging or production.
So:
	• Docker ≈ “portable apps” (isolated computers).
	• Local machine / GCP VM ≈ the physical or virtual hardware that runs Docker.
You always need some underlying machine (your laptop, a VM, a Kubernetes cluster, etc.) to host the containers.

✅ Analogy:
	• Containers = “appliances” (like a fridge, oven).
	• Docker Compose = “kitchen blueprint” that wires them up together.
	• Local machine / GCP VM = “the house” where you put the kitchen.

