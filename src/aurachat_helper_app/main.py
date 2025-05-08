import sentry_sdk
from aurachat_helper_app.controllers.root_controller import RootController
import os
from dotenv import load_dotenv

def main():
    """Main entry point for the application."""
    # Load environment variables
    load_dotenv()
    
    # Initialize Sentry
    sentry_sdk.init(
        dsn="https://41443fc5e98405232923f3c3950a04e3@o4509265194713088.ingest.us.sentry.io/4509274945486848",
        # Add data like request headers and IP for users,
        # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
        send_default_pii=True,
        # Enable performance monitoring
        traces_sample_rate=1.0,
        # Set environment
        environment=os.getenv("ENVIRONMENT", "development")
    )
    
    root_controller = RootController()
    root_controller.start()

if __name__ == "__main__":
    main()
