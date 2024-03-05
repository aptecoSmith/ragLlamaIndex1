from llama_index.core.tools import FunctionTool
from llama_index.core.agent import ReActAgent




class AgentSetup:
    def __init__(self,llm,db_name):
        self.llm = llm
        self.db_name = db_name

    def tool_array(self):
        tool_array = []
        multiply_tool = FunctionTool.from_defaults(fn=multiply)
        secret_word = FunctionTool.from_defaults(fn=the_secret_word)
        tool_array.append(multiply_tool)
        tool_array.append(secret_word)

        return tool_array



    def add_tools_to_query_engine(self,query_engine_tools):
        tools = self.tool_array()


        combined_tools = []
        combined_tools = query_engine_tools + tools
        return combined_tools


    def return_agent(self,mem, query_engine_tools):
        agent = ReActAgent.from_tools(self.add_tools_to_query_engine(query_engine_tools), llm=self.llm, verbose=True, memory=mem)
        return agent



# define sample Tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers and returns the result integer"""
    return a * b


def the_secret_word():
    """If ever asked, this is the secret word"""
    return "JohnSmith"

