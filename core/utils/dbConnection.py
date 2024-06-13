import asyncpg


class Request:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    async def getAllRequests(self):
        query = "SELECT * FROM requests"
        return await self.connector.fetch(query)

    async def showProfile(self, userId):
        query = f"SELECT * FROM volunteers WHERE id='{userId}'"
        return await self.connector.fetch(query)
    async def showPetProfile(self, petId):
        query = f"SELECT * FROM pets WHERE id='{petId}'"
        return await self.connector.fetch(query)

    async def showVolunteersPets(self, userId):
        query = f"SELECT * FROM pets WHERE vol_id='{userId}'"
        return await self.connector.fetch(query)

    async def giveFoodFromVtoV(self, fromId, toId, volume):
        query = f"UPDATE volunteers SET food_balance = food_balance - {volume} WHERE id = '{fromId}'"
        await self.connector.execute(query)
        query = f"UPDATE volunteers SET food_balance = food_balance + {volume} WHERE id = '{toId}'"
        await self.connector.execute(query)

    async def add_data_pet(self, data, vol_id):
        query = f"INSERT INTO pets (photo_id, name, is_sterilized, district, info, vol_id) " \
                f"VALUES('{data['photo_id']}', '{data['name']}', " \
                 f"'{data['is_sterilized']}', '{data['district']}', '{data['info']}', '{vol_id}') "
        await self.connector.execute(query)

    async def delete_data_pet(self, petId):
        query = f"DELETE FROM pets  WHERE id = '{petId}'"
        await self.connector.execute(query)

    async def varifyAdmin(self, candidateId):
        query = f"SELECT EXISTS(SELECT 1 FROM admins WHERE id='{candidateId}')"
        result = await self.connector.fetchval(query)
        return bool(result)

    async def varifyVolunteer(self, candidateId):
        query = f"SELECT EXISTS(SELECT 1 FROM volunteers WHERE id='{candidateId}')"
        result = await self.connector.fetchval(query)
        return bool(result)





