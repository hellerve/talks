COMPILER=xelatex
TARGET=talk

all:
	${COMPILER} -shell-escape ${TARGET}
	${COMPILER} -shell-escape ${TARGET}
	make cleanup

cleanup:
	rm -r ${TARGET}.aux ${TARGET}.log ${TARGET}.nav ${TARGET}.out ${TARGET}.snm ${TARGET}.toc ${TARGET}.vrb _minted-talk
