from bot.models import WeekCal

def calendar_upload(url):
    # do image upload
    response = functions.uploadAsset(url)

    # Delete any existing calendars for the same week
    existingCal = WeekCal.select().where(WeekCal.week_start == request.form['date'])
    if existingCal:
        cal = existingCal.get()
        cal.delete_instance()

    WeekCal.create(
        assetID=url, week_start=request.form["date"]
    )

def calendars_all():
    return WeekCal.select()
