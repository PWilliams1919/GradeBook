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

    def get_name(self):
        return self.__name

    def get_grades(self):
        return self.__grade_dict

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

student_dict = {'Spongebob':
                    {'Test 1': 90,
                     'Essay 1': 200,
                     'Pop Quiz 4': 42},
                'Gary':
                    {'Test 1': 100,
                     'Essay 1': 250,
                     'Pop Quiz 4': 50},
                'Squidward':
                    {'Test 1': 76,
                     'Essay 1': 198,
                     'Pop Quiz 4': 40},
                'Sandy':
                    {'Test 1': 100,
                     'Essay 1': 245,
                     'Pop Quiz 4': 49},
                'Pearl':
                    {'Test 1': 90,
                     'Essay 1': 215,
                     'Pop Quiz 4': 38}
                }
#DEBUG

class Logic(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        #Splash page
        self.splash_enter_button.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.main_menu_quote_label.setText(quotes[random.randint(0, len(quotes) - 1)])

        #Main Menu page
        self.main_go_button.clicked.connect(lambda: self.goto_page(self.mainmenu_dropdown.currentText()))
        #TODO: save and exit button logic

        #Enter/Edit Grades page
        self.entereditgrade_returntomain_button.clicked.connect(lambda: self.return_to_main())
        self.entereditgrade_clear_button.clicked.connect(lambda: self.clear_fields('enteredit_grade'))

        self.entereditgrade_assign_dropdown.currentIndexChanged.connect(
            lambda: self.update_text(self.entereditgrade_totalpts_label,
                                     self.entereditgrade_assign_dropdown.currentText(),
                                     self.entereditgrade_student_dropdown.currentText()))

        self.entereditgrade_student_dropdown.currentIndexChanged.connect(
            lambda: self.update_text(self.entereditgrade_totalpts_label,
                                     self.entereditgrade_assign_dropdown.currentText(),
                                     self.entereditgrade_student_dropdown.currentText()))

        self.entereditgrade_save_button.clicked.connect(lambda: self.confirm_changes('enteredit_grade',
                                                                                     self.entereditgrade_assign_dropdown.currentText(),
                                                                                     self.entereditgrade_student_dropdown.currentText(),
                                                                                     self.entereditgrade_ptsearned_linetext.text()))

        #Add/Remove Student page
        self.addstudent_returntomain_button.clicked.connect(lambda: self.return_to_main())
        self.addstudent_clear_button.clicked.connect(lambda: self.clear_fields('add_student'))

        #Course Statistics page
        self.assign_avg_returntomain_button.clicked.connect(lambda: self.return_to_main())

        #Add assignment page
        self.add_assign_returntomain_button.clicked.connect(lambda: self.return_to_main())
        self.add_assign_clear_button.clicked.connect(lambda: self.clear_fields('add_assign'))

    def goto_page(self, page_name):
        if page_name == 'Enter/Edit Grades':
            self.stackedWidget.setCurrentIndex(2)

            self.entereditgrade_student_dropdown.clear()
            self.entereditgrade_student_dropdown.addItems(students)

            self.entereditgrade_assign_dropdown.clear()
            self.entereditgrade_assign_dropdown.addItems(assignments)

        elif page_name == 'Add/Edit Assignments':
            self.stackedWidget.setCurrentIndex(3)

        elif page_name == 'Add/Remove Students':
            self.stackedWidget.setCurrentIndex(4)

        elif page_name == 'Course Statistics':
            self.stackedWidget.setCurrentIndex(5)

    def return_to_main(self):
        self.stackedWidget.setCurrentIndex(1)
        self.main_menu_quote_label.setText(quotes[random.randint(0, len(quotes)-1)])

    def clear_fields(self, page):
        if page == 'enteredit_grade':
            self.entereditgrade_student_dropdown.setCurrentIndex(0)
            self.entereditgrade_assign_dropdown.setCurrentIndex(0)
            self.entereditgrade_ptsearned_linetext.clear()
            self.entereditgrade_ptsearned_linetext.setFocus()

        elif page == 'add_student':
            self.addstudent_name_linetext.clear()
            self.addstudent_name_linetext.setFocus()

        elif page == 'remove_student':
            self.removestudent_name_dropdown.setCurrentIndex(0)

        elif page == 'add_assign':
            self.add_assign_name_linetext.clear()
            self.add_assign_possiblepts_linetext.clear()
            self.add_assign_name_linetext.setFocus()

    def update_text(self, textbox, assignment, student):
        if textbox == self.entereditgrade_totalpts_label:
            if assignment == '' or assignment == '-' or student == '' or student == '-':
                textbox.setText('N/A')
                self.entereditgrade_ptsearned_linetext.setText('---')
            else:
                textbox.setText(str(assignment_dict[assignment]))
                if assignment not in student_dict[student]:
                    self.entereditgrade_ptsearned_linetext.setText('---')
                else:
                    self.entereditgrade_ptsearned_linetext.setText(str(student_dict[student][assignment]))

    def confirm_changes(self, page, assignment, student, points):
        #TODO: data validation
        confirm_choice = self.show_confirm_popup()

        if confirm_choice == 65536:
            self.clear_fields(page)
        elif confirm_choice == 16384:
            student_dict[student][assignment] = points
            print(student_dict[student][assignment])
            self.show_success_popup(student, assignment, points)
            self.clear_fields(page)

