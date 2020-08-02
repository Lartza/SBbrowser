# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


# class ReadmeLicense(models.Model):
#     info = models.TextField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'README:LICENSE'


# class Categoryvotes(models.Model):
#     uuid = models.TextField(primary_key=True, blank=True)
#     category = models.TextField(blank=True, null=True)
#     votes = models.BigIntegerField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'categoryvotes'


class Config(models.Model):
    key = models.TextField(primary_key=True, unique=True, null=False)
    value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'config'


class Username(models.Model):
    userid = models.TextField(primary_key=True, unique=True, null=False)
    username = models.TextField(verbose_name='Username', null=False)

    class Meta:
        managed = False
        db_table = 'usernames'

    def __str__(self):
        return self.userid


class Sponsortime(models.Model):
    videoid = models.TextField(verbose_name='Video ID', null=False)
    starttime = models.FloatField(verbose_name='Start', null=False)
    endtime = models.FloatField(verbose_name='End', null=False)
    votes = models.BigIntegerField(null=False)
    incorrectvotes = models.BigIntegerField(null=False)
    uuid = models.TextField(verbose_name='UUID', primary_key=True, unique=True, null=False)
    user = models.ForeignKey(Username, verbose_name='UserID', on_delete=models.PROTECT, db_constraint=False,
                             null=False, db_column='userid')
    timesubmitted = models.BigIntegerField(verbose_name='Submitted', null=False)
    views = models.BigIntegerField(null=False)
    category = models.TextField(null=False)
    shadowhidden = models.BigIntegerField(verbose_name='Hidden', null=False)

    class Meta:
        managed = False
        db_table = 'sponsortimes'

    def ignored(self):
        return self.votes <= -2


class Vipuser(models.Model):
    userid = models.TextField(primary_key=True, unique=True, null=False)

    class Meta:
        managed = False
        db_table = 'vipusers'
