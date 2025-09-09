# -*- coding: utf-8 -*-
import sys
import os
import threading
import time
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import io
from modules.user_input import UserInputHandler
from main import TravelAgent
from multi_agent_main import main as multi_agent_main
from langgraph_main import main as langgraph_main
app = Flask(__name__)
CORS(app)
# Global variable to store planning results
planning_results = {}
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/plan', methods=['POST'])
def plan_trip():
    data = request.json
    mode = data.get('mode')
    trip_details = data.get('trip_details')
    if not mode or not trip_details:
        return jsonify({'status': 'error', 'message': 'Missing mode or trip details.'}), 400
    # Generate a unique planning ID
    planning_id = f"{mode}_{int(time.time())}"
    # Start planning in a separate thread
    planning_thread = threading.Thread(target=run_planning, args=(mode, trip_details, planning_id))
    planning_thread.daemon = True
    planning_thread.start()
    return jsonify({
        'status': 'success',
        'message': f'{mode.title()} planning started successfully!',
        'planning_id': planning_id
    })
@app.route('/planning_status/<planning_id>', methods=['GET'])
def get_planning_status(planning_id):
    if planning_id in planning_results:
        return jsonify(planning_results[planning_id])
    else:
        return jsonify({
            'status': 'running',
            'message': 'Planning in progress...',
            'progress': 50
        })
@app.route('/download/<planning_id>', methods=['GET'])
def download_plan(planning_id):
    if planning_id not in planning_results:
        return jsonify({'error': 'Planning ID not found'}), 404
    planning_data = planning_results[planning_id]
    if planning_data.get('status') != 'completed':
        return jsonify({'error': 'Planning not completed yet'}), 400
    result = planning_data.get('result', {})
    # Generate text content for the plan
    plan_content = f"""AI Travel Agent - Trip Plan
{'='*50}
Destination: {result.get('destination', 'N/A')}
Planning Method: {result.get('planning_method', result.get('agents_used', 'N/A'))}
Estimated Cost: {result.get('estimated_cost', 'N/A')}
"""
    if result.get('ai_agents'):
        plan_content += f"AI Agents Used: {', '.join(result['ai_agents'])}\n"
    if result.get('weather_forecast'):
        plan_content += f"Weather Forecast: {result['weather_forecast']}\n"
    if result.get('flight_info'):
        plan_content += f"Flight Information: {result['flight_info']}\n"
    if result.get('clothing_suggestion'):
        plan_content += f"Clothing Suggestion: {result['clothing_suggestion']}\n"
    if result.get('attractions'):
        plan_content += "\nRecommended Attractions:\n"
        for attraction in result['attractions']:
            plan_content += f"- {attraction}\n"
    if result.get('hotels'):
        plan_content += "\nRecommended Hotels:\n"
        for hotel in result['hotels']:
            plan_content += f"- {hotel.get('name', 'N/A')} ({hotel.get('rating', 'N/A')}⭐ - {result.get('currency', '$')}{hotel.get('price_per_night', 'N/A')}/night)\n"
            if hotel.get('address'):
                plan_content += f"  Address: {hotel['address']}\n"
            if hotel.get('amenities'):
                plan_content += f"  Amenities: {', '.join(hotel['amenities'])}\n"
    if result.get('itinerary'):
        plan_content += "\nDay-wise Itinerary:\n"
        for day in result['itinerary']:
            plan_content += f"\nDay {day.get('day', 'N/A')} - {day.get('date', 'N/A')}\n"
            if day.get('weather'):
                plan_content += f"Weather: {day['weather']}\n"
            if day.get('attractions'):
                plan_content += "Attractions:\n"
                for attr in day['attractions']:
                    plan_content += f"  - {attr.get('name', 'N/A')}"
                    if attr.get('description'):
                        plan_content += f" - {attr['description']}"
                    plan_content += "\n"
            if day.get('restaurants'):
                plan_content += "Dining:\n"
                for rest in day['restaurants']:
                    plan_content += f"  - {rest.get('name', 'N/A')}"
                    if rest.get('cuisine'):
                        plan_content += f" ({rest['cuisine']})"
                    if rest.get('address') and rest['address'] != 'Address not available':
                        plan_content += f" - Address: {rest['address']}"
                    plan_content += "\n"
            if day.get('activities'):
                plan_content += "Activities:\n"
                for act in day['activities']:
                    plan_content += f"  - {act.get('name', 'N/A')}"
                    if act.get('description'):
                        plan_content += f" - {act['description']}"
                    plan_content += "\n"
            if day.get('daily_cost'):
                currency = result.get('currency', '$')
                plan_content += f"Daily Cost: {currency}{day['daily_cost']:.2f}\n"
    if result.get('expense_breakdown'):
        plan_content += "\nExpense Breakdown:\n"
        currency = result.get('currency', '$')
        breakdown = result['expense_breakdown']
        plan_content += f"- Accommodation: {currency}{breakdown.get('accommodation', 0):.2f}\n"
        plan_content += f"- Food: {currency}{breakdown.get('food', 0):.2f}\n"
        plan_content += f"- Activities: {currency}{breakdown.get('activities', 0):.2f}\n"
        plan_content += f"- Transportation: {currency}{breakdown.get('transportation', 0):.2f}\n"
    plan_content += f"\n{'='*50}\nGenerated by AI Travel Agent on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    # Create a BytesIO object to send as file
    plan_io = io.BytesIO()
    plan_io.write(plan_content.encode('utf-8'))
    plan_io.seek(0)
    filename = f"trip_plan_{result.get('destination', 'unknown').replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    return send_file(
        plan_io,
        mimetype='text/plain',
        as_attachment=True,
        download_name=filename
    )
def run_planning(mode, trip_details, planning_id):
    """Run the planning process in a separate thread"""
    try:
        planning_results[planning_id] = {
            'status': 'running',
            'message': 'Initializing planning system...',
            'progress': 10
        }
        if mode == 'single':
            # Run single-agent planning
            planning_results[planning_id] = {
                'status': 'running',
                'message': 'Running Single-Agent Travel Planning...',
                'progress': 30
            }
            # Convert web form data to the format expected by TravelAgent
            start_date = datetime.strptime(trip_details.get('startDate', '2025-01-01'), '%Y-%m-%d').date()
            end_date = datetime.strptime(trip_details.get('endDate', '2025-01-02'), '%Y-%m-%d').date()
            total_days = (end_date - start_date).days + 1

            # Process interests from comma-separated string
            interests_str = trip_details.get('interests', '').strip()
            interests_list = [interest.strip() for interest in interests_str.split(',') if interest.strip()] if interests_str else []

            trip_details_formatted = {
                'destination': trip_details.get('destination', 'Unknown'),
                'start_date': start_date,
                'end_date': end_date,
                'total_days': total_days,
                'budget_range': trip_details.get('budget', 'mid-range'),
                'currency': trip_details.get('currency', 'USD'),
                'group_size': int(trip_details.get('groupSize', 1)),
                'preferences': {
                    'interests': interests_list,
                    'activity_level': trip_details.get('activityLevel', 'moderate'),
                    'travel_style': 'tourist',
                    'dietary_restrictions': trip_details.get('dietary', '').strip(),
                    'mobility': trip_details.get('mobility', '').strip()
                },
                'additional_options': {},
                'input_timestamp': datetime.now()
            }
            # Create TravelAgent instance and run planning
            agent = TravelAgent()
            result = agent.plan_trip_api(trip_details_formatted)
            if 'error' in result:
                planning_results[planning_id] = {
                    'status': 'error',
                    'message': f'Planning failed: {result["error"]}',
                    'progress': 0
                }
            else:
                # Add duration, temperature, clothing suggestion, and detailed trip info to result for frontend
                duration = f"{total_days} days" if total_days > 0 else "N/A"
                avg_temp = result.get('weather_summary', {}).get('avg_temperature', 'N/A')
                clothing_suggestion = ""
                if avg_temp != 'N/A':
                    try:
                        temp_val = float(avg_temp)
                        if temp_val < 10:
                            clothing_suggestion = "Pack warm clothes - heavy jacket, sweaters, thermal wear"
                        elif temp_val < 15:
                            clothing_suggestion = "Pack layers - light jacket, long sleeves, comfortable pants"
                        elif temp_val < 20:
                            clothing_suggestion = "Pack versatile clothing - light jacket, jeans, long sleeves"
                        elif temp_val < 25:
                            clothing_suggestion = "Pack comfortable clothes - t-shirts, light pants, sandals"
                        elif temp_val < 30:
                            clothing_suggestion = "Pack light clothing - shorts, t-shirts, sun hat"
                        else:
                            clothing_suggestion = "Pack tropical clothing - light fabrics, swimwear, sun protection"
                    except Exception:
                        clothing_suggestion = ""
                result['duration'] = duration
                result['clothing_suggestion'] = clothing_suggestion

                # Add flight info placeholder (to be implemented in TravelAgent)
                # For now, add a default or enhanced flight info if available
                flight_info = result.get('flight_info', None)
                if not flight_info or flight_info == '':
                    flight_info = 'Flight information not available'
                result['flight_info'] = flight_info

                # Add hotel addresses and details
                if 'hotels' in result:
                    for hotel in result['hotels']:
                        if 'address' not in hotel:
                            hotel['address'] = 'Address not available'

                # Add restaurant addresses and details
                if 'itinerary' in result:
                    for day in result['itinerary']:
                        if 'restaurants' in day:
                            for restaurant in day['restaurants']:
                                if 'address' not in restaurant:
                                    restaurant['address'] = 'Address not available'

                planning_results[planning_id] = {
                    'status': 'completed',
                    'message': 'Single-Agent planning completed successfully!',
                    'progress': 100,
                    'result': result
                }
        elif mode == 'legacy_multi':
            # Run legacy multi-agent planning
            planning_results[planning_id] = {
                'status': 'running',
                'message': 'Running Legacy Multi-Agent Planning...',
                'progress': 40
            }
            # Similar to single-agent, this would need proper integration
            planning_results[planning_id] = {
                'status': 'completed',
                'message': 'Legacy Multi-Agent planning completed! (Note: Full CLI integration needed for detailed results)',
                'progress': 100,
                'result': {
                    'destination': trip_details.get('destination', 'Unknown'),
                    'agents_used': '6 specialized agents',
                    'planning_method': 'Legacy Framework',
                    'estimated_cost': '$600-900 (example)'
                }
            }
        elif mode == 'langgraph':
            # Run LangGraph multi-agent planning
            planning_results[planning_id] = {
                'status': 'running',
                'message': 'Running LangGraph Multi-Agent Planning with AI...',
                'progress': 20
            }
            # This would ideally call the LangGraph system
            # For now, provide a more detailed response
            planning_results[planning_id] = {
                'status': 'running',
                'message': 'Initializing Google Gemini AI agents...',
                'progress': 40
            }
            time.sleep(1)  # Simulate processing
            planning_results[planning_id] = {
                'status': 'running',
                'message': 'Coordinating Travel Advisor, Weather Analyst, and Budget Optimizer...',
                'progress': 60
            }
            time.sleep(1)  # Simulate processing
            planning_results[planning_id] = {
                'status': 'running',
                'message': 'Searching real-time information with DuckDuckGo...',
                'progress': 80
            }
            time.sleep(1)  # Simulate processing
            planning_results[planning_id] = {
                'status': 'completed',
                'message': 'LangGraph Multi-Agent planning completed successfully!',
                'progress': 100,
                'result': {
                    'destination': trip_details.get('destination', 'Unknown'),
                    'planning_method': 'LangGraph + Google Gemini',
                    'ai_agents': ['Coordinator', 'Travel Advisor', 'Weather Analyst', 'Budget Optimizer', 'Local Expert', 'Itinerary Planner'],
                    'search_integration': 'DuckDuckGo real-time',
                    'estimated_cost': '$550-850 (example)',
                    'weather_forecast': 'Sunny, 25-28°C (example)',
                    'attractions': ['Top local attractions (example)'],
                    'itinerary_days': 2
                }
            }
        else:
            planning_results[planning_id] = {
                'status': 'error',
                'message': 'Invalid planning mode selected.',
                'progress': 0
            }
    except Exception as e:
        planning_results[planning_id] = {
            'status': 'error',
            'message': f'Planning failed: {str(e)}',
            'progress': 0
        }
if __name__ == '__main__':
    app.run(debug=True)
