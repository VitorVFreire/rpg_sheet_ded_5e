import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from dotenv import load_dotenv
import os
import psycopg_pool

load_dotenv()

async def open_pool():
    conninfo = f'host={os.getenv("HOST")} dbname=postgres port={os.getenv("PORT")} user={os.getenv("USER")} password={os.getenv("PASSWORD")}'
    pool = psycopg_pool.AsyncConnectionPool(conninfo=conninfo, open=False)
    await pool.open()
    await pool.wait()
    print("Connection Pool Opened")
    return pool

async def create_database():
    pool = await open_pool()  # Open the pool before using it
    async with pool.connection() as conn:
        # Set autocommit mode to True
        await conn.set_autocommit(True)
        async with conn.cursor() as cursor:
            try:
                await cursor.execute('DROP DATABASE IF EXISTS rpg')

                await cursor.execute("""
                    CREATE DATABASE rpg
                        WITH
                        OWNER = rpg
                        ENCODING = 'UTF8'
                        LC_COLLATE = 'en_US.utf8'
                        LC_CTYPE = 'en_US.utf8'
                        LOCALE_PROVIDER = 'libc'
                        TABLESPACE = pg_default
                        CONNECTION LIMIT = -1
                        IS_TEMPLATE = False;
                """)
            finally:
                await cursor.close()
                await pool.close()

async def create_tables():
    conninfo = f'host={os.getenv("HOST")} dbname={os.getenv("DATABASE")} port={os.getenv("PORT")} user={os.getenv("USER")} password={os.getenv("PASSWORD")}'
    pool = psycopg_pool.AsyncConnectionPool(conninfo=conninfo, open=False)
    await pool.open()
    await pool.wait()
    async with pool.connection() as conn:
        await conn.set_autocommit(True)
        async with conn.cursor() as cursor:
            try:
                await cursor.execute("""
                CREATE TABLE coin (
                    coin_id SERIAL PRIMARY KEY ,
                    coin_name VARCHAR(20) NOT NULL
                );
                """)

                await cursor.execute("""
                CREATE TABLE kind_equipment (
                    kind_equipment_id SERIAL PRIMARY KEY ,
                    kind_equipment_name VARCHAR(30) NOT NULL
                );
                """)

                await cursor.execute("""
                CREATE TABLE type_damage (
                    type_damage_id SERIAL PRIMARY KEY ,
                    type_damage_name VARCHAR(30) NOT NULL
                );
                """)

                await cursor.execute("""
                CREATE TABLE equipment (
                    equipment_id SERIAL PRIMARY KEY ,
                    kind_equipment_id SERIAL NOT NULL REFERENCES kind_equipment(kind_equipment_id) ON DELETE CASCADE,
                    equipment_name VARCHAR(100) NOT NULL,
                    description_equipment VARCHAR(200),
                    price FLOAT,
                    coin_id SERIAL REFERENCES coin(coin_id) ON DELETE CASCADE,
                    weight FLOAT,
                    armor_class INT,
                    amount_dice INT,
                    side_dice INT,
                    type_damage_id SERIAL REFERENCES type_damage(type_damage_id) ON DELETE CASCADE,
                    bonus VARCHAR(20),
                    equipment_image VARCHAR(200)
                );
                
                ALTER TABLE equipment
                ALTER COLUMN type_damage_id DROP NOT NULL;
                """)

                await cursor.execute("""
                CREATE TABLE spell (
                    spell_id SERIAL PRIMARY KEY ,
                    spell_name VARCHAR(35) NOT NULL,
                    description_spell VARCHAR(200),
                    spell_level INT NOT NULL,
                    attribute_use VARCHAR(30),
                    amount_dice INT,
                    side_dice INT,
                    type_damage_id SERIAL REFERENCES type_damage(type_damage_id) ON DELETE CASCADE,
                    add_per_level INT
                );               
                """)

                await cursor.execute("""
                CREATE TABLE class (
                    class_id SERIAL PRIMARY KEY ,
                    class_name VARCHAR(30) NOT NULL,
                    description_class VARCHAR(200)
                );
                """)

                await cursor.execute("""
                CREATE TABLE spell_class (
                    spell_class_id SERIAL PRIMARY KEY ,
                    spell_id SERIAL NOT NULL REFERENCES spell(spell_id) ON DELETE CASCADE,
                    class_id SERIAL NOT NULL REFERENCES class(class_id) ON DELETE CASCADE
                );
                """)

                await cursor.execute("""
                CREATE TABLE skill (
                    skill_id SERIAL PRIMARY KEY ,
                    skill_name VARCHAR(30) NOT NULL,
                    usage_status VARCHAR(30) NOT NULL
                );
                """)

                await cursor.execute("""
                CREATE TABLE saving_throw (
                    saving_throw_id SERIAL PRIMARY KEY ,
                    saving_throw_name VARCHAR(30) NOT NULL
                );           
                """)

                await cursor.execute("""
                CREATE TABLE room (
                    room_id SERIAL PRIMARY KEY ,
                    room_name VARCHAR(100) NOT NULL UNIQUE,
                    room_password VARCHAR(300),
                    room_image VARCHAR(200)
                );         
                """)

                await cursor.execute("""
                CREATE TABLE "user" (
                    user_id SERIAL PRIMARY KEY ,
                    user_name VARCHAR(30) NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    email VARCHAR(300) NOT NULL,
                    birth_date DATE NOT NULL,
                    user_type INT NOT NULL CHECK (user_type IN (1, 2)) DEFAULT 2,
                    date_creation DATE NOT NULL
                );
                """)

                await cursor.execute("""
                CREATE TABLE user_room (
                    user_room_id SERIAL PRIMARY KEY ,
                    user_id SERIAL NOT NULL REFERENCES "user"(user_id) ON DELETE CASCADE,
                    room_id SERIAL NOT NULL REFERENCES room(room_id) ON DELETE CASCADE,
                    user_room_type INT DEFAULT 2 CHECK (user_room_type IN (1, 2))
                );
                """)
                
                await cursor.execute("""
                CREATE TABLE square (
                    square_id SERIAL PRIMARY KEY ,
                    user_room_id SERIAL NOT NULL REFERENCES user_room(user_room_id) ON DELETE CASCADE,
                    x FLOAT,
                    y FLOAT,
                    square_image VARCHAR(200)
                );
                """)

                await cursor.execute("""
                CREATE TABLE race (
                    race_id SERIAL PRIMARY KEY ,
                    race_name VARCHAR(30) NOT NULL,
                    description_race VARCHAR(200)
                );
                """)

                await cursor.execute("""
                CREATE TABLE character (
                    character_id SERIAL PRIMARY KEY ,
                    user_id SERIAL NOT NULL REFERENCES "user"(user_id) ON DELETE CASCADE,
                    race_id SERIAL NOT NULL REFERENCES race(race_id) ON DELETE CASCADE,
                    character_name VARCHAR(30) NOT NULL,
                    date_creation DATE NOT NULL
                );
                """)

                await cursor.execute("""
                CREATE TABLE message (
                    message_id SERIAL PRIMARY KEY ,
                    room_id SERIAL NOT NULL REFERENCES room(room_id) ON DELETE CASCADE,
                    character_id SERIAL REFERENCES character(character_id) ON DELETE CASCADE,
                    user_id SERIAL REFERENCES "user"(user_id) ON DELETE CASCADE,
                    messagetime TIMESTAMP NOT NULL,
                    message VARCHAR(200) NOT NULL
                );
                
                ALTER TABLE message
                ALTER COLUMN character_id DROP NOT NULL;
                ALTER TABLE message
                ALTER COLUMN user_id DROP NOT NULL;
                """)

                await cursor.execute("""
                CREATE TABLE character_characteristic (
                    character_characteristic_id SERIAL PRIMARY KEY ,
                    character_id SERIAL NOT NULL REFERENCES character(character_id) ON DELETE CASCADE,
                    age INT,
                    height FLOAT,
                    weight FLOAT,
                    eye_color VARCHAR(20),
                    skin_color VARCHAR(20),
                    color_hair VARCHAR(20),
                    character_image VARCHAR(200)
                );
                """)
                
                await cursor.execute("""
                CREATE TABLE character_attribute (
                    character_attribute_id SERIAL PRIMARY KEY ,
                    character_id SERIAL NOT NULL REFERENCES character(character_id) ON DELETE CASCADE,
                    strength INT,
                    dexterity INT,
                    intelligence INT,
                    constitution INT,
                    wisdom INT,
                    charisma INT,
                    proficiency_bonus INT
                );
                """)

                await cursor.execute("""
                CREATE TABLE status_base (
                    status_base_id SERIAL PRIMARY KEY ,
                    character_id SERIAL NOT NULL REFERENCES character(character_id) ON DELETE CASCADE,
                    level INT,
                    experience_points FLOAT,
                    alignment VARCHAR(30),
                    faction VARCHAR(30),
                    background VARCHAR(30),
                    movement FLOAT,
                    initiative INT,
                    hit_points INT,
                    current_hit_points INT,
                    temporary_hit_points INT,
                    inspiration INT,
                    armor_class INT
                );
                """)

                await cursor.execute("""
                CREATE TABLE character_equipment (
                    character_equipment_id SERIAL PRIMARY KEY ,
                    equipment_id SERIAL NOT NULL REFERENCES equipment(equipment_id) ON DELETE CASCADE,
                    character_id SERIAL NOT NULL REFERENCES character(character_id) ON DELETE CASCADE,
                    amount INT
                );
                """)

                await cursor.execute("""
                CREATE TABLE character_coin (
                    character_coin_id SERIAL PRIMARY KEY ,
                    coin_id SERIAL NOT NULL REFERENCES coin(coin_id) ON DELETE CASCADE,
                    character_id SERIAL NOT NULL REFERENCES character(character_id) ON DELETE CASCADE,
                    amount_coin INT
                );
                """)

                await cursor.execute("""
                CREATE TABLE character_class (
                    character_class_id SERIAL PRIMARY KEY ,
                    class_id SERIAL NOT NULL REFERENCES class(class_id) ON DELETE CASCADE,
                    character_id SERIAL NOT NULL REFERENCES character(character_id) ON DELETE CASCADE
                );
                """)

                await cursor.execute("""
                CREATE TABLE character_skill (
                    character_skill_id SERIAL PRIMARY KEY ,
                    skill_id SERIAL NOT NULL REFERENCES skill(skill_id) ON DELETE CASCADE,
                    character_id SERIAL NOT NULL REFERENCES character(character_id) ON DELETE CASCADE
                );
                """)

                await cursor.execute("""
                CREATE TABLE character_saving_throw (
                    character_saving_throw_id SERIAL PRIMARY KEY ,
                    saving_throw_id SERIAL NOT NULL REFERENCES saving_throw(saving_throw_id) ON DELETE CASCADE,
                    character_id SERIAL NOT NULL REFERENCES character(character_id) ON DELETE CASCADE
                );
                """)

                await cursor.execute("""
                CREATE TABLE character_spell (
                    character_spell_id SERIAL PRIMARY KEY ,
                    spell_id SERIAL NOT NULL REFERENCES spell(spell_id) ON DELETE CASCADE,
                    character_id SERIAL NOT NULL REFERENCES character(character_id) ON DELETE CASCADE
                );
                """)

                await cursor.execute("""
                CREATE TABLE spell_slot (
                    spell_slot_id SERIAL PRIMARY KEY ,
                    character_id SERIAL NOT NULL REFERENCES character(character_id) ON DELETE CASCADE,
                    level INT NOT NULL,
                    slot INT NOT NULL
                );
                """)

            finally:
                await cursor.close()
                await pool.close()
        
async def insert_default_values():
    conninfo = f'host={os.getenv("HOST")} dbname={os.getenv("DATABASE")} port={os.getenv("PORT")} user={os.getenv("USER")} password={os.getenv("PASSWORD")}'
    pool = psycopg_pool.AsyncConnectionPool(conninfo=conninfo, open=False)
    await pool.open()
    await pool.wait()
    async with pool.connection() as conn:
        await conn.set_autocommit(True)
        async with conn.cursor() as cursor:
            try:
                #password: 123
                await cursor.execute("""
                INSERT INTO "user"(user_name, password, email, birth_date, user_type, date_creation)
                VALUES('teste', 'pmWkWSBCL51Bfkhn79xPuKBKHz//H6B+mY6G9/eieuM=', 'teste@teste', '01-01-2000', 1, '01-01-2000');
                """)
                
                await cursor.execute("""
                INSERT INTO skill (skill_name, usage_status)
                VALUES
                    ('acrobatics', 'dexterity'),
                    ('arcana', 'intelligence'),
                    ('athletics', 'strength'),
                    ('performance', 'charisma'),
                    ('deception', 'charisma'),
                    ('stealth', 'dexterity'),
                    ('history', 'intelligence'),
                    ('intimidation', 'charisma'),
                    ('insight', 'wisdom'),
                    ('investigation', 'intelligence'),
                    ('animal_handling', 'wisdom'),
                    ('medicine', 'wisdom'),
                    ('nature', 'intelligence'),
                    ('perception', 'wisdom'),
                    ('persuasion', 'charisma'),
                    ('sleight_of_hand', 'dexterity'),
                    ('religion', 'intelligence'),
                    ('survival', 'wisdom');
                """)
                
                await cursor.execute("""
                INSERT INTO coin(coin_name) VALUES('po'),('pp'),('pc'),('pl'),('da'),('pe');
                """)
                
                await cursor.execute("""
                INSERT INTO saving_throw(saving_throw_name) 
                VALUES
                    ('strength'),
                    ('intelligence'),
                    ('wisdom'),
                    ('dexterity'),
                    ('charisma'),
                    ('constitution');        
                """)
                
                await cursor.execute("""
                INSERT INTO type_damage(type_damage_name) 
                VALUES
                    ('slashing'),
                    ('bludgeoning'),
                    ('piercing'),
                    ('acid'),
                    ('cold'),
                    ('fire'),
                    ('thunder'),
                    ('lightning'),
                    ('necrotic'),
                    ('radiant'),
                    ('poison'),
                    ('psychic'),
                    ('force');        
                """)
                
                await cursor.execute("""
                INSERT INTO kind_equipment(kind_equipment_name) 
                VALUES
                    ('shild'),
                    ('sword');        
                """)
                
                await cursor.execute("""
                INSERT INTO class(class_name)
                VALUES
                    ('Druid'),
                    ('Knight'),
                    ('Hunter'),
                    ('Necromancer');
                """)
                
                await cursor.execute("""
                INSERT INTO race(race_name)
                VALUES
                    ('Dragonborn'),
                    ('Dwarconninfo'),
                    ('Elconninfo'),
                    ('Gnome'),
                    ('Half-Elconninfo');
                """)
                
                await cursor.execute("""
                INSERT INTO character(race_id, character_name, date_creation)
                VALUES (1, 'teste', '11-22-2023');
                """)
                
                await cursor.execute("""
                INSERT INTO room(room_name, room_password)
                VALUES ('teste', '123');
                """)
                
                await cursor.execute("""
                INSERT INTO user_room(room_id, user_id)
                VALUES (1, 1);
                """)
                
            finally:
                await cursor.close()
                await pool.close()


async def main():
    await create_database()
    await create_tables()
    await insert_default_values()

if __name__ == "__main__":
    asyncio.run(main())
