import asyncpg


class Request:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    async def getAllRequests(self):
        query = "SELECT * FROM requests"
        return await self.connector.fetch(query)

    async def add_data_requests(self, data, userId):
        query = f"INSERT INTO requests (name, surname, email, phone, user_id) " \
                f"VALUES('{data['forename']}', '{data['surname']}', " \
                 f"'{data['email']}', '{data['phonenumber']}', {userId}) "
        await self.connector.execute(query)