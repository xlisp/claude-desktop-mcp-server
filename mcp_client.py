import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
import httpx
from openai import AsyncOpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WeatherMCPClient:
    """天气MCP客户端，支持自定义OpenAI API"""
    
    def __init__(
        self,
        openai_api_key: str,
        openai_base_url: str = "https://api.openai.com/v1",
        model: str = "gpt-4"
    ):
        """
        初始化客户端
        
        Args:
            openai_api_key: OpenAI API密钥
            openai_base_url: OpenAI API基础URL（可自定义）
            model: 使用的模型名称
        """
        self.openai_client = AsyncOpenAI(
            api_key=openai_api_key,
            base_url=openai_base_url
        )
        self.model = model
        self.mcp_session: Optional[ClientSession] = None
        self.available_tools: List[Dict[str, Any]] = []
        
    async def connect_to_mcp_server(self, server_script_path: str):
        """连接到MCP服务器"""
        try:
            server_params = StdioServerParameters(
                command="python",
                args=[server_script_path]
            )
            
            stdio_transport = await stdio_client(server_params)
            self.mcp_session = ClientSession(stdio_transport[0], stdio_transport[1])
            await self.mcp_session.initialize()
            
            # 获取可用工具
            tools_result = await self.mcp_session.list_tools()
            self.available_tools = tools_result.tools
            
            logger.info(f"已连接到MCP服务器，可用工具: {[tool.name for tool in self.available_tools]}")
            
        except Exception as e:
            logger.error(f"连接MCP服务器失败: {e}")
            raise

    async def call_mcp_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """调用MCP工具"""
        if not self.mcp_session:
            raise RuntimeError("MCP会话未初始化")
        
        try:
            result = await self.mcp_session.call_tool(tool_name, arguments)
            if result.content:
                return result.content[0].text if result.content[0].text else ""
            return "工具调用无返回内容"
        except Exception as e:
            logger.error(f"调用MCP工具 {tool_name} 失败: {e}")
            return f"工具调用失败: {str(e)}"

    def get_openai_tools_schema(self) -> List[Dict[str, Any]]:
        """将MCP工具转换为OpenAI函数调用格式"""
        openai_tools = []
        
        for tool in self.available_tools:
            openai_tool = {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            }
            
            # 处理工具参数
            if hasattr(tool, 'inputSchema') and tool.inputSchema:
                schema = tool.inputSchema
                if "properties" in schema:
                    openai_tool["function"]["parameters"]["properties"] = schema["properties"]
                if "required" in schema:
                    openai_tool["function"]["parameters"]["required"] = schema["required"]
            
            openai_tools.append(openai_tool)
        
        return openai_tools

    async def chat_with_tools(self, user_message: str) -> str:
        """与AI聊天，支持工具调用"""
        if not self.mcp_session:
            raise RuntimeError("请先连接到MCP服务器")
        
        messages = [
            {
                "role": "system",
                "content": """你是一个天气助手，可以帮助用户查询天气信息。你有以下工具可用：
1. get_alerts - 获取美国各州的天气警报（需要州代码，如CA、NY）
2. get_forecast - 获取指定坐标的天气预报（需要纬度和经度）

请根据用户需求调用相应的工具。"""
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
        
        tools = self.get_openai_tools_schema()
        
        try:
            # 第一次调用OpenAI API
            response = await self.openai_client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )
            
            response_message = response.choices[0].message
            messages.append(response_message)
            
            # 检查是否需要调用工具
            if response_message.tool_calls:
                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    logger.info(f"调用工具: {function_name}, 参数: {function_args}")
                    
                    # 调用MCP工具
                    tool_result = await self.call_mcp_tool(function_name, function_args)
                    
                    # 添加工具调用结果
                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": tool_result
                    })
                
                # 第二次调用OpenAI API处理工具结果
                final_response = await self.openai_client.chat.completions.create(
                    model=self.model,
                    messages=messages
                )
                
                return final_response.choices[0].message.content
            else:
                return response_message.content
                
        except Exception as e:
            logger.error(f"聊天请求失败: {e}")
            return f"请求失败: {str(e)}"

    async def close(self):
        """关闭连接"""
        if self.mcp_session:
            await self.mcp_session.close()

async def main():
    """主函数示例"""
    # 配置参数
    OPENAI_API_KEY = "your-openai-api-key"  # 替换为您的API密钥
    OPENAI_BASE_URL = "https://api.openai.com/v1"  # 可自定义的API地址
    MODEL = "gpt-4"  # 使用的模型
    MCP_SERVER_PATH = "weather_server.py"  # MCP服务器脚本路径
    
    # 创建客户端
    client = WeatherMCPClient(
        openai_api_key=OPENAI_API_KEY,
        openai_base_url=OPENAI_BASE_URL,
        model=MODEL
    )
    
    try:
        # 连接MCP服务器
        await client.connect_to_mcp_server(MCP_SERVER_PATH)
        
        # 交互式聊天
        print("天气助手已启动！输入 'quit' 退出。")
        print("示例查询：")
        print("- 查询加州的天气警报")
        print("- 获取纽约市的天气预报（纬度40.7128，经度-74.0060）")
        print()
        
        while True:
            user_input = input("用户: ").strip()
            if user_input.lower() in ['quit', 'exit', '退出']:
                break
            
            if user_input:
                print("助手: 正在处理您的请求...")
                response = await client.chat_with_tools(user_input)
                print(f"助手: {response}")
                print()
    
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"程序错误: {e}")
    finally:
        await client.close()
        print("连接已关闭")

# 配置类，方便管理配置
class MCPClientConfig:
    """MCP客户端配置类"""
    
    def __init__(self):
        self.openai_api_key = ""
        self.openai_base_url = "https://api.openai.com/v1"
        self.model = "gpt-4"
        self.mcp_server_path = "weather_server.py"
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'MCPClientConfig':
        """从字典创建配置"""
        config = cls()
        for key, value in config_dict.items():
            if hasattr(config, key):
                setattr(config, key, value)
        return config
    
    @classmethod
    def from_file(cls, config_file: str) -> 'MCPClientConfig':
        """从JSON配置文件创建配置"""
        with open(config_file, 'r', encoding='utf-8') as f:
            config_dict = json.load(f)
        return cls.from_dict(config_dict)

# 使用配置文件的示例
async def main_with_config():
    """使用配置文件的主函数"""
    try:
        # 从配置文件加载配置
        config = MCPClientConfig.from_file("config.json")
    except FileNotFoundError:
        # 如果配置文件不存在，使用默认配置
        print("配置文件未找到，使用默认配置")
        config = MCPClientConfig()
        config.openai_api_key = input("请输入OpenAI API Key: ")
        config.openai_base_url = input("请输入OpenAI Base URL (回车使用默认): ") or config.openai_base_url
    
    client = WeatherMCPClient(
        openai_api_key=config.openai_api_key,
        openai_base_url=config.openai_base_url,
        model=config.model
    )
    
    try:
        await client.connect_to_mcp_server(config.mcp_server_path)
        
        # 示例查询
        queries = [
            "查询加州的天气警报",
            "获取纽约市（纬度40.7128，经度-74.0060）的天气预报",
            "查询德州有没有天气警报？"
        ]
        
        for query in queries:
            print(f"\n查询: {query}")
            response = await client.chat_with_tools(query)
            print(f"回答: {response}")
            print("-" * 50)
    
    finally:
        await client.close()

if __name__ == "__main__":
    # 运行交互式版本
    asyncio.run(main())
    
    # 或者运行配置文件版本
    # asyncio.run(main_with_config())