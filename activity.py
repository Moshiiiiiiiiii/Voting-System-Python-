import sqlite3


# BASE CLASS
class Person:
    def __init__(self, username, age):
        self.username = username
        self.age = age

    def info(self):
        return f"{self.username} ({self.age})"


# DERIVED CLASS - STUDENT
class Student(Person):

    def vote(self):
        return f"{self.username} is voting."


# DERIVED CLASS - ADMIN
class Admin(Person):

    def manage(self):
        return f"{self.username} is managing the voting system."


# MULTIPLE INHERITANCE
class StudentAdmin(Student, Admin):

    def full_access(self):
        return f"{self.username} has student and admin privileges."


# VOTING SYSTEM
class VotingSystem:

    def __init__(self):

        self.admin_username = "admin"
        self.admin_password = "1234"

        self.conn = sqlite3.connect("voters.db")
        self.cursor = self.conn.cursor()

        self.create_tables()

    # CREATE TABLES
    def create_tables(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            age INTEGER,
            password TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS polls(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            is_active INTEGER DEFAULT 0
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidates(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            poll_id INTEGER,
            position TEXT,
            name TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS votes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            poll_id INTEGER,
            position TEXT,
            candidate TEXT
        )
        """)

        self.conn.commit()

    # MAIN MENU
    def main(self):

        while True:

            print("\n====== SCHOOL VOTING SYSTEM ======")
            print("1. REGISTER")
            print("2. USER LOGIN")
            print("3. ADMIN LOGIN")
            print("4. EXIT")

            choice = input("Select: ")

            if choice == "1":
                self.register()

            elif choice == "2":
                self.login()

            elif choice == "3":
                self.admin_login()

            elif choice == "4":
                print("Thank you for using the program.")
                break

            else:
                print("Invalid choice!")

    # REGISTER
    def register(self):

        print("\n=== REGISTER ===")

        username = input("Enter Name: ")
        age = input("Enter Age: ")
        password = input("Enter Password: ")

        if not username or not age or not password:
            print("All fields required!")
            return

        if not age.isdigit():
            print("Age must be a number!")
            return

        if int(age) < 18:
            print("Not eligible to vote.")
            return

        try:

            self.cursor.execute(
                "INSERT INTO users(username,age,password) VALUES(?,?,?)",
                (username, int(age), password),
            )

            self.conn.commit()

            print("Registration Successful!")

        except sqlite3.IntegrityError:
            print("User already exists.")

    # USER LOGIN
    def login(self):

        print("\n=== USER LOGIN ===")

        username = input("Username: ")
        password = input("Password: ")

        self.cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password),
        )

        user = self.cursor.fetchone()

        if user:

            student = Student(user[1], user[2])
            print(student.vote())

            self.user_dashboard(username)

        else:
            print("Invalid login.")

    # ADMIN LOGIN
    def admin_login(self):

        print("\n=== ADMIN LOGIN ===")

        username = input("Admin Username: ")
        password = input("Admin Password: ")

        if username == self.admin_username and password == self.admin_password:

            admin = Admin(username, 40)
            print(admin.manage())

            self.admin_panel()

        else:
            print("Invalid admin login.")

    # USER DASHBOARD
    def user_dashboard(self, username):

        print(f"\nWelcome {username}")

        self.cursor.execute("SELECT id,title FROM polls WHERE is_active=1")
        poll = self.cursor.fetchone()

        if not poll:
            print("No active poll.")
            return

        poll_id = poll[0]
        print("\nActive Poll:", poll[1])

        self.cursor.execute(
            "SELECT DISTINCT position FROM candidates WHERE poll_id=?",
            (poll_id,),
        )

        positions = self.cursor.fetchall()

        letters = "abcdefghijklmnopqrstuvwxyz"

        for pos in positions:

            position = pos[0]
            print(f"\nPosition: {position}")

            self.cursor.execute(
                "SELECT name FROM candidates WHERE poll_id=? AND position=?",
                (poll_id, position),
            )

            candidates = self.cursor.fetchall()

            for i, cand in enumerate(candidates):
                print(f"{letters[i]}. {cand[0]}")

            if not candidates:
                print("No candidates.")
                continue

            while True:

                choice = input(
                    f"Select candidate ({letters[0]}-{letters[len(candidates)-1]}): "
                ).lower()

                if choice in letters[: len(candidates)]:
                    candidate = candidates[letters.index(choice)][0]
                    break
                else:
                    print("Invalid choice!")

            self.cursor.execute(
                "INSERT INTO votes(username,poll_id,position,candidate) VALUES(?,?,?,?)",
                (username, poll_id, position, candidate),
            )

            self.conn.commit()

        print("\nVote Submitted!")

    # ADMIN PANEL
    def admin_panel(self):

        super_user = StudentAdmin("SystemAdmin", 40)
        print(super_user.full_access())

        while True:

            print("\n=== ADMIN PANEL ===")
            print("1. Create Poll & Add Candidates")
            print("2. Activate Poll")
            print("3. View Results")
            print("4. Logout")

            choice = input("Select: ")

            # CREATE POLL
            if choice == "1":

                title = input("Enter Poll Title: ")

                self.cursor.execute(
                    "INSERT INTO polls(title,is_active) VALUES(?,0)",
                    (title,),
                )

                self.conn.commit()

                poll_id = self.cursor.lastrowid

                while True:

                    position = input("Enter Position (or 'done'): ")

                    if position.lower() == "done":
                        break

                    while True:

                        name = input("Candidate Name (or 'done'): ")

                        if name.lower() == "done":
                            break

                        self.cursor.execute(
                            "INSERT INTO candidates(poll_id,position,name) VALUES(?,?,?)",
                            (poll_id, position, name),
                        )

                self.conn.commit()
                print("Poll and candidates added!")

            # ACTIVATE POLL
            elif choice == "2":

                print("\n=== AVAILABLE POLLS ===")

                self.cursor.execute("SELECT title,is_active FROM polls")
                polls = self.cursor.fetchall()

                if not polls:
                    print("No polls created.")
                    continue

                for p in polls:
                    status = "ACTIVE" if p[1] == 1 else "INACTIVE"
                    print(f"{p[0]} - {status}")

                title = input("\nEnter Poll Title to Activate: ")

                self.cursor.execute("UPDATE polls SET is_active=0")

                self.cursor.execute(
                    "UPDATE polls SET is_active=1 WHERE title=?",
                    (title,),
                )

                self.conn.commit()

                print("Poll Activated!")

            # VIEW RESULTS
            elif choice == "3":

                print("\n=== AVAILABLE POLLS ===")

                self.cursor.execute("SELECT title FROM polls")
                polls = self.cursor.fetchall()

                if not polls:
                    print("No polls available.")
                    continue

                for p in polls:
                    print("-", p[0])

                title = input("\nEnter Poll Title: ")

                self.cursor.execute(
                    "SELECT id FROM polls WHERE title=?",
                    (title,),
                )

                poll = self.cursor.fetchone()

                if not poll:
                    print("Poll not found.")
                    continue

                poll_id = poll[0]

                self.cursor.execute(
                    """
                    SELECT position,candidate,COUNT(*)
                    FROM votes
                    WHERE poll_id=?
                    GROUP BY position,candidate
                    """,
                    (poll_id,),
                )

                results = self.cursor.fetchall()

                if not results:
                    print("No votes yet.")
                    continue

                print("\n=== RESULTS ===")

                for r in results:
                    print(f"{r[0]} - {r[1]} : {r[2]} votes")

            elif choice == "4":
                break

            else:
                print("Invalid choice!")


# RUN PROGRAM
if __name__ == "__main__":

    system = VotingSystem()
    system.main()