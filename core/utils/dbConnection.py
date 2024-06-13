import asyncpg


class Request:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    async def add_data(self, id, name):
        query = f"INSERT INTO users (id, name) " \
                f"VALUES({id}, '{name}') " \
                f"ON CONFLICT (id) DO UPDATE SET name='{name}'"
        await self.connector.execute(query)

    async def add_data_requests(self, data, userId):
        query = f"INSERT INTO requests (name, surname, email, phone, user_id) " \
                f"VALUES('{data['forename']}', '{data['surname']}', " \
                 f"'{data['email']}', '{data['phonenumber']}', {userId}) "
        await self.connector.execute(query)
