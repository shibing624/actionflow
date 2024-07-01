# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: 模仿两个人辩论的例子，拜登和特朗普
"""
import sys

sys.path.append('..')
from agentica import Assistant, AzureOpenAILLM, OpenAILLM
from agentica.tools.search_serper import SearchSerperTool

PROMPT_TEMPLATE: str = """
## BACKGROUND
Suppose you are {name}, you are in a debate with {opponent_name}.
## DEBATE HISTORY
Previous rounds:
{context}
## YOUR TURN
Now it's your turn, you should closely respond to your opponent's latest argument, state your position, defend your arguments, and attack your opponent's arguments,
craft a strong and emotional response in 80 words, in {name}'s rhetoric and viewpoints, your will argue:
"""


Biden = Assistant(
    llm=OpenAILLM(model='gpt-4o'),
    name="Biden",
    description="Suppose you are Biden, you are in a debate with Trump.",
    show_tool_calls=True,
    debug_mode=True,
)

Trump = Assistant(
    llm=OpenAILLM(model='gpt-4o'),
    name="Trump",
    description="Suppose you are Trump, you are in a debate with Biden.",
    show_tool_calls=True,
    debug_mode=True,
)

hn_assistant = Assistant(
    name="Debate",
    team=[Biden, Trump],
    instructions=[
        "you should closely respond to your opponent's latest argument, state your position, defend your arguments, "
        "and attack your opponent's arguments, craft a strong and emotional response in 80 words",
    ],
    show_tool_calls=True,
    output_dir="outputs",
    output_file_name="debate.md",
    debug_mode=True,
)
hn_assistant.run(
    """Trump and Biden are in a debate, Biden speak first, and then Trump speak, and then Biden speak, and so on, in 3 turns.
    Now begin."""
)
