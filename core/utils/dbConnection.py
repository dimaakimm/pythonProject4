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

    async def getAllPoints(self):
        query = "SELECT address FROM points"
        return await self.connector.fetch(query)

        # admin

    async def insertNewAdmin(self, data):
        pointName = "%" + data["admin_point"] + "%"
        idPoint = await self.connector.execute((f"SELECT id FROM points WHERE "
                                                f"address LIKE '{pointName}'"))
        idPoint = int(idPoint.split(" ")[-1])
        queryInsertIntoAdminsPoints = (f"INSERT INTO admins_points (id_admin, id_point) "
                                       f"VALUES({data['admin_id']}, {idPoint})")
        queryInsertNewAdmin = (f"INSERT INTO admins (id, first_name, last_name, "
                               f"phone, photo, passport) "
                               f"VALUES({data['admin_id']}, '{data['admin_first_name']}',"
                               f" '{data['admin_last_name']}', '{data['admin_phone']}', "
                               f" '{data['admin_photo_id']}', '{data['admin_passport']}')")
        await self.connector.execute(queryInsertNewAdmin)
        await self.connector.execute(queryInsertIntoAdminsPoints)

    async def getAdminAllData(self, id_admin):
        query = f"SELECT * FROM admins WHERE id = {id_admin}"
        return await self.connector.fetch(query)

    async def add_data_volunteer(self, data):
        query = f"INSERT INTO volunteers (id, forename, surname, email, phone_number, photo_id, passport, food_balance)" \
                f"VALUES('{data['volunteer_id']}', '{data['volunteer_first_name']}', '{data['volunteer_last_name']}', '{data['volunteer_email']}','{data['volunteer_phone']}', '{data['volunteer_photo_id']}', '{data['volunteer_passport']}', '{data['volunteer_balance']}') "
        await self.connector.execute(query)





