import os

# Database Information
DB_USER     = os.getenv("DB_USER","root")
DB_PASS     = os.getenv("DB_PASS","root")
DB_IP       = os.getenv("DB_HOST","127.0.0.1")
DB_PORT     = os.getenv("DB_PORT","5430")
DB_NAME     = os.getenv("DB_NAME","license_db")

# Encryption
ENC_KEY     = os.getenv("ENC_KEY","qc1Un8Utu4wapfMzVcFpo9cXWVRQv6_oFbwQexhV3PM=")

# Folder Path
APP_PATH        = os.getenv("APP_PATH","/usr/src/app/data/app")
IMG_PATH        = os.getenv("IMG_PATH","/usr/src/app/data/images")
ORG_DATA_PATH   = os.getenv("ORG_DATA_PATH","/usr/src/app/data/license/original_data")
ENC_DATA_PATH   = os.getenv("ENC_DATA_PATH","/usr/src/app/data/license/encrypted_data")

# Payment Credentials
CLIENT_ID       = os.getenv("CLIENT_ID","321006c79ba794b84a59522df8600123")
CLIENT_SECRET   = os.getenv("CLIENT_SECRET","1ea7cb51ebbb80442562b5bedf891f0841f6d8d1")
PAYMENT_URL     = os.getenv("PAYMENT_URL","https://sandbox.cashfree.com/pg/orders/")