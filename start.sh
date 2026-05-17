#!/bin/bash
cd backend
npm install
node server.js &
NODE_PID=$!
cd ..
python main.py
kill $NODE_PID
