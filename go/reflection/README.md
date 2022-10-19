# go gRPC server - reflection

This example starts a gRPC server (with reflection enabled) as well as an http server.

The http server is used to respond to Azure's HTTP health check pings to ensure the container is started.

Steps to run this:
- Build the image locally
- Push the image to a container registry of your choice
- Create a Web Apps for Container application on Azure. Configure this application to pull the image we pushed to the registry.
- Under Set the Configuration -> Application Settings, add an Application Setting named `WEBSITES_PORT` set to 8000 and `HTTP20_ONLY_PORT` set to 50051
- Under Configuration -> General Settings, set HTTP Version to 2.0
- Under Configuration -> General Settings, set HTTP 2.0 Proxy to "On"

> **IMPORTANT**: You may see a HTTP 502 on the root path "/", even though the container is started (you can still connect to the gRPC endpoint) - to access the HTTP endpoint, disable HTTPS ONLY to "OFF"