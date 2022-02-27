from pittapi import course
import structs

# Returns courses available in specific term for a particular department ("2231" is Fall '22 and "CS" is CS classes)
# Returns Subject object (has department, courses (dictionary of str to Course object), term)

cs_graph = structs.Graph("2231", "CS")
print(cs_graph.toJSON())

'''
# CScourses.courses['0007'] returns Course object (subject_code, course_number, course_title, sections --> list of Section objects) 
cs_0007 = CScourses.courses['0007']
sectionDet = course.get_extra_section_details(section=cs_0007.sections[0] , term="2231", class_number="0007")

for CSnumber, CScourse in CScourses.courses.items():
    # Do not account for grad level courses
    if int(CSnumber) >= 2000:
        break
    try:
        sectionDet = course.get_extra_section_details(section=CScourse.sections[0] , term="2231", class_number=CSnumber)
        print(CSnumber, ": ", sectionDet.preqs)
    except:
        print(CSnumber, ": ", "error")

# cs_0007 = CScourses.courses['0447']
# sectionDet = course.get_extra_section_details(section=cs_0007.sections[0] , term="2231", class_number="1501")
#sectionDet = course.get_section_details('2231', cs_0007.sections[0].class_number)
# print(sectionDet)
# print(sectionDet.preqs)
#print(cs_0007)
# If starts c or p, CS 
'''