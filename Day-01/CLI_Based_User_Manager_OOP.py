class User:
    def __init__(self,name,email,age):
        self.name = name
        self.email = email
        self.age = age

class UserManager:
    def __init__(self):
        self.users = {}
    
    def add_user(self):
        name = input("Enter user name: ")
        if name in self.users:
            print("User already exists")
        else:
            email = input("Enter email id: ")
            print("Enter age: ",end="")
            try:
                age = int(input())
            except ValueError:
                print("Enter valid age")
                return
            u1 = User(name,email,age)
            self.users[name] = u1
    
    def view_users(self):
        if not self.users :
            print("No users found")
            return
        
        for x in self.users:
            print("Name: ",self.users[x].name)
            print("Email: ",self.users[x].email)
            print("age: ",self.users[x].age)
            print("")

    def delete_user(self,user_name):
        if user_name not in self.users:
            print("User not found")
            return
        else:
            del self.users[user_name]
            print("User is deleted")

    def update_user(self,user_name):
        if user_name not in self.users:
            print("User not found")
            return
        else:
            while 1:
                print("select an option to continue: ")
                print("1. update user name")
                print("2. update email id")
                print("3. update age")
                print("type any key to exit")
                print("Enter an option: ",end="")
                opt = input()
                if opt=="1":
                    new_name = input("Enter new username: ")
                    if new_name in self.users:
                        print("User name already exists")
                    else:
                        self.users[new_name] = self.users.pop(user_name)
                        self.users[new_name].name = new_name
                        user_name = new_name
                        print("new user name updated")
                
                elif opt == "2":
                    print("Enter new email address: ",end="")
                    new_email = input()
                    self.users[user_name].email = new_email
                    print("Email is updated") 
                elif opt == "3":
                    print("Enter new age: ",end="")
                    try:
                        new_age = int(input())
                    except ValueError:
                        print("Invalid age")
                        continue
                    self.users[user_name].age = new_age
                    print("Age is updated")
                else:
                    print("exiting update function...")
                    print("")
                    break

start = UserManager()
while 1:
    print("")
    print("Select a choice to proceed: ")
    print("1. Add user")
    print("2. View user")
    print("3. Update users")
    print("4. Delete user")
    print("5. Exit")
    print("")
    print("Enter your choice: ",end="")
    try:
        x = int(input())
    except ValueError:
        print("Invalid choice")
        continue

    if x==1:
        start.add_user()
    elif x==2:
        start.view_users()
    elif x==3:
        username = input("Enter the user name: ")
        start.update_user(username)
    elif x==4:
        username = input("Enter the user name: ")
        start.delete_user(username)
    elif x==5:
        print("exiting user manager....")
        print()
        break
    else:
        continue