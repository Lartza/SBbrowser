# SPDX-License-Identifier: AGPL-3.0-or-later
from django.db import models


class Config(models.Model):
    key = models.TextField(primary_key=True)
    value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'config'


class Username(models.Model):
    userid = models.TextField(primary_key=True, db_column='userID')
    username = models.TextField(blank=True, null=True, verbose_name='Username', db_column='userName')

    class Meta:
        managed = False
        db_table = 'userNames'

    def __str__(self) -> str:
        return self.userid


class Vipuser(models.Model):
    userid = models.TextField(primary_key=True, db_column='userID')

    class Meta:
        managed = False
        db_table = 'vipUsers'


class Lockcategory(models.Model):
    videoid = models.TextField(primary_key=True, db_column='videoID')
    userid = models.TextField(blank=True, null=True, db_column='userID')
    actiontype = models.TextField(blank=True, null=False, db_column='actionType')
    category = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lockCategories'


class Sponsortime(models.Model):
    videoid = models.TextField(blank=True, null=True, verbose_name='Video ID', db_column='videoID')
    starttime = models.FloatField(blank=True, null=True, verbose_name='Start', db_column='startTime')
    endtime = models.FloatField(blank=True, null=True, verbose_name='End', db_column='endTime')
    votes = models.IntegerField(blank=True, null=True)
    locked = models.IntegerField(blank=True, null=True)
    incorrectvotes = models.IntegerField(blank=True, null=True, db_column='incorrectVotes')
    uuid = models.TextField(primary_key=True, verbose_name='UUID', db_column='UUID')
    user = models.ForeignKey(Username, blank=True, null=True, on_delete=models.PROTECT, db_constraint=False,
                             db_column='userID', verbose_name='UserID')
    timesubmitted = models.BigIntegerField(blank=True, null=True, verbose_name='Submitted', db_column='timeSubmitted')
    views = models.IntegerField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    service = models.TextField(blank=True, null=True)
    videoduration = models.FloatField(db_column='videoDuration')
    actiontype = models.TextField(db_column='actionType')
    hidden = models.IntegerField(blank=True, null=True)
    shadowhidden = models.IntegerField(blank=True, null=True, verbose_name='Shadowhidden', db_column='shadowHidden')
    hashedvideoid = models.TextField(blank=True, null=True, db_column='hashedVideoID')
    useragent = models.TextField(blank=True, null=False, default='', db_column='userAgent')

    class Meta:
        managed = False
        db_table = 'sponsorTimes'

    def ignored(self) -> int:
        return self.votes <= -2

    def length(self) -> float:
        return self.endtime - self.starttime

# class Categoryvote(models.Model):
#    uuid = models.TextField(primary_key=True, db_column='UUID')
#    category = models.TextField(blank=True, null=True)
#    votes = models.IntegerField(blank=True, null=True)
#
#    class Meta:
#        managed = False
#        db_table = 'categoryVotes'


# class Warnings(models.Model):
#    userid = models.TextField(db_column='userID')  # Field name made lowercase.
#    issuetime = models.BigIntegerField(db_column='issueTime')  # Field name made lowercase.
#    issueruserid = models.TextField(db_column='issuerUserID')  # Field name made lowercase.
#    enabled = models.IntegerField()
#
#    class Meta:
#        managed = False
#        db_table = 'warnings'
