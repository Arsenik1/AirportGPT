# AirportGPT

AirportGPT is an AI-powered virtual assistant for airport-related information and services in Istanbul Airport. It uses FastAPI for the backend with LangChain for AI capabilities and Next.js for the frontend.

## Demo

![AirportGPT Demo](AirportGPT.gif)

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
- [Ollama](https://ollama.com/) - Running locally with the Qwen2.5 7B model

### Frontend
- Node.js 18+
- Next.js
- React

## Installation

### Clone the repository
```bash
git clone https://github.com/Arsenik1/AirportGPT.git
cd AirportGPT
```

### Ollama Setup
1. Install [Ollama](https://ollama.com/) for your operating system
2. Pull the Qwen2.5 7B model:
```bash
ollama pull qwen2.5:latest
```
3. Ensure Ollama is running in the background before starting the backend server

> **Important:** The agent is specifically optimized for the Qwen2.5 7B model. Other models (including different parameter counts of Qwen2.5) may cause the agent to fail or perform unpredictably. The 7B model provides an optimal balance between performance and resource efficiency, allowing it to run on a single RTX 4060 GPU or equivalent.

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
1. Ensure Ollama is running with the qwen2.5 model loaded
2. Run the backend server:
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

## Project Architecture & Privacy Considerations

AirportGPT is designed with privacy and data security as core principles, which is particularly important for airport operations. The application uses a local LLM (Large Language Model) deployment through Ollama instead of cloud-based alternatives for several important reasons:

### On-premises Data Processing
- All user queries and sensitive airport information remain within the local infrastructure
- No data is sent to external cloud providers, ensuring complete data sovereignty
- Complies with strict privacy requirements for airport operations

### Resource Efficiency
- The Qwen2.5 7B model is specifically selected to balance performance and hardware requirements
- Can run effectively on consumer-grade hardware (single RTX 4060 GPU)
- Lower latency compared to API calls to remote services

### Customization
- The local model can be fine-tuned for airport-specific terminology and use cases
- Custom tools have been implemented to handle flight information and airport services queries

### Offline Capability
- The system can function without an internet connection, ensuring reliability during network issues
- Critical airport information remains accessible even during connectivity problems

## Environment Variables

Create a `.env` file in the appropriate directories if needed for API keys or other configurations.

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
