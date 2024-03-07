from llama_index.core.tools import QueryEngineTool, ToolMetadata

#from response_enginefrom_index import ResponseEngine


class QueryEngineSetup:
    def __init__(self,llm):
        self.llm = llm


    def get_query_engine_array(self,db_name,response_engine):
        #chat_engine = response_engine.as_chat_engine(db_name, 1024, llm=self.llm)


        query_engine_tools = [
            QueryEngineTool(
                query_engine=response_engine,
                metadata=ToolMetadata(
                    name="startup_context",
                    description=(
                        "Information and documentation relevant to the use of Apteco Orbit software including documentation."                        
                        "Use any question regarding marketing, or using Apteco software as input to the tool."
                        "Any answer regarding Apteco Orbit should match the information retrieved."
                    ),
                ),
            )

        ]

        return query_engine_tools