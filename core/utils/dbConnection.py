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

    async def showVolunteerBalance(self, userId):
        query = f"SELECT * FROM volunteers_food WHERE volunteer_id='{userId}'"
        return await self.connector.fetch(query)

    async def showPetProfile(self, petId):
        query = f"SELECT * FROM pets WHERE id='{petId}'"
        return await self.connector.fetch(query)

    async def showVolunteersToOrder(self):
        query = f"SELECT * FROM volunteers WHERE state='wait'"
        return await self.connector.fetch(query)

    async def showPointsToOrder(self):
        query = f"SELECT * FROM points"
        return await self.connector.fetch(query)

    async def getAdressById(self, pointId):
        query = f"SELECT address FROM points WHERE id = '{pointId}' LIMIT 1"
        return await self.connector.fetchval(query)

    async def getVolunteerFoodById(self, volunteerId):
        query = f"SELECT * FROM volunteers_food LIMIT 1" #ДОБАВИТЬ ЧТОБЫ БРАЛАСЬ ИНФА ПО АЙДИШНИКУ ИЗ VOLUNTEERS_FOOD
        return await self.connector.fetch(query)

    async def showVolunteersPets(self, userId):
        query = f"SELECT * FROM pets WHERE vol_id='{userId}'"
        return await self.connector.fetch(query)

    async def giveFoodFromVtoV(self, fromId, toId, raw_cat_food, dry_cat_food, raw_dog_food, dry_dog_food):
        query = f"UPDATE volunteers_food SET" \
                f" raw_cat_food = raw_cat_food - {raw_cat_food}," \
                f" dry_cat_food = dry_cat_food - {dry_cat_food}," \
                f" raw_dog_food = dry_cat_food - {raw_dog_food}," \
                f" dry_dog_food = dry_cat_food - {dry_dog_food}" \
                f" WHERE volunteer_id = '{fromId}'"
        await self.connector.execute(query)
        query = f"UPDATE volunteers_food SET" \
                f" raw_cat_food = raw_cat_food + {raw_cat_food}," \
                f" dry_cat_food = dry_cat_food + {dry_cat_food}," \
                f" raw_dog_food = dry_cat_food + {raw_dog_food}," \
                f" dry_dog_food = dry_cat_food + {dry_dog_food}" \
                f" WHERE volunteer_id = '{toId}'"
        await self.connector.execute(query)

    async def add_data_pet(self, data, vol_id):
        query = f"INSERT INTO pets (photo_id, name, is_sterilized, district, info, vol_id) " \
                f"VALUES('{data['photo_id']}', '{data['name']}', " \
                f"'{data['is_sterilized']}', '{data['district']}', '{data['info']}', '{vol_id}') "
        await self.connector.execute(query)

    async def add_data_admin(self, data):
        query = f"INSERT INTO admins (id, first_name, last_name, phone, photo, passport) " \
                f"VALUES('{data['admin_id']}', '{data['admin_first_name']}', '{data['admin_last_name']}', '{data['admin_phone']}', '{data['admin_photo']}', '{data['admin_passport']}') "
        await self.connector.execute(query)

    async def add_data_volunteer(self, data):
        query = (
            f"INSERT INTO volunteers (id, forename, surname, email, phone_number, photo_id, passport, food_balance)" \
            f"VALUES('{data['volunteer_id']}', '{data['volunteer_first_name']}', '{data['volunteer_last_name']}', '{data['volunteer_email']}','{data['volunteer_phone']}', '{data['volunteer_photo_id']}', '{data['volunteer_passport']}', '{data['volunteer_balance']}') ")

        await self.connector.execute(query)

    async def add_data_volunteers_food(self, data):
        querryBalance = (
            f'INSERT INTO volunteers_food (volunteer_id, raw_cat_food, raw_dog_food, dry_dog_food, dry_cat_food)' \
            f"VALUES({data['volunteer_id']}, 0, 0, 0, 0)")

        await self.connector.execute(querryBalance)

    async def delete_data_pet(self, petId):
        query = f"DELETE FROM pets  WHERE id = '{petId}'"
        await self.connector.execute(query)

    async def delete_data_admin(self, adminId):
        query = f"DELETE FROM admins WHERE id = '{adminId}'"
        await self.connector.execute(query)

    async def delete_data_volunteers(self, volunteersId):
        query = f"DELETE FROM volunteers WHERE id = '{volunteersId}'"
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

    async def showPinnedPoints(self, adminId):
        query = f"SELECT f.* \
                FROM points f \
                JOIN admins_points s on f.id = s.id_point \
                WHERE s.id_admin='{adminId}'"
        return await self.connector.fetch(query)

    async def showPointInfo(self, pointId):
        query = f"SELECT f.* \
                 FROM points f \
                 WHERE id='{pointId}'"
        return await self.connector.fetch(query)

    async def updatePointFood(self, data, updateType):
        if updateType == "increase":
            query = f"UPDATE points SET {data['foodType']} = {data['foodType']} + {data['foodVolume']} \
            WHERE id = '{data['pointId']}'"
        elif updateType == "decrease":
            query = f"UPDATE points SET {data['foodType']} = {data['foodType']} - {data['foodVolume']} \
            WHERE id = '{data['pointId']}'"
        await self.connector.execute(query)

    async def upgradeVolunteerFoodBalance(self, data, updateType):
        if updateType == "increase":
            query = f"UPDATE volunteers_food SET {data['foodType']} = {data['foodType']} + {data['foodVolume']} \
            WHERE volunteer_id = {data['volunteer_id']}"
        elif updateType == "decrease":
            query = f"UPDATE volunteers_food SET {data['foodType']} = {data['foodType']} - {data['foodVolume']} \
            WHERE volunteer_id = {data['volunteer_id']}"
        await self.connector.execute(query)

    async def addNewOrder(self, idVolunteer, data):
        query = f"INSERT INTO orders (volunteer_id, raw_cat_food, raw_dog_food, dry_dog_food, dry_cat_food)" \
                f"VALUES('{idVolunteer}', '{data['raw_cat_food']}', '{data['raw_dog_food']}', '{data['dry_dog_food']}', '{data['dry_cat_food']}')"
        await self.connector.execute(query)

    async def InsertNewPhoto(self, photo):
        orderIdQuery = "SELECT MAX(id) FROM orders"
        orderId = await self.connector.execute(orderIdQuery)
        orderId = orderId.split(" ")[-1]
        query = f"INSERT INTO photo (photo, order_id) VALUES('{photo}', '{orderId}')"
        await self.connector.execute(query)

    async def updateVolunteerGetOrderStatus(self, idVolunteer, newStatus, pointId=None):
        query = f"UPDATE volunteers SET state = '{newStatus}' WHERE id = '{idVolunteer}'"
        await self.connector.execute(query)
        if (pointId != None):
            query = f"UPDATE volunteers SET point_id = '{pointId}' WHERE id = '{idVolunteer}'"
        else:
            query = f"UPDATE volunteers SET point_id = DEFAULT WHERE id = '{idVolunteer}'"
        await self.connector.execute(query)
