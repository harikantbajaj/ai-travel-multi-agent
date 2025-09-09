#!/usr/bin/env python3
"""
AI Travel Agent & Expense Planner
Main application entry point - Now with Multi-Agent Support!
"""
import sys
import os
from datetime import datetime
# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.user_input import UserInputHandler
from modules.weather_service import WeatherService
from modules.attraction_finder import AttractionFinder
from modules.hotel_estimator import HotelEstimator
from modules.currency_converter import CurrencyConverter
from modules.expense_calculator import ExpenseCalculator
from modules.itinerary_planner import ItineraryPlanner
from modules.trip_summary import TripSummaryGenerator
class TravelAgent:
    """Main Travel Agent orchestrator class (Legacy Single-Agent Version)"""
    def __init__(self):
        """Initialize all service modules"""
        self.input_handler = UserInputHandler()
        self.weather_service = WeatherService()
        self.attraction_finder = AttractionFinder()
        self.hotel_estimator = HotelEstimator()
        self.currency_converter = CurrencyConverter()
        self.expense_calculator = ExpenseCalculator()
        self.itinerary_planner = ItineraryPlanner()
        self.summary_generator = TripSummaryGenerator()
    def run(self):
        """Main application flow"""
        try:
            print("🤖 AI Travel Agent & Expense Planner (Single-Agent Version)")
            print("=" * 70)
            # Step 1: Get user input
            print("\n📝 Step 1: Collecting Trip Details...")
            trip_details = self.input_handler.get_trip_details()
            if not self.input_handler.confirm_details(trip_details):
                print("❌ Trip planning cancelled.")
                return
            print("\n🔍 Step 2: Planning your perfect trip...")
            # Step 2: Get weather information
            print("🌤️  Fetching weather forecast...")
            weather_data = self.weather_service.get_weather_forecast(
                trip_details["destination"], trip_details["total_days"]
            )
            # Step 3: Find attractions, restaurants, and activities
            print("🏛️  Finding attractions and activities...")
            attractions = self.attraction_finder.find_attractions(trip_details)
            restaurants = self.attraction_finder.find_restaurants(trip_details)
            activities = self.attraction_finder.find_activities(trip_details)
            # Step 4: Estimate hotel costs
            print("🏨 Estimating accommodation costs...")
            hotels = self.hotel_estimator.find_hotels(trip_details)
            # Step 5: Calculate total expenses
            print("💰 Calculating expenses...")
            expense_breakdown = self.expense_calculator.calculate_total_expenses(
                trip_details, hotels, attractions, restaurants, activities
            )
            # Step 6: Convert currency
            print("💱 Converting currency...")
            converted_expenses = self.currency_converter.convert_expenses(
                expense_breakdown, trip_details["currency"]
            )
            # Step 7: Generate itinerary
            print("📅 Creating your itinerary...")
            itinerary = self.itinerary_planner.create_itinerary(
                trip_details, weather_data, attractions, restaurants, activities
            )
            # Step 8: Generate final summary
            print("📋 Generating trip summary...")
            final_summary = self.summary_generator.generate_summary(
                trip_details, weather_data, hotels, converted_expenses, itinerary
            )
            # Display results
            self._display_results(final_summary)
            # Offer to save results
            self._offer_save_option(final_summary)
        except KeyboardInterrupt:
            print("\n\n❌ Trip planning interrupted by user.")
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            print("Please try again or contact support.")
    def _display_results(self, summary):
        """Display the complete trip summary"""
        print("\n" + "=" * 60)
        print("🎉 YOUR COMPLETE TRAVEL PLAN")
        print("=" * 60)
        # Basic trip info
        print(f"\n🏖️  DESTINATION: {summary.destination}")
        print(f"📅 DATES: {summary.start_date} to {summary.end_date}")
        print(f"⏰ DURATION: {summary.total_days} days")
        print(f"💰 TOTAL COST: {summary.converted_total:.2f} {summary.currency}")
        print(f"📊 DAILY BUDGET: {summary.daily_budget:.2f} {summary.currency}")
        # Weather summary
        if hasattr(summary, "weather_summary"):
            print(f"\n🌤️  WEATHER OVERVIEW:")
            weather = summary.weather_summary
            avg_temp = weather.get('avg_temperature', 'N/A')
            if avg_temp != 'N/A':
                print(f"   Average Temperature: {avg_temp}°C")
                # Add clothing suggestions based on temperature
                if avg_temp < 10:
                    print("   👕 Clothing Suggestion: Pack warm clothes - heavy jacket, sweaters, thermal wear")
                elif avg_temp < 15:
                    print("   👕 Clothing Suggestion: Pack layers - light jacket, long sleeves, comfortable pants")
                elif avg_temp < 20:
                    print("   👕 Clothing Suggestion: Pack versatile clothing - light jacket, jeans, long sleeves")
                elif avg_temp < 25:
                    print("   👕 Clothing Suggestion: Pack comfortable clothes - t-shirts, light pants, sandals")
                elif avg_temp < 30:
                    print("   👕 Clothing Suggestion: Pack light clothing - shorts, t-shirts, sun hat")
                else:
                    print("   👕 Clothing Suggestion: Pack tropical clothing - light fabrics, swimwear, sun protection")
            else:
                print(f"   Average Temperature: {avg_temp}°C")

            print(f"   Conditions: {', '.join(set(weather.get('conditions', [])))}")
            if weather.get("recommendations"):
                print("   Recommendations:")
                for rec in weather["recommendations"]:
                    print(f"   • {rec}")
        # Hotels
        if summary.hotels:
            print(f"\n🏨 RECOMMENDED HOTELS:")
            for hotel in summary.hotels[:3]:  # Show top 3
                print(f"   • {hotel.name} ({hotel.rating}⭐)")
                print(f"     ${hotel.price_per_night:.2f}/night - {hotel.address}")
        # Itinerary preview
        if summary.itinerary:
            print(f"\n📅 ITINERARY PREVIEW:")
            for day_plan in summary.itinerary[:3]:  # Show first 3 days
                print(f"\n   Day {day_plan.day} ({day_plan.date}):")
                print(f"   Weather: {day_plan.weather}")
                if day_plan.attractions:
                    print("   Attractions:")
                    for attraction in day_plan.attractions[:2]:
                        print(f"   • {attraction.name}")
                if day_plan.restaurants:
                    print("   Dining:")
                    for restaurant in day_plan.restaurants[:1]:
                        print(f"   • {restaurant.name}")
                print(f"   Daily Cost: ${day_plan.daily_cost:.2f}")
        print("\n" + "=" * 60)
        print("✅ Trip planning completed successfully!")
        print("=" * 60)
    def plan_trip_api(self, trip_details):
        """API-friendly method that returns structured planning results"""
        try:
            # Step 2: Get weather information
            weather_data = self.weather_service.get_weather_forecast(
                trip_details["destination"], trip_details["total_days"]
            )
            # Step 3: Find attractions, restaurants, and activities
            attractions = self.attraction_finder.find_attractions(trip_details)
            restaurants = self.attraction_finder.find_restaurants(trip_details)
            activities = self.attraction_finder.find_activities(trip_details)
            # Step 4: Estimate hotel costs
            hotels = self.hotel_estimator.find_hotels(trip_details)
            # Step 5: Calculate total expenses
            expense_breakdown = self.expense_calculator.calculate_total_expenses(
                trip_details, hotels, attractions, restaurants, activities
            )
            # Step 6: Convert currency
            converted_expenses = self.currency_converter.convert_expenses(
                expense_breakdown, trip_details["currency"]
            )
            # Step 7: Generate itinerary
            itinerary = self.itinerary_planner.create_itinerary(
                trip_details, weather_data, attractions, restaurants, activities
            )
            # Step 8: Generate final summary
            final_summary = self.summary_generator.generate_summary(
                trip_details, weather_data, hotels, converted_expenses, itinerary
            )
            # Convert summary to dictionary for API response
            result = {
                'destination': final_summary.destination,
                'start_date': str(final_summary.start_date),
                'end_date': str(final_summary.end_date),
                'total_days': final_summary.total_days,
                'currency': final_summary.currency,
                'estimated_cost': final_summary.converted_total,
                'planning_method': 'Single-Agent Planning',
                'daily_budget': final_summary.daily_budget,
                'weather_summary': {
                    'avg_temperature': final_summary.weather_summary.get('avg_temperature', 'N/A'),
                    'conditions': final_summary.weather_summary.get('conditions', []),
                    'recommendations': final_summary.weather_summary.get('recommendations', []),
                    'clothing_suggestion': self._get_clothing_suggestion(final_summary.weather_summary.get('avg_temperature', 'N/A'))
                } if hasattr(final_summary, 'weather_summary') else {},
                'hotels': [
                    {
                        'name': hotel.name,
                        'rating': hotel.rating,
                        'price_per_night': hotel.price_per_night,
                        'address': hotel.address
                    } for hotel in (final_summary.hotels or [])[:3]
                ],
                'itinerary': [
                    {
                        'day': day_plan.day,
                        'date': str(day_plan.date),
                        'weather': day_plan.weather,
                        'attractions': [
                            {'name': attr.name, 'description': getattr(attr, 'description', '')}
                            for attr in (day_plan.attractions or [])
                        ],
                        'restaurants': [
                            {'name': rest.name, 'cuisine': getattr(rest, 'cuisine', '')}
                            for rest in (day_plan.restaurants or [])
                        ],
                        'activities': [
                            {'name': act.name, 'description': getattr(act, 'description', '')}
                            for act in (day_plan.activities or [])
                        ],
                        'daily_cost': day_plan.daily_cost
                    } for day_plan in (final_summary.itinerary or [])
                ],
                'expense_breakdown': {
                    'accommodation': converted_expenses.get('accommodation_cost', 0),
                    'food': converted_expenses.get('food_cost', 0),
                    'activities': converted_expenses.get('activities_cost', 0),
                    'transportation': converted_expenses.get('transportation_cost', 0),
                    'miscellaneous': converted_expenses.get('miscellaneous_cost', 0)
                }
            }
            return result
        except Exception as e:
            return {'error': str(e)}

    def _get_clothing_suggestion(self, avg_temp):
        """Get clothing suggestion based on average temperature"""
        if avg_temp == 'N/A' or not isinstance(avg_temp, (int, float)):
            return "Unable to determine clothing suggestion due to unavailable temperature data"

        if avg_temp < 10:
            return "Pack warm clothes - heavy jacket, sweaters, thermal wear, gloves, and warm accessories"
        elif avg_temp < 15:
            return "Pack layers - light jacket, long sleeves, comfortable pants, and a light scarf"
        elif avg_temp < 20:
            return "Pack versatile clothing - light jacket, jeans, long sleeves, and comfortable walking shoes"
        elif avg_temp < 25:
            return "Pack comfortable clothes - t-shirts, light pants, sandals, and a light jacket for evenings"
        elif avg_temp < 30:
            return "Pack light clothing - shorts, t-shirts, sun hat, sunglasses, and sunscreen"
        else:
            return "Pack tropical clothing - light fabrics, swimwear, sun protection, and breathable materials"

    def _offer_save_option(self, summary):
        """Offer to save the trip plan to a file"""
        while True:
            save = input("\n💾 Save trip plan to file? (y/n): ").lower().strip()
            if save in ["y", "yes"]:
                filename = f"trip_plan_{summary.destination.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                try:
                    self.summary_generator.save_to_file(summary, filename)
                    print(f"✅ Trip plan saved to: {filename}")
                except Exception as e:
                    print(f"❌ Error saving file: {e}")
                break
            elif save in ["n", "no"]:
                print("👋 Thank you for using AI Travel Agent!")
                break
            else:
                print("Please enter 'y' or 'n'.")
def choose_planning_mode():
    """Let user choose between planning modes"""
    print("\n" + "=" * 80)
    print("🤖 AI TRAVEL PLANNING SYSTEM")
    print("=" * 80)
    print("Choose your planning experience:")
    print()
    print("1. 🔧 Single-Agent Planning (Classic)")
    print("   • Traditional single AI agent")
    print("   • Direct planning approach")
    print("   • Proven reliability")
    print()
    print("2. 🚀 Multi-Agent Planning (Legacy Framework)")
    print("   • 6 specialized AI agents working together")
    print("   • Custom multi-agent framework")
    print("   • Enhanced recommendations")
    print()
    print("3. 🌟 LangGraph Multi-Agent (Advanced)")
    print("   • Google Gemini Flash-2.0 powered agents")
    print("   • DuckDuckGo real-time search integration")
    print("   • LangGraph workflow orchestration")
    print("   • State-of-the-art multi-agent collaboration")
    print()
    while True:
        choice = input("Select planning mode (1, 2, or 3): ").strip()
        if choice in ["1", "2", "3"]:
            return choice
        else:
            print("Please enter 1, 2, or 3.")
def main():
    """Application entry point with mode selection"""
    try:
        # Let user choose planning mode
        mode = choose_planning_mode()
        if mode == "1":
            # Run traditional single-agent system
            agent = TravelAgent()
            agent.run()
        elif mode == "2":
            # Import and run legacy multi-agent system
            try:
                from multi_agent_main import main as multi_agent_main
                multi_agent_main()
            except ImportError as e:
                print(f"❌ Legacy multi-agent system not available: {e}")
                print("Falling back to single-agent planning...")
                agent = TravelAgent()
                agent.run()
        elif mode == "3":
            # Import and run LangGraph multi-agent system
            try:
                from langgraph_main import main as langgraph_main
                langgraph_main()
            except ImportError as e:
                print(f"❌ LangGraph system not available: {e}")
                print("Please install required dependencies:")
                print("pip install langgraph langchain-google-genai duckduckgo-search")
                print("\nFalling back to single-agent planning...")
                agent = TravelAgent()
                agent.run()
            except Exception as e:
                print(f"❌ LangGraph system error: {e}")
                print("Falling back to single-agent planning...")
                agent = TravelAgent()
                agent.run()
    except KeyboardInterrupt:
        print("\n\n❌ Planning interrupted by user.")
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        print("Please check your inputs and try again.")
if __name__ == "__main__":
    main()
