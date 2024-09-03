import azure.functions as func

from . import visit_counter_app

app = func.AsgiFunctionApp(
    app=visit_counter_app,
    http_auth_level=func.AuthLevel.ANONYMOUS,
)
