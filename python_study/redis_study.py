import datetime

import redis

r = redis.Redis(host='localhost', port=6379, db=7)

"""
node code
// 업스케일 요청에 대한 정보를 레디스에 저장한다.
insertRequestInfo: (hashKey, userId, requestId, filename, routingKey) => {
    redisClient.hmset(
        // hm key
        hashKey,
        // #region HM Value
        'userId',
        userId,
        'requestId',
        requestId,
        'filename',
        filename,
        'routingKey',
        routingKey,
        'status',
        'sendMQ',
        // #endregion hm value
        redisClient.print
    );
    // redisClient.expire(hashKey, 60 * 60 * 24 * 5);  // 업스케일 작업 정보는 레디스에서 5일 동안 저장된다.
},
updateProgress: (hashKey, progress, nowProcessing) => {
    redisClient.HMSET(hashKey, 'progress', progress, redisClient.print);
    redisClient.HMSET(hashKey, 'nowProcessing', nowProcessing, redisClient.print);
}
"""

def insert_request_info(hashkey, user_id, request_id, filename, routingkey):
    data = {
        'user_id':user_id,
        'request_id':request_id,
        'filename':filename,
        'routingkey':routingkey
    }
    r.hset(hashkey, mapping=data)
    r.expire(hashkey, datetime.timedelta(days=5))

def update_progress(hashkey, progress):
    r.hset(hashkey, mapping={'progress':progress})

insert_request_info('ssamko', 'ssamko', '17', 'kobra', '360')
update_progress('ssamko', 70)
