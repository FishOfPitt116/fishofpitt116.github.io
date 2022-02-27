from pittapi import course
import json
# Convert all subject codes into JSON representation to add into selection bar of dropdown menu
courses = { "codes" : course.get_subject_codes() }

with open("../json/codes.json", "w") as f:
    json.dump(courses, f)