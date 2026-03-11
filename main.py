class VotingSystem:

    def __init__(self):

        # fixed accounts
        self.admin_username = "admin"
        self.admin_password = "1234"

        self.user_username = "user"
        self.user_password = "1234"

        # poll data
        self.poll_title = ""
        self.is_active = False
        self.candidates = {}
        self.votes = {}

    # ---------------- USER LOGIN ----------------
    def user_login(self):

        print("\n=== USER LOGIN ===")

        username = input("Username: ")
        password = input("Password: ")

        if username == self.user_username and password == self.user_password:
            print("Login Successful!")
            self.user_dashboard()
        else:
            print("Invalid Login")

    # ---------------- USER DASHBOARD ----------------
    def user_dashboard(self):

        if not self.is_active:
            print("No active poll.")
            return

        print("\nActive Poll:", self.poll_title)

        for position in self.candidates:

            print(f"\nPosition: {position}")

            for i, name in enumerate(self.candidates[position], start=1):
                print(i, name)

            choice = int(input("Select candidate number: "))
            candidate = self.candidates[position][choice - 1]

            key = (position, candidate)

            if key in self.votes:
                self.votes[key] += 1
            else:
                self.votes[key] = 1

        print("\nVote Submitted!")

    # ---------------- ADMIN LOGIN ----------------
    def admin_login(self):

        print("\n=== ADMIN LOGIN ===")

        username = input("Admin Username: ")
        password = input("Admin Password: ")

        if username == self.admin_username and password == self.admin_password:
            self.admin_panel()
        else:
            print("Invalid Admin Login")

    # ---------------- ADMIN PANEL ----------------
    def admin_panel(self):

        while True:

            print("\n=== ADMIN PANEL ===")
            print("1. Create Poll")
            print("2. Activate Poll")
            print("3. Add Candidate")
            print("4. View Results")
            print("5. Back")

            choice = input("Select: ")

            if choice == "1":
                self.poll_title = input("Poll Title: ")
                print("Poll Created!")

            elif choice == "2":
                self.is_active = True
                print("Poll Activated!")

            elif choice == "3":

                position = input("Position: ")
                name = input("Candidate Name: ")

                if position not in self.candidates:
                    self.candidates[position] = []

                self.candidates[position].append(name)

                print("Candidate Added!")

            elif choice == "4":

                print("\n=== RESULTS ===")

                for key, count in self.votes.items():
                    position, candidate = key
                    print(f"{position} - {candidate} : {count} votes")

            elif choice == "5":
                break

    # ---------------- MAIN MENU ----------------
    def run(self):

        while True:

            print("\n===== SCHOOL VOTING SYSTEM =====")
            print("1. User Login")
            print("2. Admin Login")
            print("3. Exit")

            choice = input("Select: ")

            if choice == "1":
                self.user_login()

            elif choice == "2":
                self.admin_login()

            elif choice == "3":
                print("Goodbye")
                break


# ---------------- RUN PROGRAM ----------------
app = VotingSystem()
app.run()
