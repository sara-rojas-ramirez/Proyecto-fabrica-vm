require 'yaml'

curso = ENV['CURSO'] || 'web'
archivo = File.join(__dir__, 'plantillas', "#{curso}.yaml")
abort "No existe la plantilla: #{curso}" unless File.exist?(archivo)
plantilla = YAML.load_file(archivo)

Vagrant.configure("2") do |config|
  config.vm.box = "generic/debian12"

  plantilla['maquinas'].each do |m|
    config.vm.define m['nombre'] do |nodo|
      nodo.vm.hostname = m['nombre']
      nodo.vm.network "private_network", ip: m['ip']

      nodo.vm.provider "virtualbox" do |vb|
        vb.name   = "#{curso}-#{m['nombre']}"
        vb.memory = m['memoria']
        vb.cpus   = m['cpus']
      end

      nodo.vm.provision "shell", path: "provision/base.sh",
                        args: plantilla['paquetes'] || []
      nodo.vm.provision "shell", path: "provision/seguridad.sh"
    end
  end
end
