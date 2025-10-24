
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import sys
import warnings
warnings.filterwarnings('ignore', category=UserWarning)

# Initialize Firebase
try:
    cred = credentials.Certificate('serviceAccountKey.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("Connected to Firebase!\n")
except Exception as e:
    print(f"Firebase Error: {e}")
    sys.exit(1)

current_user = None

# Create user account

def register_user():
    print("\nREGISTER USER ")
    username = input("Username: ").strip()
    if not username:
        print("Username required")
        return

    users = db.collection('users')
    if list(users.where('username', '==', username).limit(1).stream()):
        print("Username taken")
        return
    
    name = input("Full name: ").strip()
    try:
        age = int(input("Age: "))
        weight = float(input("Weight (kg): "))
    except ValueError:
        print("Invalid input!")
        return
    
    users.add({
        'username': username,
        'name': name,
        'age': age,
        'weight_kg': weight,
        'created_at': datetime.now()
    })
    print(f"User '{username}' created!")

# Create activity log

def log_activity():
    if not current_user:
        print("Login required")
        return
    
    print("\nLOG ACTIVITY")
    print("Types: Running, Cycling, Swimming, Gym, Walking, Other")
    activity_type = input("Activity type: ").strip()
    
    try:
        duration = int(input("Duration (minutes): "))
        calories = int(input("Calories burned: "))
    except ValueError:
        print("Invalid input!")
        return
    
    db.collection('activities').add({
        'user_id': current_user['id'],
        'activity_type': activity_type,
        'duration_minutes': duration,
        'calories_burned': calories,
        'date': datetime.now()
    })
    print(f"✓ {activity_type} logged")

# User login

def login_user():
    global current_user
    print("\nLOGIN")
    username = input("Username: ").strip()
    
    users = db.collection('users')
    user_docs = list(users.where('username', '==', username).limit(1).stream())
    
    if not user_docs:
        print("User not found")
        return False
    
    user = user_docs[0]
    current_user = {
        'id': user.id,
        'username': user.to_dict()['username'],
        'name': user.to_dict()['name']
    }
    print(f"Welcome, {current_user['name']}")
    return True

# View user activities

def view_activities():
    if not current_user:
        print("Login required")
        return
    
    print(f"\n{current_user['name']}'s ACTIVITIES")
    
    activities = db.collection('activities')
    user_activities = list(activities.where('user_id', '==', current_user['id']).stream())
    
    if not user_activities:
        print("No activities yet. Select option 3 to create log.")
        return
    
    print(f"Total: {len(user_activities)} activities\n")
    
    for i, activity in enumerate(user_activities, 1):
        data = activity.to_dict()
        date = data['date'].strftime('%Y-%m-%d')
        print(f"{i}. {data['activity_type']} - {data['duration_minutes']}min - {data['calories_burned']}cal")
        print(f"   Date: {date} | ID: {activity.id}")
        print()

# Update Activity

def update_activity():
    if not current_user:
        print("Login required")
        return
    
    print("\nUPDATE ACTIVITY")
    activity_id = input("Activity ID: ").strip()
    
    try:
        activity_ref = db.collection('activities').document(activity_id)
        activity = activity_ref.get()
        
        if not activity.exists:
            print("Activity not found")
            return
        
        data = activity.to_dict()
        
        if data['user_id'] != current_user['id']:
            print("Invalid ID")
            return
        
        print(f"\nCurrent: {data['activity_type']} - {data['duration_minutes']}min - {data['calories_burned']}cal")
        print("\nUpdate:")
        print("1. Duration")
        print("2. Calories")
        
        choice = input("Select (1-2): ").strip()
        
        if choice == '1':
            new_val = int(input("New duration (min): "))
            activity_ref.update({'duration_minutes': new_val})
            print("Duration updated")
        elif choice == '2':
            new_val = int(input("New calories: "))
            activity_ref.update({'calories_burned': new_val})
            print("Calories updated")
        else:
            print("Invalid choice")
            
    except Exception as e:
        print(f"Error: {e}")

# Delete Activity

def delete_activity():
    if not current_user:
        print("Login required")
        return
    
    print("\nDELETE ACTIVITY")
    activity_id = input("Activity ID: ").strip()
    
    try:
        activity_ref = db.collection('activities').document(activity_id)
        activity = activity_ref.get()
        
        if not activity.exists:
            print("Activity not found")
            return
        
        data = activity.to_dict()

        if data['user_id'] != current_user['id']:
            print("Not your activity")
            return
        
        print(f"\nActivity: {data['activity_type']} - {data['date'].strftime('%Y-%m-%d')}")
        confirm = input("Delete? (yes/no): ").lower()
        
        if confirm == 'yes':
            activity_ref.delete()
            print("Deleted")
        else:
            print("Cancelled.")
            
    except Exception as e:
        print(f"Error: {e}")

# Main Screen

def main():
    global current_user
    
    print("  HEALTH & FITNESS TRACKER")
    
    while True:
        print("\n" + "=" * 50)
        if current_user:
            print(f"Logged in: {current_user['name']}")
        
        print("\n1. Register User")
        print("2. Login")
        print("3. Log Activity")
        print("4. View Activities")
        print("5. Update Activity")
        print("6. Delete Activity")
        print("7. Logout" if current_user else "7. N/A")
        print("0. Exit")
        
        choice = input("\nOption: ").strip()
        
        if choice == '1':
            register_user()
        elif choice == '2':
            login_user()
        elif choice == '3':
            log_activity()
        elif choice == '4':
            view_activities()
        elif choice == '5':
            update_activity()
        elif choice == '6':
            delete_activity()
        elif choice == '7':
            if current_user:
                print(f"\nGoodbye, {current_user['name']}!")
                current_user = None
            else:
                print("\nGoodbye!")
                sys.exit(0)
        elif choice == '0':
            print("\nGoodbye!")
            sys.exit(0)
        else:
            print("Invalid option")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)