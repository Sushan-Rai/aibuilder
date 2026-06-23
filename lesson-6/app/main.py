from agent import run_agent


while True:

    q=input("User: ")

    print(
        "Agent:",
        run_agent(q)
    )