from django.contrib import admin

from .models import Fund


class FundAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'apply_date', 'activity_date', 'charger', 'fund_status')       


admin.site.register(Fund, FundAdmin)
