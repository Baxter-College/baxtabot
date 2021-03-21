from bot.models import WeekCal

def calendar_upload(url, date):
    '''
    Uploads a weekly calendar.
    If there is an existing calendar for that week, deletes it.

    Parameters:
    - url : of image
    - date : of week

    Exceptions:
    - InputError: Loading the url provided does not return a 200 status code
    - InputError: Date is not a valid date

    Return value: None
    '''
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
    '''
    Returns a list of all calendars.
    '''
    return WeekCal.select()
