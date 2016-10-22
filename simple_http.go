package main

import (
	"net"
	"strconv"
	"fmt"
	"bufio"
	"strings"
)

const PORT = 3333

func main() {
	listener, err := net.Listen("tcp", ":" + strconv.Itoa(PORT))
	if err != nil {
		panic("could not listening: " + err.Error())
	}

	conns := fetchConn(listener)
	handleConn(conns)
}

func fetchConn(listener net.Listener) chan net.Conn {
	connChan := make(chan net.Conn)
	i := 0
	go func() {
		ACCEPT:
		for {
			client, err := listener.Accept()
			if err != nil {
				fmt.Printf("could not accept: " + err.Error())
				continue ACCEPT
			}
			i++
			fmt.Printf("%d: %v <=== %v \n", i, client.LocalAddr(), client.RemoteAddr())
			connChan <- client
		}
	}()
	return connChan
}

func handleConn(conns chan net.Conn) {
	for {
		go func(cli net.Conn) {
			bs := bufio.NewReader(cli)
			ECHO:
			for {
				context := ""
				line, err := bs.ReadString('\n')
				if err != nil {
					// EOF, or worse
					break ECHO
				}
				if strings.Contains(line, "GET") {
					line_arr := strings.Split(line, " ")
					path := line_arr[1]
					context = strings.TrimLeft(path, "/")
				}
				cli.Write([]byte("你所访问的路径为: " + context + "\n"))
				cli.Close()
			}

		}(<-conns)
	}
}