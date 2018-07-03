package main

import (
	"flag"
	"github.com/Shopify/sarama"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strings"
)

var (
	addr    = flag.String("addr", ":80", "The address to bind to")
	brokers = flag.String("brokers", "localhost:9094", "The Kafka brokers to connect to, as a comma separated list")
	topic   = flag.String("topic", "tx", "The Kafka topic")
	verbose = flag.Bool("verbose", false, "Turn on Sarama logging")
)

type Server struct {
	producer sarama.SyncProducer
}

func (s *Server) Run(addr string) error {
	log.Printf("Listering to %s\n", addr)

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		log.Printf("%s %s %s\n", r.RemoteAddr, r.Method, r.URL)
		b, err := ioutil.ReadAll(r.Body)
		if err != nil {
			log.Print(err)
			http.Error(w, err.Error(), 500)
			return
		}

		_, _, err = s.producer.SendMessage(&sarama.ProducerMessage{
			Topic: *topic,
			Value: sarama.StringEncoder(b),
		})

		if err != nil {
			log.Print(err)
			http.Error(w, err.Error(), 500)
			return
		}
		w.WriteHeader(200)

	})

	return http.ListenAndServe(addr, nil)
}

func newProducer(brokerList []string) sarama.SyncProducer {
	config := sarama.NewConfig()
	config.Producer.RequiredAcks = sarama.WaitForAll // Wait for all in-sync replicas to ack the message
	config.Producer.Retry.Max = 10                   // Retry up to 10 times to produce the message
	config.Producer.Return.Successes = true

	producer, err := sarama.NewSyncProducer(brokerList, config)

	if err != nil {
		log.Fatalln("Failed to start Sarama producer:", err)
	}

	return producer
}

func main() {
	flag.Parse()

	if *verbose {
		sarama.Logger = log.New(os.Stdout, "[receiver] ", log.LstdFlags)
	}

	if *brokers == "" {
		flag.PrintDefaults()
		os.Exit(1)
	}

	brokerList := strings.Split(*brokers, ",")

	server := &Server{
		newProducer(brokerList),
	}

	if err := server.Run(*addr); err != nil {
		log.Fatal(err)
	}
}
