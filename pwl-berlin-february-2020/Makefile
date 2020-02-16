COMPILER=xelatex
TARGET=talk

all:
	${COMPILER} -shell-escape ${TARGET}
	${COMPILER} -shell-escape ${TARGET}
	make cleanup

cleanup:
	rm ${TARGET}.aux ${TARGET}.log ${TARGET}.nav ${TARGET}.out ${TARGET}.snm ${TARGET}.toc ${TARGET}.vrb
	rm -r _minted-talk
