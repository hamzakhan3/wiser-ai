# Wiser AI - Machine Monitoring & Anomaly Detection System

A comprehensive AI-powered machine monitoring system that provides real-time anomaly detection, vision analysis, and intelligent chat assistance for industrial equipment.

## 🚀 Features

### 🔍 **Real-Time Anomaly Detection**
- **Machine Health Monitoring**: Continuous monitoring of vibration, temperature, and humidity sensors
- **Anomaly Visualization**: Interactive charts showing sensor data patterns and anomaly points
- **Critical Health Alerts**: Real-time notifications for machines requiring immediate attention
- **Historical Analysis**: Trend analysis and pattern recognition over time

### 🤖 **AI-Powered Chat Assistant**
- **Dual Chat Interfaces**: 
  - **Main Chat Page**: General machine monitoring and database queries
  - **Anomaly Inspection Page**: Specialized analysis with image context
- **Real-Time Streaming**: Character-by-character streaming responses for immediate feedback
- **Intelligent Routing**: Context-aware responses based on query source and content
- **Work Order Generation**: Automatic creation of maintenance work orders from chat interactions

### 🖼️ **Machine Vision Analysis**
- **Image-Based Anomaly Detection**: AI analysis of machine images and sensor data visualizations
- **Cached Analysis System**: Efficient storage and retrieval of previous image analyses
- **Contextual Responses**: Follow-up questions use saved analysis for enhanced accuracy
- **Multi-Modal AI**: Combines visual and textual data for comprehensive insights

### 📊 **Data Management**
- **PostgreSQL Database**: Robust data storage with comprehensive schema
- **Real-Time Data Processing**: Live sensor data ingestion and processing
- **Caching System**: Redis-based caching for improved performance
- **Data Visualization**: Interactive charts and graphs for data analysis

### 🔧 **Maintenance Management**
- **Work Order System**: Automated generation and tracking of maintenance tasks
- **Maintenance Scheduling**: Planned maintenance with parts inventory management
- **Technician Assignment**: Resource allocation and task distribution
- **Parts Inventory**: Real-time tracking of machine parts and maintenance supplies

## 🏗️ **Architecture**

### **Backend (Flask)**
- **API Endpoints**: RESTful API for all system operations
- **Streaming Support**: Server-Sent Events (SSE) for real-time communication
- **Database Integration**: SQLAlchemy ORM with PostgreSQL
- **AI Integration**: OpenAI GPT-4o for chat and vision analysis
- **Caching Layer**: Redis for performance optimization

### **Frontend (React + TypeScript)**
- **Modern UI**: Built with React, TypeScript, and Tailwind CSS
- **Component Library**: shadcn/ui components for consistent design
- **Real-Time Updates**: WebSocket-like streaming for live data
- **Responsive Design**: Mobile-friendly interface
- **State Management**: React hooks for efficient state handling

### **Database Schema**
- **Machine Data**: Equipment information, sensor readings, and health status
- **Anomaly Detection**: Anomaly records and detection algorithms
- **Vision Analysis**: Cached AI analysis results and image metadata
- **Work Orders**: Maintenance tasks, assignments, and completion tracking
- **User Management**: Authentication and role-based access control

## 🚀 **Getting Started**

### **Prerequisites**
- Python 3.11+
- Node.js 18+
- PostgreSQL 13+
- Redis (optional, for caching)

### **Installation**

1. **Clone the repository**
   ```bash
   git clone https://github.com/hamzakhan3/wiser-ai.git
   cd wiser-ai
   ```

2. **Backend Setup**
   ```bash
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Set up environment variables
   cp .env.example .env
   # Edit .env with your database and API credentials
   ```

3. **Frontend Setup**
   ```bash
   # Install dependencies
   npm install
   
   # Start development server
   npm run dev
   ```

4. **Database Setup**
   ```bash
   # Create PostgreSQL database
   createdb wiser_ai
   
   # Run migrations (if available)
   python src/services/migrate.py
   ```

5. **Start Services**
   ```bash
   # Terminal 1: Start backend
   cd /path/to/wiser-ai
   source venv/bin/activate
   python src/services/app.py
   
   # Terminal 2: Start frontend
   npm run dev
   ```

## 📱 **Usage**

### **Machine Health Dashboard**
1. Navigate to `/machine-health` to view all machines
2. Click on any machine to see detailed health metrics
3. Use filters to focus on specific sensor types or time ranges
4. Click "Inspect Anomaly" for detailed analysis

### **Anomaly Inspection**
1. From the machine health page, click "Inspect Anomaly" on any machine
2. View interactive charts showing sensor data and anomaly points
3. Use the chat interface to ask questions about the anomalies
4. Generate work orders directly from the chat interface

### **AI Chat Assistant**
1. **Main Chat**: Navigate to `/chat` for general queries about machines, production, or data
2. **Anomaly Chat**: Use the chat interface on the inspection page for context-aware analysis
3. **Streaming Responses**: Watch responses appear in real-time as the AI generates them
4. **Work Orders**: Ask to "generate a work order" to create maintenance tasks

### **Vision Analysis**
1. Upload machine images or use existing sensor data visualizations
2. AI analyzes the images for anomalies and patterns
3. Ask follow-up questions that use the saved analysis for context
4. Get detailed insights about potential issues and solutions

## 🔧 **API Endpoints**

### **Query Endpoints**
- `POST /query` - Main query endpoint with streaming support
- `POST /stream` - Legacy streaming endpoint
- `GET /inspection` - Get inspection data with filters

### **Machine Data**
- `GET /machines` - List all machines
- `GET /machine/{id}` - Get specific machine details
- `GET /machine-health` - Get health status for all machines

### **Anomaly Detection**
- `GET /anomalies` - List detected anomalies
- `POST /anomaly/analyze` - Analyze specific anomaly
- `GET /anomaly/{id}` - Get anomaly details

### **Work Orders**
- `GET /work-orders` - List all work orders
- `POST /work-order` - Create new work order
- `PUT /work-order/{id}` - Update work order status

## 🎯 **Key Features in Detail**

### **Real-Time Streaming**
- **Character-by-character streaming** for immediate user feedback
- **Status updates** during processing (e.g., "Analyzing machine anomaly...")
- **Error handling** with graceful fallbacks
- **Consistent experience** across all chat interfaces

### **Intelligent Context Management**
- **Source-aware routing** (main chat vs. anomaly page)
- **Cached analysis integration** for follow-up questions
- **Enhanced prompts** with image analysis context
- **Fallback mechanisms** for missing data

### **Advanced Caching**
- **Database caching** for vision analysis results
- **Redis caching** for frequently accessed data
- **Smart cache invalidation** based on data freshness
- **Fallback strategies** when cache is unavailable

### **Work Order Intelligence**
- **Intent detection** for work order requests
- **Automatic field population** from chat context
- **Integration with parts inventory**
- **Technician assignment logic**

## 🔒 **Security & Performance**

### **Security Features**
- **Input validation** and sanitization
- **SQL injection prevention** through ORM
- **CORS configuration** for cross-origin requests
- **Environment variable management** for sensitive data

### **Performance Optimizations**
- **Database indexing** for fast queries
- **Connection pooling** for database efficiency
- **Caching strategies** for reduced API calls
- **Streaming responses** for better user experience

## 🧪 **Testing**

### **Backend Testing**
```bash
# Run backend tests
python -m pytest tests/
```

### **Frontend Testing**
```bash
# Run frontend tests
npm test
```

### **Integration Testing**
```bash
# Test API endpoints
curl -X POST http://localhost:5001/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Show me machine health status", "source": "chat"}'
```

## 📈 **Monitoring & Analytics**

### **System Metrics**
- **Response times** for API endpoints
- **Database query performance**
- **Cache hit rates**
- **Error rates and types**

### **User Analytics**
- **Chat interaction patterns**
- **Most common queries**
- **Feature usage statistics**
- **User engagement metrics**

## 🚀 **Deployment**

### **Production Setup**
1. **Environment Configuration**
   ```bash
   # Set production environment variables
   export FLASK_ENV=production
   export DATABASE_URL=postgresql://user:pass@host:port/db
   export OPENAI_API_KEY=your_api_key
   ```

2. **Database Migration**
   ```bash
   # Run production migrations
   python src/services/migrate.py --env=production
   ```

3. **Build Frontend**
   ```bash
   # Build for production
   npm run build
   ```

4. **Deploy Backend**
   ```bash
   # Use production WSGI server
   gunicorn -w 4 -b 0.0.0.0:5001 src.services.app:app
   ```

### **Docker Deployment**
```bash
# Build and run with Docker
docker-compose up -d
```

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 **Support**

For support and questions:
- Create an issue in the GitHub repository
- Check the documentation in the `/docs` folder
- Review the API documentation at `/api-docs`

## 🔄 **Recent Updates**

### **Feature-Sage-006** (Latest)
- ✅ **Real-time streaming** for anomaly page
- ✅ **Enhanced context** in AI prompts
- ✅ **Improved caching** with fallback logic
- ✅ **Consistent streaming** experience across all pages
- ✅ **Better error handling** and debug logging

### **Previous Features**
- ✅ Machine health monitoring dashboard
- ✅ AI-powered chat assistant
- ✅ Vision analysis with image processing
- ✅ Work order generation system
- ✅ Real-time anomaly detection
- ✅ Interactive data visualization

---

**Built with ❤️ for industrial machine monitoring and maintenance optimization.**