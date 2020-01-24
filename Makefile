run: jupyter
.PHONY: run

build-and-run:
	$(MAKE) jupyter-image
	$(MAKE) jupyter
.PHONY: build-and-run

stop:
	docker stop mloncode/workshop > /dev/null 2>&1 || true
.PHONY: stop

jupyter-image:
	docker build -t mloncode/workshop .
.PHONY: jupyter-image

jupyter:
	docker start mloncode/workshop > /dev/null 2>&1 \
		|| docker run \
		    --rm \
		    --name mloncode/workshop \
		    --publish 8888:8888 \
		    --volume $(PWD)/notebooks:/workdir/notebooks \
		    mloncode/workshop
.PHONY: jupyter
