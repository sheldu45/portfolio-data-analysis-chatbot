# DataFrameBot: A LLM Interface for Pandas DataFrames Analysis

## Overview

DataFrameBot is a chatbot that allows users to interact with a pandas DataFrame using natural language questions. Leveraging large language models (LLMs), the bot interprets user queries to perform specific data analysis tasks.

Unlike the standard LangChain implementation where the DataFrame is passed during agent initialization, this bot follows a more flexible design as requested in the challenge. The bot is designed to decouple the agent initialization from the process of passing the DataFrame. Instead, the DataFrame is provided to the agent only during the invocation. This approach allows for greater flexibility when working with various DataFrames in a production environment, making the bot more adaptable and scalable.

The custom agent executor is designed with the following interface, ensuring that the DataFrame is passed only when the bot is asked to perform specific tasks, enhancing usability and efficiency.

The bot supports both:

- **OpenAI GPT Models** (e.g., `gpt-3.5-turbo`)
- **Ollama Local Models** (e.g., `llama3.1`)

## Project Structure

```
portfolio-data-analysis-chatbot/
│
├── data/
│   └── physical_exam_study.csv
│
├── src/
│   └── dataframe_bot/
│       ├── __init__.py
│       ├── main.py
│       └── util/
│           ├── __init__.py
│           ├── parser.py
│           ├── prompt.py
│           └── tools.py
│
├── venv/                  (virtual environment folder)
├── .env                   (environment variables configuration)
├── .gitignore             (Git ignore file)
├── example_env            (sample environment configuration)
├── challenge_b_ollama.ipynb
├── challenge_b_openai.ipynb
├── nlp_assignment.pdf
├── README.md              (project description and instructions)
└── requirements.txt       (Python dependencies file)
```

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- [pip](https://pip.pypa.io/en/stable/installation/)
- [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html) (optional but recommended)

Depending on your choice of language model (OpenAI or Ollama), follow the corresponding setup instructions below.

---

### Option 1: Using OpenAI GPT Models

#### 1. Obtain OpenAI API Key

- **Sign up or log in** to your OpenAI account.
- Navigate to **[API Keys](https://platform.openai.com/account/api-keys)**.
- **Create a new API key** or use an existing one.

#### 2. Set Up Environment Variables

- **Copy** the example environment file:

  ```bash
  cp example_env .env
  ```

- **Open** the `.env` file and add your OpenAI API key:

  ```dotenv
  OPENAI_API_KEY=your_openai_api_key_here
  ```

#### 3. Create and Activate Virtual Environment

- **Create** a virtual environment:

  ```bash
  python -m venv venv
  ```

- **Activate** the virtual environment:

  - On macOS/Linux:

    ```bash
    source venv/bin/activate
    ```

  - On Windows:

    ```bash
    venv\Scripts\activate
    ```

#### 4. Install Dependencies

- **Install** the required Python packages:

  ```bash
  pip install -r requirements.txt
  ```

#### 5. Run the Bot

- **Run** the Jupyter notebook:

  ```bash
  jupyter notebook challenge_b_openai.ipynb
  ```

  or

- **Run** the main script:

  ```bash
  python src/dataframe_bot/main.py --openai --model gpt-3.5-turbo --data data/physical_exam_study.csv
  ```

---

### Option 2: Using Ollama with Local Models

#### 1. Install Ollama

- **Install Ollama** by running:

  ```bash
  curl -fsSL https://ollama.com/install.sh | sh
  ```

#### 2. Pull the Model

- **Pull** the `llama3.1` model:

  ```bash
  ollama pull llama3.1
  ```

#### 3. Serve the Model

- **Start** the Ollama server:

  ```bash
  ollama serve
  ```

#### 4. Create and Activate Virtual Environment

- **Create** a virtual environment:

  ```bash
  python -m venv venv
  ```

- **Activate** the virtual environment:

  - On macOS/Linux:

    ```bash
    source venv/bin/activate
    ```

  - On Windows:

    ```bash
    venv\Scripts\activate
    ```

#### 5. Install Dependencies

- **Install** the required Python packages:

  ```bash
  pip install -r requirements.txt
  ```

#### 6. Run the Bot

- **Run** the Jupyter notebook:

  ```bash
  jupyter notebook challenge_b_ollama.ipynb
  ```

  or

- **Run** the main script:

  ```bash
  python src/dataframe_bot/main.py --model llama3.1 --data data/physical_exam_study.csv
  ```

---

## Usage

- **Interact** with the bot by typing your questions when prompted.

### Example Questions

- **Question**: _"What is the mean and standard deviation of the workout intensity for men?"_
- **Answer**: The bot will compute and return the numerical results based on the DataFrame.

## Project Details

### Data

- **Data File**: `data/physical_exam_study.csv`
- The DataFrame contains columns related to a physical exam study.

### Language Models

- **OpenAI GPT Models**: Requires an API key and internet connection.
- **Ollama Local Models**: Runs locally without sending data to external servers.

---

*Happy Data Analyzing!*