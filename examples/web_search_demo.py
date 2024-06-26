# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: Web search demo, using SearchSerperTool(google) to search the web.
"""
import sys

sys.path.append('..')
from agentica import Assistant, AzureOpenAILLM
from agentica.tools.search_serper import SearchSerperTool

m = Assistant(
    llm=AzureOpenAILLM(model="gpt-4o"),
    tools=[SearchSerperTool()],
    add_datetime_to_instructions=True,
    show_tool_calls=True,
    # Enable the assistant to read the chat history
    read_chat_history=True,
    debug_mode=True,
)
m.run("一句话介绍林黛玉")
m.run("北京最近的新闻", stream=True, print_output=True)
r = m.run("总结前面的问答", stream=False, print_output=False)
print(r)
