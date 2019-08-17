from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import math
from django.views import generic
from h_masterdata.models import Distance,Company,Project,Employee
from rest_framework import generics
from h_masterdata.serializers import EmployeeSerializer, ProjectSerializer


# to calculate the distance between 2 shops when shop ids are given
class DistanceView(APIView):
    permission_classes = ()
    authentication_classes = ()
    def get(self, request, *args, **kwargs):
        id1 = request.GET.get("first")
        id2 = request.GET.get("second")
        try:
            shop_1 = Distance.objects.get(shop_id = id1)
        except:
            return Response({"status": False, "msg": "shop not found"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            shop_2 = Distance.objects.get(shop_id = id2)
        except:
            return Response({"status": False, "msg": "shop not found"},
                            status=status.HTTP_400_BAD_REQUEST)
        lon1 = shop_1.longitude
        lat1 = shop_1.latitude
        lon2 = shop_2.longitude
        lat2 = shop_2.latitude
        
        R=6371000                               # radius of Earth in meters
        phi_1=math.radians(lat1)
        phi_2=math.radians(lat2)

        delta_phi=math.radians(lat2-lat1)
        delta_lambda=math.radians(lon2-lon1)

        a=math.sin(delta_phi/2.0)**2+\
           math.cos(phi_1)*math.cos(phi_2)*\
           math.sin(delta_lambda/2.0)**2
        c=2*math.atan2(math.sqrt(a),math.sqrt(1-a))

        self.meters=R*c                         # output distance in meters
        self.km=self.meters/1000.0              # output distance in kilometers
        
        data= {
            "kilometer":  self.km
        }
        return Response({"status": True, "msg": data}, status=status.HTTP_200_OK)

#Updating details of the company
class UpdateCompany(generics.UpdateAPIView):
    def post(self, request, *args, **kwargs):
        company_id = request.data.get("company_id")
        name = request.data.get("name")
        location = request.data.get("location")

        try:
            company_obj = Company.objects.get(id=company_id)
        except:
            return Response({"status":False, "msg":"Company not found"}, status=status.HTTP_400_BAD_REQUEST)

        company_obj.update(company_name=name,company_location=location)
        return Response({"status":True, "msg": 'Company deatils upated successfully!', 'response':{}}, status=status.HTTP_200_OK)


# Adding projects
class AddProject(APIView):
    def post(self, request, *args, **kwargs):
        project_name = request.data.get("name")
        company_id = request.data.get("pk")
        try:
            company_obj = Company.objects.get(id=company_id)
        except:
            return Response({"status":False, "msg":"Company not found"}, status=status.HTTP_400_BAD_REQUEST)
        project_obj = Project.objects.create(company=company_obj,Project_name= project_name, is_active=True)
        return Response({"status":True, "msg": 'Project created successfully!', 'response':{}}, status=status.HTTP_200_OK)

# Adding employees
class AddEmployee(APIView):
    def post(self, request, *args, **kwargs):
        company_id = request.data.get("pk")
        employee_name = request.data.get("name")
        try:
            company_obj = Company.objects.get(id=company_id)
        except:
            return Response({"status":False, "msg":"Company not found"}, status=status.HTTP_400_BAD_REQUEST)
        project_obj = Employee.objects.create(company=company_obj,employee_name= employee_name, is_active=True)
        return Response({"status":True, "msg": 'Employee created successfully!', 'response':{}}, status=status.HTTP_200_OK)

# Assigning projects to employees
class AssignProject(generics.UpdateAPIView):
    def post(self, request, *args, **kwargs):
        project_id = request.data.get("project_id")
        employee_id = request.data.get("employee_id")
        try:
            project_obj = Project.objects.get(id=project_id)
        except:
            return Response({"status":False, "msg":"Project not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            employee_obj = Employee.objects.get(id=employee_id)
        except:
            return Response({"status":False, "msg":"Employee not found"}, status=status.HTTP_400_BAD_REQUEST)
        employee_obj.project.add(project_obj)
        return Response({"status":True, "msg": 'Project added successfully!', 'response':{}}, status=status.HTTP_200_OK)

        
# Deleting project
class DeleteProject(generic.DeleteView):

    def get(self, request, *args, **kwargs):
        project_id = kwargs['pk']
        try:
            project_obj = Project.objects.get(id=project_id)
        except:
            return Response({"status":False, "msg":"Project not found"}, status=status.HTTP_400_BAD_REQUEST)

        project_obj.update(is_active=False)
        return Response({"status":True, "msg": 'Project deleted successfully!', 'response':{}}, status=status.HTTP_200_OK)



# list of employees
class EmployeeLIstView(generics.ListAPIView):
    permission_classes = ()
    authentication_classes = ()

    def get(self, request, *args, **kwargs):
        company_id = request.GET.get('company_id')

        try:
            company_obj = Company.objects.get(id=company_id)
        except:
            return Response({"status":False, "msg":"company not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            employee_obj = Employee.objects.filter(company=company_obj,is_active=True)
            employee_list = EmployeeSerializer(instance=employee_obj, many=True).data
        except:
            return Response({"status":False, "msg":"no employees found."}, status=status.HTTP_400_BAD_REQUEST)
        data={
            'employee_list':employee_list,
        }
        return Response({"status":True, "msg": 'Success', 'response':data}, status=status.HTTP_200_OK)

# Get list of projects of a specific employee
class EmployeeProjectList(ListAPIView):
    def get(self, request, *args, **kwargs):
        employee_id = request.GET.get('employee_id')

        try:
            employee_obj = Employee.objects.get(id=employee_id)
        except:
            return Response({"status":False, "msg":"Employee not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            project_list = ProjectSerializer(instance=employee_obj.project.all(), many=True).data
        except:
            return Response({"status":False, "msg":"no Projects found."}, status=status.HTTP_400_BAD_REQUEST)
        data={
            'Project':project_list,
        }
        return Response({"status":True, "msg": 'Success', 'response':data}, status=status.HTTP_200_OK)


# Get list of employees working in a project
class ProjectEmployeeList(ListAPIView):
    def get(self, request, *args, **kwargs):
        project_id = request.GET.get('project_id')
        employee_obj = Employee.objects.filet(is_active=True)
        employee_list = []
        for each in employee_obj:
            for emplo in each.project.all():
                if emplo.id==project_id:
                    employee_list.append(emplo)
        employe_detail = EmployeeSerializer(instance=employee_list, many=True).data
        data={
            'employee_details':employe_detail,
        }
        return Response({"status":True, "msg": 'Success', 'response':data}, status=status.HTTP_200_OK)

