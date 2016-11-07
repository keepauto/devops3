from docker import Client


Class Container:
    def __init__(self):
        self.cli = Client(base_url='unix://var/run/docker.sock')

    def start(self, service_port, image, cmd):
        self.container = self.cli.create_container(
            image, cmd, ports = [service_port],
            host_config = self.cli.create_host_config(port_bindings={
                service_port:None
            })
        )
        resp = self.cli.start(container=self.container.get('Id'))
        """{u'1111/tcp': [{u'HostPort': u'32769', u'HostIp': u'0.0.0.0'}]}"""
        return self.cli.start(self.container.get('Id'))['NetworkSettings']['Ports']['%d/tcp'%service_port][0]['HOST']


    if __name__ == "__main__":
        print Container().start(1111,"contos","tail -f /etc/hosts")
