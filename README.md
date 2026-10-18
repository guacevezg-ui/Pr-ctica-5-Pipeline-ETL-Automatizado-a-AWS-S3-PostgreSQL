# Complete ETL Pipeline - AWS Academy

This project contains an End-to-End Extraction, Transformation, and Loading (ETL) pipeline developed in Python. The script generates mock customer data, performs data transformations (normalization and binning), and loads the results into two targets: a **PostgreSQL** database and an **Amazon S3** bucket.

---

## 🛠️ Prerequisites in AWS Academy

Before running the code, make sure you have the following resources active in your **Learner Lab**:
1. An active **EC2 instance** (preferably Ubuntu or Amazon Linux 2023).
2. An **S3 Bucket** created in your AWS Management Console.
3. A **PostgreSQL database** (either installed locally on the EC2 instance or via **Amazon RDS**).

---

## 🚀 Setup and Installation Guide

Follow these steps inside your EC2 instance terminal:

### 1. Update the System and Install Python
Depending on your EC2 operating system, run the corresponding commands:

* **For Ubuntu:**
  ```bash
  sudo apt update
  sudo apt install python3-pip python3-venv postgresql-client -y
  ```
* **For Amazon Linux 2023:**
  ```bash
  sudo dnf update -y
  sudo dnf install python3-pip postgresql15 -y
  ```

### 2. Configure the Virtual Environment
To keep your Python packages isolated and prevent conflicts, create and activate a virtual environment:

```bash
# Create project folder and move into it
mkdir etl-pipeline && cd etl-pipeline

# Create the virtual environment
python3 -m venv env

# Activate the virtual environment
source env/bin/activate
```
*(You will know it is active when `(env)` appears at the beginning of your terminal prompt).*

### 3. Install Dependencies
With the virtual environment active, install the required Python libraries:

```bash
pip install pandas scikit-learn sqlalchemy psycopg2-binary boto3
```

---

## 📝 Code Configuration

Before running `etl_pipeline.py`, open the file using a text editor (e.g., `nano etl_pipeline.py`) and verify or modify the following parameters:

1. **Database Connection:** In the PostgreSQL section, if you are using **Amazon RDS**, replace `"localhost"` with your actual database Endpoint:
   ```python
   HOST = "://amazonaws.com"
   ```
2. **Amazon S3:** Replace the `BUCKET_NAME` value with your actual S3 bucket name. Make sure to initialize the client without hardcoded credentials (`boto3` will automatically detect the AWS Academy Lab IAM role):
   ```python
   s3_client = boto3.client('s3', region_name='us-east-1')
   BUCKET_NAME = "your-bucket-name-here"
   ```

---

## 🏃‍♂️ Running the Script

To execute the ETL pipeline, simply run the following command in your terminal (with the virtual environment active):

```bash
python etl_pipeline.py
```

The script will output the progress of each phase (Extract, Transform, Load) and confirm whether the data was successfully loaded into PostgreSQL and uploaded to S3.

---

## 🔍 How to Query the Generated Table

Once the script completes successfully, you can query the `clientes_transformados` table directly from your EC2 terminal.

### If PostgreSQL is running on the same EC2 instance (Localhost):
```bash
PGPASSWORD=postgres psql -U postgres -d postgres -h localhost -c "SELECT * FROM clientes_transformados;"
```

### If you are using Amazon RDS:
```bash
PGPASSWORD=postgres psql -U postgres -d postgres -h YOUR_RDS_://amazonaws.com -p 5432 -c "SELECT * FROM clientes_transformados;"
```

> 💡 **Navigation Tip:** If the table contains many records and the screen locks up showing a `:` or the word `(END)`, simply press the **`q`** key on your keyboard to exit the query view and return to the normal terminal.

---

## 🛑 Cost Optimization & Clean Up (Important!)
When you finish your tests in **AWS Academy**, remember to:
1. Exit the virtual environment by running `deactivate`.
2. **Stop your EC2 instance** (`Stop Instance`) and your RDS database from the AWS Console, or click **Stop Lab** in the Academy portal to avoid exhausting your educational credits.
