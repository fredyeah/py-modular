COMPILER = cc
FLAGS = -fPIC -shared

all: tests.so sine.so

tests.so: tests.c
	$(COMPILER) $(FLAGS) -o $@ $^

sine.so: sine.c
	$(COMPILER) $(FLAGS) -o $@ $^


# all: $(TARG).so $(TARG).c
# 	@echo $(TEST)
# $(TARG).so: $(TARG).c
# 	$(COMP) $(OPTS) -o $(TARG).so $(TARG).c

clean:
	rm -rf *.so
