import asyncio
from db import get_connection_without_async  # Assuming this imports the function

async def teste():
    # Get the cursor directly
    pool = await get_connection_without_async()
    async with pool.connection() as conn:
        await conn.set_autocommit(True)
        async with conn.cursor() as cursor:
            try:
                # Execute the query
                await cursor.execute('SELECT * FROM "user" WHERE user_id = %s;', (1,))  # Note: No tuple here

                # Fetch the results
                result = await cursor.fetchall()

                print(result)
            finally:
                # Close the cursor after processing results
                await cursor.close()

# Run the asynchronous function
asyncio.run(teste())
