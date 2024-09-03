import azure.functions as func
from visit_counter import vist_counter_app

app = func.AsgiFunctionApp(
    app=vist_counter_app,
    http_auth_level=func.AuthLevel.ANONYMOUS,
)
