from asyncio import create_task

class Player:
    def __init__(self, Member):
        self.MemberObject = Member
        self.Name = self.MemberObject.name
        self.Nickname = self.MemberObject.global_name
        self.UUID = self.MemberObject.id
        self.Health = 20
        self.Hunger = 0
        self.Thirst = 0
        self.Sanity = 100
        self.Morale = 500
        self.Age = 1
        self.Jobs = []