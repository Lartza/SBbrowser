# SPDX-License-Identifier: AGPL-3.0-or-later
from django.db import models


class Config(models.Model):
    key = models.TextField(primary_key=True)
    value = models.TextField()

    class Meta:
        managed = False
        db_table = 'config'


class Username(models.Model):
    userid = models.TextField(primary_key=True, db_column='userID')
    username = models.TextField(verbose_name='Username', db_column='userName')
    locked = models.IntegerField(default=0)

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
    videoid = models.TextField(db_column='videoID')
    userid = models.TextField(db_column='userID')
    actiontype = models.TextField(default='skip', db_column='actionType')
    category = models.TextField()
    hashedvideoid = models.TextField(blank=True, default='', db_column='hashedVideoID')
    reason = models.TextField(blank=True, default='')
    service = models.TextField(default='YouTube')
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'lockCategories'


class Sponsortime(models.Model):
    videoid = models.TextField(verbose_name='Video ID', db_column='videoID')
    starttime = models.FloatField(verbose_name='Start', db_column='startTime')
    endtime = models.FloatField(verbose_name='End', db_column='endTime')
    votes = models.IntegerField()
    locked = models.IntegerField(default=0)
    incorrectvotes = models.IntegerField(default=1, db_column='incorrectVotes')
    uuid = models.TextField(primary_key=True, verbose_name='UUID', db_column='UUID')
    user = models.ForeignKey(Username, on_delete=models.PROTECT, db_constraint=False, verbose_name='UserID',
                             db_column='userID')
    timesubmitted = models.BigIntegerField(verbose_name='Submitted', db_column='timeSubmitted')
    views = models.IntegerField()
    category = models.TextField(default='sponsor')
    actiontype = models.TextField(default='skip', db_column='actionType')
    service = models.TextField(default='YouTube')
    videoduration = models.FloatField(default=0, db_column='videoDuration')
    hidden = models.IntegerField(default=0)
    reputation = models.FloatField(default=0)
    shadowhidden = models.IntegerField(verbose_name='Shadowhidden', db_column='shadowHidden')
    hashedvideoid = models.TextField(blank=True, default='', db_column='hashedVideoID')
    useragent = models.TextField(blank=True, default='', db_column='userAgent')
    description = models.TextField(blank=True, default='')

    class Meta:
        managed = False
        db_table = 'sponsorTimes'

    def ignored(self) -> int:
        return self.votes <= -2

    def length(self) -> float:
        return self.endtime - self.starttime


class Categoryvote(models.Model):
    uuid = models.TextField(db_column='UUID')
    category = models.TextField()
    votes = models.IntegerField(default=0)
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'categoryVotes'


class Warnings(models.Model):
    userid = models.TextField(db_column='userID')
    issuetime = models.IntegerField(db_column='issueTime')
    issueruserid = models.TextField(db_column='issuerUserID')
    enabled = models.IntegerField()
    reason = models.TextField(blank=True, default='')

    class Meta:
        managed = False
        db_table = 'warnings'
