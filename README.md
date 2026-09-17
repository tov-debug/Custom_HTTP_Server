# Custom HTTP Server

A lightweight, educational HTTP server.
It was created to practice networking concepts like TCP connection handling, HTTP parsing, and basic traffic filtering without relying on external web frameworks.

## Key Features
* **Raw TCP Sockets:** Handles client-server connections directly at the transport layer.
* **Custom HTTP Parsing:** Extracts HTTP methods, paths, and headers from incoming byte streams.
* **Layered Filtering:** Applies basic IP subnet blocking (CIDR) and regex-based request inspection.
* **Dockerized:** Packaged in a container for a clean, isolated execution environment.

## Technologies Used

* Python with Standard Library: `socket`, `argparse`, `re`.
* Docker
  
### Run via Docker

**Build the image:**

```bash
docker build -t custom-http-server .
```

**Run the server:**

```bash
docker run -p 8085:8085 custom-http-server
```

The server listens on port `8085`.

---

> **Note:** It is a demo project applying hands-on networking concepts. It is not intended as a production-grade HTTP server or WAF.
