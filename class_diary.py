from pymongo import MongoClient
from datetime import date


client = MongoClient("mongodb://localhost:27017")  #  Change it to your MongoDB connection string
db = client.database
schoolname = input("Input school's name: ")  #  Will be used as collection's name
collection = db[schoolname.lower().replace(' ', '')]  #  Reformatting school's name to look better as collection name
date = str(date.today())

def register_student():
    student = input("Student's full name: ").lower()
    collection.insert_one({"name": student,
                           "lessons": [
                               {
                                   "date" : date,
                                   "content" : "register"
                               }
                           ]
                           })
    print("Student register done")

def update_diary():
    student_name = input("Student's full name: " ).lower()
    lesson_content = input("Enter today's lesson content: ")
    collection.update_one({"name": student_name},
                          {"$push" : {
                              "lessons" : {
                                  "$each": [
                                      {"date": date, "content": lesson_content}
                                  ]
                              }
                          }})

    print("Wrote on class diary")


def read_diary():
    student_name = input("Student's full name: " ).lower()
    student_info = collection.find_one({"name": student_name}, {"_id": 0, "name": 1, "lessons.date": 1, "lessons.content": 1})
    print("\nName: " + student_info['name'].title())
    for lesson in student_info['lessons']:
        print(lesson['date'] + ': ' + lesson['content'])

active = True

while active == True:
    switch = int(input("\n1 - Update class diary\n2 - Read class diary\n3 - Register student\n0 - Exit\n\nChoose an option (0-3): "))
    match switch:
        case 1:
            update_diary()
        case 2:
            read_diary()
        case 3:
            register_student()
        case 0:
            exit()