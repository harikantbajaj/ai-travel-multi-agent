# 🚀 AI Travel Agent & Expense Planner - LangGraph Multi-Agent System

## Overview

A state-of-the-art multi-agent travel planning system built with **LangGraph**, **Google Gemini Flash-2.0**, and **DuckDuckGo Search**. The system offers three different planning approaches, from traditional single-agent to cutting-edge multi-agent collaboration using modern industry frameworks.

## 🤖 Planning Options

Choose from three different planning experiences:

### 1. 🔧 Single-Agent Planning (Classic)
- Traditional single AI agent approach
- Direct planning methodology
- Proven reliability and efficiency

### 2. 🚀 Legacy Multi-Agent (Custom Framework)
- 6 specialized AI agents working together
- Custom multi-agent framework
- Enhanced recommendations through collaboration

### 3. 🌟 LangGraph Multi-Agent (Advanced) ⭐ **RECOMMENDED**
- **Google Gemini Flash-2.0** powered agents
- **DuckDuckGo real-time search** integration
- **LangGraph workflow** orchestration
- State-of-the-art multi-agent collaboration

## 🏗️ LangGraph System Architecture

### Framework Components
- **LangGraph StateGraph**: Workflow orchestration and state management
- **Google Gemini Flash-2.0**: Advanced AI reasoning and natural language processing
- **DuckDuckGo Search**: Real-time information retrieval (no API key needed)
- **Pydantic**: Type safety and data validation
- **Custom Agent Protocols**: Specialized communication between agents

### 🤖 AI Agent Network

| Agent | Role | Capabilities |
|-------|------|-------------|
| **Coordinator** | Workflow orchestration & decision synthesis | Master planning, task delegation, consensus building |
| **Travel Advisor** | Destination expertise with live search | Attraction research, destination insights, cultural guidance |
| **Weather Analyst** | Weather intelligence with current data | Weather forecasting, climate analysis, packing advice |
| **Budget Optimizer** | Cost analysis with real-time pricing | Budget planning, cost optimization, savings strategies |
| **Local Expert** | Insider knowledge with local info | Local tips, hidden gems, cultural etiquette |
| **Itinerary Planner** | Schedule optimization & logistics | Day-by-day planning, route optimization, timing |

## 🎯 Key Features

### Advanced Capabilities
- ✅ **Real-time Search Integration**: Live data from DuckDuckGo
- ✅ **State Management**: Persistent conversation state across agents
- ✅ **Tool-Augmented Agents**: Each agent has specialized search tools
- ✅ **Collaborative Decision Making**: Agents work together to create optimal plans
- ✅ **Workflow Orchestration**: LangGraph manages complex agent interactions
- ✅ **Error Handling**: Robust error recovery and fallback mechanisms

### Search Tools
1. **Destination Information**: General destination research
2. **Weather Intelligence**: Current and forecasted weather data
3. **Attraction Discovery**: Top attractions and activities
4. **Hotel Research**: Accommodation options and pricing
5. **Restaurant Finder**: Dining recommendations and reviews
6. **Local Insights**: Cultural tips and insider knowledge
7. **Budget Analysis**: Cost estimates and budget planning

## 🚀 Quick Start

### Prerequisites
```bash
# Python 3.8+
pip install -r requirements.txt
```

### Setup
1. **Get Gemini API Key**: Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Configure Environment**: Add your API key to `.env` file
   ```bash
   GEMINI_API_KEY=your_actual_api_key_here
   ```
3. **Verify Installation**: Run the test script
   ```bash
   python test_langgraph_system.py
   ```

### Running the System

#### Option 1: Main Menu (All 3 Systems)
```bash
python main.py
# Select option 3 for LangGraph (Recommended)
# Select option 2 for Legacy Multi-Agent
# Select option 1 for Single-Agent
```

#### Option 2: Direct LangGraph System
```bash
python langgraph_main.py
```

#### Option 3: Test Without API Key
```bash
python test_langgraph_system.py
```

## 📊 Usage Examples

### Demo Mode
```bash
python langgraph_main.py
# Select option 1 for Tokyo demonstration
```

### Interactive Planning
```bash
python langgraph_main.py
# Select option 2 for custom trip planning
```

### System Validation
```bash
python test_langgraph_system.py
# Tests all components without API calls
```

## 🛠️ Configuration

### Environment Variables
```bash
# Required for LangGraph System
GEMINI_API_KEY=your_gemini_api_key

# Optional (for legacy systems)
OPENWEATHER_API_KEY=your_weather_api_key
GOOGLE_PLACES_API_KEY=your_places_api_key
EXCHANGERATE_API_KEY=your_exchange_rate_api_key
```

### Model Configuration
```python
class LangGraphConfig:
    GEMINI_MODEL = "gemini-2.0-flash"
    TEMPERATURE = 0.7
    MAX_TOKENS = 4000
    TOP_P = 0.9
```

### API Configuration (Optional)
For enhanced legacy functionality, obtain free API keys:

1. **Google Gemini API** (Required for LangGraph system)
   - Get key: https://makersuite.google.com/app/apikey
   - Add to .env: `GEMINI_API_KEY=your_key`

2. **OpenWeather API** (Legacy weather data)
   - Get key: https://openweathermap.org/api
   - Add to .env: `OPENWEATHER_API_KEY=your_key`

3. **Google Places API** (Legacy attractions/hotels)
   - Get key: Google Cloud Console
   - Add to .env: `GOOGLE_PLACES_API_KEY=your_key`

4. **Exchange Rate API** (Legacy currency conversion)
   - Get key: https://exchangerate-api.com/
   - Add to .env: `EXCHANGERATE_API_KEY=your_key`

**Note**: The LangGraph system uses DuckDuckGo search (no API key needed) and works independently of legacy APIs.

## 🏗️ Architecture

### Project Structure
```
📁 ai_travel_agent/
├── main.py                    # Multi-system entry point
├── langgraph_main.py          # LangGraph system entry
├── test_langgraph_system.py   # Comprehensive testing
├── agents/                    # Agent implementations
│   ├── langgraph_agents.py   # LangGraph agent system
│   ├── multi_agent_orchestrator.py # Legacy multi-agent
│   └── travel_agents.py      # Individual agent classes
├── config/                   # Configuration management
│   ├── langgraph_config.py   # LangGraph configuration
│   ├── api_config.py         # Legacy API settings
│   └── app_config.py         # Application settings
├── tools/                    # LangGraph tools
│   └── travel_tools.py       # 7 DuckDuckGo search tools
├── data/                     # Data models
│   └── models.py             # Data classes
├── modules/                  # Legacy business logic
│   ├── user_input.py         # Input handling & validation
│   ├── weather_service.py    # Weather data integration
│   ├── attraction_finder.py  # Attraction discovery
│   ├── hotel_estimator.py    # Accommodation estimation
│   ├── currency_converter.py # Currency conversion
│   ├── expense_calculator.py # Cost calculations
│   ├── itinerary_planner.py  # Day-by-day planning
│   └── trip_summary.py       # Report generation
└── utils/                    # Utility functions
    └── helpers.py            # Common helper functions
```

### System Comparison

| Feature | Single-Agent | Legacy Multi-Agent | LangGraph System |
|---------|-------------|-------------------|------------------|
| **Framework** | Custom | Custom | LangGraph + LangChain |
| **LLM** | Mock/Static | Mock/Static | Google Gemini Flash-2.0 |
| **Search** | Static Data | Static Data | DuckDuckGo Real-time |
| **State Management** | None | Basic | Advanced (StateGraph) |
| **Tool Integration** | Limited | Limited | Full Tool Ecosystem |
| **Collaboration** | None | Basic | Advanced Workflows |
| **Scalability** | Low | Medium | High |
| **Maintainability** | Low | Medium | High |

## 📦 Dependencies

### Required Packages
```bash
pip install -r requirements.txt
```

## 🧪 Testing

### Run Tests
```bash
# LangGraph system validation (no API key needed)
python test_langgraph_system.py

# Legacy system tests
pytest tests/
```

### System Validation
The `test_langgraph_system.py` script validates:
- All LangGraph components
- Tool integrations
- Configuration management
- Import compatibility
- System readiness

## 🚨 Troubleshooting

### Common Issues

1. **API Quota Exceeded**
   ```
   Error: 429 You exceeded your current quota
   Solution: Wait for quota reset or upgrade API plan
   ```

2. **Import Errors**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configuration Issues**
   ```bash
   python test_langgraph_system.py
   ```

4. **Missing API Key**
   ```
   Error: GEMINI_API_KEY not found
   Solution: Add your API key to .env file
   ```

### Debug Mode
```bash
export DEBUG=true
python langgraph_main.py
```

## Contributing

### Code Structure
- Follow object-oriented design principles
- Maintain modular architecture
- Include comprehensive error handling
- Add unit tests for new features

### Development Setup
```bash
pip install -r requirements.txt
python validate.py
pytest tests/
```

## License

This project is for educational purposes as part of the AI Agents assignment.

## Support

For issues or questions:
1. Check the validation script: `python validate.py`
2. Review error messages and logs
3. Verify API key configuration (if using external APIs)

---

**Built with ❤️ for intelligent travel planning**
