def get_workflow(intent: str) -> list:
    if intent == "sales":

        workflow = ["CRM Agent", "Lead Agent",
            {
                "parallel": [
                    "Notification Agent",
                    "Chat Agent"
                ]
            },
        ]

        visualization(workflow)
        return workflow

    return []


def visualization(workflow: list) -> str:
    print("Workflow Visualization:")
    for step in workflow:
        if isinstance(step, dict) and "parallel" in step:
            print("---------------------------")
            for i in range(len(step["parallel"])):
                print(" | ", end="\t\t\t")
            print()
            for parallel_step in step["parallel"]:
                print(f"{parallel_step}", end="\t")
            print()
        else:
            print(f"\t{step}", end="\n\t|\n")


if __name__ == "__main__":
    intent = "sales"
    workflow = get_workflow(intent)