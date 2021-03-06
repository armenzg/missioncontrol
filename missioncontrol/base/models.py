from django.db import models


class Platform(models.Model):
    '''
    Represents a platform e.g. "windows"
    '''
    name = models.CharField(max_length=100, unique=True)
    telemetry_name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'platform'


class Channel(models.Model):
    '''
    Represents a release channel e.g. "beta", "esr", "nightly"
    '''
    name = models.CharField(max_length=100, unique=True)
    update_interval = models.DurationField()

    class Meta:
        db_table = 'channel'


class Build(models.Model):
    '''
    Represents a specific build of the product
    '''
    platform = models.ForeignKey(Platform)
    channel = models.ForeignKey(Channel)
    build_id = models.CharField(max_length=14)
    version = models.CharField(max_length=10)

    class Meta:
        db_table = 'build'
        unique_together = ('platform', 'channel', 'build_id', 'version')


class Measure(models.Model):
    '''
    Represents a type of measure (e.g. "main_crashes") on a particular channel

    Some measures occur only on specific types of platform (e.g. "gpu_crashes"
    is Windows-only)
    '''
    name = models.SlugField(max_length=100)
    min_version = models.PositiveIntegerField(null=True)
    # may want to add max_version in future (but for now, YAGNI)
    platform = models.ForeignKey(Platform)

    class Meta:
        db_table = 'measure'
        unique_together = ('name', 'platform')


class Series(models.Model):
    '''
    Represents a signature for a type of series on a specific build
    '''
    build = models.ForeignKey(Build)
    measure = models.ForeignKey(Measure)

    class Meta:
        db_table = 'series'


class Datum(models.Model):
    '''
    An individual data point for a specific series (see above)
    '''
    id = models.BigAutoField(primary_key=True)
    series = models.ForeignKey(Series)
    timestamp = models.DateTimeField()
    value = models.FloatField()
    usage_hours = models.FloatField()
    client_count = models.PositiveIntegerField()

    class Meta:
        db_table = 'datum'
