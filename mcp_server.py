# 导入 FastMCP 框架，这是一个用于构建 MCP（Model Context Protocol）服务的工具库
from fastmcp import FastMCP
# 导入 Python 标准库中的 datetime 模块，用于处理日期和时间
from datetime import datetime

# 创建 FastMCP 实例，参数 "WeatherServer" 是服务的名称标识
mcp = FastMCP("WeatherServer")

# @mcp.tool() 装饰器：将函数注册为 MCP 工具，可供 AI 调用
@mcp.tool()
# 定义获取天气的工具函数，接收城市名参数，返回字符串类型
def get_weather(city: str) -> str:
    """函数文档字符串：描述函数功能为获取城市天气信息"""
    # 返回格式化的天气信息字符串
    return f"{city} 今天晴天，33℃"

# @mcp.tool() 装饰器：将函数注册为另一个 MCP 工具
@mcp.tool()
# 定义获取当前时间的工具函数，无参数，返回字符串类型
def get_time() -> str:
    """函数文档字符串：描述函数功能为获取当前时间"""
    # 返回格式化的当前时间字符串，格式为 YYYY-MM-DD HH:MM:SS
    return f"当前时间是 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

# @mcp.resource("uri") 装饰器：将函数注册为 MCP 资源，通过指定的 URI 访问
@mcp.resource("time://now")
# 定义获取当前时间的资源函数
def get_current_time():
    """函数文档字符串：描述函数功能为返回当前时间作为资源"""
    # 返回 ISO 8601 标准格式的当前时间
    return datetime.now().isoformat()

# 主程序入口：当脚本直接运行时执行以下代码
if __name__ == "__main__":
    # 启动 MCP 服务，使用 SSE（Server-Sent Events）传输协议，监听端口 9000
    mcp.run(transport="sse", port=9000)
    # 注释掉的代码：使用标准输入输出（stdio）传输协议启动服务
    # mcp.run(transport="stdio")