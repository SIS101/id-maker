import Models

def handle_data(data: list, offset: int, overwrite):
    studentModel = Models.StudentsModel()
    #programmesModel = Models.ProgrammesModel()
    init = offset
    for item in data:
        write = True
        if len(item[4]) < 9:
            write = True
        else:
            if overwrite:
                write = True
            else:
                write = False
        
        if write:
            number = init+1
            n = str(number)
            if len(n) == 1:
                n = "00"+n
            elif len(n) == 2:
                n = "0"+n
            stid = str(item[3])+str(item[2])+n
            print(f"\n{item[0]}: {stid}")
            response = studentModel.update(uid=item[0], data={"stid":stid})
        else:
            response = "Cannot overwrite existing student ID"
            
        print(response)
        init += 1

def handle_response(response: dict, begin: int, end: int, offset: int, overwrite = False):
    if response["success"]:
        if response["data"]:
            if end == None:
                handle_data(response["data"][begin:], offset, overwrite)
            else:
                handle_data(response["data"][begin:end], offset, overwrite)
        else:
            print("No data to handle")
    else:
        print(response["message"])

def generate_id(programme: str = None,begin: int = 0, end: int = None, offset: int = 0, overwrite = False):
    studentsModel = Models.StudentsModel()
    if programme != None:
        response = studentsModel.find(programme=programme)
    else:
        response = studentsModel.all()
    handle_response(response, begin, end, offset, overwrite)

generate_id(programme="01", offset=20)