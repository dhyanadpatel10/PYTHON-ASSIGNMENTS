def solve_q2():
    sample_data ="""3
admin
college
qwerty
11
Valid1@
MyPass9$
A1@b
VeryLongPassword123@
lowercase1@
UPPERCASE1@
NoNumbers@
NoSpecial123
Paaaass1@
AdminUser1@
college99#A"""

    lines = sample_data.split('\n')
    
    b = int(lines[0])
    banned_words = []
    for i in range(1, b + 1):
        banned_words.append(lines[i].lower()) # Store banned words in lowercase
        
    n = int(lines[b + 1])
    passwords = lines[b + 2 : b + 2 + n]
    
    # Check each password
    for index in range(len(passwords)):
        pwd = passwords[index]
        pwd_number = index + 1
        
        # 1. Check length
        if len(pwd) < 6 or len(pwd) > 12:
            print(f"{pwd_number}: WEAK_LENGTH")
            continue
            
        # 2. Check for required character types
        has_lower = False
        has_upper = False
        has_digit = False
        has_special = False
        
        for char in pwd:
            if char.islower(): has_lower = True
            elif char.isupper(): has_upper = True
            elif char.isdigit(): has_digit = True
            elif char in "$#@": has_special = True
            
        if not (has_lower and has_upper and has_digit and has_special):
            print(f"{pwd_number}: WEAK_PATTERN")
            continue
            
        # 3. Check for 3 consecutive repeating characters
        repeating = False
        for i in range(len(pwd) - 3):
            if pwd[i] == pwd[i+1] == pwd[i+2] == pwd[i+3]:
                repeating = True
                break
                
        if repeating:
            print(f"{pwd_number}: WEAK_PATTERN")
            continue
            
        # 4. Check for banned words
        pwd_lower = pwd.lower()
        is_compromised = False
        for banned in banned_words:
            if banned in pwd_lower:
                is_compromised = True
                break
                
        if is_compromised:
            print(f"{pwd_number}: COMPROMISED")
        else:
            print(f"{pwd_number}: STRONG")

# Run the program
solve_q2()
