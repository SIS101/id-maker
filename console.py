import Models

def print_response(response: dict):
    if response["success"]:
        if response["data"]:
            print(response["data"])
        else:
            print(response["message"])
    else:
        print(response["message"])

#Students functions
def install_students():
    studentsModel = Models.StudentsModel()
    response = studentsModel.up()
    print_response(response)
    studentsModel.conn.close()

def uninstall_students():
    studentsModel = Models.StudentsModel()
    response = studentsModel.down()
    print_response(response)
    studentsModel.conn.close()

def show_students():
    studentsModel = Models.StudentsModel()
    students = studentsModel.all()
    print_response(students)
    studentsModel.conn.close()

def add_student(student: dict):
    studentsModel = Models.StudentsModel()
    response = studentsModel.insert(student)
    print_response(response)
    studentsModel.conn.close()

def add_student_wizard():
    name = input("id-maker: Student Name = ")
    programme = input("id-maker: Student Programme = ")
    intake_year = input("id-maker: Student Intake Year = ")

    student = {
        "name": name,
        "programme": programme,
        "intake_year": intake_year
    }

    add_student(student)

#Programmes functions
def install_programmes():
    programmesModel = Models.ProgrammesModel()
    response = programmesModel.up()
    print_response(response)
    programmesModel.conn.close()

def uninstall_programmes():
    programmesModel = Models.ProgrammesModel()
    response = programmesModel.down()
    print_response(response)
    programmesModel.conn.close()

def show_programmes():
    programmesModel = Models.ProgrammesModel()
    response = programmesModel.all()
    print_response(response)
    programmesModel.conn.close()

def add_programme(programme: dict):
    programmesModel = Models.ProgrammesModel()
    response = programmesModel.insert(programme)
    print_response(response)
    programmesModel.conn.close()

def add_programme_wizard():
    name = input("id-maker: Programme Name = ")
    code = input("id-maker: Programme Code = ")

    programme = {
        "name": name,
        "code": code
    }

    add_programme(programme)

def execute_command(cmd_items: list):
    if cmd_items[0] == "show-students":
        show_students()
    elif cmd_items[0] == "add-student":
        add_student_wizard()
    elif cmd_items[0] == "install-students":
        install_students()
    elif cmd_items[0] == "uninstall-students":
        uninstall_students()

    elif cmd_items[0] == "show-programmes":
        show_programmes()
    elif cmd_items[0] == "add-programme":
        add_programme_wizard()
    elif cmd_items[0] == "install-programmes":
        install_programmes()
    elif cmd_items[0] == "uninstall-programmes":
        uninstall_programmes()
    elif cmd_items[0] == "exit":
        exit()
    else:
        print("Command not recognised")

while True:
    cmd = input("id-maker: ")
    
    cmd_items = cmd.split(" ")
    execute_command(cmd_items)
