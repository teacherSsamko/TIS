import importlib.util


spec = importlib.util.spec_from_file_location("schedule_api", "/Users/ssamko/Documents/aircode_api/schedule_api.py")
foo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(foo)
scheduler = foo.Scheduler()
scheduler.get_schedule()