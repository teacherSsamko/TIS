import GPUtil

def get_available_device(max_memory=0.49):
    GPUs = GPUtil.getGPUs()
    freeMemory = 0
    available = -1
    for GPU in GPUs:
        # print('GPU.memoryUtil type =>', type(GPU.memoryUtil))
        # print('max_memory type =>', type(max_memory))
        if GPU.memoryUtil > max_memory:
            continue
        if GPU.memoryFree >= freeMemory:
            freeMemory = GPU.memoryFree
            available = GPU.id
        
    return available

try:
    deviceID = GPUtil.getFirstAvailable(order = 'first', maxLoad=0.75, maxMemory=0.5, attempts=2, interval=2, verbose=False)
    print(deviceID)
except:
    print('error')