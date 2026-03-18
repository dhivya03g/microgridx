# config.py

class Config:
    DEBUG = True
    HOST = "127.0.0.1"
    PORT = 5000

    # Energy thresholds
    LOW_BATTERY = 30
    HIGH_TEMP = 45
    FAILURE_THRESHOLD = 200

    # Carbon factor
    CARBON_FACTOR = 0.0007