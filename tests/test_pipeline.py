import tempfile

import mario

fun0 = mario.node.Compute(
    "fun0",
    "image:tag",
    command=["python3", "/entrypoint/main.py"],
    arg_names=["arg1", "arg2"],
)
fun1 = mario.node.Compute("fun1", "image:tag", command=["sh", "-c", "ls /mnt/data/"])


@mario.node.PyScript.with_image("image:tag")
def fun2(x: int = None):
    if x:
        for _ in range(x ** 2):
            print(f"hello {x}")


vol0 = mario.node.VolumeLoad("nfs")
vol1 = mario.node.VolumeClaim("claimed", "1Gi")
secret = mario.node.PullSecrets("secret")


def sequential_mount(a: int, b: str):

    secret()
    vol = vol0()
    fun0["/mnt/data/"] = vol
    fun0(arg1=a, arg2=b)
    fun0.config.set_gpu_limit(1)
    fun1["/mnt/data/"] = fun0["/mnt/data/"]
    fun1()
    fun0.config.set_gpu_limit(1)
    fun2["/mnt/data/"] = fun1["/mnt/data/"]
    fun2()
    fun0.config.set_gpu_limit(1)


def sequential_load(a: int, b: str):

    secret()
    vol = vol1()
    fun0["/mnt/data/"] = vol
    f0 = fun0(arg1=a, arg2=b)
    f0.set_gpu_limit(1)
    fun1["/mnt/data/"] = fun0["/mnt/data/"]
    f1 = fun1()
    f1.set_gpu_limit(1)
    fun2["/mnt/data/"] = fun1["/mnt/data/"]
    f2 = fun2()
    f2.set_gpu_limit(2)


def parallel(a: int):
    vol = vol0()
    fun0["/mnt/"] = vol
    fun0(arg1=a)
    fun1["/mnt/"] = vol
    fun1()
    fun2["/mnt/"] = vol
    fun2()


def test_save_pipeline():

    with tempfile.TemporaryDirectory() as p:
        mario.script.save(sequential_mount, root=p)
        mario.script.save(sequential_load, root=p)
        mario.script.save(parallel, root=p)
