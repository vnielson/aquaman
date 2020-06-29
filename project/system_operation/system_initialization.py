from project.valves import views


def initialize_system():
    print("In system Initialization")
    all_valves = views.close_all_valves()
    print("All Valves")
    print(all_valves)