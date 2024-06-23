```python
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QScrollArea, QGridLayout, QMessageBox

class GPACalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dynamic GPA Calculator")
        self.semesters = []
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Scroll Area Setup
        self.scrollArea = QScrollArea(self)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        layout.addWidget(self.scrollArea)

        self.content_layout = QVBoxLayout(self.scrollAreaWidgetContents)

        # Buttons and result label
        self.add_semester_button = QPushButton("Add Semester", self)
        self.add_semester_button.clicked.connect(self.add_semester)
        self.content_layout.addWidget(self.add_semester_button)

        self.calculate_cumulative_button = QPushButton("Calculate Cumulative GPA", self)
        self.calculate_cumulative_button.clicked.connect(self.calculate_cumulative_gpa)
        self.content_layout.addWidget(self.calculate_cumulative_button)

        self.result_label = QLabel("", self)
        self.content_layout.addWidget(self.result_label)

        self.setLayout(layout)

    def add_semester(self):
        semester_frame = QWidget()
        grid_layout = QGridLayout()

        semester_number = len(self.semesters) + 1
        semester_label = QLabel(f"Semester {semester_number}")
        grid_layout.addWidget(semester_label, 0, 0, 1, 5)

        # Adding column headers
        headers = ["Module", "Score", "CU", "GP", "Grade"]
        for i, header in enumerate(headers):
            grid_layout.addWidget(QLabel(header), 1, i)

        # Entries and labels for modules
        labels, score_entries, cu_entries, grade_point_labels, grade_letter_labels = [], [], [], [], []
        for i in range(6):
            label = QLabel(f"Module {i+1}:")
            grid_layout.addWidget(label, i+2, 0)
            labels.append(label)

            score_entry = QLineEdit()
            grid_layout.addWidget(score_entry, i+2, 1)
            score_entries.append(score_entry)

            cu_entry = QLineEdit()
            grid_layout.addWidget(cu_entry, i+2, 2)
            cu_entries.append(cu_entry)

            grade_point_label = QLabel()
            grid_layout.addWidget(grade_point_label, i+2, 3)
            grade_point_labels.append(grade_point_label)

            grade_letter_label = QLabel()
            grid_layout.addWidget(grade_letter_label, i+2, 4)
            grade_letter_labels.append(grade_letter_label)

            # Connect score entry changes to update the GP label
            score_entry.textChanged.connect(lambda text, lbl=grade_point_label, gr_lbl=grade_letter_label: self.update_gp_label(text, lbl, gr_lbl))

        calculate_button = QPushButton("Calculate Semester GPA", self)
        calculate_button.clicked.connect(lambda: self.calculate_semester_gpa(score_entries, cu_entries))
        grid_layout.addWidget(calculate_button, 8, 0, 1, 5)

        semester_frame.setLayout(grid_layout)
        self.content_layout.addWidget(semester_frame)
        self.semesters.append((semester_frame, score_entries, cu_entries, grade_point_labels, grade_letter_labels))

    def update_gp_label(self, text, gp_label, grade_label):
        try:
            score = float(text)
            if 90 <= score <= 100:
                gpa_point = 5.0
                grade = "A"
            elif 80 <= score <= 89:
                gpa_point = 5.0
                grade = "A"
            elif 75 <= score <= 79:
                gpa_point = 4.5
                grade = "B+"
            elif 70 <= score <= 74:
                gpa_point = 4.0
                grade = "B"
            elif 65 <= score <= 69:
                gpa_point = 3.5
                grade = "C+"
            elif 60 <= score <= 64:
                gpa_point = 3.0
                grade = "C"
            elif 55 <= score <= 59:
                gpa_point = 2.5
                grade = "D+"
            elif 50 <= score <= 54:
                gpa_point = 2.0
                grade = "D"
            elif 0 <= score <= 49:
                gpa_point = 0.0
                grade = "F"
            else:
                gp_label.setText("Invalid score")
                grade_label.setText("")
                return
            gp_label.setText(f"{gpa_point}")
            grade_label.setText(grade)
        except ValueError:
            gp_label.setText("")
            grade_label.setText("")

    def calculate_semester_gpa(self, score_entries, cu_entries):
        try:
            scores = [float(entry.text()) for entry in score_entries if entry.text()]
            credits = [float(entry.text()) for entry in cu_entries if entry.text()]
        except ValueError:
            QMessageBox.critical(self, "Input Error", "Please enter valid numerical grades and credit units.")
            return

        if len(scores) != len(credits):
            QMessageBox.critical(self, "Input Error", "The number of grades and credit units must match.")
            return

        weighted_gpa_points = 0
        total_credits = 0
        for score, credit in zip(scores, credits):
            if 90 <= score <= 100:
                gpa_point = 5.0
            elif 80 <= score <= 89:
                gpa_point = 5.0
            elif 75 <= score <= 79:
                gpa_point = 4.5
            elif 70 <= score <= 74:
                gpa_point = 4.0
            elif 65 <= score <= 69:
                gpa_point = 3.5
            elif 60 <= score <= 64:
                gpa_point = 3.0
            elif 55 <= score <= 59:
                gpa_point = 2.5
            elif 50 <= score <= 54:
                gpa_point = 2.0
            elif 0 <= score <= 49:
                gpa_point = 0.0
            else:
                QMessageBox.critical(self, "Range Error", "Grades should be between 0 and 100.")
                return

            weighted_gpa_points += gpa_point * credit
            total_credits += credit

        if total_credits > 0:
            semester_gpa = weighted_gpa_points / total_credits
            QMessageBox.information(self, "Semester GPA", f"Semester GPA: {semester_gpa:.2f}")
        else:
            QMessageBox.information(self, "Semester GPA", "No grades or credit units entered.")

    def calculate_cumulative_gpa(self):
        all_weighted_gpa_points = []
        all_total_credits = []
        for _, score_entries, cu_entries, _, _ in self.semesters:
            try:
                scores = [float(entry.text()) for entry in score_entries if entry.text()]
                credits = [float(entry.text()) for entry in cu_entries if entry.text()]
            except ValueError:
                QMessageBox.critical(self, "Input Error", "Please enter valid numerical grades and credit units.")
                return

            if len(scores) != len(credits):
                QMessageBox.critical(self, "Input Error", "The number of grades and credit units must match.")
                return

            weighted_gpa_points = 0
            total_credits = 0
            for score, credit in zip(scores, credits):
                if 90 <= score <= 100:
                    gpa_point = 5.0
                elif 80 <= score <= 89:
                    gpa_point = 5.0
                elif 75 <= score <= 79:
                    gpa_point = 4.5
                elif 70 <= score <= 74:
                    gpa_point = 4.0
                elif 65 <= score <= 69:
                    gpa_point = 3.5
                elif 60 <= score <= 64:
                    gpa_point = 3.0
                elif 55 <= score <= 59:
                    gpa_point = 2.5
                elif 50 <= score <= 54:
                    gpa_point = 2.0
                elif 0 <= score <= 49:
                    gpa_point = 0.0
                else:
                    QMessageBox.critical(self, "Range Error", "Grades should be between 0 and 100.")
                    return

                weighted_gpa_points += gpa_point * credit
                total_credits += credit

            if total_credits > 0:
                all_weighted_gpa_points.append(weighted_gpa_points)
                all_total_credits.append(total_credits)

        if all_total_credits:
            cumulative_weighted_gpa_points = sum(all_weighted_gpa_points)
            cumulative_total_credits = sum(all_total_credits)
            cumulative_gpa = cumulative_weighted_gpa_points / cumulative_total_credits
            self.result_label.setText(f"Cumulative GPA: {cumulative_gpa:.2f}")
        else:
            self.result_label.setText("No grades or credit units entered.")

if __name__ == "__main__":
    app = QApplication([])
    gpa_calculator = GPACalculator()
    gpa_calculator.show()
    app.exec_()
```
