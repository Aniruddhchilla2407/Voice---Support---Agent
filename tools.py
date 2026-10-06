# Mock tools the agent can call

def get_order_status(order_id: str) -> str:
    fake_db = {
        "1234": "shipped, arriving in 2 days",
        "5678": "delivered yesterday",
    }
    return fake_db.get(order_id, "order not found")

def get_weather(city: str) -> str:
    fake_weather = {
        "hyderabad": "32°C, sunny",
        "mumbai": "28°C, rainy",
    }
    return fake_weather.get(city.lower(), "weather data not available")

# Tool schema OpenAI's function-calling API expects
TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "get_order_status",
            "description": "Get the status of an order by its ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "description": "The order ID"}
                },
                "required": ["order_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name"}
                },
                "required": ["city"],
            },
        },
    },
]

AVAILABLE_FUNCTIONS = {
    "get_order_status": get_order_status,
    "get_weather": get_weather,
}