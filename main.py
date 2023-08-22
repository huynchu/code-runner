import docker
import tarfile
import os


#start the docker client  
try:
    client = docker.from_env()
except:
    raise Exception("Error when starting the Docker client.")

# start the container here to run forever.
# The important thing here is the tty. It is what keeps the container running.
# The detach attribute is so we can have the container variable to manipulate.
try:
    # make sure to build an image 'python_empty' first with /languages/python/Dockerfile
    container = client.containers.run('python_empty', tty=True, detach=True, remove=True)
except:
    raise Exception("Error when starting the container.")

# copy the file to the container
# /files_to_exec/hello.py is the code file to copy into docker
# /tmp is the folder to copy the file to
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    code_file = os.path.join(script_dir, "files_to_exec", "hello.py")
    with tarfile.open('/tmp/file.tar', 'w') as tar:
        tar.add(code_file, os.path.basename(code_file))

    with open('/tmp/file.tar', 'rb') as f:
        container.put_archive('/usr/src/myapp/', f.read())
except:
    raise Exception("Error when copying the file to the container.")

# execute the file in the container
try:
    exec_command = 'python3 hello.py'
    run_result = container.exec_run(exec_command, demux=True)
    # Returns A tuple of (exit_code, output)
    # output:
    #   demux=True, a tuple of two bytes: stdout and stderr. 
    #    A bytestring containing response data otherwise.
   
    stdout = run_result.output[0].decode("utf-8") if run_result and run_result.output[0] else ''
    stderr = run_result.output[1].decode("utf-8") if run_result and run_result.output[1] else ''

    print("STDOUT:\n", stdout)
    print("STDERR:\n", stderr)

        
except:
    raise Exception("Error when executing the file in the container.")

# stop the container
# TODO: make this async/concurrent its takes alot of time to stop the container
try:
    container.stop()
except:
    raise Exception("Error when stopping the container.")
