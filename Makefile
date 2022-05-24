all:
	docker build -t cronycle_ml:latest

run:
	docker run -p 5000:5000 cronycle_ml