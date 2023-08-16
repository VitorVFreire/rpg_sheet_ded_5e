from src import Usuario
import asyncio

async def teste():
    pessoa = Usuario(email='vitor@vitor', senha='123')
    await pessoa.get_usuario()

    
loop = asyncio.get_event_loop()
loop.run_until_complete(teste())