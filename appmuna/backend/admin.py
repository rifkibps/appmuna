from django.contrib import admin
from . import models


# Register your models here.



class CharacteristicItemsStacked(admin.StackedInline):
    model = models.BackendCharacteristicItemsModel

class CharacteristicItems(admin.ModelAdmin):
    inlines = [CharacteristicItemsStacked]



class RowsItemsStacked(admin.StackedInline):
    model = models.BackendRowsItemsModel

class RowsItems(admin.ModelAdmin):
    inlines = [RowsItemsStacked]


class PeriodsItemsStacked(admin.StackedInline):
    model = models.BackendPeriodNameItemsModel

class PeriodsItems(admin.ModelAdmin):
    inlines = [PeriodsItemsStacked]


admin.site.register(models.BackendIndicatorsModel)
admin.site.register(models.BackendSubjectsModel)
admin.site.register(models.BackendSubjectsSCAModel)
admin.site.register(models.BackendCharacteristicsModel, CharacteristicItems)
admin.site.register(models.BackendRowsModel, RowsItems)
admin.site.register(models.BackendPeriodsModel, PeriodsItems)

admin.site.register(models.BackendContentStatisModel)
admin.site.register(models.BackendContentIndicatorsModel)
admin.site.register(models.BackendUnitsModel)
admin.site.register(models.BackendInfographicsModel)
admin.site.register(models.BackendVideoGraphicsModel)
admin.site.register(models.BackendStatsNewsModel)

admin.site.register(models.BackendDataRequestsModel)
admin.site.register(models.BackendPublicationsModel)

