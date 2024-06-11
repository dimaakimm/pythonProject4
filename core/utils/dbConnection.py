import asyncpg


class Request:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    async def getAllRequests(self):
        query = "SELECT * FROM requests"
        return await self.connector.fetch(query)

    async def showProfile(self, userId):
        query = f"SELECT * FROM volunteers WHERE tg_id='{userId}'"
        return await self.connector.fetch(query)
    async def showPetProfile(self, petId):
        query = f"SELECT * FROM pets WHERE id='{petId}'"
        return await self.connector.fetch(query)

    async def showVolunteersPets(self, userId):
        query = f"SELECT * FROM pets WHERE vol_id='{userId}'"
        return await self.connector.fetch(query)

    async def add_data_pet(self, data, vol_id):
        query = f"INSERT INTO pets (photo_id, name, is_sterilized, district, info, vol_id) " \
                f"VALUES('{data['photo_id']}', '{data['name']}', " \
                 f"'{data['is_sterilized']}', '{data['district']}', '{data['info']}', '{vol_id}') "
        await self.connector.execute(query)

    async def delete_data_pet(self, pet_id):
        query = f"DELETE FROM pets  WHERE id = '{pet_id}'"
        await self.connector.execute(query)




