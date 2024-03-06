from llama_index.core.tools import FunctionTool
from llama_index.core.agent import ReActAgent


class AgentSetup:
    def __init__(self, llm, db_name):
        self.llm = llm
        self.db_name = db_name

    def tool_array(self):
        tool_array = []
        multiply_tool = FunctionTool.from_defaults(fn=multiply)
        secret_word = FunctionTool.from_defaults(fn=the_secret_word)
        tool_array.append(multiply_tool)
        tool_array.append(secret_word)

        return tool_array

    def add_tools_to_query_engine(self, query_engine_tools):
        tools = self.tool_array()

        combined_tools = []
        combined_tools = query_engine_tools + tools
        return combined_tools

    def return_agent(self, mem, query_engine_tools, inbound_context):
        # context = ("You are a chatbot, specifically designed to "
        #            "advise on how to use the Apteco Orbit platform.  Your answers should only ever be about using "
        #            "Apteco software, and most answers can be found from the database.  Never suggest answers that are "
        #            "not factually based on the retrieved text."
        #            "An 'Audience', sometimes called a 'Selection' or 'Segment' is created using the Orbit Audiences "
        #            "tool.  "
        #            "Audience, selection and segment are keywords that indicate we should be using 'Orbit "
        #            "Audiences'.Here are the relevant documents for the context:\n"
        #            "{context_str}"
        #            "\nInstruction: Use the previous chat history, or the context above, to interact and help the "
        #            "user.  Where possible do not repeat earlier answers.")
        agent = ReActAgent.from_tools(self.add_tools_to_query_engine(query_engine_tools), llm=self.llm, verbose=True,
                                      memory=mem, context=inbound_context,similarity_top_k=5)
        return agent


# define sample Tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers and returns the result integer"""
    return a * b


def the_secret_word():
    """If ever asked, this is the secret word"""
    return "JohnSmith"
