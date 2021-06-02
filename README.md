# Mario

Make Kubeflow pipelines intuitive

```bash
mario
├── __init__.py
├── node
│   ├── __init__.py
│   ├── base.py
│   ├── compute.py
│   ├── config.py
│   └── volume.py
├── script.py
└── volume.py
```

## Install

`pip install -e .`

## Usage

The most important class `mario.node.Node` has following subclasses

* `mario.node.Compute`: perform computation using a container image
* `mario.node.VolumeLoad`: load an existing volume
* `mario.node.VolumeClaim`: claim a new volume
* `mario.node.PullSecrets`: add pull secret to the pipeline

### Define pipeline nodes

```python
import mario

# computer nodes
fun0 = mario.node.Compute('fun0', 
                          'image:tag', 
                          command=['python3', 
                                   '/helloworld/main.py'], 
                          arg_names=['arg1', 'arg2'])

fun1 = mario.node.Compute('fun1', 
                          'image:tag', 
                          command=['sh', '-c', 'ls /mnt/data/'])

fun2 = mario.node.Compute('fun2', 
                          'image:tag', 
                          command=['sh', '-c', 'ls /mnt/data/'])

# load existing volume
vol0 = mario.node.VolumeLoad('existing_vol')

# claim new volume
vol1 = mario.node.VolumeClaim('claimed', '1Gi')

# pipeline pull secret
secret = mario.node.PullSecrets('your-pull-secret')
```

## Define pipeline topology

The pipeline is wrapped in a `Callable` with typed input args. The `Callable` name will become pipeline name and the doc string will become the pipeline description.

* Use `(arg1, arg2,...)` to pass args to container entry-point.
* Use `[/mount-point]` to indicate mount point in the container
* The mount points indicate the compute node topology

### Sequential

```python
def sequential_mount(a: int, b: str):
    """Doc string will become the pipeline description"""
    secret()
    vol = vol0()
    optional_container_handle = fun0['/mnt/data/'] = vol
    # set additional attributes using optional_container_handle
    fun0(arg1 = a, arg2 = b)
    fun1['/mnt/data/'] = fun0['/mnt/data/']
    fun1()
    fun2['/mnt/data/'] = fun1['/mnt/data/']
    fun2()
```

```python
def sequential_claim(a: int, b: str):
    secret()
    vol = vol1()
    fun0['/mnt/data/'] = vol
    fun0(arg1 = a, arg2 = b)
    fun1['/mnt/data/'] = fun0['/mnt/data/']
    fun1()
    fun2['/mnt/data/'] = fun1['/mnt/data/']
    fun2()
```

```mermaid
stateDiagram
	Mount --> Fun0 
	Fun0 --> Fun1 
	Fun1 --> Fun2

```
### Parallel

```python
def distributed_network():
    secret()
    v = vol1()
    fun0['/data/'] = v
    fun0()
    fun1['/data/'] = v
    fun1()
    fun2['/data/'] = v
    fun2()
```

```mermaid
stateDiagram
	Mount --> Fun0 
	Mount --> Fun1 
	Mount --> Fun2

```

## Script

`mario.script.save(function: Callable, filename: Optional[str]=None, **kwargs) -> None`

```python
mario.script.save(sequential_mount, 'optional_name.yaml')
```



