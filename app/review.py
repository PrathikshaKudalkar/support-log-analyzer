def review_analysis(root_cause, draft_reply):
    print("\nAI Root Cause:")
    print(root_cause)

    print("\nAI Draft Reply:")
    print(draft_reply)

    while True:
        choice = input(
            "\n[a]pprove / [e]dit / [r]eject: "
        ).strip().lower()

        if choice == "a":
            return {
                "root_cause": root_cause,
                "draft_reply": draft_reply,
                "review_status": "approved",
            }

        if choice == "e":
            edited_root_cause = input(
                "\nEnter edited root cause: "
            ).strip()

            edited_reply = input(
                "Enter edited customer reply: "
            ).strip()

            return {
                "root_cause": edited_root_cause,
                "draft_reply": edited_reply,
                "review_status": "edited",
            }

        if choice == "r":
            return {
                "root_cause": root_cause,
                "draft_reply": draft_reply,
                "review_status": "rejected",
            }

        print("Please enter a, e, or r.")