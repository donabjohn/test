# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Distance(models.Model):
    shop_id = models.IntegerField(unique=True)
    shop_name = models.TextField(null=True,blank=True) 
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    location_name = models.TextField(null=True,blank=True) 

    class Meta:
        db_table = 'Distance'

class Company(models.Model):
    company_name = models.TextField(null=True,blank=True) 
    # employee = models.ForeignKey(Employee, null=True, blank=True)
    company_location = models.TextField(null=True,blank=True)
    is_active = models.BooleanField(default=True) 
    def __unicode__(self):
        return self.company_name
    

class Project(models.Model):
    Project_name = models.TextField(null=True,blank=True)
    company = models.ForeignKey(Company, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    def __unicode__(self):
        return self.Project_name

class Employee(models.Model):
    employee_name = models.TextField(null=True,blank=True)
    employee_id = models.IntegerField(unique=True,null=True,blank=True)
    project = models.ManyToManyField(Project, null=True, blank=True)
    company = models.ForeignKey(Company, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    def __unicode__(self):
        return self.employee_name































