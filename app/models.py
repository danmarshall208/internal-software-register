from django.db import models
import datetime


class User(models.Model):
    name = models.CharField(max_length=100)
    sesa = models.CharField(max_length=20, primary_key=True)
    email = models.CharField(max_length=100)
    manager = models.ForeignKey('self', related_name="team_members", blank=True, null=True)
    DN = models.CharField(max_length=200)
    active = models.BooleanField()

    def __str__(self):
        return self.name


class DependencyTag(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name


class BusinessTag(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name


class Tool(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, related_name="tools_owned")
    developer = models.CharField(max_length=100)
    created_by = models.CharField(max_length=100)
    date_added = models.DateField(auto_now_add=True)
    year_created = models.IntegerField(blank=True, null=True)
    short_description = models.CharField(max_length=500)
    long_description = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    restricted_access = models.BooleanField()
    instructions = models.TextField(blank=True, null=True)
    dependency_tags = models.ManyToManyField(DependencyTag, related_name="tools", blank=True)
    business_tags = models.ManyToManyField(BusinessTag, related_name="tools", blank=True)
    active = models.BooleanField()
    future_plans = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def register_update(self, updater, description):
        update = Update(date=datetime.datetime.now(), tool=self, updated_by=updater, description=description)
        update.save()


class Update(models.Model):
    date = models.DateField(auto_now_add=True)
    tool = models.ForeignKey(Tool, related_name='updates')
    updated_by = models.ForeignKey(User, related_name='updates')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.tool.name + " - " + str(self.date)

class Feedback(models.Model):
    date = models.DateField(auto_now_add=True)
    sesa = models.CharField(max_length=20)
    text = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.text
