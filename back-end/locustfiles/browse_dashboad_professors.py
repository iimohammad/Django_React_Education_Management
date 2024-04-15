from locust import HttpUser , task , between
import json

class SiteUser(HttpUser):
    wait_time = between(1, 3)
    def on_start(self):
        self.login2()

    def login2(self):
        response = self.client.get('/login/')
        csrftoken = response.cookies['csrftoken']
        response = self.client.post('/login/',
                                    {'username': 'user1', 'password': 'P@ssword1'},
                                    headers={'X-CSRFToken': csrftoken})
        return response
    
    @task(3)
    def view_show_profile(self):
        self.client.get('/dashboard_professors/show-profile/' ,
                        name = 'show-profile')
    @task(3)
    def view_revision_requests(self):
        self.client.get('/dashboard_professors/revision-requests/' ,
                        name = 'revision-requests')
    @task(3)
    def view_evaluate(self):
        self.client.get('/dashboard_professors/evaluate/' ,
                        name = 'evaluate')
    
    @task(3)
    def view_UnitSelectionConfirmation(self):
        self.client.get('/dashboard_professors/AdvisorRole/UnitSelectionConfirmation/' ,
                        name = 'UnitSelectionConfirmation')
    
    @task(3)
    def view_ShowMyStudents(self):
        self.client.get('/dashboard_professors/AdvisorRole/ShowMyStudents/' ,
                        name = 'ShowMyStudents')
    
    @task(3)
    def view_AddRemoveConfirmation(self):
        self.client.get('/dashboard_professors/AdvisorRole/AddRemoveConfirmation/' ,
                        name = 'AddRemoveConfirmation')
    
    @task(3)
    def view_EmploymentEducationConfirmation(self):
        self.client.get('/dashboard_professors/AdvisorRole/EmploymentEducationConfirmation/' ,
                        name = 'EmploymentEducationConfirmation')
    @task(3)
    def view_SemesterRegistrationConfirmation(self):
        self.client.get('/dashboard_professors/AdvisorRole/SemesterRegistrationConfirmation/' ,
                        name = 'SemesterRegistrationConfirmation')
    @task(3)
    def view_StudentDeleteSemesterConfirmation(self):
        self.client.get('/dashboard_professors/AdvisorRole/StudentDeleteSemesterConfirmation/' ,
                        name = 'StudentDeleteSemesterConfirmation')
        
    @task(3)
    def view_EmergencyRemovalConfirmation(self):
        self.client.get('/dashboard_professors/AdvisorRole/EmergencyRemovalConfirmation/' ,
                        name = 'EmergencyRemovalConfirmation')
        
    @task(3)
    def view_my_Courses_Semester(self):
        self.client.get('/dashboard_professors/TeacherRole/my-Courses-Semester/' ,
                        name = 'my-Courses-Semester')
    @task(2)
    def view_Semester_Show(self):
        self.client.get('/dashboard_professors/TeacherRole/Semester-Show/' ,
                        name = 'Semester-Show')