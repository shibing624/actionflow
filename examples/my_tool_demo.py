from actionflow import Assistant, AzureOpenAILLM

def multiply(first_int: int, second_int: int) -> str:
    """Multiply two integers together."""
    return str(first_int * second_int)


def add(first_int: int, second_int: int) -> str:
    """Add two integers."""
    return str(first_int + second_int)


def exponentiate(base: int, exponent: int) -> str:
    """Exponentiate the base to the exponent power."""
    return str(base**exponent)


assistant = Assistant(llm=AzureOpenAILLM(), tools=[multiply, add, exponentiate])
assistant.print_response("3乘以10000005是啥?")
assistant.print_response(
    "将3的五次方乘以12和3的总和. Only show the result."
)