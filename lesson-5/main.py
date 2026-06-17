from graph import graph

print("Multi-Agent Support System")
print("Type exit to quit")

while True:

    query = input("\nUser: ")

    if query.lower() == "exit":
        break

    result = graph.invoke(
        {
            "query": query
        }
    )

    print("\nAssistant:")
    print(result["response"])