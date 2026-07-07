COMPILER=xelatex
TARGET=talk

# Canonical deck: the Cyberwitchery-themed talk (talk.tex + content.tex).
all:
	${COMPILER} -shell-escape ${TARGET}
	${COMPILER} -shell-escape ${TARGET}
	make cleanup

cleanup:
	rm -f ${TARGET}.aux ${TARGET}.log ${TARGET}.nav ${TARGET}.out ${TARGET}.snm ${TARGET}.toc ${TARGET}.vrb

clean: cleanup
	rm -f ${TARGET}.pdf
