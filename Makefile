all: make.docker run.benchmark
make.docker:
	docker build . --tag=gunflawor:latest
run.benchmark:
	python main.py