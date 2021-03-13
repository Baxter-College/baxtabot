from bot.models import WeekCal

def calendar_upload(url, date):
    # do image upload
    # response = functions.uploadAsset(url)

    # Delete any existing calendars for the same week
    existingCal = WeekCal.select().where(WeekCal.week_start == date)
    if existingCal:
        cal = existingCal.get()
        cal.delete_instance()

    WeekCal.create(
        assetID=url, week_start=date
    )

def calendars_all():
    return WeekCal.select()
