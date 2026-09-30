def solve_q1():
    # Sample input from the assignment
    sample_data = """5 2 3
    1037 Dhyana 5 8.75 97 82 73
    1038 Diya 5 7.85 88 92 74
    1039 Diya 3 9.10 90 65 70
    1030 Dharmi 5 7.80 74 80 85
    1075 Mansi 3 9.10 93 77 86"""
    
    # Split the data into lines instead of individual words
    lines = sample_data.strip().split('\n')
    
    # --- 1. READ THE SETUP LINE ---
    first_line = lines[0].split()
    n = int(first_line[0]) # Number of students (5)
    k = int(first_line[1]) # Top K students to pick (2)
    m = int(first_line[2]) # Number of subjects (3)
    
    # --- 2. SETUP STORAGE ---
    semesters = {} 
    
    # Prepare storage for subject high scores
    subject_highest = {}
    subject_toppers = {}
    for i in range(m):
        subject_highest[i] = -1
        subject_toppers[i] = []
        
    # --- 3. PROCESS EACH STUDENT ---
    # Loop through lines 1 to 5
    for i in range(1, n + 1):
        # Split the current student's line into a list
        student_info = lines[i].split() 
        
        enrollment = student_info[0]
        name = student_info[1]
        sem = int(student_info[2])
        cpi = float(student_info[3])
        
        # Grab the marks (they start at position 4 in the line)
        marks = []
        for j in range(4, 4 + m):
            marks.append(int(student_info[j]))
            
        avg_marks = sum(marks) / m
        
        # Group students by semester
        if sem not in semesters:
            semesters[sem] = []
            
        # Create an easy-to-read dictionary for the student
        student_record = {
            'enrollment': enrollment,
            'cpi': cpi,
            'avg_marks': avg_marks
        }
        semesters[sem].append(student_record)
        
        # Check if they are a topper in any subject
        for subj_index in range(m):
            mark = marks[subj_index]
            
            if mark > subject_highest[subj_index]:
                subject_highest[subj_index] = mark
                subject_toppers[subj_index] = [enrollment] # Start a new list
            elif mark == subject_highest[subj_index]:
                subject_toppers[subj_index].append(enrollment) # Tie! Add them

    # --- 4. SORTING HELPER FUNCTION ---
    # We sort by CPI (High to Low), then Avg Marks (High to Low), then Enrollment (Low to High)
    # Putting a minus sign (-) makes it sort High to Low.
    def sort_rules(student):
        return (-student['cpi'], -student['avg_marks'], student['enrollment'])

    # --- 5. PRINT RESULTS ---
    for sem in sorted(semesters.keys()):
        students_in_sem = semesters[sem]
        
        # Sort them using our custom rules!
        students_in_sem.sort(key=sort_rules)
        
        # Grab only the top K students
        top_k = []
        for i in range(min(k, len(students_in_sem))):
            top_k.append(students_in_sem[i]['enrollment'])
            
        print(f"Semester {sem}: {' '.join(top_k)}")
        
    # Print Subject Toppers
    for i in range(m):
        toppers = sorted(subject_toppers[i])
        print(f"S{i+1}: {' '.join(toppers)}")

# Run the program
solve_q1()