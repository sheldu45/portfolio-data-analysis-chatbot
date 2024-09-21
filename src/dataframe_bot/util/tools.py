from langchain.tools import Tool
import pandas as pd

class DataFramePythonREPLTool(Tool):
    def __init__(self):
        super().__init__(
            name="Python_REPL",
            func=self._run,
            description="Executes Python code with access to a DataFrame 'df'."
        )

    def _run(self, code: str, **kwargs):
        df = kwargs.get('df')
        if df is None:
            return "Error: DataFrame 'df' not provided."
        local_vars = {'df': df}
        try:
            exec(code, {}, local_vars)
            result = local_vars.get('result', 'No result variable defined.')
            return str(result)
        except Exception as e:
            return f"Error executing code: {e}"

    async def _arun(self, code: str, **kwargs):
        raise NotImplementedError("Asynchronous execution not supported.")