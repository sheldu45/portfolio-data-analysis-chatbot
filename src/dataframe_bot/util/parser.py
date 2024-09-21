import re
from langchain.schema import AgentAction, AgentFinish
from langchain.agents import AgentOutputParser

class CustomOutputParser(AgentOutputParser):
    def parse(self, text: str) -> AgentAction or AgentFinish:
        if "```" in text:
            # Extract code between code fences
            pattern = r"```(?:python)?\n(.*?)```"
            match = re.search(pattern, text, re.DOTALL)
            if match:
                code = match.group(1)
                return AgentAction(tool="Python_REPL", tool_input=code, log=text)
        return AgentFinish(return_values={"output": text}, log=text)