import os
import tempfile

import mario


def test_volume():
    v0 = mario.node.VolumeLoad("existing-vol")
    v1 = mario.node.VolumeClaim("new-vol", "1Gi")

    print(v0)
    print(v1)


def test_compute_node():
    f0 = mario.node.Compute(
        "f0",
        "your-registry:tag",
        command=["python3", "/entrypoint/main.py"],
        arg_names=["arg1", "arg2"],
    )
    print(f0)

    with tempfile.TemporaryDirectory() as d:
        f0.to_component_yaml(os.path.join(d, "f0.yaml"))
        f1 = mario.node.Compute.from_component_yaml(os.path.join(d, "f0.yaml"))
        f1(arg1=2, arg2=3.0)

        assert str(f0) == str(f1)


def test_pull_secret_node():
    secret = mario.node.PullSecrets("pull-secret", "another-pull-secret")
    print(secret)


def test_pyscript_node():
    def pyfunc(x: int, y: float):
        return x * y

    f0 = mario.node.PyScript(pyfunc, image="image:tag")
    f0(x=1, y=1.2)

    with tempfile.TemporaryDirectory() as d:
        f0.to_component_yaml(os.path.join(d, "f0.yaml"))
        f1 = mario.node.PyScript.from_component_yaml(os.path.join(d, "f0.yaml"))

        f1(x=2, y=3.0)

        assert f0.arg_names == f1.arg_names
        assert f0.command == f1.command
