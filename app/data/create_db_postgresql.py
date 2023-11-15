import os
from dotenv import load_dotenv
import asyncpg
import asyncio

load_dotenv()


async def create_database():
    connection = await asyncpg.connect(
        user='postgres',
        password='123',
        host='localhost',
        port='5432'
    )
    try:
        await connection.execute('''DROP DATABASE IF EXISTS "RPG"''')
        await connection.execute("""
            CREATE DATABASE "RPG"
                WITH
                OWNER = postgres
                ENCODING = 'UTF8'
                LC_COLLATE = 'Portuguese_Brazil.utf8'
                LC_CTYPE = 'Portuguese_Brazil.utf8'
                LOCALE_PROVIDER = 'libc'
                TABLESPACE = pg_default
                CONNECTION LIMIT = -1
                IS_TEMPLATE = False;
        """)
    finally:
        await connection.close()


async def create_tables():
    connection = await asyncpg.connect(
        user='postgres',
        password='123',
        host='localhost',
        port='5432',
        database='RPG'
    )

    try:
        # Verifica se a sequência já existe antes de tentar criá-la
        existing_sequence = await connection.fetchval("""
            SELECT 1 FROM pg_sequences WHERE schemaname = 'public' AND sequencename = 'custom_id_seq';
        """)

        if not existing_sequence:
            await connection.execute("""
                CREATE SEQUENCE custom_id_seq START 1;
            """)

        await connection.execute("""
            CREATE OR REPLACE FUNCTION generate_custom_id(prefix VARCHAR(2), seq_val BIGINT)
            RETURNS VARCHAR(10) AS $$
            BEGIN
                RETURN prefix || LPAD(seq_val::TEXT, 8, '0');
            END;
            $$ LANGUAGE plpgsql;
        """)

        await connection.execute("""
        CREATE TABLE coin (
            coin_id VARCHAR(10) PRIMARY KEY DEFAULT generate_custom_id('CI', nextval('custom_id_seq')),
            coin_name VARCHAR(20) NOT NULL
        );
        """)

        await connection.execute("""
        CREATE TABLE kind_equipment (
            kind_equipment_id VARCHAR(10) PRIMARY KEY DEFAULT generate_custom_id('KE', nextval('custom_id_seq')),
            kind_equipment_name VARCHAR(30) NOT NULL
        );
        """)

        await connection.execute("""
        CREATE TABLE type_damage (
            type_damage_id VARCHAR(10) PRIMARY KEY DEFAULT generate_custom_id('TD', nextval('custom_id_seq')),
            type_damage_name VARCHAR(30) NOT NULL
        );
        """)

        await connection.execute("""
        CREATE TABLE equipment (
            equipment_id VARCHAR(10) PRIMARY KEY DEFAULT generate_custom_id('EQ', nextval('custom_id_seq')),
            kind_equipment_id VARCHAR(10) NOT NULL REFERENCES kind_equipment(kind_equipment_id) ON DELETE CASCADE,
            equipment_name VARCHAR(100) NOT NULL,
            description_equipment VARCHAR(200),
            price FLOAT,
            coin_id VARCHAR(10) REFERENCES coin(coin_id) ON DELETE SET NULL,
            weight FLOAT,
            armor_class INT,
            amount_dice INT,
            side_dice INT,
            type_damage_id VARCHAR(10) REFERENCES type_damage(type_damage_id) ON DELETE SET NULL,
            bonus VARCHAR(20)
        );
        """)

        await connection.execute("""
        CREATE TABLE spell (
            spell_id VARCHAR(10) PRIMARY KEY DEFAULT generate_custom_id('SP', nextval('custom_id_seq')),
            spell_name VARCHAR(35) NOT NULL,
            description_spell VARCHAR(200),
            spell_level INT NOT NULL,
            attribute_use VARCHAR(30),
            amount_dice INT,
            side_dice INT,
            type_damage_id VARCHAR(10) REFERENCES type_damage(type_damage_id) ON DELETE SET NULL,
            add_per_level INT
        );               
        """)

        await connection.execute("""
        CREATE TABLE class (
            class_id VARCHAR(10) PRIMARY KEY DEFAULT generate_custom_id('CL', nextval('custom_id_seq')),
            class_name VARCHAR(30) NOT NULL,
            description_class VARCHAR(200)
        );
        """)

        await connection.execute("""
        CREATE TABLE spell_class (
            spell_class_id VARCHAR(10) PRIMARY KEY DEFAULT generate_custom_id('SC', nextval('custom_id_seq')),
            spell_id VARCHAR(10) NOT NULL REFERENCES spell(spell_id) ON DELETE CASCADE,
            class_id VARCHAR(10) NOT NULL REFERENCES class(class_id) ON DELETE CASCADE
        );
        """)

        await connection.execute("""
        CREATE TABLE skill (
            skill_id VARCHAR(10) PRIMARY KEY DEFAULT generate_custom_id('SK', nextval('custom_id_seq')),
            skill_name VARCHAR(30) NOT NULL,
            usage_status VARCHAR(30) NOT NULL
        );
        """)

        await connection.execute("""
        CREATE TABLE saving_throw (
            saving_throw_id VARCHAR(10) PRIMARY KEY DEFAULT generate_custom_id('ST', nextval('custom_id_seq')),
            saving_throw_name VARCHAR(30) NOT NULL
        );           
        """)

        await connection.execute("""
        CREATE TABLE room (
            room_id VARCHAR(10) PRIMARY KEY DEFAULT generate_custom_id('RM', nextval('custom_id_seq')),
            room_name VARCHAR(100) NOT NULL,
            room_password VARCHAR(300) NOT NULL
        );         
        """)

        await connection.execute("""
            CREATE TABLE "user" (
                user_id VARCHAR(10) PRIMARY KEY DEFAULT generate_custom_id('US', nextval('custom_id_seq')),
                user_name VARCHAR(30) NOT NULL,
                password VARCHAR(255) NOT NULL,
                email VARCHAR(300) NOT NULL,
                birth_date DATE NOT NULL,
                user_type INT NOT NULL CHECK (user_type IN (1, 2)) DEFAULT 2,
                date_creation DATE NOT NULL
            );
        """)

        await connection.execute("""
        CREATE TABLE user_room (
            user_room_id VARCHAR(10) PRIMARY KEY DEFAULT generate_custom_id('UR', nextval('custom_id_seq')),
            user_id VARCHAR(10) NOT NULL REFERENCES "user"(user_id) ON DELETE CASCADE,
            room_id VARCHAR(10) NOT NULL REFERENCES room(room_id) ON DELETE CASCADE,
            user_room_type INT DEFAULT 2 CHECK (user_room_type IN (1, 2))
        );
        """)

        await connection.execute("""
        CREATE TABLE race (
            race_id VARCHAR(10) PRIMARY KEY DEFAULT generate_custom_id('RC', nextval('custom_id_seq')),
            race_name VARCHAR(30) NOT NULL,
            description_race VARCHAR(200)
        );
        """)

        await connection.execute("""
        CREATE TABLE character (
            character_id VARCHAR(10) PRIMARY KEY DEFAULT generate_custom_id('CH', nextval('custom_id_seq')),
            user_id VARCHAR(10) NOT NULL REFERENCES "user"(user_id) ON DELETE CASCADE,
            race_id VARCHAR(10) NOT NULL REFERENCES race(race_id) ON DELETE CASCADE,
            character_name VARCHAR(30) NOT NULL,
            date_creation DATE NOT NULL
        );
        """)
        
        await connection.execute("""
        CREATE TABLE message (
            message_id VARCHAR(10) PRIMARY KEY DEFAULT generate_custom_id('MS', nextval('custom_id_seq')),
            user_room_id VARCHAR(10) NOT NULL REFERENCES user_room(user_room_id) ON DELETE CASCADE,
            character_id VARCHAR(10) NOT NULL REFERENCES character(character_id) ON DELETE CASCADE,
            messagetime TIMESTAMP NOT NULL,
            message VARCHAR(200) NOT NULL
        );
        """)

        await connection.execute("""
        CREATE TABLE character_characteristic (
            character_characteristic VARCHAR(10) PRIMARY KEY DEFAULT generate_custom_id('CC', nextval('custom_id_seq')),
            character_id VARCHAR(10) NOT NULL REFERENCES character(character_id) ON DELETE CASCADE,
            age INT,
            height FLOAT,
            weight FLOAT,
            eye_color VARCHAR(20),
            skin_color VARCHAR(20),
            color_hair VARCHAR(20),
            character_image VARCHAR(200)
        );
        """)

        await connection.execute("""
        CREATE TABLE status_base (
            status_base_id VARCHAR(10) PRIMARY KEY DEFAULT generate_custom_id('SB', nextval('custom_id_seq')),
            character_id VARCHAR(10) NOT NULL REFERENCES character(character_id) ON DELETE CASCADE,
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

        await connection.execute("""
        CREATE TABLE character_equipment (
            character_equipment_id VARCHAR(10) PRIMARY KEY DEFAULT generate_custom_id('CE', nextval('custom_id_seq')),
            equipment_id VARCHAR(10) NOT NULL REFERENCES equipment(equipment_id) ON DELETE CASCADE,
            character_id VARCHAR(10) NOT NULL REFERENCES character(character_id) ON DELETE CASCADE
        );
        """)

        await connection.execute("""
        CREATE TABLE character_coin (
            character_coin_id VARCHAR(10) PRIMARY KEY DEFAULT generate_custom_id('CN', nextval('custom_id_seq')),
            coin_id VARCHAR(10) NOT NULL REFERENCES coin(coin_id) ON DELETE CASCADE,
            character_id VARCHAR(10) NOT NULL REFERENCES character(character_id) ON DELETE CASCADE,
            amount_coin INT
        );
        """)

        await connection.execute("""
        CREATE TABLE character_class (
            character_class_id VARCHAR(10) PRIMARY KEY DEFAULT generate_custom_id('C', nextval('custom_id_seq')),
            class_id VARCHAR(10) NOT NULL REFERENCES class(class_id) ON DELETE CASCADE,
            character_id VARCHAR(10) NOT NULL REFERENCES character(character_id) ON DELETE CASCADE
        );
        """)

        await connection.execute("""
        CREATE TABLE character_skill (
            character_skill_id VARCHAR(10) PRIMARY KEY DEFAULT generate_custom_id('CK', nextval('custom_id_seq')),
            skill_id VARCHAR(10) NOT NULL REFERENCES skill(skill_id) ON DELETE CASCADE,
            character_id VARCHAR(10) NOT NULL REFERENCES character(character_id) ON DELETE CASCADE
        );
        """)

        await connection.execute("""
        CREATE TABLE character_saving_throw (
            character_saving_throw_id VARCHAR(10) PRIMARY KEY DEFAULT generate_custom_id('CT', nextval('custom_id_seq')),
            saving_throw_id VARCHAR(10) NOT NULL REFERENCES saving_throw(saving_throw_id) ON DELETE CASCADE,
            character_id VARCHAR(10) NOT NULL REFERENCES character(character_id) ON DELETE CASCADE
        );
        """)

        await connection.execute("""
        CREATE TABLE character_spell (
            character_spell_id VARCHAR(10) PRIMARY KEY DEFAULT generate_custom_id('CS', nextval('custom_id_seq')),
            spell_id VARCHAR(10) NOT NULL REFERENCES spell(spell_id) ON DELETE CASCADE,
            character_id VARCHAR(10) NOT NULL REFERENCES character(character_id) ON DELETE CASCADE
        );
        """)

        await connection.execute("""
        CREATE TABLE spell_slot (
            spell_slot_id VARCHAR(10) PRIMARY KEY DEFAULT generate_custom_id('SS', nextval('custom_id_seq')),
            character_id VARCHAR(10) NOT NULL REFERENCES character(character_id) ON DELETE CASCADE,
            level INT NOT NULL,
            slot INT NOT NULL
        );
        """)

    finally:
        await connection.close()


async def main():
    await create_database()
    await create_tables()

if __name__ == "__main__":
    asyncio.run(main())
