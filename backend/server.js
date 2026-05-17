const express = require('express');
const http = require('http');
const { Server } = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
    cors: {
        origin: "*",
        methods: ["GET", "POST"]
    }
});

app.use(express.json());

// Basic health check endpoint
app.get('/health', (req, res) => {
    res.json({ status: "JARVIS Orchestration Node.js Backend is running." });
});

io.on('connection', (socket) => {
    console.log(`[WebSocket] Client connected: ${socket.id}`);

    socket.on('agent_event', (data) => {
        console.log('[WebSocket] Agent Event Received:', data);
        // Broadcast the event to all other connected clients (e.g. dashboards)
        socket.broadcast.emit('agent_event', data);
    });

    socket.on('disconnect', () => {
        console.log(`[WebSocket] Client disconnected: ${socket.id}`);
    });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
    console.log(`[Server] Listening on port ${PORT}`);
});
