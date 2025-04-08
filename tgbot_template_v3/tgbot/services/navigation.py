from aiogram.fsm.context import FSMContext

CALLBACKS_KEY = "callbacks"
#MESSAGE_ID_KEY = "message_id"

class CategoryNavigator:
    def __init__(self,state:FSMContext):
        self.state = state

    """  async def set_message_id(self,message_id):
        await self.state.update_data(MESSAGE_ID_KEY=message_id)
    
    @property
    async def message_id(self):
        data = await self.state.get_data()
        return data.get(MESSAGE_ID_KEY) """

    async def push(self,callback):
        data = await self.state.get_data()
        stack = data.get(CALLBACKS_KEY,[])
        stack.append(callback)
        await self.state.update_data(callbacks=stack)
    
    async def peek(self):
        data = await self.state.get_data()
        print(data)
        stack = data.get(CALLBACKS_KEY,[])
        if not stack:
            return None
        return stack[-1]

    async def pop(self):
        data = await self.state.get_data()
        stack = data.get(CALLBACKS_KEY,[])
        if not stack:
            return None
        step = stack.pop()
        await self.state.update_data(CALLBACKS_KEY=stack)
        return step
    
    async def clear(self):
        await self.state.clear()