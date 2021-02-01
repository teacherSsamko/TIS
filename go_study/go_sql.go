package main

import (
	"database/sql"
	"fmt"

	_ "github.com/go-sql-driver/mysql"
)

func main() {
	db, _ := sql.Open("mysql", "ssamko:pwd@tcp(127.0.0.1:3306)/pwd")
	defer db.Close()

	var version string
	db.QueryRow("SELECT VERSION()").Scan(&version)
	fmt.Println("Connected to:", version)

	// var wg sync.WaitGroup
	// for i := 0; i

}
