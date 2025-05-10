# AirportGPT

AirportGPT is an AI-powered virtual assistant for airport-related information and services in Istanbul Airport. It uses FastAPI for the backend with LangChain for AI capabilities and Next.js for the frontend.

## Project Structure

```
AirportGPT/
├── agent/                  # Python backend
│   ├── AgentBackend.py     # FastAPI server
│   ├── iGA_globals.py      # Global variables and state
│   ├── iGA_tools.py        # Custom LangChain tools
│   └── ...
├── airportgpt_front/       # Next.js frontend
│   ├── public/
│   ├── src/
│   └── ...
└── README.md
```

## Requirements

### Backend
- Python 3.9+
- FastAPI
- LangChain
- uvicorn

### Frontend
- Node.js 18+
- Next.js
- React

## Installation

### Clone the repository
```bash
git clone https://github.com/yourusername/AirportGPT.git
cd AirportGPT
```

### Backend Setup
```bash
cd agent
pip install -r requirements.txt
```

### Frontend Setup
```bash
cd airportgpt_front
npm install
```

## Running the Application

### Start the Backend Server
```bash
cd agent
python AgentBackend.py
```
The backend API will start at http://localhost:8002

### Start the Frontend Development Server
```bash
cd airportgpt_front
npm run dev
```
The frontend will be accessible at http://localhost:3000

## API Documentation

Once the backend server is running, you can access the API documentation at http://localhost:8002/docs

## Environment Variables

Create a `.env` file in the appropriate directories if needed for API keys or other configurations.

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request

## License

[Your chosen license]
