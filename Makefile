all: make.docker run.benchmark
make.docker:
	echo docker build . --tag=gunflawor:latest
run.benchmark:
	echo python main.py