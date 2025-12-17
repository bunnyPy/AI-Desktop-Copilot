from planner import create_plan
from executor import execute_plan

if __name__ == "__main__":
    user_goal = input("\nWhat do you want to do?\n> ")

    print("\n🧠 Planning...")
    plan = create_plan(user_goal)

    print("\n📋 Plan:")
    for step in plan:
        print(step)

    print("\n⚙️ Executing...")
    results = execute_plan(plan)

    print("\n✅ Results:")
    for r in results:
        print(r)
