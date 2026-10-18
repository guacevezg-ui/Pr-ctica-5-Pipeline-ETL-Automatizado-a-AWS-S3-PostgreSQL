import io
import boto3
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sqlalchemy import create_engine

# ==========================================
# REEMPLAZA ESTOS VALORES CON TUS CREDENCIALES REALES DE AWS
# ==========================================
AWS_ACCESS_KEY_ID = " "
AWS_SECRET_ACCESS_KEY = " "
AWS_SESSION_TOKEN = " "  # Déjalo como None o "" si usas credenciales permanentes
AWS_REGION = " "
# ==========================================


def pipeline_etl_completo():
    print("=== 1. FASE DE EXTRACCIÓN (Extract) ===")
    raw_data = {
        "cliente": ["A", "B", "C", "D"],
        "edad": [22, 35, 48, 67],
        "monto_compras": [1200.0, 50000.0, 30000.0, 15000.0],
    }
    df_raw = pd.DataFrame(raw_data)

    print("=== 2. FASE DE TRANSFORMACIÓN (Transform) ===")
    df_raw["categoria_edad"] = pd.cut(
        df_raw["edad"],
        bins=[0, 25, 50, 100],
        labels=["Joven", "Adulto", "Senior"],
    )

    scaler = MinMaxScaler()
    df_raw["monto_normalizado"] = scaler.fit_transform(
        df_raw[["monto_compras"]]
    )

    df_raw["score_promocional"] = df_raw["monto_normalizado"] * 100

    print("Dataset Transformado:")
    print(df_raw)

    print("\n=== 3. FASE DE CARGA (Load) ===")

    try:
        USER, PASSWORD, HOST, PORT, DB_NAME = (
            "postgres",
            "postgres",
            "localhost",
            "5432",
            "postgres",
        )
        connection_url = (
            f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
        )
        engine = create_engine(connection_url)

        df_raw.to_sql(
            "clientes_transformados",
            con=engine,
            if_exists="replace",
            index=False,
        )
        print(
            "-> Éxito: Datos cargados en PostgreSQL (tabla 'clientes_transformados')."
        )
    except Exception as e:
        print(f"-> Error al cargar en PostgreSQL: {e}")

    try:
        csv_buffer = io.StringIO()
        df_raw.to_csv(csv_buffer, index=False)

        # Aquí pasamos las variables de configuración válidas a la sesión de AWS
        session = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            aws_session_token=AWS_SESSION_TOKEN,
            region_name=AWS_REGION,
        )

        s3_client = session.client("s3")
        BUCKET_NAME = "aws-academy-datacenter-bucket-1902676"
        KEY_NAME = "processed/etl_output.csv"

        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=KEY_NAME,
            Body=csv_buffer.getvalue().encode("utf-8"),
            ContentType="text/csv",
        )

        print(
            f"-> Éxito: Archivo CSV subido a AWS S3 en 's3://{BUCKET_NAME}/{KEY_NAME}'"
        )
    except Exception as e:
        print(f"-> Error al subir a S3: {e}")


if __name__ == "__main__":
    pipeline_etl_completo()
