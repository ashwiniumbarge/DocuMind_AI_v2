from core.memory import memory

memory.add_user_message("What is Machine Learning?")
memory.add_assistant_message("Machine Learning is a subset of AI.")

memory.add_user_message("Explain Decision Tree.")
memory.add_assistant_message("Decision Tree is a supervised learning algorithm.")

print(memory.get_messages())

print("\nPrompt Format:\n")
print(memory.to_prompt())

memory.clear()

print("\nAfter Clear:")
print(memory.get_messages())