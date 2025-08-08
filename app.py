"""
Databricks Serving Endpoint Bot

This script implements a chatbot that interacts with Databricks' Serving Endpoints.
"""

"""
Startup Command for your Web App Configuration:
python3 -m aiohttp.web -H 0.0.0.0 -P 8000 app:init_func
"""


import os
import json
import logging
from typing import List
from aiohttp import web
import traceback
from aiohttp.web import Request, Response, json_response
from botbuilder.core import (
    ActivityHandler,
    TurnContext,
)
from botbuilder.core.integration import aiohttp_error_middleware
from botbuilder.integration.aiohttp import (
    CloudAdapter,
    ConfigurationBotFrameworkAuthentication,
)
from botbuilder.schema import (
    Activity,
    ActivityTypes,
    ChannelAccount,
)
import aiohttp

from config import DefaultConfig

CONFIG = DefaultConfig()
ADAPTER = CloudAdapter(ConfigurationBotFrameworkAuthentication(CONFIG))

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def on_error(context: TurnContext, error: Exception):
    """Handle errors that occur during bot execution."""
    logger.error(f"Bot error: {str(error)}")
    traceback.print_exc()
    
    await context.send_activity("Sorry, I encountered an error processing your request.")


ADAPTER.on_turn_error = on_error


async def ask_serving_endpoint(question: str) -> str:
    """
    Call the Databricks serving endpoint with a chat completion request.
    """
    try:
        # Prepare messages (single turn conversation)
        messages = [
            {
                "role": "system",
                "content": "You are a helpful AI assistant."
            },
            {
                "role": "user",
                "content": question
            }
        ]
        
        # Request payload
        payload = {
            "messages": messages,
        }
        
        # Headers
        headers = {
            "Authorization": f"Bearer {CONFIG.DATABRICKS_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # Make request
        endpoint_url = f"{CONFIG.DATABRICKS_HOST}/serving-endpoints/{CONFIG.ENDPOINT_NAME}/invocations"
        
        async with aiohttp.ClientSession() as session:
            async with session.post(endpoint_url, json=payload, headers=headers) as response:
                if response.status == 200:
                    result = await response.json()
                    if "choices" in result and len(result["choices"]) > 0:
                        content = result["choices"][0]["message"]["content"]
                        # Ensure we return a string
                        return str(content) if content is not None else "I didn't receive a proper response from the AI model."
                    else:
                        return "I didn't receive a proper response from the AI model."
                else:
                    error_text = await response.text()
                    logger.error(f"Serving endpoint error {response.status}: {error_text}")
                    return "I'm experiencing technical difficulties. Please try again later."
                    
    except Exception as e:
        logger.error(f"Error in ask_serving_endpoint: {str(e)}")
        return "An error occurred while processing your request."


class MyBot(ActivityHandler):
    def __init__(self):
        pass

    async def on_message_activity(self, turn_context: TurnContext):
        try:
            # Validate turn context and activity
            if not turn_context or not hasattr(turn_context, 'activity'):
                logger.error("Invalid turn context or missing activity")
                return
            
            activity = turn_context.activity
            if not activity or not hasattr(activity, 'text'):
                logger.error("Invalid activity or missing text")
                return
                
            question = activity.text
            if not question or not question.strip():
                logger.info("Empty message received")
                return
            
            # Get response from serving endpoint (no conversation history)
            response = await ask_serving_endpoint(question.strip())
            
            # Ensure response is a string before sending
            if isinstance(response, list):
                response = str(response)
            elif response is None:
                response = "I'm sorry, I couldn't generate a response."
            
            await turn_context.send_activity(str(response))
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            traceback.print_exc()
            try:
                await turn_context.send_activity("An error occurred while processing your request.")
            except:
                logger.error("Failed to send error message to user")

    async def on_members_added_activity(self, members_added: List[ChannelAccount], turn_context: TurnContext):
        try:
            if not members_added or not turn_context:
                return
                
            for member in members_added:
                try:
                    # Simple welcome message without complex attribute checking
                    await turn_context.send_activity("Welcome to the Databricks AI Assistant!")
                    break  # Only send one welcome message
                except Exception as e:
                    logger.error(f"Error sending welcome message: {str(e)}")
                    
        except Exception as e:
            logger.error(f"Error in members added: {str(e)}")
            traceback.print_exc()


BOT = MyBot()


async def messages(req: Request) -> Response:
    """Handle incoming messages."""
    try:
        # Check content type
        if "application/json" not in req.headers.get("Content-Type", ""):
            return Response(status=415)

        # Get the request body
        body = await req.json()
        
        # Validate that we have a proper activity structure
        if not isinstance(body, dict):
            logger.error("Request body is not a dictionary")
            return Response(status=400)
        
        # Process the request through the Bot Framework adapter
        response = await ADAPTER.process(req, BOT)
        
        if response:
            return json_response(data=response.body, status=response.status)
        return Response(status=201)
        
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in request: {str(e)}")
        return Response(status=400)
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        traceback.print_exc()
        return Response(status=500)


def init_func(argv):
    """Initialize the web application."""
    app = web.Application(middlewares=[aiohttp_error_middleware])
    app.router.add_post("/api/messages", messages)
    return app


if __name__ == "__main__":
    app = init_func(None)
    try:
        web.run_app(app, host="0.0.0.0", port=CONFIG.PORT)
    except Exception as error:
        raise error
