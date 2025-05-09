from PyQt6.QtWidgets import *

from gui import *
import csv
import random

quotes = [f'{'"Instruction does much, but encouragement everything"'}\n-Johann Wolfgang von Goethe',
          f'{'"Education is what remains after one has forgotten what one has learned in school."'}\n-Albert Einstein',
          f'{'"He who opens a school door, closes a prison."'}\n-Victor Hugo',
          f'{'"The foundation of every state is the education of its youth."'}\n-Diogenes',
          f'{'"Education is the most powerful weapon which you can use to change the world."'}\n- Nelson Mandela',
          f'{'"Children must be taught how to think, not what to think."'}\n-Margaret Mead',
          f'{'"The mind is not a vessel to be filled, but a fire to be kindled."'}\n-Plutarch',
          ]

assignment_dict = {}
try:
    with open('assignment_template.csv', 'r') as assigncsv:
        assignreader = csv.reader(assigncsv)
        for row in assignreader:
            assignment_dict[row[0]] = int(row[1])
except FileNotFoundError:
    with open('assignment_template.csv', 'w') as assigncsv:
        assignreader = csv.reader(assigncsv)

student_dict = {}
try:
    with open('student_grades.csv', 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            student_dict[row['name']] = {}
            for col in row:
                if col != 'name':
                    student_dict[row['name']][col] = int(row[col])
except FileNotFoundError:
    with open('student_grades.csv', 'w') as csvfile:
        csvreader = csv.DictReader(csvfile)

class Logic(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        #Splash page
        self.splash_enter_button.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.main_menu_quote_label.setText(quotes[random.randint(0, len(quotes) - 1)])

        #Main Menu page
        self.main_go_button.clicked.connect(lambda: self.goto_page(self.mainmenu_dropdown.currentText()))
        self.save_exit_button.clicked.connect(lambda: self.saveandexit())

        #Enter/Edit Grades page
        self.entereditgrade_returntomain_button.clicked.connect(lambda: self.return_to_main())
        self.entereditgrade_clear_button.clicked.connect(lambda: self.clear_fields())

        self.entereditgrade_assign_dropdown.currentIndexChanged.connect(
            lambda: self.update_text(self.entereditgrade_totalpts_label,
                                     self.entereditgrade_assign_dropdown.currentText(),
                                     self.entereditgrade_student_dropdown.currentText()))

        self.entereditgrade_student_dropdown.currentIndexChanged.connect(
            lambda: self.update_text(self.entereditgrade_totalpts_label,
                                     self.entereditgrade_assign_dropdown.currentText(),
                                     self.entereditgrade_student_dropdown.currentText()))

        self.entereditgrade_save_button.clicked.connect(
            lambda: self.edit_grade(self.entereditgrade_assign_dropdown.currentText(),
                                    self.entereditgrade_student_dropdown.currentText(),
                                    self.entereditgrade_ptsearned_linetext.text()))


        #Add/Edit Assignment page
        self.addedit_assign_add_button.clicked.connect(lambda: self.add_assignment())

        self.addedit_assign_list.currentRowChanged.connect(lambda:self.update_text(self.addedit_assign_del_button))

        self.addedit_assign_edit_button.clicked.connect(
            lambda: self.edit_assignment(self.addedit_assign_list.currentRow()))

        self.addedit_assign_del_button.clicked.connect(
            lambda: self.del_assignment(self.addedit_assign_list.currentRow()))

        self.addedit_assign_returntomain_button.clicked.connect(lambda: self.return_to_main())

        #Add/Remove Student page
        self.addremovestudent_add_button.clicked.connect(lambda: self.add_student())

        self.addremove_student_list.currentRowChanged.connect(lambda: self.update_text(self.addremovestudent_remove_button))

        self.addremove_student_returntomain_button.clicked.connect(lambda: self.return_to_main())

        self.addremovestudent_remove_button.clicked.connect(
            lambda: self.remove_student(self.addremove_student_list.currentItem().text()))

        #Statistics page
        self.statistics_returntomain_button.clicked.connect(lambda: self.return_to_main())

        self.buttonGroup.buttonClicked.connect(lambda: self.update_text(self.statistics_list))

        self.statistics_calculate_button.clicked.connect(
            lambda: self.calculate_stats(self.buttonGroup.checkedButton().text(), self.statistics_list.currentItem().text()))

        #Results page
        self.results_back_button.clicked.connect(lambda: self.goto_page('Course Statistics'))

    def goto_page(self, page_name: str) -> None:
        """
        Goes to page of stacked widget based on page name passed as parameter, refreshes values in appropriate page
        widgets to reflect most current assignments, grades and student roster.
        :param page_name: Name of page to be navigated to.
        :return: None
        """
        if page_name == 'Enter/Edit Grades':
            self.stackedWidget.setCurrentIndex(2)

            self.entereditgrade_student_dropdown.clear()
            self.entereditgrade_student_dropdown.addItem('-')
            for student in student_dict:
                self.entereditgrade_student_dropdown.addItem(student)

            self.entereditgrade_assign_dropdown.clear()
            self.entereditgrade_assign_dropdown.addItem('-')
            for assignment in assignment_dict:
                self.entereditgrade_assign_dropdown.addItem(assignment)

        elif page_name == 'Add/Edit Assignments':
            self.stackedWidget.setCurrentIndex(3)
            self.update_text(self.addedit_assign_list)
            self.addedit_assign_edit_button.setEnabled(False)
            self.addedit_assign_del_button.setEnabled(False)

        elif page_name == 'Add/Remove Students':
            self.stackedWidget.setCurrentIndex(4)
            self.update_text(self.addremove_student_list)
            self.addremovestudent_remove_button.setEnabled(False)

        elif page_name == 'Course Statistics':
            self.stackedWidget.setCurrentIndex(5)
            self.statistics_list.clear()
            self.statistics_zeros_checkbox.setVisible(False)
            self.assign_avg_zeros_label.setVisible(False)
            self.assign_avg_zeros_label_2.setVisible(False)
            self.statistics_zeros_checkbox.setChecked(False)
            self.buttonGroup.setExclusive(False)
            self.statistics_assignment_radioButton.setChecked(False)
            self.statistics_student_radioButton.setChecked(False)
            self.statistics_course_radioButton.setChecked(False)
            self.buttonGroup.setExclusive(True)
            self.statistics_calculate_button.setEnabled(False)

    def saveandexit(self) -> None:
        """
        Saves student_dict and assignment_dict to student_grades.csv and assignment_grades.csv respectively and exits
        program.
        :return: None
        """
        fieldnames = ['name']
        for assignment in assignment_dict:
            fieldnames.append(assignment)
        with open('student_grades.csv', 'w') as savefile:
            writer = csv.DictWriter(savefile, fieldnames=fieldnames, lineterminator='\n')
            writer.writeheader()
            for student in student_dict:
                row = {'name': student}
                for assignment in student_dict[student]:
                    row[assignment] = int(student_dict[student][assignment])
                writer.writerow(row)

        fieldnames.pop(0)
        with open('assignment_template.csv', 'w') as assignment_file:
            writer = csv.writer(assignment_file, lineterminator='\n')
            for assignment in assignment_dict:
                writer.writerow([assignment, assignment_dict[assignment]])

        self.close()

    def return_to_main(self) -> None:
        """
        Returns to main page of program and refreshes quote text based on randomly generated integer.
        :return: None
        """
        self.stackedWidget.setCurrentIndex(1)
        self.main_menu_quote_label.setText(quotes[random.randint(0, len(quotes)-1)])
        self.mainmenu_dropdown.setCurrentIndex(0)

    def clear_fields(self) -> None:
        """
        Clears all fields on the Enter/Edit grades page, sets both dropdowns to '-' and calls the update_text() function.
        :return: None
        """
        self.entereditgrade_student_dropdown.setCurrentIndex(0)
        self.entereditgrade_assign_dropdown.setCurrentIndex(0)
        self.entereditgrade_ptsearned_linetext.clear()
        self.entereditgrade_ptsearned_linetext.setFocus()
        self.update_text(self.entereditgrade_totalpts_label)

    def update_text(self, textbox: QLabel, assignment: str =None, student: str =None) -> None:
        """
        Updates textboxes, lists, dropdowns and textlines. Also enables/disables buttons and hides/shows
        options based on user selection.
        :param textbox: QLabel item from the page that is being updated.
        :param assignment: Selected assignment in assignment dropdown of Enter/Edit Grades page.
        :param student: Selected student in student dropdown of Enter/Edit Grades page.
        :return: None
        """
        if textbox == self.entereditgrade_totalpts_label:
            if (assignment == '' or assignment == '-' or assignment == None or
                    student == '' or student == '-' or student == None):
                textbox.setText('N/A')
                self.entereditgrade_ptsearned_linetext.setText('---')
                self.entereditgrade_save_button.setEnabled(False)
            else:
                textbox.setText(str(assignment_dict[assignment]))
                if assignment not in student_dict[student]:
                    self.entereditgrade_ptsearned_linetext.setText('---')
                else:
                    self.entereditgrade_ptsearned_linetext.setText(str(student_dict[student][assignment]))
                    self.entereditgrade_save_button.setEnabled(True)

        elif textbox == self.addedit_assign_list:
            self.addedit_assign_list.clear()
            for assignment in assignment_dict:
                self.addedit_assign_list.addItem(f"{assignment:{'.'}<20}{int(assignment_dict[assignment]):{'.'}>5}")

        elif textbox == self.addedit_assign_del_button:
            self.addedit_assign_del_button.setEnabled(True)
            self.addedit_assign_edit_button.setEnabled(True)

        elif textbox == self.addremove_student_list:
            self.addremove_student_list.clear()
            for student in student_dict:
                self.addremove_student_list.addItem(student)

        elif textbox == self.addremovestudent_remove_button:
            self.addremovestudent_remove_button.setEnabled(True)

        elif textbox == self.statistics_list:
            error_flag = True
            for assignment in assignment_dict:
                for student in student_dict:
                    if assignment in student_dict[student] and student_dict[student][assignment] != 'N/A':
                        error_flag = False
                        break

            if error_flag == True:
                self.assign_avg_zeros_label_2.setVisible(True)
            else:
                self.assign_avg_zeros_label_2.setVisible(False)

            self.statistics_list.clear()
            self.statistics_calculate_button.setEnabled(False)

            if self.statistics_assignment_radioButton.isChecked():
                for assignment in assignment_dict:
                    self.statistics_list.addItem(assignment)
                self.assign_avg_zeros_label.setVisible(True)
                self.statistics_zeros_checkbox.setVisible(True)
                self.statistics_list.setCurrentRow(0)
            elif self.statistics_student_radioButton.isChecked():
                for student in student_dict:
                    self.statistics_list.addItem(student)
                self.assign_avg_zeros_label.setVisible(True)
                self.statistics_zeros_checkbox.setVisible(True)
                self.statistics_list.setCurrentRow(0)
            elif self.statistics_course_radioButton.isChecked():
                self.statistics_list.addItem('*Click Calculate*')
                self.assign_avg_zeros_label.setVisible(False)
                self.statistics_zeros_checkbox.setVisible(False)

    def edit_grade(self, assignment: str, student: str, points: str) -> None:
        """
        Captures and processes new point grade for selected student and assignment. Validates that "points" value
        is an integer and displays error pop-up if not.
        :param assignment: Name of selected assignment
        :param student: Name of selected student
        :param points: New score for student on selected assignment.
        :return: None
        """
        confirm_choice = self.show_confirm_popup()
        try:
            if confirm_choice == 65536:
                self.clear_fields()
            elif confirm_choice == 16384:
                if student in student_dict and assignment in assignment_dict:
                    student_dict[student][assignment] = int(points)
                    self.show_success_popup()
                    self.clear_fields()
        except ValueError:
            self.show_error_popup(1)
            self.clear_fields()

    def edit_assignment(self, index: int) -> None:
        """
        Displays popup to capture new point total for selected assignment. Iterates through student_dict to change
        score to new total if saved score is higher.
        :param index: Index number for selected assignment.
        :return: None
        """
        assignments = []
        for assignment in assignment_dict:
            assignments.append(assignment)
        new_points = self.show_editassignment_popup()
        if new_points >0:
            assignment_dict[assignments[index]] = new_points
            self.show_success_popup()
            self.update_text(self.addedit_assign_list)
            for student in student_dict:
                if student_dict[student][assignments[index]] > assignment_dict[assignments[index]]:
                    student_dict[student][assignments[index]] = assignment_dict[assignments[index]]

    def del_assignment(self, index: int) -> None:
        """
        Deletes selected assignment after user confirms selection. Removes selection from assignment dict and iterates
        through student_dict to remove assignment from each student's stored grades.
        :param index: Index number of selected assignment
        :return: None
        """
        assignments = []
        for assignment in assignment_dict:
            assignments.append(assignment)

        confirm_choice = self.show_confirm_popup()

        if confirm_choice == 65536:
            self.clear_fields()
        elif confirm_choice == 16384:
            del assignment_dict[assignments[index]]
            for student in student_dict:
                del student_dict[student][assignments[index]]
            self.show_success_popup()
            self.update_text(self.addedit_assign_list)

    def add_assignment(self) -> None:
        """
        Displays popups to capture new assignment name and total score. Saves values in assignment_dict and iterates
        through student_dict to add the new assignment to saved scores with 'N/A' grade.
        :return: None
        """
        name = self.show_addassignmentname_popup()
        if (name != '' and name != None) and name not in assignment_dict:
            score = self.show_addassignmentscore_popup(name)
            if str(score).isnumeric() and int(score) > 0:
                assignment_dict[name] = score
                for student in student_dict:
                    student_dict[student][name] = 'N/A'
                self.update_text(self.addedit_assign_list)
        elif name in assignment_dict:
            self.show_assignmentexists_popup()

    def add_student(self) -> None:
        """
        Displays popup to capture name of student to be added. Adds student to student_dict with 'N/A' grade for every
        existing assignment.
        :return: None
        """
        student_name = self.show_addstudent_popup()
        if student_name in student_dict:
            self.show_studentexists_popup()
        elif student_name != '' and student_name != None:
            student_dict[student_name] = {}
            for assignment in assignment_dict:
                student_dict[student_name][assignment] = 'N/A'
            self.show_success_popup()
            self.update_text(self.addremove_student_list)

    def remove_student(self, student: str) -> None:
        """
        Removes selected student from student_dict after user confirmation.
        :param student: Name of selected student.
        :return: None
        """
        confirm_choice = self.show_confirm_popup()
        if confirm_choice == 65536:
            return
        elif confirm_choice == 16384:
            del student_dict[student]
            self.update_text(self.addremove_student_list)

    def calculate_stats(self, group: str, selection: str) -> None:
        """
        Displays averages of either a single assignment, single student, or the entire course based on user selection.
        :param group: Radio button selection (Assignment, Student, or Course)
        :param selection: Selected assignment or student.
        :return: None
        """
        self.stackedWidget.setCurrentIndex(6)
        self.results_text.clear()

        total_poss = 0
        earned = 0

        if group == 'By Student':
            if self.statistics_zeros_checkbox.isChecked():
                for assignment in assignment_dict:
                    total_poss += int(assignment_dict[assignment])
                    score_string = ''
                    if student_dict[selection][assignment] == 'N/A':
                        score_string += '0/'
                    else:
                        earned += int(student_dict[selection][assignment])
                        score_string += str(student_dict[selection][assignment]) + '/'
                    score_string += str(assignment_dict[assignment])
                    self.results_text.append(f'{assignment:.<15}{score_string:.>20}')

            elif not self.statistics_zeros_checkbox.isChecked():
                for assignment in assignment_dict:
                    if student_dict[selection][assignment] == 'N/A':
                        pass
                    else:
                        score = ''
                        if assignment in student_dict[selection]:
                            earned += int(student_dict[selection][assignment])
                            score += str(student_dict[selection][assignment])+'/'
                            score += str(assignment_dict[assignment])
                            total_poss += int(assignment_dict[assignment])
                            self.results_text.append(f'{assignment:.<15}{score:.>20}')
                        elif assignment not in student_dict[selection]:
                            self.results_text.append(f'{assignment:.<15}{'missing':.>20}')

            self.results_text.append(40*'=')
            percent_grade = (earned/total_poss)*100
            letter_grade = self.get_letter_grade(percent_grade)
            self.results_text.append(f'Current Grade for {selection} - {(earned / total_poss)*100:.2f}% : {letter_grade}')

        elif group == 'By Assignment':
            total_score = 0
            if self.statistics_zeros_checkbox.isChecked():
                for student in student_dict:
                    print_string = ''
                    if selection in student_dict[student]:
                        total_score += student_dict[student][selection]
                        print_string += str(student_dict[student][selection]) + '/'
                    else:
                        print_string += '0/'
                    print_string += str(assignment_dict[selection])
                    self.results_text.append(f'{student:.<15}{print_string:.>20}')

            elif not self.statistics_zeros_checkbox.isChecked():
                for student in student_dict:
                    print_string = ''
                    if selection in student_dict[student] and student_dict[student][selection] != 'N/A':
                        total_score += int(student_dict[student][selection])
                        print_string += str(student_dict[student][selection]) + '/'
                        print_string += str(assignment_dict[selection])
                        self.results_text.append(f'{student:.<15}{print_string:.>20}')
                    elif selection not in student_dict[student]:
                        self.results_text.append(f'{student:.<15}{'missing':.>20}')

            percent_avg = ((total_score/len(student_dict))/assignment_dict[selection] * 100)
            letter_grade = self.get_letter_grade(percent_avg)
            submission_count=0

            for student in student_dict:
                if student_dict[student][selection] != 'N/A':
                    submission_count += 1
            if submission_count > 0:
                self.results_text.append(40 * '=')
                self.results_text.append(f'Average Grade for {selection} - {percent_avg:.2f}% : {letter_grade}')
            elif submission_count == 0:
                self.results_text.append(f'No Grades Found For {selection}.')

        elif group == 'By Course':
            course_total = 0
            total_possible = 0

            for assignment in assignment_dict:
                total_possible += assignment_dict[assignment]

            for assignment in assignment_dict:
                print_string = ''
                total_score = 0
                for student in student_dict:
                    total_score += student_dict[student][assignment]
                avg = total_score/len(student_dict)
                print_string += str(f'{avg:.2f}') + '/' + str(f'{assignment_dict[assignment]}')
                course_total += total_score
                self.results_text.append(f'Avg. for {assignment:.<15}{print_string:.>20}')

            for student in student_dict:
                for assignment in assignment_dict:
                    total_possible += student_dict[student][assignment]

            self.results_text.append(40*'=')
            self.results_text.append(f'Overall Course Average - {course_total/total_possible*100:.2f} : {self.get_letter_grade(course_total/total_possible*100)}')

    def get_letter_grade(self, percent_grade: float) -> str:
        """
        Given a floating number representation of a percent grade, returns the appropriate letter grade as a string.
        :param percent_grade: Calculated percent grade
        :return: Letter grade corresponding to percent grade
        """

        if percent_grade >= 96.67:
            letter_grade = 'A+'
        elif percent_grade >= 93.33:
            letter_grade = 'A'
        elif percent_grade >= 90.00:
            letter_grade = 'A-'
        elif percent_grade >= 86.67:
            letter_grade = 'B+'
        elif percent_grade >= 83.33:
            letter_grade = 'B'
        elif percent_grade >= 80.00:
            letter_grade = 'B-'
        elif percent_grade >= 76.67:
            letter_grade = 'C+'
        elif percent_grade >= 73.33:
            letter_grade = 'C'
        elif percent_grade >= 70.00:
            letter_grade = 'C-'
        elif percent_grade >= 66.67:
            letter_grade = 'D+'
        elif percent_grade >= 63.33:
            letter_grade = 'D'
        elif percent_grade >= 60.00:
            letter_grade = 'D-'
        else:
            letter_grade = 'F'

        return letter_grade