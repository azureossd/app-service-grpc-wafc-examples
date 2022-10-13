import grpc
import os
import greeter_pb2
import greeter_pb2_grpc
import asyncio
from aiohttp import web

from grpc.experimental.aio import init_grpc_aio
from concurrent import futures

HOST = os.environ.get('HOST')
routes = web.RouteTableDef()


class Greeter(greeter_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        return greeter_pb2.HelloReply(message='Hello world, from app-service-grpc-wafc-examples-python-no-reflection - gRPC')


@routes.get('/')
async def index(self):
    data = { 'msg': 'Hello world, from app-service-grpc-wafc-examples-python-reflection - HTTP' }
    return web.json_response(data)


class Application(web.Application):
    def __init__(self):
        super().__init__()
        self.grpc_task = None
        self.grpc_server = GrpcServer()
        self.add_routes()
        self.on_startup.append(self.__on_startup())
        self.on_shutdown.append(self.__on_shutdown())

    def __on_startup(self):
        async def _on_startup(app):
            self.grpc_task = \
                asyncio.ensure_future(app.grpc_server.start())
        return _on_startup

    def __on_shutdown(self):
        async def _on_shutdown(app):
            await app.grpc_server.stop()
            app.grpc_task.cancel()
            await app.grpc_task
        return _on_shutdown

    def add_routes(self):
        return self.router.add_get('/', index)


    def run(self):
        print(f'HTTP server starting on {HOST}:8000')
        return web.run_app(self, host=f'{HOST}', port=8000)


class GrpcServer():
    def __init__(self):
        init_grpc_aio()

        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        self.servicer = Greeter()
        # Add a port for our gRPC service over 50051
        self.server.add_insecure_port(f'{HOST}:50051')

        greeter_pb2_grpc.add_GreeterServicer_to_server(self.servicer, self.server)

    async def start(self):
        # Start the servers
        print(f'gRPC server starting on {HOST}:50051')
        await self.server.start()

    async def stop(self):
        await self.server.wait_for_termination()


application = Application()


if __name__ == '__main__':
    application.run()
