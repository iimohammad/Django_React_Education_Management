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
        
    #requests
    #get courese
    #get exams
    #get profile
    @task(10)
    def view_student_courses(self):
        self.client.get('/dashboard_student/student_courses/' , 
                        name = '/dashboard_student/student_courses/')
        
    
        
    @task(10)
    def view_exams(self):
        self.client.get('/dashboard_student/student_exams/' , 
                        name = '/dashboard_student/student_exams/')
        
    @task(9)
    def view_semester_courses(self):
        self.client.get('/dashboard_student/semester_courses/' , 
                        name = '/dashboard_student/semester_courses/')
    
    @task(6)
    def view_semester_registrations(self):
        self.client.get('/dashboard_student/unit_selection/' , 
                        name = '/dashboard_student/unit_selection/') 
    
    @task(5)
    def view_semester_registrations(self):
        self.client.get('/dashboard_student/semester_registration/' , 
                        name = '/dashboard_student/semester_registration/')    
        
    @task(3)
    def view_delete_semester_requests(self):
        self.client.get('/dashboard_student/revision_request/' , 
                        name = '/dashboard_student/revision_request/')  
    
    @task(1)
    def view_delete_semester_requests(self):
        self.client.get('/dashboard_student/delete_semester_request/' , 
                        name = '/dashboard_student/delete_semester_request/')  
    
    @task(1)
    def view_profile(self):
        self.client.get('/dashboard_student/profile/' , 
                        name = '/dashboard_student/profile/')