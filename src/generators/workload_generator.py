import pandas as pd

QUEUE_CONFIG = {
    "Claims": {
        "base_volume": 850,
        "base_aht": 450
    },
    "Billing": {
        "base_volume": 650,
        "base_aht": 300
    },
    "Customer Service": {
        "base_volume": 1200,
        "base_aht": 350
    },
    "Escalations": {
        "base_volume": 150,
        "base_aht": 700
    },
    "Technical Support": {
        "base_volume": 450,
        "base_aht": 600
    }
}

DOW_MULTIPLIER = {
    0: 1.20,
    1: 1.15,
    2: 1.05,
    3: 1.00,
    4: 0.90,
    5: 0.70,
    6: 0.50
}

MONTH_MULTIPLIER = {
    1: 1.00,
    2: 0.98,
    3: 1.00,
    4: 1.08,
    5: 1.12,
    6: 1.10,
    7: 0.92,
    8: 0.90,
    9: 1.08,
    10: 1.12,
    11: 1.15,
    12: 1.25
}

