from channels import include


project_routing = [
    include("Addicore.routing.app_routing", path=r"^/custom_websocket_path"),
]
