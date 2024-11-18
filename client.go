package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
)

func main() {
	// Connect to the server
	conn, err := net.Dial("tcp", "127.0.0.1:6667")
	if err != nil {
		fmt.Println("Error connecting:", err)
		return
	}
	defer conn.Close() // Ensure the connection is closed when done

	// Receive the list of available languages from the server
	buffer := make([]byte, 2048)
	n, err := conn.Read(buffer)
	if err != nil {
		fmt.Println("Error reading available languages:", err)
		return
	}

	// Print available languages
	languages := string(buffer[:n])
	fmt.Println("Available languages:", languages)

	// Input the desired language abbreviation
	reader := bufio.NewReader(os.Stdin)
	fmt.Print("Enter the abbreviation of the language you want to translate to: ")
	abbreviation, err := reader.ReadString('\n')
	if err != nil {
		fmt.Println("Error reading abbreviation:", err)
		return
	}
	abbreviation = abbreviation[:len(abbreviation)-1] // Trim the newline character

	// Send the abbreviation to the server
	_, err = conn.Write([]byte(abbreviation))
	if err != nil {
		fmt.Println("Error sending abbreviation:", err)
		return
	}

	// Input the phrase to be translated
	fmt.Print("Enter the phrase you want to translate: ")
	phrase, err := reader.ReadString('\n')
	if err != nil {
		fmt.Println("Error reading phrase:", err)
		return
	}
	phrase = phrase[:len(phrase)-1] // Trim the newline character

	// Send the phrase to the server
	_, err = conn.Write([]byte(phrase))
	if err != nil {
		fmt.Println("Error sending phrase:", err)
		return
	}

	// Receive the translated phrase from the server
	n, err = conn.Read(buffer)
	if err != nil {
		fmt.Println("Error reading translation:", err)
		return
	}

	// Print the translated response
	translation := string(buffer[:n])
	fmt.Println("Translated text:", translation)
}
