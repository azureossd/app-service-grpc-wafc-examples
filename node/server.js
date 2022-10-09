const grpc = require("@grpc/grpc-js");
const protoLoader = require("@grpc/proto-loader");
const express = require("express");
const app = express();

const PROTO_PATH = "./greeter.proto";
const EXPRESS_PORT = process.env.EXPRESS_PORT || 3000;
const GRPC_PORT = process.env.GRPC_PORT || 50051;
const HOST = process.env.HOST || "localhost";
const GRPC_SERVER_DEFINITION = `${HOST}:${GRPC_PORT}`;

const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true,
});

const greeter_proto = grpc.loadPackageDefinition(packageDefinition).greeter;

/**
 * Implements the SayHello RPC method.
 */
const sayHello = (_, callback) => {
  const message = "Hello, from app-service-grpc-wafc-examples-node";
  callback(null, { message: message });
};

app.get("/", (_req, res) => {
  res.json({ msg: "Hello World!" });
});

/**
 * Starts an RPC server that receives requests for the Greeter service at the
 * sample server port
 */
const main = () => {
  const server = new grpc.Server();
  server.addService(greeter_proto.Greeter.service, { sayHello: sayHello });
  server.bindAsync(
    `${GRPC_SERVER_DEFINITION}`,
    grpc.ServerCredentials.createInsecure(),
    () => {
      console.log(`Starting gRPC server on ${GRPC_SERVER_DEFINITION}`);
      server.start();
    }
  );
  // Starting an HTTP server to response to App Service Linux's initial container start up pings over HTTP/2
  // Or else the container will never start if this is ONLY set for gRPC requests
  app.listen(EXPRESS_PORT, () => {
    console.log(`Express is listening on ${EXPRESS_PORT}`);
  });
};

main();
