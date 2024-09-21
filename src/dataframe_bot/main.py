import os
import argparse
import sys
from typing import Optional

import pandas as pd
from dotenv import load_dotenv

from langchain.agents import AgentExecutor, LLMSingleActionAgent
from langchain.chains import LLMChain

class DataframeBot:
    """
    A bot for interacting with a pandas DataFrame using natural language questions.
    """

    def __init__(self, openai: bool, model: str):
        """
        Initializes the DataframeBot with the specified language model.

        Args:
            openai (bool): If True, uses OpenAI's ChatOpenAI; otherwise, uses ChatOllama.
            model (str): The language model to use (e.g., 'gpt-3.5-turbo', 'llama3.1').
        """
        self.openai = openai
        self.model = model
        self.df: Optional[pd.DataFrame] = None  # DataFrame is initially not loaded

        # Initialize language model
        if self.openai:
            # Only import OpenAI module if OpenAI model is selected
            from langchain_openai import ChatOpenAI
            load_dotenv()  # Load environment variables from .env
            openai_api_key = os.getenv("OPENAI_API_KEY")
            if not openai_api_key:
                raise ValueError("OPENAI_API_KEY not found in environment variables.")
            self.llm = ChatOpenAI(
                model=self.model,
                temperature=0,
                openai_api_key=openai_api_key
            )
        else:
            # Only import Ollama module if Ollama model is selected
            from langchain_ollama import ChatOllama
            self.llm = ChatOllama(
                model=self.model,
                temperature=0
            )

        # Initialize tools
        self.tools = [DataFramePythonREPLTool()]

        # Define the main prompt template
        main_template = """You are a data analysis assistant with access to a pandas DataFrame 'df' containing the study data.
        Here is the description of the DataFrame columns:
        {header_description}

        You can use Python code to perform computations on 'df'. 

        Question: {input}

        Provide the answer with numerical results only."""
        
        self.prompt = CustomPromptTemplate(template=main_template, input_variables=["input", "header_description"])

        # Initialize output parser
        self.output_parser = CustomOutputParser()

        # Create LLM chain
        self.llm_chain = LLMChain(llm=self.llm, prompt=self.prompt)

        # Configure the agent
        self.agent = LLMSingleActionAgent(
            llm_chain=self.llm_chain,
            output_parser=self.output_parser,
            stop=["\nObservation:"],
            allowed_tools=["Python_REPL"],
            prompt=self.prompt
        )

        # Create Agent Executor
        self.agent_executor = AgentExecutor.from_agent_and_tools(
            agent=self.agent,
            tools=self.tools,
            verbose=True
        )

    def load_dataframe(self, file_path: str):
        """
        Loads the pandas DataFrame from the specified CSV file and performs header analysis.

        Args:
            file_path (str): The path to the CSV file.

        Returns:
            str: The description of the DataFrame columns.
        """
        try:
            self.df = pd.read_csv(file_path)
            print(f"DataFrame loaded successfully from '{file_path}'.")

            # Extract the header from the DataFrame
            header = list(self.df.columns)

            # Get a sample of the DataFrame to pass to the LLM
            df_sample = self.df.head().to_dict(orient='records')

            # Define the initial prompt template to describe the DataFrame columns
            header_template = """You are a data analysis assistant. Here is the header of the DataFrame:
            {header}

            Here is a sample of the DataFrame:
            {df_sample}

            Describe each column in terms of data type and content. Provide the description in the following JSON format:
            [
            {{
                "column_name": "column1",
                "data_type": "type1",
                "description": "description1"
            }},
            {{
                "column_name": "column2",
                "data_type": "type2",
                "description": "description2"
            }},
            ...
            ]"""
            
            header_prompt = CustomPromptTemplate(template=header_template, input_variables=["header", "df_sample"])

            # Create LLM chain for header description
            header_llm_chain = LLMChain(llm=self.llm, prompt=header_prompt)

            # Get the description of each column
            header_description = header_llm_chain.run({"header": header, "df_sample": df_sample})

            # Return the header description
            return header_description

        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            self.prompt.input_variables["header_description"] = header_description
        except Exception as e:
            print(f"Error loading DataFrame: {e}")
            
    def chat(self, header_description: str, question: str) -> str:
        """
        Processes a natural language question and returns the numerical answer.

        Args:
            question (str): The user's question.

        Returns:
            str: The numerical answer or an error message.
        """
        if self.df is None:
            return "Error: DataFrame not loaded. Please load the DataFrame before asking questions."

        try:
            answer = self.agent_executor.run(header_description=header_description, input=question, df=self.df)
            return answer
        except Exception as e:
            return f"Error executing the agent: {e}"

def parse_arguments():
    """
    Parses command-line arguments.

    Returns:
        argparse.Namespace: The parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="DataframeBot: A natural language interface for pandas DataFrames."
    )

    parser.add_argument(
        "-o", "--openai",
        action="store_true",
        help="Use OpenAI's ChatOpenAI model. If not set, ChatOllama is used."
    )

    parser.add_argument(
        "-m", "--model",
        type=str,
        required=True,
        help="The language model to use (e.g., 'gpt-3.5-turbo', 'llama3.1')."
    )

    parser.add_argument(
        "-d", "--data",
        type=str,
        required=True,
        help="Path to the CSV file containing the DataFrame."
    )

    return parser.parse_args()

def main():
    """
    The main function that initializes the DataframeBot and handles user interactions.
    """
    # Parse command-line arguments
    args = parse_arguments()

    # Initialize DataframeBot
    try:
        bot = DataframeBot(openai=args.openai, model=args.model)
    except Exception as e:
        print(f"Error initializing DataframeBot: {e}")
        sys.exit(1)

    # Load the DataFrame (and get the header description)
    header_description = bot.load_dataframe(args.data)

    # Check if DataFrame was loaded successfully
    if bot.df is None:
        print("Failed to load the DataFrame. Exiting.")
        sys.exit(1)

    print("\nDataframeBot is ready to answer your questions. Type 'exit' to quit.\n")

    # Interactive loop for user questions
    while True:
        try:
            question = input("Enter your question: ")
            if question.lower() in ['exit', 'quit']:
                print("Exiting DataframeBot. Goodbye!")
                break
            answer = bot.chat(header_description, question)
            print("Answer:", answer, "\n")
        except KeyboardInterrupt:
            print("\nInterrupted by user. Exiting.")
            break
        except Exception as e:
            print(f"An error occurred: {e}\n")

if __name__ == "__main__":
    from util import CustomPromptTemplate, CustomOutputParser, DataFramePythonREPLTool
    main()
else:
    # Relative import for when running as part of a package
    from .util import CustomPromptTemplate, CustomOutputParser, DataFramePythonREPLTool