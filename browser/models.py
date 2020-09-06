# SPDX-License-Identifier: AGPL-3.0-or-later
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
    key = models.TextField(primary_key=True, unique=True)
    value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'config'


class Username(models.Model):
    userid = models.TextField(primary_key=True, unique=True)
    username = models.TextField(verbose_name='Username')

    class Meta:
        managed = False
        db_table = 'usernames'

    def __str__(self) -> str:
        return self.userid


class Sponsortime(models.Model):
    videoid = models.TextField(verbose_name='Video ID')
    starttime = models.FloatField(verbose_name='Start')
    endtime = models.FloatField(verbose_name='End')
    votes = models.BigIntegerField()
    incorrectvotes = models.BigIntegerField()
    uuid = models.TextField(verbose_name='UUID', primary_key=True, unique=True)
    user = models.ForeignKey(Username, verbose_name='UserID', on_delete=models.PROTECT, db_constraint=False,
                             null=False, db_column='userid')
    timesubmitted = models.BigIntegerField(verbose_name='Submitted')
    views = models.BigIntegerField()
    category = models.TextField()
    shadowhidden = models.BigIntegerField(verbose_name='Shadowhidden')

    class Meta:
        managed = False
        db_table = 'sponsortimes'

    def ignored(self) -> int:
        return self.votes <= -2

    def length(self) -> float:
        return self.endtime - self.starttime


class Vipuser(models.Model):
    userid = models.TextField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = 'vipusers'
