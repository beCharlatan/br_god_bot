from agents.graph import graph
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

def main():
    print("Чат-бот запущен. Введите 'exit' для выхода.")
    messages = []
    config = {"configurable": {"thread_id": "1"}}
    
    while True:
        try:
            user_input = input("\nВы: ")
            if user_input.lower() == 'exit':
                break
                    
            # Create a proper HumanMessage object
            messages.append(HumanMessage(content=user_input))
            
            try:
                state = graph.invoke({"messages": messages}, config)
                if state and "messages" in state:
                    messages = state["messages"]
                    if messages and len(messages) > 0:
                        last_message = messages[-1]
                        if isinstance(last_message, (AIMessage, SystemMessage)):
                            print(f"\nБот: {last_message.content}")
            except Exception as e:
                print(f"\nПроизошла ошибка: {str(e)}\n")
                
        except Exception as e:
            print(f"\nОшибка: {str(e)}")
    
    print("\nЧат завершен. До свидания!")

if __name__ == "__main__":
    main()
