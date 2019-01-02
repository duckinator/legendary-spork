#!/usr/bin/python3

from build_lib import *

# FIXME: This mklib() function seems like a hack.
def mklib(srcdir):
    lib = Library(srcdir)
    lib.needs(files_with_suffixes(srcdir, [".c", ".asm"]))
    return lib


libraries = list(map(mklib, [
    "ali", "cadel", "dmm", "flail", "greeter", "hal", "shell", "tests", "tinker",
]))

ARCH = "i386"

@recipe(target="*.o", match="{}.c")
def build_c_obj(target, source, deps):
    return run([CC, *CFLAGS, "-c", source, "-o", target, *deps])


@recipe(target="*.o", match="{}.asm")
def build_asm_obj(target, match, deps):
    return run([AS, *ASFLAGS, "-o", target, match])


@recipe(target="src/kernel.exe", match="{}.exe")
def build_kernel_exe(target, match, deps):
    return run([LD, "-o", target, "-L", "src/libraries", *LDFLAGS,
                "-T", "src/link-{}.ld".format(ARCH),
                "src/kernel/start-{}.o".format(ARCH), "src/kernel/main.o"])


kernel = Resource("src/kernel.exe")
kernel.needs(*libraries)
kernel.needs(["src/kernel/start-{}.o".format(ARCH), "src/kernel/main.o"])

#if __file__ == "__main__":
exit(build(kernel))
