facts = {
    "HighAttendance",
    "CGPAAbove7",
    "PassedAllSubjects",
    "SubmittedAssignments",
    "CompletedProjects",
}

rules = [
    ("GoodAcademicPerformance", ["CGPAAbove7", "PassedAllSubjects"]),         
    ("RegularStudent",          ["HighAttendance", "SubmittedAssignments"]),   
    ("PlacementReady",          ["GoodAcademicPerformance", "RegularStudent"]),
    ("EligibleForPlacement",    ["PlacementReady", "CompletedProjects"]),     
    ("NeedsExtraPractice",      ["LowCGPA", "BacklogSubjects"]),               
]

def backward_chain(goal, depth=0, in_progress=None):
    if in_progress is None:
        in_progress = set()
    indent = "    " * depth

    print(f"{indent}GOAL: Can we prove '{goal}'?")

    if goal in facts:
        print(f"{indent}  -> '{goal}' is a known FACT. PROVED")
        return True

    if goal in in_progress:
        print(f"{indent}  -> '{goal}' is already being proved (cycle). FAILED")
        return False
    in_progress = in_progress | {goal}

    matching = [(i + 1, r) for i, r in enumerate(rules) if r[0] == goal]
    if not matching:
        print(f"{indent}  -> No fact and no rule concludes '{goal}'. FAILED")
        return False

    for num, (concl, conditions) in matching:
        print(f"{indent}  Using R{num}: IF {' AND '.join(conditions)} THEN {concl}")
        if all(backward_chain(c, depth + 1, in_progress) for c in conditions):
            print(f"{indent}  -> All conditions of R{num} hold, so '{goal}' PROVED")
            return True
        print(f"{indent}  -> R{num} failed for '{goal}'")

    return False


if __name__ == "__main__":
    print("Known facts:", sorted(facts))
    print()

    for goal in ["EligibleForPlacement", "NeedsExtraPractice"]:
        print("=" * 60)
        print(f"Selected goal: {goal}")
        print("=" * 60)
        result = backward_chain(goal)
        print()
        if result:
            print(f"FINAL CONCLUSION: '{goal}' is TRUE for this student.")
        else:
            print(f"FINAL CONCLUSION: '{goal}' cannot be proved (FALSE).")
        print()