import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

async def main():
    # Create server parameters for stdio connection
    server_params = StdioServerParameters(
        command="python",
        # Make sure to update to the full absolute path to your math_server.py file
        args=["/Users/clojure/Desktop/filesystem-mcp-server/langchain-mcp/math_server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Get tools
            tools = await load_mcp_tools(session)

            # Create OpenRouter LLM instance
            # Set your OpenRouter API key as environment variable: OPENROUTER_API_KEY
            llm = ChatOpenAI(
                model="openai/gpt-4o",  # or any other model available on OpenRouter
                openai_api_key=os.getenv("OPENROUTER_API_KEY"),
                openai_api_base="https://openrouter.ai/api/v1"
            )

            # Create and run the agent
            agent = create_react_agent(llm, tools)
            agent_response = await agent.ainvoke({"messages": "what's (3 + 5) x 12?"})
            
            print("Agent Response:", agent_response)

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())

