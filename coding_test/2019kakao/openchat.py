class OpenChat:
    def __init__(self):
        self.member = {}
        self.result = []
        self.idx = 0
        self.functions = dict(
            Enter=self.Enter, 
            Leave=self.Leave,
            Change=self.Change)

    def input_proc(self, line):
        (task, *user) = line.split()
        # print(task)
        # print(user)
        self.functions[task](*user)

    def Enter(self, *args):
        print(args)
        uid, nick = args
        # if self.member.get(uid):
        #     for item in self.result:
        #         if item.get('uid') == uid:
        #             item['nick'] = nick
        self.member[uid] = nick
        data = {
            'idx':self.idx,
            'uid':uid,
            'nick':nick,
            'text':'님이 들어왔습니다.'
        }
        self.result.append(data)
        self.idx += 1
        print(data)
        
    def Leave(self, *args):
        uid = args[0]
        data = {
            'idx':self.idx,
            'uid':uid,
            'nick':self.member[uid],
            'text':'님이 나갔습니다.'
        }
        self.result.append(data)
        self.idx += 1
        print(data)

    def Change(self, *args):

        uid, nick = args
        self.member[uid] = nick
        # result 변경
        # for item in self.result:
        #     if item.get('uid') == uid:
        #         item['nick'] = nick
        print(self.member)
        print(self.result)

        self.idx += 1

    def make_result(self):
        for item in self.result:
            item['nick'] = self.member[item['uid']]
        self.result = list(map(lambda x: x['nick']+x['text'], self.result))

def solution(record):
    room = OpenChat()
    for item in record:
        room.input_proc(item)
    room.make_result()
    answer = room.result
    print(answer)
    
    return answer

def test_solution():
    record = ["Enter uid1234 Muzi", "Enter uid4567 Prodo","Leave uid1234","Enter uid1234 Prodo","Change uid4567 Ryan"]
    answer = ["Prodo님이 들어왔습니다.", "Ryan님이 들어왔습니다.", "Prodo님이 나갔습니다.", "Prodo님이 들어왔습니다."]
    assert(solution(record) == answer)
    print('pass')

if __name__=="__main__":
    test_solution()