package main

import (
	"fmt"
	"runtime"
)
func memUsage() {
	var m runtime.MemStats
        runtime.ReadMemStats(&m)
	fmt.Println("Alloc:", m.Alloc, "TotalAlloc:", m.TotalAlloc, "HeapAlloc:", m.HeapAlloc)
}
func main() {
	runtime.GC(); memUsage() // basically 0
	
        m := make(map[int]int)
	
	for i := 0; i < 100000; i++ {
	  m[i] = i
	}
	
	runtime.GC(); memUsage() // we have a map
	
	for i := 0; i < 100000; i++ {
	  delete(m, i)
	}
	
	runtime.GC(); memUsage()
	
	fmt.Println(m)
}
