# SPDX-License-Identifier: AGPL-3.0-or-later
from django.db import models


class Config(models.Model):
    key = models.TextField(primary_key=True)
    value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'config'


class Username(models.Model):
    userid = models.TextField(primary_key=True)
    username = models.TextField(blank=True, null=True, verbose_name='Username')

    class Meta:
        managed = False
        db_table = 'usernames'

    def __str__(self) -> str:
        return self.userid


class Vipuser(models.Model):
    userid = models.TextField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'vipusers'


class Nosegment(models.Model):
    videoid = models.TextField(primary_key=True)
    userid = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nosegments'


class Sponsortime(models.Model):
    videoid = models.TextField(blank=True, null=True, verbose_name='Video ID')
    starttime = models.FloatField(blank=True, null=True, verbose_name='Start')
    endtime = models.FloatField(blank=True, null=True, verbose_name='End')
    votes = models.BigIntegerField(blank=True, null=True)
#    incorrectvotes = models.BigIntegerField(blank=True, null=True)
    uuid = models.TextField(primary_key=True, verbose_name='UUID')
    user = models.ForeignKey(Username, blank=True, null=True, on_delete=models.PROTECT, db_constraint=False,
                             db_column='userid', verbose_name='UserID')
    timesubmitted = models.BigIntegerField(blank=True, null=True, verbose_name='Submitted')
    views = models.BigIntegerField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    shadowhidden = models.BigIntegerField(blank=True, null=True, verbose_name='Shadowhidden')
#    hashedvideoid = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sponsortimes'

    def ignored(self) -> int:
        return self.votes <= -2

    def length(self) -> float:
        return self.endtime - self.starttime

# class Categoryvote(models.Model):
#    uuid = models.TextField(blank=True, null=True)
#    category = models.TextField(blank=True, null=True)
#    votes = models.BigIntegerField(blank=True, null=True)
#
#    class Meta:
#        managed = False
#        db_table = 'categoryvotes'
