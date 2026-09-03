EC ?= easycrypt
THEORIES = UFHY1.ec EPSILON.ec MODE.ec

.PHONY: check install-status admitted test

check:
	@command -v $(EC) >/dev/null || { echo "easycrypt absent — label stays honest"; exit 2; }
	@for t in $(THEORIES); do echo "== $$t"; $(EC) -I . $$t || exit 1; done

admitted:
	@grep -n admitted *.ec || true
	@echo "admitted lemmas are obligations, not theorems"

test:
	python3 test_door.py

install-status:
	@command -v $(EC) >/dev/null && $(EC) -version || echo "easycrypt: not on PATH"
