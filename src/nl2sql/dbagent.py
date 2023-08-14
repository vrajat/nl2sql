from pathlib import Path
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.agents import AgentExecutor
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI

class DBAgent:
    prompt: str
    agent: AgentExecutor

    def __init__(self, openai_key: Path, db_path: Path):
        self.prompt = """Given an input question,
                         first create a syntactically correct sqlite query to run,
                         then look at the results of the query and return the answer.
                         The question: {question}"""

        db = SQLDatabase.from_uri(f"sqlite:///{db_path.absolute()}")
        openai_key = openai_key.read_text().strip()

        llm = ChatOpenAI(temperature=0, openai_api_key=openai_key, model_name='gpt-3.5-turbo-16k')

        toolkit = SQLDatabaseToolkit(db=db, llm=llm)
        self.agent = create_sql_agent(
            llm=llm,
            toolkit=toolkit,
            verbose=True,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        )
