from agents.supervisor import graph
from langchain_core.messages import HumanMessage

def main():
    print("Чат-бот запущен. Введите 'exit' для выхода.")
    messages = []
    config = {"configurable": {"thread_id": "1"}}
    
    while True:
        try:
            user_input = input("\nВы: ")
            if user_input.lower() == 'exit':
                break
                
            messages.append(HumanMessage(content=user_input))
            response = graph.invoke({"messages": messages}, config)
            
            if response and "messages" in response:
                messages = response["messages"]
                if messages:
                    print(f"\nБот: {messages[-1].content}")
                    
        except Exception as e:
            print(f"\nОшибка: {str(e)}")
    
    print("\nЧат завершен. До свидания!")

if __name__ == "__main__":
    main()
