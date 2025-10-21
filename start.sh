#!/bin/bash

echo "🔨 Building React frontend..."
npm run build

echo "🚀 Starting Flask server..."
python src/services/app.py
