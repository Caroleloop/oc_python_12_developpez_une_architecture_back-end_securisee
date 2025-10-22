import os
import sentry_sdk
from dotenv import load_dotenv

# Charge les variables d'environnement
load_dotenv()

# Initialisation de Sentry
SENTRY_DSN = os.getenv("SENTRY_DSN")
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        traces_sample_rate=1.0,  # Pour activer le tracing (optionnel)
    )
