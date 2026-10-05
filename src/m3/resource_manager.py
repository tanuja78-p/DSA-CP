from .resource import Resource
from .hash_map import ShelterHashMap
from .priority_queue import ShelterPriorityQueue


class ResourceManager:
    """
    Manages disaster-relief resources.

    DSA used:
    - Custom HashMap for resource lookup
    - Custom Priority Queue for prioritized resource requests
    """

    def __init__(self):
        self.resources = ShelterHashMap()
        self.request_queue = ShelterPriorityQueue()

    # ---------------------------------------------------------
    # RESOURCE MANAGEMENT
    # ---------------------------------------------------------

    def add_resource(self, resource):
        """Add or replace a resource in the resource pool."""

        if not isinstance(resource, Resource):
            raise TypeError("resource must be a Resource object")

        self.resources.put(resource.resource_id, resource)

    def add_resources(self, resources):
        """Add multiple resources."""

        for resource in resources:
            self.add_resource(resource)

    def get_resource(self, resource_id):
        """Return a resource by ID."""

        return self.resources.get(resource_id)

    def get_all_resources(self):
        """Return all resources."""

        return self.resources.values()

    def get_available_resources(self):
        """Return only resources with quantity > 0."""

        return [
            resource
            for resource in self.resources.values()
            if resource.is_available()
        ]

    # ---------------------------------------------------------
    # STOCK MANAGEMENT
    # ---------------------------------------------------------

    def add_stock(self, resource_id, quantity):
        """Increase the quantity of a resource."""

        resource = self.get_resource(resource_id)

        if resource is None:
            raise KeyError(f"Resource not found: {resource_id}")

        resource.add_quantity(quantity)

        return resource.to_dict()

    def remove_stock(self, resource_id, quantity):
        """Decrease the quantity of a resource."""

        resource = self.get_resource(resource_id)

        if resource is None:
            raise KeyError(f"Resource not found: {resource_id}")

        resource.remove_quantity(quantity)

        return resource.to_dict()

    # ---------------------------------------------------------
    # RESOURCE REQUESTS
    # ---------------------------------------------------------

    def request_resource(
        self,
        resource_id,
        quantity,
        requester,
        priority=1,
    ):
        """
        Request a resource.

        Higher priority requests are processed first.

        Returns a request record.
        """

        if quantity <= 0:
            raise ValueError("Requested quantity must be greater than zero")

        if priority < 1:
            raise ValueError("Priority must be at least 1")

        resource = self.get_resource(resource_id)

        if resource is None:
            return {
                "success": False,
                "reason": "Resource not found",
                "resource_id": resource_id,
                "requester": requester,
            }

        if resource.quantity < quantity:
            return {
                "success": False,
                "reason": "Insufficient resource quantity",
                "resource_id": resource_id,
                "available": resource.quantity,
                "requested": quantity,
                "requester": requester,
            }

        request = {
            "resource_id": resource_id,
            "quantity": quantity,
            "requester": requester,
            "priority": priority,
        }

        # Our custom Priority Queue is a min-heap.
        # Therefore use negative priority so that higher
        # priority numbers are processed first.
        self.request_queue.push(
            -priority,
            request
        )

        return {
            "success": True,
            "message": "Resource request queued",
            "request": request,
        }

    # ---------------------------------------------------------
    # PROCESS REQUESTS
    # ---------------------------------------------------------

    def process_next_request(self):
        """
        Process the highest-priority resource request.

        Returns None if no request is waiting.
        """

        if len(self.request_queue) == 0:
            return None

        item = self.request_queue.pop()

        request = item.shelter

        resource = self.get_resource(request["resource_id"])

        if resource is None:
            return {
                "success": False,
                "reason": "Resource no longer exists",
                "request": request,
            }

        if resource.quantity < request["quantity"]:
            return {
                "success": False,
                "reason": "Insufficient quantity at processing time",
                "request": request,
                "available": resource.quantity,
            }

        resource.remove_quantity(request["quantity"])

        return {
            "success": True,
            "message": "Resource allocated successfully",
            "resource_id": resource.resource_id,
            "resource_name": resource.name,
            "quantity_allocated": request["quantity"],
            "requester": request["requester"],
            "priority": request["priority"],
            "remaining_quantity": resource.quantity,
        }

    # ---------------------------------------------------------
    # QUEUE INFORMATION
    # ---------------------------------------------------------

    def pending_request_count(self):
        """Return number of pending resource requests."""

        return len(self.request_queue)

    def clear_requests(self):
        """Clear all pending requests."""

        self.request_queue.clear()

    # ---------------------------------------------------------
    # DISPLAY / REPORTING
    # ---------------------------------------------------------

    def resource_report(self):
        """Return a simple resource inventory report."""

        report = []

        for resource in self.resources.values():
            report.append(resource.to_dict())

        return report