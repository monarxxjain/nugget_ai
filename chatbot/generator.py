from typing import Tuple
from langchain_google_genai import ChatGoogleGenerativeAI
from retriever import get_relevant_chunks
from datetime import datetime
from utils.logger import get_logger
from config.rag_config import GENERATION_MODEL, TEMPERATURE, TOP_P
from dotenv import load_dotenv
from tools import TOOLS
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_community.cache import SQLiteCache
from langchain.globals import set_llm_cache
from prompt import CONTEXTULIZE_SYSTEM_PROMPT, SYSTEM_PROMPT
import uuid

set_llm_cache(SQLiteCache(database_path=".langchain.db"))

load_dotenv()

logger = get_logger()

llm = ChatGoogleGenerativeAI(
    model=GENERATION_MODEL,
    temperature=TEMPERATURE,
    top_p=TOP_P,
)

# Simple in-memory chat history manager
chats_by_session_id = {}


def get_chat_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in chats_by_session_id:
        chats_by_session_id[session_id] = InMemoryChatMessageHistory()
    return chats_by_session_id[session_id]


def generate_answer(query: str, session_id: str = None) -> Tuple[str]:
    logger.info(f"[+] Generating answer for query: {query}")
    logger.info("[+] Retrieving context...")

    if session_id is None:
        session_id = str(uuid.uuid4())  # Auto-create if missing
    chat_history = get_chat_history(session_id)

    reformulated_query = reformulate_question(query, chat_history.messages)
    logger.info(f"[+] Reformulated Query: {reformulated_query}")

    # Get context based on standalone version
    context_chunks = get_relevant_chunks(reformulated_query)

    context = "\n".join(context_chunks)

    logger.debug(f"[+] Retrieved context: {context}")

    history_raw = []
    history_messages = chat_history.messages.copy()
    for message in history_messages:
        if isinstance(message, HumanMessage):
            history_raw.append(("human", message.content))
        elif isinstance(message, AIMessage):
            history_raw.append(("ai", message.content))
        else:
            continue
    history_raw.insert(0, ("system", SYSTEM_PROMPT))
    history_raw.append(("human", "{input}"))
    history_raw.append(("placeholder", "{agent_scratchpad}"))
    messages_template = ChatPromptTemplate.from_messages(history_raw)

    agent = create_tool_calling_agent(llm, TOOLS, messages_template)
    agent_executor = AgentExecutor(agent=agent, tools=TOOLS, verbose=False)

    # Prepare agent input
    inputs = {
        "input": query,
        "date_and_time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "context": context,
    }

    # Invoke agent
    response = agent_executor.invoke(inputs)

    output_text = response["output"]
    logger.info(f"[+] Response: {output_text}")

    # Save conversation
    chat_history.add_messages(
        [HumanMessage(content=query), AIMessage(content=output_text)]
    )

    return (output_text.strip(), session_id)

def reformulate_question(query: str, chat_history: list[BaseMessage]) -> str:
    """
    Reformulate a user query into a standalone question using the conversation history.
    """
    if not chat_history:
        return query

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", CONTEXTULIZE_SYSTEM_PROMPT),
            *[(m.type, m.content) for m in chat_history if m.type != "system"],
            ("human", "{input}"),
        ]
    )

    chain = prompt | llm | StrOutputParser()

    reformulated_question = chain.invoke({"input": query})

    logger.info("[+] Reformulated question: %s", reformulated_question)

    return reformulated_question.strip()