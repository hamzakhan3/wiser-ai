# Wiser AI - Machine Monitoring System

A comprehensive AI-powered machine monitoring and data analysis platform built with React, Python Flask, and PostgreSQL. Features real-time streaming chat interface, machine health monitoring, production analytics, and intelligent data insights.

## 🚀 Features

### Core Functionality
- **AI-Powered Chat Interface** - Real-time streaming responses with character-by-character typing effect
- **Machine Health Monitoring** - Track machine status, health metrics, and critical alerts
- **Production Analytics** - Monitor production data, downtime, and efficiency metrics
- **Intelligent Data Insights** - Natural language queries with GPT-4o powered responses
- **Work Order Management** - Create and manage maintenance work orders
- **Inspection Tools** - Comprehensive machine inspection capabilities

### Technical Features
- **Server-Sent Events (SSE)** - Real-time streaming for instant responses
- **Natural Language Processing** - Query your data using plain English
- **PostgreSQL Integration** - Robust data storage and retrieval
- **LlamaIndex Integration** - Advanced SQL query generation from natural language
- **GPT-4o Refinement** - Enhanced response formatting and clarity
- **Responsive Design** - Modern UI with Tailwind CSS and shadcn/ui components

## 🛠️ Tech Stack

### Frontend
- **React 18** - Modern React with hooks and functional components
- **TypeScript** - Type-safe development
- **Vite** - Fast build tool and development server
- **Tailwind CSS** - Utility-first CSS framework
- **shadcn/ui** - Beautiful, accessible UI components
- **Recharts** - Data visualization and charting
- **React Markdown** - Markdown rendering for AI responses

### Backend
- **Python Flask** - Lightweight web framework
- **PostgreSQL** - Relational database for data storage
- **SQLAlchemy** - Python SQL toolkit and ORM
- **LlamaIndex** - Natural language to SQL query engine
- **OpenAI GPT-4o** - AI response refinement and formatting
- **Server-Sent Events** - Real-time streaming communication

## 📋 Prerequisites

- **Node.js** (v18 or higher) - [Install with nvm](https://github.com/nvm-sh/nvm#installing-and-updating)
- **Python 3.11+** - [Download from python.org](https://www.python.org/downloads/)
- **PostgreSQL** - [Download from postgresql.org](https://www.postgresql.org/download/)
- **Git** - [Download from git-scm.com](https://git-scm.com/downloads)

## 🚀 How to Start the Project

### Prerequisites Check
Make sure you have the following installed:
- **Node.js** (v18+) - Check with `node --version`
- **Python 3.11+** - Check with `python --version`
- **PostgreSQL** - Check with `psql --version`
- **Git** - Check with `git --version`

### Step 1: Clone and Navigate
```bash
git clone https://github.com/hamzakhan3/wiser-ai.git
cd wiser-ai
```

### Step 2: Backend Setup

#### Create and Activate Python Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# You should see (venv) in your terminal prompt
```

#### Install Python Dependencies
```bash
# Install required packages
pip install flask sqlalchemy psycopg2-binary llama-index openai python-dotenv
```

#### Database Setup
1. **Start PostgreSQL service** (if not running)
2. **Create database**:
   ```bash
   # Connect to PostgreSQL
   psql -U postgres
   
   # Create database
   CREATE DATABASE wiser_ai;
   
   # Exit psql
   \q
   ```

#### Start Backend Server
```bash
# Make sure you're in the project root and venv is activated
python src/services/app.py
```

**✅ Backend is running at:** `http://localhost:5001`

### Step 3: Frontend Setup

#### Open a New Terminal Window
```bash
# Navigate to project directory
cd wiser-ai

# Install Node.js dependencies
npm install
```

#### Start Frontend Development Server
```bash
npm run dev
```

**✅ Frontend is running at:** `http://localhost:8080`

### Step 4: Verify Everything is Working

1. **Open your browser** and go to `http://localhost:8080`
2. **You should see** the Wiser AI interface
3. **Test the chat** by typing "hello" or "list of machines"
4. **Check backend logs** in the terminal running `python src/services/app.py`

### 🎯 Quick Start Commands Summary

```bash
# Terminal 1 - Backend
cd wiser-ai
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install flask sqlalchemy psycopg2-binary llama-index openai python-dotenv
python src/services/app.py

# Terminal 2 - Frontend  
cd wiser-ai
npm install
npm run dev
```

### 🔧 Troubleshooting

**Backend Issues:**
- Make sure PostgreSQL is running
- Check if port 5001 is available
- Verify database connection in `src/services/app.py`

**Frontend Issues:**
- Make sure Node.js is installed
- Try `npm install` again if dependencies fail
- Check if port 8080 is available

**Database Issues:**
- Ensure PostgreSQL service is running
- Verify database `wiser_ai` exists
- Check database credentials in the backend code

## 🎯 Usage

### Chat Interface
- Navigate to the main chat page
- Ask questions about your machines, production data, or health status
- Experience real-time streaming responses with typing effect
- Get formatted markdown responses with proper headings and lists

### Example Queries
- "Show me all machines with critical health status"
- "Which machines had the most downtime this week?"
- "List the production output for each machine"
- "What's the health status of CNC Machine A?"

### Machine Monitoring
- View real-time machine health metrics
- Monitor production efficiency and downtime
- Track maintenance schedules and work orders
- Generate inspection reports

## 🔧 Development

### Project Structure
```
wiser-ai/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── ui/             # shadcn/ui components
│   │   ├── Chart.tsx       # Data visualization
│   │   ├── Sidebar.tsx     # Navigation sidebar
│   │   └── ...
│   ├── pages/              # Main application pages
│   │   ├── ChatPage.tsx    # Main chat interface
│   │   ├── InspectionPage.tsx # Machine inspection
│   │   └── ...
│   ├── services/           # API and backend services
│   │   ├── app.py          # Flask backend server
│   │   ├── apiService.ts   # Frontend API client
│   │   └── ...
│   └── lib/                # Utility functions
├── public/                 # Static assets
└── README.md
```

### Available Scripts
```bash
# Development
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Run ESLint

# Backend
python src/services/app.py  # Start Flask server
```

### Environment Variables
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=postgresql://username:password@localhost:5432/wiser_ai
```

## 🚀 Deployment

### Frontend Deployment
The frontend can be deployed to any static hosting service:
- **Vercel**: Connect your GitHub repository
- **Netlify**: Drag and drop the `dist` folder after `npm run build`
- **GitHub Pages**: Use GitHub Actions for automated deployment

### Backend Deployment
The Flask backend can be deployed to:
- **Heroku**: Use the included `Procfile`
- **Railway**: Connect your GitHub repository
- **DigitalOcean App Platform**: Deploy with automatic scaling
- **AWS/GCP/Azure**: Use container services

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up --build
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/hamzakhan3/wiser-ai/issues) page
2. Create a new issue with detailed information
3. Contact the development team

## 🔮 Roadmap

- [ ] Advanced analytics dashboard
- [ ] Machine learning predictions
- [ ] Mobile application
- [ ] Multi-tenant support
- [ ] Advanced reporting features
- [ ] Integration with IoT sensors
- [ ] Real-time notifications

---

**Built with ❤️ for intelligent machine monitoring**