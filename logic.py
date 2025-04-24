from PyQt6.QtWidgets import *
from gui import *
import csv
import random

quotes = [f'{'"Instruction does much, but encouragement everything"'}\n{'-Johann Wolfgang von Goethe'}',
          f'{'"Education is what remains after one has forgotten what one has learned in school."'}\n{'-Albert Einstein'}',
          f'{'"He who opens a school door, closes a prison."'}\n{'-Victor Hugo'}',
          f'{'"The foundation of every state is the education of its youth."'}\n{'-Diogenes'}'
          ]

class Student:
    def __init__(self, student_name):
        self.__name = student_name
        self.__grade_dict = {}

    def add_grade(self, assignment, grade):
        pass

    def edit_grade(self, assignment, grade):
        pass

#DEBUG
students = ['-', 'Spongebob', 'Gary', 'Squidward', 'Sandy', 'Pearl']
assignments = ['-', 'Test 1', 'Essay 1', 'Pop Quiz 4']
assignment_dict = {'-':'N/A',
                   'Test 1': 100,
                   'Essay 1': 250,
                   'Pop Quiz 4': 50
                   }
#DEBUG

class Logic(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        #Splash page
        self.splash_enter_button.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))

        #Main menu page
        self.enter_grades_button.clicked.connect(lambda: self.goto_page(2))
        self.edit_grades_button.clicked.connect(lambda: self.goto_page(3))
        self.add_student_button.clicked.connect(lambda: self.goto_page(4))
        self.remove_student_button.clicked.connect(lambda: self.goto_page(5))
        self.assign_avg_button.clicked.connect(lambda: self.goto_page(6))
        self.course_avg_button.clicked.connect(lambda: self.goto_page(7))
        self.add_assignment_button.clicked.connect(lambda: self.goto_page(8))
        self.main_menu_quote_label.setText(quotes[random.randint(0, len(quotes)-1)])

        #Enter grade page
        self.entergrade_returntomain_button.clicked.connect(lambda: self.return_to_main())
        self.entergrade_clear_button.clicked.connect(lambda: self.clear_fields('enter_grade'))
        self.entergrade_assign_dropdown.currentIndexChanged.connect(lambda: self.entergrade_totalpts_label.setText(str(assignment_dict[self.entergrade_assign_dropdown.currentText()])))

        #Edit grade page
        self.editgrade_returntomain_button.clicked.connect(lambda: self.return_to_main())
        self.editgrade_clear_button.clicked.connect(lambda: self.clear_fields('edit_grade'))

        #Add student page
        self.addstudent_returntomain_button.clicked.connect(lambda: self.return_to_main())
        self.addstudent_clear_button.clicked.connect(lambda: self.clear_fields('add_student'))

        #Remove student page
        self.removestudent_returntomain_button.clicked.connect(lambda: self.return_to_main())
        self.removestudent_clear_button.clicked.connect(lambda: self.clear_fields('remove_student'))

        #Assignment average page
        self.assign_avg_returntomain_button.clicked.connect(lambda: self.return_to_main())

        #Course average page
        self.course_avg_returntomain_button.clicked.connect(lambda: self.return_to_main())

        #Add assignment page
        self.add_assign_returntomain_button.clicked.connect(lambda: self.return_to_main())
        self.add_assign_clear_button.clicked.connect(lambda: self.clear_fields('add_assign'))

    def goto_page(self, stack_index):
        #FIXME: addItems method is duplicating combobox entries when going to page multiple times
        self.stackedWidget.setCurrentIndex(stack_index)
        if stack_index == 2:
            self.entergrade_student_dropdown.addItems(students)
            self.entergrade_assign_dropdown.addItems(assignments)
        elif stack_index == 3:
            self.editgrade_student_dropdown.addItems(students)
            self.editgrade_assign_dropdown.addItems(assignments)
        elif stack_index == 5:
            self.removestudent_name_dropdown.addItems(students)
        elif stack_index == 6:
            self.assign_avg_assign_dropdown.addItems(assignments)

    def return_to_main(self):
        self.stackedWidget.setCurrentIndex(1)
        self.main_menu_quote_label.setText(quotes[random.randint(0, len(quotes)-1)])

    def clear_fields(self, page):
        if page == 'enter_grade':
            self.entergrade_student_dropdown.setCurrentIndex(0)
            self.entergrade_assign_dropdown.setCurrentIndex(0)
            self.entergrade_ptsearned_linetext.clear()
            self.entergrade_ptsearned_linetext.setFocus()
        elif page == 'edit_grade':
            self.editgrade_student_dropdown.setCurrentIndex(0)
            self.editgrade_assign_dropdown.setCurrentIndex(0)
            self.editgrade_newgrade_linetext.clear()
            self.editgrade_newgrade_linetext.setFocus()
        elif page == 'add_student':
            self.addstudent_name_linetext.clear()
            self.addstudent_name_linetext.setFocus()
        elif page == 'remove_student':
            self.removestudent_name_dropdown.setCurrentIndex(0)
        elif page == 'add_assign':
            self.add_assign_name_linetext.clear()
            self.add_assign_possiblepts_linetext.clear()
            self.add_assign_name_linetext.setFocus()
