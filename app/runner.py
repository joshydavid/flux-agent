from app.workflow import ContentLoopWorkflow


class DemoRunner:
    """Manages the CLI interaction for the Graph Loop Demo."""

    def __init__(self):
        self.workflow = ContentLoopWorkflow()

    def print_welcome(self):
        print("\n🔄 Graph with Loops & MCP Tools Example\n")
        print("This example demonstrates multi-agent graphs with loops and MCP tools.")
        print("The writer agent can now use the 'fetch' tool to get web content.")
        print("\nOptions:")
        print("  'demo' - Run demo with haiku task")
        print("  'tool' - Run demo with web fetching task")
        print("  'exit' - Exit the program")
        print("\nOr enter any content creation task:")
        print("  'Write a short story about AI'")
        print("  'Create a product description for a smart watch'")

    def run(self):
        self.print_welcome()
        while True:
            try:
                user_input = input("\n> ")

                if user_input.lower() == "exit":
                    print("\nGoodbye! 👋")
                    break
                elif user_input.lower() == "demo":
                    user_input = "Write a haiku about programming loops"
                    print(f"Running demo task: {user_input}")
                elif user_input.lower() == "tool":
                    user_input = "Fetch the content of 'https://www.dell.com/en-sg/lp/edge-solutions-nativeedge' and summarize it."
                    print(f"Running tool demo task: {user_input}")

                # Run the workflow
                result = self.workflow.execute(user_input)

                # Show statistics
                self._display_results(result)

            except KeyboardInterrupt:
                print("\n\nExecution interrupted. Exiting...")
                break
            except Exception as e:
                print(f"\nAn error occurred: {str(e)}")
                print("Please try a different request.")

    def _display_results(self, result):
        path = " -> ".join([node.node_id for node in result.execution_order])
        print(f"\nExecution path: {path}")

        # Show loop statistics
        node_visits = {}
        for node in result.execution_order:
            node_visits[node.node_id] = node_visits.get(node.node_id, 0) + 1

        loops = [
            f"{node_id} ({count}x)"
            for node_id, count in node_visits.items()
            if count > 1
        ]
        if loops:
            print(f"Loops detected: {', '.join(loops)}")

        # Show final result
        if "finalizer" in result.results:
            print(f"\n✨ Final Result:\n{result.results['finalizer'].result}")
