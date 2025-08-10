# Q-Intelli: MCP Server & Smart Queue Helper

Welcome to Q-Intelli, a real-time queue management and virtual token reservation system designed for efficient crowd handling during emergencies and daily operations.

This project was built as part of the [Puch AI Hackathon](https://puch.ai/hack) and consists of:

- MCP Server: A Flask-based server exposing APIs for virtual token reservation and advice.
- Queue Helper GUI: A Python Tkinter desktop application to interact with the server, scan queue types, and reserve virtual tokens.

## Features

- Secure API key-protected server for managing virtual reservations.
- Intelligent wait time estimation based on queue type and urgency.
- Real-time token generation with countdown.
- Heatmap visualization for crowd density insights.
- Easy-to-use GUI for quick interaction without technical knowledge.

## Usage

1. Run the MCP server ('mcp_server.py') locally or deploy on a public server.
2. Launch the GUI ('queue_identifier.py'), connect to the server, and reserve tokens.
3. Share your virtual tokens to manage queues efficiently.

## Tech Stack

- Python 3.8+
- Flask (for MCP Server)
- Tkinter (for GUI)
- Requests (HTTP client)
- JSON for data persistence
