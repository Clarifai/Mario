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


def test_resource_node():
    secret = mario.node.PullSecrets("pull-secret", "another-pull-secret")
    print(secret)
