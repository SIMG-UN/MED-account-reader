from sqlalchemy.engine import Engine
from ..toolkit import PostgresToolKit
from typing import TypedDict, Annotated, List, Literal

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage

from langgraph.graph.state import CompiledStateGraph
from langgraph.graph import add_messages, StateGraph, START, END
from langgraph.prebuilt import ToolNode


def create_SQL_agent(llm : BaseChatModel, engine : Engine) -> CompiledStateGraph:

    toolkit = PostgresToolKit(engine=engine)
    tools = toolkit.get_tools()

    llm_with_tools = llm.bind_tools(tools=tools)

    class State(TypedDict):
        messages = Annotated[List[BaseMessage], add_messages]

    tool_invoker = ToolNode(tools=tools, messages_key="messages")
    

    def ReAct_node(state : State) -> State:
        messages = state["messages"]

        ai_message = llm_with_tools.invoke(messages)
        
        return {"messages":ai_message}
    

    def tool_node_wrapper(state : State) -> State:
        tools_response = tool_invoker.invoke(state)
        return tools_response



    def should_end(state : State) -> Literal["tool_node_wrapper", END]: # type: ignore
        last_ai_message = state["message"][-1]
        if last_ai_message.tool_calls:
            return "tool_node_wrapper"
        return END
    

    builder = StateGraph(State)

    builder.add_node("ReAct_node", ReAct_node)
    builder.add_node("tool_node_wrapper", tool_node_wrapper)

    builder.add_edge(START, "ReAct_node")
    builder.add_conditional_edges("ReAct_node", should_end)
    builder.add_edge("tool_node_wrapper", tool_node_wrapper)

    return builder.compile()





if __name__=="__main__":
    
    pass