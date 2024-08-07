"""
The research Assistant searches for EXA for a topic
and writes an article in Markdown format.
"""

import sys

sys.path.append('..')
from agentica.python_assistant import PythonAssistant
from agentica import AzureOpenAILLM
from agentica.tools.search_serper import SearchSerperTool

m = PythonAssistant(
    llm=AzureOpenAILLM(model='gpt-4o'),
    tools=[SearchSerperTool()],
    description="You are a helpful AI, 中文回答问题",
    add_datetime_to_instructions=True,
    markdown=True,
    show_tool_calls=True,
    debug_mode=True,
)
r = m.run(
    "如果Eliud Kipchoge能够无限期地保持他创造记录的马拉松速度，那么他需要多少小时才能跑完地球和月球在最近接时之间的距离？"
    "请在进行计算时使用维基百科页面上的最小近地点值。将结果用中文回答"
)
print("".join(r))
