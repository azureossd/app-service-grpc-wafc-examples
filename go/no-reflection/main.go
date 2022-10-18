package main

import (
	"context"
	"flag"
	"fmt"
	"log"
	"net"
	"net/http"
	"io"

	"google.golang.org/grpc"
	pb "github.com/Ajsalemo/app-service-grpc-wafc-examples/proto"
)

var (
	port = flag.Int("port", 50051, "The server port")
)

// server is used to implement helloworld.GreeterServer.
type server struct {
	pb.UnimplementedGreeterServer
}

func index(w http.ResponseWriter, r *http.Request) {
	io.WriteString(w, "Hello, from app-service-grpc-wafc-examples - HTTP")
}

// SayHello implements helloworld.GreeterServer
func (s *server) SayHello(ctx context.Context, in *pb.Empty) (*pb.HelloReply, error) {
	return &pb.HelloReply{Message: "Hello, from app-service-grpc-wafc-examples - gRPC"}, nil
}

func main() {
	// Implement a goroutine to start the HTTP server concurrently
	go func ()  {
		http.HandleFunc("/", index)
		log.Printf("server listening at localhost:8080")
		err := http.ListenAndServe(":8080", nil)

		if err != nil {
			log.Fatalf("Failed to start the HTTP server!")
		}
	}()

	flag.Parse()
	lis, err := net.Listen("tcp", fmt.Sprintf(":%d", *port))
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	s := grpc.NewServer()
	pb.RegisterGreeterServer(s, &server{})
	log.Printf("server listening at %v", lis.Addr())
	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}