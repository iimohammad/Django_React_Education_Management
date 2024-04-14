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
        
    @task(10)
    def view_student_courses(self):
        self.client.get('/dashboard_student/student_courses/' ,
                        name = 'student_courses')
        
    
        
    @task(8)
    def view_exams(self):
        self.client.get('/dashboard_student/student_exams/' ,
                        name = 'student_exams')
        
    @task(8)
    def view_semester_courses(self):
        self.client.get('/dashboard_student/semester_courses/' ,
                        name = 'semester_courses')
    @task(8)
    def view_unit_selection(self):
        self.client.get('/dashboard_student/unit_selection/' ,
                        name = 'unit_selection')
    @task(8)
    def view_addremove_equests(self):
        self.client.get('/dashboard_student/AddRemoveRequestViewSet/' ,
                        name = 'AddRemoveRequestViewSet')
    
    @task(7)
    def view_courses(self):
        self.client.get('/dashboard_student/courses/' ,
                        name = 'courses')
        
    @task(7)
    def view_passed_courses(self):
        self.client.get('/dashboard_student/passed_courses/' ,
                        name = 'passed_courses')
    
    
    @task(5)
    def view_semester_registrations(self):
        self.client.get('/dashboard_student/semester_registration/' ,
                        name = 'semester_registration')
    
    @task(3)
    def view_employment_education_requests(self):
        self.client.get('/dashboard_student/employment_education_request/' ,
                        name = 'employment_education_request')
        
    @task(3)
    def view_revision_request_requests(self):
        self.client.get('/dashboard_student/revision_request/' ,
                        name = 'revision_request')
    
    @task(3)
    def view_delete_semester_requests(self):
        self.client.get('/dashboard_student/delete_semester_request/' ,
                        name = 'delete_semester_request')
    
    @task(3)
    def view_profile(self):
        self.client.get('/dashboard_student/profile/' ,
                        name = 'profile')