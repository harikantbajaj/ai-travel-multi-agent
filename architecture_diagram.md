# LangGraph Multi-Agent AI Travel Planning System
## ASCII Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        🚀 LANGGRAPH AI TRAVEL AGENT SYSTEM                              │
│                     Powered by Google Gemini Flash-2.0 & DuckDuckGo                     │
└─────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                    🎯 ENTRY POINTS                                      │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│  main.py                    langgraph_main.py              test_langgraph_system.py     │
│  ┌─────────────┐           ┌─────────────────┐            ┌─────────────────────┐       │
│  │ User Choice │──────────▶│ LangGraph Entry │            │ Testing & Validation│       │
│  │ 1,2,3 Mode  │           │ Point (Option 3)│            │ No API Keys Required│       │
│  │ Selection   │           │                 │            │                     │       │
│  └─────────────┘           └─────────────────┘            └─────────────────────┘       │
└─────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              🧠 CORE LANGGRAPH ARCHITECTURE                             │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌──────────────────────────────────────────────────────────────────────────────────┐   │
│  │                           📊 TRAVEL PLAN STATE                                   │   │
│  │  ┌─────────────────────────────────────────────────────────────────────────────┐ │   │
│  │  │ • messages: List[HumanMessage|AIMessage|SystemMessage]                      │ │   │
│  │  │ • destination: str                                                          │ │   │
│  │  │ • duration: int                                                             │ │   │
│  │  │ • budget_range: str                                                         │ │   │
│  │  │ • interests: List[str]                                                      │ │   │
│  │  │ • group_size: int                                                           │ │   │
│  │  │ • travel_dates: str                                                         │ │   │
│  │  │ • current_agent: str                                                        │ │   │
│  │  │ • agent_outputs: Dict[str, Any]                                             │ │   │
│  │  │ • final_plan: Dict[str, Any]                                                │ │   │
│  │  │ • iteration_count: int                                                      │ │   │
│  │  └─────────────────────────────────────────────────────────────────────────────┘ │   │
│  └──────────────────────────────────────────────────────────────────────────────────┘   │
│                                           │                                             │
│                                           ▼                                             │
│  ┌──────────────────────────────────────────────────────────────────────────────────┐   │
│  │                          🎯 COORDINATOR AGENT                                    │   │
│  │                         (Entry Point & Orchestrator)                             │   │
│  │  ┌─────────────────────────────────────────────────────────────────────────────┐ │   │
│  │  │ • Analyzes travel requests                                                  │ │   │
│  │  │ • Routes to specialized agents                                              │ │   │
│  │  │ • Manages workflow state                                                    │ │   │
│  │  │ • Synthesizes final recommendations                                         │ │   │
│  │  │ • Controls iteration and completion                                         │ │   │
│  │  └─────────────────────────────────────────────────────────────────────────────┘ │   │
│  └──────────────────────────────────────────────────────────────────────────────────┘   │
│                                           │                                             │
│                         ┌─────────────────┴─────────────────┐                           │
│                         ▼                                   ▼                           │
│  ┌──────────────────────────────────────┐    ┌──────────────────────────────────────┐   │
│  │        📈 AGENT ROUTING              │    │         🔧 TOOL EXECUTION            │   │
│  │    (Conditional Edges)               │    │                                      │   │
│  │                                      │    │  ┌─────────────────────────────────┐ │   │
│  │ Coordinator decides based on:        │    │  │  7 DuckDuckGo Search Tools      │ │   │
│  │ • Current state                      │    │  │  • search_destination_info      │ │   │
│  │ • Agent completion status            │    │  │  • search_weather_info          │ │   │
│  │ • Information gaps                   │    │  │  • search_attractions           │ │   │
│  │ • Tool execution needs               │    │  │  • search_hotels                │ │   │
│  │                                      │    │  │  • search_restaurants           │ │   │
│  │ Routes to:                           │    │  │  • search_local_tips            │ │   │
│  │ ✈️ Travel Advisor                    │    │  │  • search_budget_info           │ │   │
│  │ 🌤️ Weather Analyst                   │    │  └─────────────────────────────────┘ │   │
│  │ 💰 Budget Optimizer                  │    │                                      │   │
│  │ 🏠 Local Expert                      │    │  Results fed back to Coordinator     │   │
│  │ 📅 Itinerary Planner                 │    │                                      │   │
│  │ 🔧 Tools                             │    │                                      │   │
│  │ 🏁 END                               │    │                                      │   │
│  └──────────────────────────────────────┘    └──────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              🤖 SPECIALIZED AGENT NETWORK                               │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│ ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐      │
│ │   ✈️ TRAVEL     │  │  🌤️ WEATHER     │  │  💰 BUDGET      │  │  🏠 LOCAL       │      │
│ │   ADVISOR       │  │   ANALYST       │  │   OPTIMIZER     │  │   EXPERT        │      │
│ │                 │  │                 │  │                 │  │                 │      │
│ │ • Destination   │  │ • Weather       │  │ • Cost analysis │  │ • Insider tips  │      │
│ │   expertise     │  │   intelligence  │  │ • Budget        │  │ • Local culture │      │
│ │ • Attractions   │  │ • Climate data  │  │   optimization  │  │ • Hidden gems   │      │
│ │ • Cultural      │  │ • Seasonal      │  │ • Price         │  │ • Safety info   │      │
│ │   insights      │  │   planning      │  │   comparison    │  │ • Transportation│      │
│ │ • Best          │  │ • Activity      │  │ • Value         │  │ • Local events  │      │
│ │   practices     │  │   recommendations│  │   recommendations│  │ • Etiquette    │     │
│ └─────────────────┘  └─────────────────┘  └─────────────────┘  └─────────────────┘      │
│         │                     │                     │                     │              │
│         └─────────────────────┼─────────────────────┼─────────────────────┘              │
│                               │                     │                                    │
│                    ┌─────────────────┐              │                                    │
│                    │  📅 ITINERARY   │              │                                    │
│                    │   PLANNER       │              │                                    │
│                    │                 │              │                                    │
│                    │ • Schedule      │              │                                    │
│                    │   optimization  │              │                                    │
│                    │ • Logistics     │              │                                    │
│                    │ • Time          │              │                                    │
│                    │   management    │              │                                    │
│                    │ • Activity      │              │                                    │
│                    │   sequencing    │              │                                    │
│                    │ • Route         │              │                                    │
│                    │   planning      │              │                                    │
│                    └─────────────────┘              │                                    │
│                               │                     │                                    │
│                               └─────────────────────┘                                    │
│                                                                                           │
│           Each agent can:                                                                 │
│           • Request tool execution                                                        │
│           • Return to coordinator                                                         │
│           • Complete and end workflow                                                     │
│                                                                                           │
└─────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              🛠️ TECHNOLOGY STACK INTEGRATION                            │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐          │
│  │   🧠 GOOGLE GEMINI   │    │  🔍 DUCKDUCKGO API  │    │  🕸️ LANGGRAPH       │         │
│  │   FLASH-2.0          │    │                     │    │   FRAMEWORK         │         │
│  │                     │    │                     │    │                     │          │
│  │ • ChatGoogleGenAI   │    │ • Real-time search  │    │ • StateGraph        │          │
│  │ • Temperature: 0.7  │    │ • 7 specialized     │    │ • Conditional edges │          │
│  │ • Max tokens: 4000  │    │   search functions  │    │ • Message handling  │          │
│  │ • Top-p: 0.9        │    │ • Region: wt-wt     │    │ • State management  │          │
│  │ • Advanced reasoning│    │ • Safe search       │    │ • Workflow control  │          │
│  │ • Multi-turn conv   │    │ • Error handling    │    │ • Agent orchestration│         │
│  └─────────────────────┘    └─────────────────────┘    └─────────────────────┘          │
│           │                            │                            │                    │
│           └────────────────────────────┼────────────────────────────┘                    │
│                                        │                                                 │
│  ┌─────────────────────────────────────┴─────────────────────────────────────┐          │
│  │                        📦 LANGCHAIN CORE                                   │          │
│  │                                                                             │          │
│  │  • Tool decorators (@tool)                                                 │          │
│  │  • Message types (HumanMessage, AIMessage, SystemMessage)                 │          │
│  │  • Tool execution and validation                                           │          │
│  │  • LLM integration and response handling                                   │          │
│  │  • Error handling and retry mechanisms                                     │          │
│  └─────────────────────────────────────────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                📁 SYSTEM CONFIGURATION                                    │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                           │
│  config/langgraph_config.py                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐ │
│  │ • GEMINI_API_KEY environment variable management                                     │ │
│  │ • Model configuration (gemini-2.0-flash-exp)                                        │ │
│  │ • Temperature, tokens, and AI parameters                                             │ │
│  │ • DuckDuckGo search settings                                                         │ │
│  │ • Timeout and retry configurations                                                   │ │
│  │ • Region and safety settings                                                         │ │
│  └─────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                           │
│  tools/__init__.py                                                                       │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐ │
│  │ • Tool registry and exports                                                          │ │
│  │ • Tool availability validation                                                       │ │
│  │ • Import and initialization handling                                                 │ │
│  └─────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                           │
└─────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                               🔄 WORKFLOW EXECUTION PATTERN                               │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                           │
│    USER INPUT                                                                             │
│         │                                                                                 │
│         ▼                                                                                 │
│    ┌─────────────┐                                                                        │
│    │ Initialize  │                                                                        │
│    │ State with  │                                                                        │
│    │ Travel Req  │                                                                        │
│    └─────────────┘                                                                        │
│         │                                                                                 │
│         ▼                                                                                 │
│    ┌─────────────┐         ┌──────────────┐         ┌─────────────┐                     │
│    │ COORDINATOR │──────▶  │ ROUTING      │──────▶  │ SPECIALIZED │                     │
│    │ ANALYSIS    │         │ DECISION     │         │ AGENT       │                     │
│    └─────────────┘         └──────────────┘         └─────────────┘                     │
│         ▲                         │                         │                           │
│         │                         ▼                         ▼                           │
│    ┌─────────────┐         ┌──────────────┐         ┌─────────────┐                     │
│    │ SYNTHESIZE  │◀─────── │ TOOL         │◀────────│ TOOL        │                     │
│    │ RESULTS     │         │ EXECUTION    │         │ REQUEST     │                     │
│    └─────────────┘         └──────────────┘         └─────────────┘                     │
│         │                                                                                 │
│         ▼                                                                                 │
│    ┌─────────────┐                                                                        │
│    │ FINAL PLAN  │                                                                        │
│    │ DELIVERY    │                                                                        │
│    └─────────────┘                                                                        │
│                                                                                           │
│  Loop continues until:                                                                    │
│  • All agents have provided input                                                         │
│  • Information gaps are filled                                                            │
│  • Coordinator determines completion                                                      │
│  • Maximum iterations reached                                                             │
│                                                                                           │
└─────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                               🎯 KEY ARCHITECTURAL FEATURES                               │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                           │
│  ✅ STATE-DRIVEN ARCHITECTURE                                                            │
│     • Persistent state across all agent interactions                                     │
│     • Type-safe state management with TypedDict                                          │
│     • Message history and context preservation                                           │
│                                                                                           │
│  ✅ CONDITIONAL WORKFLOW ROUTING                                                         │
│     • Dynamic agent selection based on current needs                                     │
│     • Intelligent tool execution decisions                                               │
│     • Completion detection and workflow termination                                      │
│                                                                                           │
│  ✅ REAL-TIME DATA INTEGRATION                                                           │
│     • Live search results from DuckDuckGo                                                │
│     • Current weather and pricing information                                            │
│     • Up-to-date attraction and event data                                               │
│                                                                                           │
│  ✅ ADVANCED LLM CAPABILITIES                                                            │
│     • Google Gemini Flash-2.0 for all AI reasoning                                       │
│     • Multi-turn conversation support                                                    │
│     • Context-aware responses with memory                                                │
│                                                                                           │
│  ✅ SCALABLE AGENT ARCHITECTURE                                                          │
│     • Modular agent design for easy extension                                            │
│     • Specialized expertise domains                                                      │
│     • Coordinated multi-agent collaboration                                              │
│                                                                                           │
│  ✅ ROBUST ERROR HANDLING                                                                │
│     • Tool execution failure recovery                                                    │
│     • API timeout and retry mechanisms                                                   │
│     • Graceful degradation to offline knowledge                                          │
│                                                                                           │
└─────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                  📊 SYSTEM METRICS                                        │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                           │
│  🎯 AGENTS: 6 specialized agents + 1 coordinator                                         │
│  🔧 TOOLS: 7 DuckDuckGo search tools with real-time data                                 │
│  🧠 AI MODEL: Google Gemini Flash-2.0 (latest generation)                               │
│  📊 STATE FIELDS: 10 typed state management fields                                       │
│  🔀 WORKFLOW EDGES: Conditional routing with 7 decision points                           │
│  🌐 SEARCH CAPABILITY: Global real-time information retrieval                            │
│  💾 MEMORY: Full conversation history and context preservation                           │
│  🔄 EXECUTION: Asynchronous multi-agent collaboration                                    │
│                                                                                           │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

## System Overview

The LangGraph Multi-Agent AI Travel Planning System represents a state-of-the-art implementation of collaborative AI agents working together to create comprehensive travel plans. Built on the LangGraph framework with Google Gemini Flash-2.0 and DuckDuckGo search integration, this system provides real-time, intelligent travel planning through coordinated multi-agent workflows.

### Core Components

1. **LangGraph StateGraph**: Manages workflow orchestration and state persistence
2. **Coordinator Agent**: Central orchestrator that routes requests and synthesizes results
3. **Specialized Agents**: 5 domain-expert agents with specific travel planning expertise
4. **Real-time Tools**: 7 DuckDuckGo search tools providing current information
5. **Google Gemini Integration**: Advanced AI reasoning with the latest Gemini model
6. **State Management**: Comprehensive state tracking across all agent interactions

### Workflow Architecture

The system follows a hub-and-spoke architecture with the Coordinator Agent at the center, intelligently routing requests to specialized agents based on current state and information needs. Each agent can request tool execution for real-time data or return results to the coordinator for synthesis.

### Key Innovations

- **Dynamic Routing**: Conditional edges that adapt workflow based on current planning state
- **Real-time Integration**: Live data from DuckDuckGo search across multiple travel domains
- **State Persistence**: Full conversation and planning context maintained throughout workflow
- **Multi-modal Planning**: Combines AI reasoning with current market data and conditions
- **Scalable Design**: Modular architecture supporting easy addition of new agents and tools

This architecture ensures comprehensive, current, and personalized travel planning through the coordinated intelligence of multiple specialized AI agents.
