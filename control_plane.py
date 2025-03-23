import logging

# Configure Logging
logging.basicConfig(
    filename="control_plane.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class ControlPlane:
    def __init__(self):
        self.routing_table = {}
        self.service_registry = {}

    def register_service(self, service_name, address):
        if service_name in self.service_registry:
            logging.warning(
                f"Service {service_name} is already registered. Updating address."
            )

        self.service_registry[service_name] = address
        logging.info(f"Service registered: {service_name} -> {address}")

    def get_service_address(self, service_name):
        address = self.service_registry.get(service_name)
        if address:
            logging.info(f"Service address retrieved: {service_name} -> {address}")
        else:
            logging.warning(f"Service {service_name} not found.")
        return address

    def add_route(self, route, service_name):
        if service_name not in self.service_registry:
            logging.error(f"Cannot add route. Service {service_name} is not registered")
            return
        self.routing_table[route] = service_name
        logging.info(f"Route added: {route} -> {service_name}")

    def remove_route(self, route):
        if route in self.routing_table:
            del self.routing_table[route]
            logging.info(f"Route removed: {route}")
        else:
            logging.warning(f"Attempted to remove non-existent route: {route}")

    def get_routes(self):
        logging.info("Retrieving all routes.")
        return self.routing_table

    def resolve_target(self, path):
        for route, service_name in self.routing_table.items():
            if path.startswith(route):
                address = self.get_service_address(service_name)
                if address:
                    logging.info(f"Path {path} resolved to {address}")
                    return address
                else:
                    logging.error(
                        f"Service {service_name} for route {route} is not registered."
                    )
        logging.warning(f"No route found for path: {path}")
        return None


if __name__ == "__main__":
    cp = ControlPlane()

    # Example Usage
    cp.register_service("service1", "http://localhost:8001")
    cp.register_service("service2", "http://localhost:8002")

    cp.add_route("/service1", "service1")
    cp.add_route("/service2", "service2")

    print(cp.get_routes())
    print(cp.resolve_target("/service1/resource"))
    print(cp.resolve_target("/unknown"))
