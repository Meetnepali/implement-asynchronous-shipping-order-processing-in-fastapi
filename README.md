# Guide to the Project

## Task Overview
This project is a modular FastAPI application designed for asynchronous processing of shipping orders. It exposes endpoints allowing clients to create new shipping orders and query their status. Order intake undergoes strict input validation, and each order is assigned a unique ID and a 'pending' status. Background processing asynchronously assigns a delivery route after a short delay. All order data is stored in-memory, making this suitable for demonstration and prototyping without persistent storage.

## Objectives
- Accept and process new shipping orders via a dedicated API endpoint.
- Validate input data with Pydantic, ensuring completeness and type correctness.
- Assign a unique order ID and maintain order status using in-memory storage.
- Handle delivery route assignment asynchronously via a background task.
- Expose endpoints for checking order status and assigned route.
- Use FastAPI routers for clean modularity of order-related logic.
- Implement structured error handling and application-level logging for traceability.
- Deliver a developer-friendly, containerized solution suitable for local or cloud deployment.

## Verifying Your Solution
- Check that submitting a shipping order returns a unique order ID and initial status of 'pending'.
- Observe that after a short delay, the order status updates to 'assigned' with a randomly selected delivery route.
- Confirm that the API rejects invalid order submissions with appropriate validation errors and logging.
- Ensure the application is organized using routers, and logging output is present and structured.
- Make sure the container builds and runs the service successfully without additional configuration.
