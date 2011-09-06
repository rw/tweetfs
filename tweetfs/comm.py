MemoryCtr, MemoryKV = -1, {}
def memory_uploader(bson_blob):
    global MemoryCtr
    global MemoryKV
    MemoryCtr += 1
    MemoryKV[MemoryCtr] = bson_blob
    return MemoryCtr

def memory_downloader(tweet_id):
    return MemoryKV[tweet_id]
