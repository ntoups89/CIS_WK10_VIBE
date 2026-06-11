#Nathaniel Toups
#CIS261
#WK10 VIBE Coding

import os

DATA_FILE = 'student_grades.txt'
 
student_records = [] 
 
def calculate_average_and_grade(scores): 
    if not scores: 
        return 0.0, 'N/A' 
    total_score = sum(scores) 
    average = total_score / len(scores) 
    if 90 <= average <= 100: 
        grade = 'A' 
    elif 80 <= average < 90: 
        grade = 'B' 
    elif 70 <= average < 80: 
        grade = 'C' 
    elif 60 <= average < 70: 
        grade = 'D' 
    else: 
        grade = 'F' 
    return round(average, 2), grade
 
def load_records():  
    global student_records 
    student_records = [] 
    if os.path.exists(DATA_FILE): 
        with open(DATA_FILE, 'r') as f: 
            for line in f: 
                try: 
                    parts = line.strip().split('|') 
                    if len(parts) >= 3: 
                        student_id = parts[0] 
                        name = parts[1] 
                        scores_str = parts[2:] 
                        scores = [int(s) for s in scores_str if s.isdigit()] 
                        average, grade = calculate_average_and_grade(scores) 
                        student_records.append({ 
                            'id': student_id, 
                            'name': name, 
                            'scores': scores, 
                            'average': average, 
                            'grade': grade 
                            }) 
                except ValueError: 
                    print(f"Warning: Skipping malformed line in {DATA_FILE}: {line.strip()}") 
    print(f"Loaded {len(student_records)} student records.") 

def save_records(): 
    with open(DATA_FILE, 'w') as f: 
        for student in student_records: 
            scores_str = '|'.join(map(str, student['scores'])) 
            f.write(f"{student['id']}|{student['name']}|{scores_str}\n") 
    print(f"Saved {len(student_records)} student records.") 

def get_next_id():  
    if not student_records: 
        return 'S001'  
    max_id_num = 0 
    for student in student_records: 
        try: 
            num_part = int(student['id'][1:])  
            if num_part > max_id_num: 
                max_id_num = num_part 
        except (ValueError, IndexError): 
            continue  
    return f"S{max_id_num + 1:03d}" 
 
def add_student():  
    print("\n--- Add New Student ---") 
    name = input("Enter student name: ").strip() 
    if not name: 
        print("Student name cannot be empty.") 
        return 
     
    for student in student_records: 
        if student['name'].lower() == name.lower(): 
            print(f"Error: Student with name '{name}' already exists.") 
            return 
    scores = [] 
    while True: 
        score_input = input("Enter test score (or 'done' to finish): ").strip() 
        if score_input.lower() == 'done': 
            break 
        try: 
            score = int(score_input) 
            if 0 <= score <= 100: 
                scores.append(score) 
            else: 
                print("Score must be between 0 and 100.") 
        except ValueError: 
            print("Invalid input. Please enter a number or 'done'.") 
    student_id = get_next_id() 
    average, grade = calculate_average_and_grade(scores) 
    student_records.append({ 
        'id': student_id, 
        'name': name, 
        'scores': scores, 
        'average': average, 
        'grade': grade 
        }) 
    print(f"Student '{name}' (ID: {student_id}) added successfully.") 
    save_records() 

def view_all_students():  
    print("\n--- ALL STUDENT RECORDS ---") 
    if not student_records: 
        print("No student records found.") 
        return 
    print(f"{'ID':<5} {'Name':<20} {'Scores':<20} {'Average':<10} {'Grade':<5}") 
    print("-" * 70) 
    for student in student_records: 
        scores_display = ', '.join(map(str, student['scores'])) 
        print(f"{student['id']:<5} {student['name']:<20} {scores_display:<20} {student['average']:<10.2f} {student['grade']:<5}") 
    print("-" * 70) 
    print(f"Total students: {len(student_records)}") 
    
def search_student_by_name():  
    print("\n--- Search Student by Name ---") 
    search_name = input("Enter student name to search: ").strip().lower() 
    found_students = [student for student in student_records if search_name in student['name'].lower()] 
    if not found_students: 
        print(f"Record not found for '{search_name}'.") 
    else: 
        print(f"Found {len(found_students)} student(s) matching '{search_name}':") 
        print(f"{'ID':<5} {'Name':<20} {'Scores':<20} {'Average':<10} {'Grade':<5}") 
        print("-" * 70) 
        for student in found_students: 
            scores_display = ', '.join(map(str, student['scores'])) 
            print(f"{student['id']:<5} {student['name']:<20} {scores_display:<20} {student['average']:<10.2f} {student['grade']:<5}") 
        print("-" * 70) 

def update_student_scores():  
    print("\n--- Update Student Scores ---") 
    student_id_to_update = input("Enter student ID to update scores: ").strip().upper() 
    found_student = None 
    for student in student_records: 
        if student['id'] == student_id_to_update: 
            found_student = student 
            break 
    if not found_student: 
        print(f"Student with ID '{student_id_to_update}' not found.") 
        return 
    print(f"Updating scores for: {found_student['name']} (ID: {found_student['id']})") 
    print(f"Current scores: {', '.join(map(str, found_student['scores']))}") 
    new_scores = [] 
    while True: 
        score_input = input("Enter new test score (or 'done' to finish, 'keep' to retain current scores): ").strip() 
        if score_input.lower() == 'done': 
            break 
        if score_input.lower() == 'keep': 
            new_scores = found_student['scores']  
            break 
        try: 
            score = int(score_input) 
            if 0 <= score <= 100: 
                new_scores.append(score) 
            else: 
                print("Score must be between 0 and 100.") 
        except ValueError: 
            print("Invalid input. Please enter a number, 'done', or 'keep'.") 
    if new_scores: 
        found_student['scores'] = new_scores 
        found_student['average'], found_student['grade'] = calculate_average_and_grade(new_scores) 
        print(f"Scores for {found_student['name']} updated successfully.") 
        save_records() 
    else: 
        print("No new scores entered. Scores not updated.") 

def delete_student():  
    print("\n--- Delete Student ---") 
    student_id_to_delete = input("Enter student ID to delete: ").strip().upper() 
    global student_records 
    initial_count = len(student_records) 
    student_records = [student for student in student_records if student['id'] != student_id_to_delete] 
    if len(student_records) < initial_count: 
        print(f"Student with ID '{student_id_to_delete}' deleted successfully.") 
        save_records() 
    else: 
        print(f"Student with ID '{student_id_to_delete}' not found.") 
 
def main_menu():  
    load_records() # Load records at startup 
    while True: 
        print("\n--- Student Grade Calculator Menu ---") 
        print("1. Add New Student") 
        print("2. View All Students") 
        print("3. Search Student by Name") 
        print("4. Update Student Scores") 
        print("5. Delete Student") 
        print("6. Exit (Press ESC key to exit)") 
             
        choice = input("Enter your choice (1-6): ").strip() 
        
        if choice == '1': 
            add_student() 
        elif choice == '2': 
            view_all_students() 
        elif choice == '3': 
            search_student_by_name() 
        elif choice == '4': 
            update_student_scores() 
        elif choice == '5': 
            delete_student() 
        elif choice == '6': 
            print("Exiting Student Grade Calculator. Goodbye!") 
            break 
        else: 
            print("Invalid choice. Please enter a number between 1 and 6.") 
 
if __name__ == "__main__": 
    main_menu()