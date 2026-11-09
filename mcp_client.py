# 导入 MCP 客户端会话类，用于与 MCP 服务建立连接和通信
from mcp import ClientSession, StdioServerParameters
# 导入 asyncio 库，用于编写异步代码
import asyncio
# 导入 sse_starlette 库，用于支持 SSE（Server-Sent Events）协议
import sse_starlette
# 从 mcp.client.sse 模块导入 sse_client，用于创建 SSE 客户端连接
from mcp.client.sse import sse_client

# 从 mcp.client.stdio 模块导入 stdio_client，用于创建 stdio 客户端连接
from mcp.client.stdio import stdio_client

# 定义 SSE 模式的演示函数
async def sse_demo():
    """
    通过 SSE（Server-Sent Events）协议连接 MCP 服务的示例
    
    SSE 模式特点：
    - 通过 HTTP 长连接通信
    - 服务端监听端口（如 9000）
    - 支持远程访问
    - 适合高并发场景
    """
    # 创建 SSE 客户端连接，连接到本地 9000 端口的 /sse 端点
    async with sse_client("http://127.0.0.1:9000/sse") as (read, write):
        # 创建客户端会话，建立与 MCP 服务的通信通道
        async with ClientSession(read, write) as session:
            # 初始化会话，完成握手协议
            await session.initialize()
            
            # 获取服务端注册的所有工具列表
            tools = await session.list_tools()
            print("可用工具：", [tool.name for tool in tools.tools])
            
            # 调用 get_weather 工具，传入城市参数
            result = await session.call_tool("get_weather", {"city": "北京"})
            print("get_weather 结果：", result.content[0].text)
            
            # 调用 get_time 工具，无参数
            result = await session.call_tool("get_time", {})
            print("get_time 结果：", result.content[0].text)


# 定义 stdio 模式的演示函数
async def stdio_demo():
    """
    通过 stdio（标准输入输出）协议连接 MCP 服务的示例
    
    stdio 模式特点：
    - 通过进程管道通信（stdin/stdout）
    - 服务端作为子进程启动
    - 仅支持本地访问
    - 适合 IDE 集成、本地开发调试
    """
    # 配置 stdio 服务参数
    server_params = StdioServerParameters(
        command="python",           # 启动服务的命令
        args=["mcp_server.py"],  # 命令参数，指定要运行的 MCP 服务脚本
    )
    
    # 创建 stdio 客户端连接，启动并连接到 MCP 服务进程
    async with stdio_client(server_params) as (read, write):
        # 创建客户端会话，建立与 MCP 服务的通信通道
        async with ClientSession(read, write) as session:
            # 初始化会话，完成握手协议
            await session.initialize()
            
            # 获取服务端注册的所有工具的列表
            tools = await session.list_tools()
            print("可用工具：", [tool.name for tool in tools.tools])
            
            # 调用 get_weather 工具，传入城市参数
            result = await session.call_tool("get_weather", {"city": "北京"})
            print("get_weather 结果：", result.content[0].text)
            
            # 调用 get_time 工具，无参数    
            result = await session.call_tool("get_time", {})
            print("get_time 结果：", result.content[0].text)

# 主程序入口
if __name__ == "__main__":
    # 运行 SSE 模式演示
    asyncio.run(sse_demo())

    # 运行 stdio 模式演示（需先确保 mcp_server.py 存在）
    # asyncio.run(stdio_demo())