import datetime

def chainlogis_date_format(data_str):
    # 2020-08-04T22:24:03.000Z
    date_str = data_str.split("T")[0]
    time_str = data_str.split("T")[1][:8]
    new_dt = "{} {}".format(date_str, time_str)
    print(new_dt)
    new_dt = datetime.datetime.strptime(new_dt, "%Y-%m-%d %H:%M:%S")
    print(type(new_dt))
    


chainlogis_date_format('2020-08-04T22:24:03.000Z')