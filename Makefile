SHELL := /bin/bash
RM    := rm -rf
MKDIR := mkdir -p

.PHONY: default debug release distclean clean-debug clean-release
default: debug ;

debug:
	@ $(MKDIR) debug > /dev/null
	@ cd debug > /dev/null 2>&1 && cmake -DCMAKE_BUILD_TYPE=Debug ..
	@ $(MAKE) -s -C debug

release:
	@ $(MKDIR) release > /dev/null
	@ cd release > /dev/null 2>&1 && cmake -DCMAKE_BUILD_TYPE=Release ..
	@ $(MAKE) -s -C release

distclean:
	@ $(RM) ./debug
	@ $(RM) ./release

clean: clean-debug clean-release

clean-debug:
	@ if [ -d "./debug"  ]; then cd debug > /dev/null 2>&1 && make -s clean; fi

clean-release:
	@ if [ -d "./release"  ]; then cd release > /dev/null 2>&1 && make -s clean; fi
