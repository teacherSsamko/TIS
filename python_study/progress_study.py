import time
import progressbar

# for i in progressbar.progressbar(range(100)):
    # time.sleep(0.05)


# for i in progressbar.progressbar(range(100), redirect_stdout=True):
#     print('Some text', i)
#     time.sleep(0.1)

# bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
# for i in range(20):
#     time.sleep(0.1)
#     bar.update(i)

widgets=[
    ' [', progressbar.Timer(), '] ',
    progressbar.ETA(),
    ' (', progressbar.ETA(), ') ',
]
for i in progressbar.progressbar(range(60), widgets=widgets):
    time.sleep(0.1)