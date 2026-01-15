from langchain_classic.memory import ConversationBufferMemory


memory_store = {}

def get_memory(session_id : str) :
    if session_id not in memory_store:
        memory_store[session_id] = ConversationBufferMemory(
            return_messages=True
        )
    return memory_store[session_id]